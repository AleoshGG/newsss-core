import asyncio
from dataclasses import dataclass
from typing import Literal

from src.core.llm.llm_client import LLMClient
from src.features.github.domain.repositories.github_repository import GitHubRepository
from src.features.google_news.domain.repositories.google_news_repository import GoogleNewsRepository
from src.features.youtube.domain.repositories.youtube_repository import YouTubeRepository

from ..entities.marketing_campaign_entity import MarketingCampaign
from ..entities.normalized_item_entity import CleaningStats
from ..repositories.marketing_repository import MarketingRepository
from .clean_and_normalize import CleanAndNormalizeUseCase
from .cluster_content import ClusterContentUseCase
from .generate_marketing_content import GenerateMarketingContentUseCase
from .intent_filter import IntentFilterUseCase


@dataclass
class PipelineConfig:
    """Configuration for a single marketing pipeline run."""

    limit_per_source: int = 50
    min_intent_score: float = 0.25
    n_clusters: int = 5
    campaign_type: Literal["linkedin_post", "twitter_thread", "email_newsletter"] = "linkedin_post"
    translate_non_english: bool = True


@dataclass
class PipelineResult:
    """Output of a complete marketing pipeline run."""

    campaigns: list[MarketingCampaign]
    cleaning_stats: CleaningStats
    clusters_found: int
    items_processed: int
    items_after_filter: int


class RunMarketingPipelineUseCase:
    """
    Orchestrates the full 5-stage ML marketing pipeline:

      Stage 0+1 (CleanAndNormalize): Reads raw data from PostgreSQL (YouTube,
        GitHub, Google News), applies source-specific cleaning (markdown strip,
        empty transcript detection, captcha/paywall detection), detects language,
        and translates non-English content to English via the LLM.

      Stage 2 (IntentFilter): Scores each NormalizedItem for B2B marketing intent
        using keyword matching + engagement + recency. Discards low-signal items.

      Stage 3 (ClusterContent): Generates semantic embeddings locally with
        sentence-transformers and clusters items using K-Means. Extracts TF-IDF
        keywords per cluster for automatic topic labeling. Runs fully on CPU.

      Stage 4 (GenerateMarketingContent): For each cluster, calls the Gemini LLM
        to generate a structured marketing campaign (hook, body, CTA, hashtags)
        calibrated for B2B / consulting firm audiences. Cluster calls are
        concurrent via asyncio.gather for minimal latency.

    Results are persisted to PostgreSQL and returned to the caller.
    Errors in individual cluster generation are isolated — a failure in one
    cluster does not abort the rest of the pipeline.
    """

    def __init__(
        self,
        youtube_repo: YouTubeRepository,
        github_repo: GitHubRepository,
        google_news_repo: GoogleNewsRepository,
        marketing_repo: MarketingRepository,
        llm: LLMClient,
    ) -> None:
        self._youtube_repo = youtube_repo
        self._github_repo = github_repo
        self._google_news_repo = google_news_repo
        self._marketing_repo = marketing_repo
        self._llm = llm

    async def execute(self, config: PipelineConfig) -> PipelineResult:
        """
        Runs the full pipeline and returns the result.
        Raises ValueError if no usable items are found after cleaning.
        """

        # ------------------------------------------------------------------
        # Stage 0+1 — Clean & Normalize
        # ------------------------------------------------------------------
        normalize_uc = CleanAndNormalizeUseCase(
            youtube_repo=self._youtube_repo,
            github_repo=self._github_repo,
            google_news_repo=self._google_news_repo,
            llm=self._llm,
            limit_per_source=config.limit_per_source,
            translate_non_english=config.translate_non_english,
        )
        items, stats = await normalize_uc.execute()

        if not items:
            return PipelineResult(
                campaigns=[],
                cleaning_stats=stats,
                clusters_found=0,
                items_processed=0,
                items_after_filter=0,
            )

        # ------------------------------------------------------------------
        # Stage 2 — Intent filter
        # ------------------------------------------------------------------
        scored = IntentFilterUseCase().execute(items, min_score=config.min_intent_score)

        if not scored:
            return PipelineResult(
                campaigns=[],
                cleaning_stats=stats,
                clusters_found=0,
                items_processed=len(items),
                items_after_filter=0,
            )

        # ------------------------------------------------------------------
        # Stage 3 — Semantic clustering (local ML)
        # ------------------------------------------------------------------
        cluster_uc = ClusterContentUseCase(n_clusters=config.n_clusters)
        clusters = await cluster_uc.execute(scored)

        # Persist clusters using bulk save and capture db IDs
        if clusters:
            try:
                clusters = await self._marketing_repo.save_many_clusters(clusters)
            except Exception as e:
                print(f"Bulk cluster save error: {e}")

        # ------------------------------------------------------------------
        # Stage 4 — LLM content generation (concurrent per cluster)
        # ------------------------------------------------------------------
        gen_uc = GenerateMarketingContentUseCase(
            llm=self._llm,
            campaign_type=config.campaign_type,
        )

        generation_results = await asyncio.gather(
            *(gen_uc.execute(c) for c in clusters),
            return_exceptions=True,
        )

        campaigns: list[MarketingCampaign] = []
        for i, result in enumerate(generation_results):
            if isinstance(result, Exception):
                print(f"Campaign generation error (cluster={clusters[i].topic_label}): {result}")
            else:
                campaigns.append(result)

        # Persist campaigns using bulk save
        if campaigns:
            try:
                await self._marketing_repo.save_many_campaigns(campaigns)
            except Exception as e:
                print(f"Bulk campaign save error: {e}")

        return PipelineResult(
            campaigns=campaigns,
            cleaning_stats=stats,
            clusters_found=len(clusters),
            items_processed=len(items),
            items_after_filter=len(scored),
        )
