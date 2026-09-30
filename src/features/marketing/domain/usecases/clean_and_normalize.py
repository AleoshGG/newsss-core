import asyncio
import html
import re
from datetime import datetime, timezone

from langdetect import detect, LangDetectException

from src.core.llm.llm_client import LLMClient
from src.features.github.domain.repositories.github_repository import GitHubRepository
from src.features.google_news.domain.repositories.google_news_repository import GoogleNewsRepository
from src.features.youtube.domain.repositories.youtube_repository import YouTubeRepository

from ..entities.normalized_item_entity import CleaningStats, NormalizedItem


# ---------------------------------------------------------------------------
# Data Cleaner — source-specific cleaning logic
# ---------------------------------------------------------------------------

class DataCleaner:
    """
    Source-aware data cleaner that handles the real-world messiness of each
    ingested source before ML processing.

    Problems addressed:
    - YouTube: transcripts stored as "Transcript not available" literal strings
    - GitHub: READMEs full of markdown badges, code fences, tables, links
    - Google News: content=None from captchas/paywalls, residual HTML from scraping
    - All sources: mixed English/Spanish content
    """

    MIN_BODY_LENGTH: int = 80

    # Known strings that signal an absent transcript
    EMPTY_TRANSCRIPT_MARKERS: frozenset[str] = frozenset({
        "transcript not available",
        "no transcript",
        "transcripts are disabled",
        "could not retrieve a transcript",
        "subtitles are disabled for this video",
        "",
    })

    # Paywall/captcha fingerprints found in the first 300 chars of scraped content
    PAYWALL_PATTERNS: list[str] = [
        r"please enable javascript",
        r"access denied",
        r"captcha",
        r"subscribe to (continue|read)",
        r"sign in to read",
        r"this content is for subscribers",
        r"create a free account",
        r"403 forbidden",
    ]

    @staticmethod
    def clean_youtube_transcript(transcript: str | None) -> str | None:
        """
        Returns cleaned transcript text, or None if the transcript is absent/unusable.
        Strips auto-caption noise tags like [Music] or [Applause].
        """
        if not transcript:
            return None

        normalized = transcript.strip().lower()
        if normalized in DataCleaner.EMPTY_TRANSCRIPT_MARKERS:
            return None

        # Remove auto-generated caption noise: [Music], [Applause], [Laughter], etc.
        cleaned = re.sub(r"\[.*?\]", "", transcript)
        # Collapse excess whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        return cleaned if len(cleaned) >= DataCleaner.MIN_BODY_LENGTH else None

    @staticmethod
    def clean_github_readme(readme: str | None, description: str | None) -> str | None:
        """
        Strips markdown syntax from a GitHub README to produce plain readable text.
        Falls back to the repo description if the cleaned README is too short.
        Badge-heavy READMEs (common in popular repos) are reduced to their prose content.
        """
        def _strip_markdown(text: str) -> str:
            # Remove fenced code blocks (``` ... ```)
            text = re.sub(r"```[\s\S]*?```", "", text)
            # Remove inline code (`code`)
            text = re.sub(r"`[^`\n]+`", "", text)
            # Remove shield/badge image links: [![alt](img_url)](link_url) — entire construct
            text = re.sub(r"!\[([^\]]*)\]\([^\)]*\)\]\([^\)]*\)", "", text)
            # Remove standalone badge images: ![alt](url)
            text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", "", text)
            # Remove markdown links, keep the label text: [label](url) → label
            text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
            # Remove raw HTML tags
            text = re.sub(r"<[^>]+>", "", text)
            # Remove markdown headers (# ## ###)
            text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
            # Remove horizontal rules (--- *** ___)
            text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
            # Remove markdown table rows (| col | col |)
            text = re.sub(r"^\|.+\|$", "", text, flags=re.MULTILINE)
            # Remove leading list markers (- item, * item, 1. item)
            text = re.sub(r"^[\-\*\+]\s+", "", text, flags=re.MULTILINE)
            text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)
            # Collapse blank lines and trailing whitespace
            text = re.sub(r"\n{3,}", "\n\n", text)
            text = re.sub(r"[ \t]+", " ", text)
            return text.strip()

        cleaned_readme = ""
        if readme:
            stripped = _strip_markdown(readme)
            if len(stripped) >= DataCleaner.MIN_BODY_LENGTH:
                cleaned_readme = stripped[:4000]

        if not cleaned_readme:
            # Fallback: use repo description
            desc = (description or "").strip()
            return desc if len(desc) >= DataCleaner.MIN_BODY_LENGTH else None

        return cleaned_readme

    @staticmethod
    def clean_news_content(content: str | None, title: str) -> str | None:
        """
        Cleans scraped news article content.
        Handles None content (captcha/paywall) and residual HTML from BeautifulSoup.
        Falls back to title if content is absent but title is substantial enough.
        """
        if not content:
            # Only use title as fallback if it's descriptive enough
            return title.strip() if len(title.strip()) >= 60 else None

        # Unescape HTML entities (&amp; → &, &nbsp; → space, etc.)
        cleaned = html.unescape(content)

        # Detect paywall/captcha by scanning the first 300 characters
        head = cleaned[:300].lower()
        for pattern in DataCleaner.PAYWALL_PATTERNS:
            if re.search(pattern, head):
                return None

        # Collapse whitespace from scraping artefacts
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        return cleaned[:5000] if len(cleaned) >= DataCleaner.MIN_BODY_LENGTH else None

    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detects the ISO 639-1 language code of the text.
        Samples the first 500 chars for speed. Returns 'en' on detection failure.
        """
        try:
            return detect(text[:500])
        except LangDetectException:
            return "en"


# ---------------------------------------------------------------------------
# CleanAndNormalizeUseCase — Stage 0 + Stage 1
# ---------------------------------------------------------------------------

class CleanAndNormalizeUseCase:
    """
    Stage 0 + Stage 1 of the marketing pipeline.

    Reads raw data from all three sources (YouTube, GitHub, Google News),
    applies source-specific cleaning, detects language, optionally translates
    non-English content to English via the LLM, and produces a unified list of
    NormalizedItems ready for intent filtering and ML clustering.

    Items that fail quality thresholds (empty body, too short) are silently
    discarded and counted in the returned CleaningStats for observability.
    """

    def __init__(
        self,
        youtube_repo: YouTubeRepository,
        github_repo: GitHubRepository,
        google_news_repo: GoogleNewsRepository,
        llm: LLMClient,
        limit_per_source: int = 50,
        translate_non_english: bool = True,
    ) -> None:
        self._youtube_repo = youtube_repo
        self._github_repo = github_repo
        self._google_news_repo = google_news_repo
        self._llm = llm
        self._limit = limit_per_source
        self._translate = translate_non_english
        self._stats = CleaningStats()

    async def execute(self) -> tuple[list[NormalizedItem], CleaningStats]:
        """
        Returns (normalized_items, cleaning_stats).
        All three sources are processed concurrently for performance.
        """
        self._stats = CleaningStats()

        yt_items, gh_items, gn_items = await asyncio.gather(
            self._process_youtube(),
            self._process_github(),
            self._process_google_news(),
        )

        all_items = yt_items + gh_items + gn_items
        self._stats.passed = len(all_items)
        return all_items, self._stats

    # ------------------------------------------------------------------
    # YouTube
    # ------------------------------------------------------------------

    async def _process_youtube(self) -> list[NormalizedItem]:
        raw_videos = await self._youtube_repo.find_recent(limit=self._limit)
        self._stats.total_fetched += len(raw_videos)
        self._stats.by_source["youtube"] = 0

        items: list[NormalizedItem] = []
        for video in raw_videos:
            body = DataCleaner.clean_youtube_transcript(video.transcript)
            if not body:
                self._stats.discarded_empty_body += 1
                continue

            body, lang = await self._maybe_translate(body)

            engagement = (
                (video.metrics.likes * 3 + video.metrics.views) / 1000
            )

            pub_at = video.published_at
            if pub_at.tzinfo is None:
                pub_at = pub_at.replace(tzinfo=timezone.utc)

            items.append(NormalizedItem(
                id=f"yt_{video.id}",
                source="youtube",
                title=video.title,
                body=body,
                url=video.url,
                tags=[video.channel],
                engagement_score=round(engagement, 4),
                published_at=pub_at,
                original_language=lang,
            ))
            self._stats.by_source["youtube"] += 1

        return items

    # ------------------------------------------------------------------
    # GitHub
    # ------------------------------------------------------------------

    async def _process_github(self) -> list[NormalizedItem]:
        raw_repos = await self._github_repo.find_recent(limit=self._limit)
        self._stats.total_fetched += len(raw_repos)
        self._stats.by_source["github"] = 0

        items: list[NormalizedItem] = []
        for repo in raw_repos:
            body = DataCleaner.clean_github_readme(repo.readme, repo.description)
            if not body:
                self._stats.discarded_empty_body += 1
                continue

            body, lang = await self._maybe_translate(body)

            engagement = (repo.stargazers_count * 2) + (repo.forks_count or 0)

            # Parse updated_at string → datetime
            try:
                pub_at = datetime.fromisoformat(
                    repo.updated_at.replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pub_at = datetime.now(timezone.utc)

            items.append(NormalizedItem(
                id=f"gh_{repo.id}",
                source="github",
                title=repo.name,
                body=body,
                url=repo.html_url,
                tags=repo.topics or [],
                engagement_score=round(float(engagement), 4),
                published_at=pub_at,
                original_language=lang,
            ))
            self._stats.by_source["github"] += 1

        return items

    # ------------------------------------------------------------------
    # Google News
    # ------------------------------------------------------------------

    async def _process_google_news(self) -> list[NormalizedItem]:
        raw_articles = await self._google_news_repo.find_recent(limit=self._limit)
        self._stats.total_fetched += len(raw_articles)
        self._stats.by_source["google_news"] = 0

        items: list[NormalizedItem] = []
        for article in raw_articles:
            body = DataCleaner.clean_news_content(article.content, article.title)
            if not body:
                self._stats.discarded_empty_body += 1
                continue

            body, lang = await self._maybe_translate(body)

            # Parse pub_date — it can be a string or datetime
            try:
                if isinstance(article.pub_date, datetime):
                    pub_at = article.pub_date
                else:
                    pub_at = datetime.fromisoformat(
                        str(article.pub_date).replace("Z", "+00:00")
                    )
                if pub_at.tzinfo is None:
                    pub_at = pub_at.replace(tzinfo=timezone.utc)
            except (ValueError, AttributeError):
                pub_at = datetime.now(timezone.utc)

            items.append(NormalizedItem(
                id=f"gn_{article.id}",
                source="google_news",
                title=article.title,
                body=body,
                url=article.link,
                tags=[article.source_name],
                engagement_score=0.5,  # News articles have no engagement metric
                published_at=pub_at,
                original_language=lang,
            ))
            self._stats.by_source["google_news"] += 1

        return items

    # ------------------------------------------------------------------
    # Language detection & translation helper
    # ------------------------------------------------------------------

    async def _maybe_translate(self, text: str) -> tuple[str, str]:
        """
        Detects the language of text. If non-English and translation is enabled,
        calls the LLM to translate it. Returns (final_text, detected_lang).
        """
        lang = DataCleaner.detect_language(text)
        if lang != "en" and self._translate:
            try:
                translated = await self._llm.translate_to_english(text)
                self._stats.translated += 1
                return translated, lang
            except Exception as e:
                print(f"Translation error (lang={lang}): {e}")
        return text, lang
