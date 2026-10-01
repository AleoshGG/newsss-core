import asyncio
from datetime import datetime, timezone
from typing import List

import httpx

from ..entities.google_news_article_data_entity import GoogleNewsArticleDataEntity
from ..repositories.google_news_repository import GoogleNewsRepository


class GoogleNewsFetcherUseCase:
    """
    Reads search config from DB, fetches two concurrent RSS feeds from Google News
    (configured language + English AI fallback), scrapes og:image and article content
    via BeautifulSoup, and saves articles via UPSERT.
    Config is loaded automatically — no parameters needed.
    """

    def __init__(self, repository: GoogleNewsRepository):
        self.repository = repository

    async def execute(self) -> List[GoogleNewsArticleDataEntity]:
        """Loads config from DB, fetches & scrapes news articles, and saves them."""
        config = await self.repository.get_config()

        limits = httpx.Limits(max_keepalive_connections=20, max_connections=50)
        async with httpx.AsyncClient(
            limits=limits,
            follow_redirects=True,
            timeout=15.0,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        ) as client:
            # Phase 1: Fetch 2 RSS feeds concurrently
            entries = await self._fetch_rss_feeds(client, config)
            if not entries:
                config.last_search_at = datetime.now(timezone.utc)
                await self.repository.save_config(config)
                return []

            # Phase 2: Scrape og:image + article content concurrently
            enriched = await self._scrape_articles(client, entries, config.max_results)

            # Phase 3: Bulk DB saving
            if enriched:
                await self.repository.save_many(enriched)

        # Update last_search_at in config
        config.last_search_at = datetime.now(timezone.utc)
        await self.repository.save_config(config)

        return enriched

    async def _fetch_rss_feeds(self, client: httpx.AsyncClient, config) -> List:
        """Fetch two concurrent RSS feeds: configured language and English AI fallback."""
        import feedparser

        base_url = "https://news.google.com/rss/search"

        # Build primary query with optional filters
        q_primary = config.q
        if config.site:
            q_primary += f" site:{config.site}"
        if config.intitle:
            q_primary += f" intitle:{config.intitle}"

        params_primary = {
            "q": q_primary,
            "hl": config.hl,
            "gl": config.gl,
            "ceid": config.ceid,
        }
        if config.when:
            params_primary["when"] = config.when

        params_english = {
            "q": f"{config.q} AI",
            "hl": "en-US",
            "gl": "US",
            "ceid": "US:en",
        }
        if config.when:
            params_english["when"] = config.when

        async def fetch_feed(params: dict) -> List:
            try:
                r = await client.get(base_url, params=params)
                r.raise_for_status()
                feed = feedparser.parse(r.text)
                return feed.entries
            except Exception as e:
                print(f"RSS fetch error (params={params}): {e}")
                return []

        results = await asyncio.gather(fetch_feed(params_primary), fetch_feed(params_english))

        # Flatten and deduplicate by link
        seen: set[str] = set()
        entries: List = []
        for entry in (e for sub in results for e in sub):
            link = getattr(entry, "link", "")
            if link and link not in seen:
                seen.add(link)
                entries.append(entry)

        return entries

    async def _scrape_articles(self, client: httpx.AsyncClient, entries: List, max_results: int) -> List[GoogleNewsArticleDataEntity]:
        """Scrape og:image and readable article text for each RSS entry."""
        import trafilatura
        from bs4 import BeautifulSoup
        try:
            from googlenewsdecoder import gnews_decoder_async
        except ImportError:
            gnews_decoder_async = None

        async def scrape_one(entry) -> GoogleNewsArticleDataEntity:
            link = getattr(entry, "link", "")
            image_url: str | None = None
            content: str | None = None

            real_url = link
            # 1. Decode Google News encrypted URL
            if gnews_decoder_async and "news.google.com" in link:
                try:
                    decoded = await gnews_decoder_async(link)
                    if decoded and decoded.get("decoded_url"):
                        real_url = decoded["decoded_url"]
                except Exception as e:
                    print(f"URL decode error for {link}: {e}")

            # 2. Scrape real URL
            try:
                r = await client.get(real_url, timeout=10.0, follow_redirects=True)
                if r.status_code == 200:
                    html = r.text
                    soup = BeautifulSoup(html, "lxml")

                    # Extract og:image
                    og_tag = soup.find("meta", property="og:image")
                    if og_tag:
                        image_url = og_tag.get("content")

                    # Strategy A: trafilatura — semantic article extraction (more robust)
                    extracted = trafilatura.extract(
                        html, include_comments=False, include_tables=False
                    )
                    if extracted and len(extracted.strip()) > 100:
                        content = extracted.strip()[:5000]
                    else:
                        # Strategy B: BeautifulSoup fallback — remove noise tags first
                        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                            tag.decompose()
                        article_tag = soup.find("article") or soup.find("main")
                        if article_tag:
                            content = article_tag.get_text(separator=" ", strip=True)[:5000]
            except Exception:
                pass

            # Fallback to RSS summary if content is missing (e.g. encrypted Google links)
            if not content:
                summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
                if summary:
                    content = BeautifulSoup(summary, "lxml").get_text(separator=" ", strip=True)
            if not content:
                content = getattr(entry, "title", "")

            # Extract source info from feedparser entry
            source = getattr(entry, "source", None)
            if isinstance(source, dict):
                source_name = source.get("title", "")
                source_url = source.get("href", "")
            else:
                source_name = getattr(source, "title", "") if source else ""
                source_url = getattr(source, "href", "") if source else ""

            entry_id = getattr(entry, "id", None) or link

            return GoogleNewsArticleDataEntity(
                id=entry_id,
                title=getattr(entry, "title", ""),
                link=link,
                pub_date=getattr(entry, "published", ""),
                source_name=source_name,
                source_url=source_url,
                fetched_at=datetime.now(timezone.utc),
                image_url=image_url,
                content=content,
            )

        tasks = [scrape_one(e) for e in entries[:max_results]]
        return list(await asyncio.gather(*tasks))
