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
        async with httpx.AsyncClient(limits=limits, follow_redirects=True, timeout=15.0) as client:
            # Phase 1: Fetch 2 RSS feeds concurrently
            entries = await self._fetch_rss_feeds(client, config)
            if not entries:
                config.last_search_at = datetime.now(timezone.utc)
                await self.repository.save_config(config)
                return []

            # Phase 2: Scrape og:image + article content concurrently
            enriched = await self._scrape_articles(client, entries, config.max_results)

            # Phase 3: UPSERT all
            if enriched:
                await asyncio.gather(*(self.repository.save(a) for a in enriched))

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
        from bs4 import BeautifulSoup

        async def scrape_one(entry) -> GoogleNewsArticleDataEntity:
            link = getattr(entry, "link", "")
            image_url: str | None = None
            content: str | None = None

            try:
                r = await client.get(link, timeout=10.0)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, "lxml")

                    # Extract og:image
                    og_tag = soup.find("meta", property="og:image")
                    if og_tag:
                        image_url = og_tag.get("content")

                    # Extract article text — remove noise tags first
                    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                        tag.decompose()

                    article_tag = soup.find("article") or soup.find("main") or soup.body
                    if article_tag:
                        content = article_tag.get_text(separator=" ", strip=True)[:5000]
            except Exception as e:
                print(f"Scraping error for {link}: {e}")

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
