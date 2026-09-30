import asyncio
from datetime import datetime, timedelta, timezone
from typing import List

import httpx

from ..entities.github_data_entity import GitHubDataEntity
from ..repositories.github_repository import GitHubRepository


class GitHubFetcherUseCase:
    """
    Reads search config from DB, fetches GitHub repositories concurrently
    by keyword+topic combination, applies post-API filters (language, stars,
    forks, license), downloads READMEs, and saves via UPSERT.
    Config is loaded automatically — no parameters needed.
    """

    def __init__(self, repository: GitHubRepository, token: str | None = None):
        self.repository = repository
        self.token = token

    async def execute(self) -> List[GitHubDataEntity]:
        """Loads config from DB, fetches GitHub repos, and saves them. Returns the saved entities."""
        config = await self.repository.get_config()

        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"

        limits = httpx.Limits(max_keepalive_connections=20, max_connections=50)
        async with httpx.AsyncClient(headers=headers, limits=limits) as client:
            # Phase 1: Search concurrently per topic
            raw_repos = await self._search_repos(client, config)
            if not raw_repos:
                config.last_search_at = datetime.now(timezone.utc)
                await self.repository.save_config(config)
                return []

            # Phase 2: Apply post-API filters
            filtered = self._apply_filters(raw_repos, config)

            # Phase 3: Fetch READMEs concurrently and map to entities
            entities = await self._fetch_readmes_and_map(client, filtered)

            # Phase 4: Bulk DB saving
            if entities:
                await self.repository.save_many(entities)

        # Update last_search_at in config
        config.last_search_at = datetime.now(timezone.utc)
        await self.repository.save_config(config)

        return entities

    async def _search_repos(self, client: httpx.AsyncClient, config) -> List[dict]:
        """
        GitHub API doesn't support 'topic:A OR topic:B', so we make one request per topic
        concurrently, then deduplicate by repo ID.
        """
        pushed_date = (datetime.now(timezone.utc) - timedelta(days=config.days_active)).strftime("%Y-%m-%d")
        kw_part = " OR ".join(config.keywords) if config.keywords else ""
        base_q_parts = []
        if kw_part:
            base_q_parts.append(f"({kw_part})")
        base_q_parts.append(f"stars:>={config.min_stars}")
        base_q_parts.append(f"forks:>={config.min_forks}")
        base_q_parts.append(f"pushed:>={pushed_date}")
        base_q = " ".join(base_q_parts)

        search_url = "https://api.github.com/search/repositories"
        topics = config.selected_topics if config.selected_topics else [None]

        async def search_one(topic: str | None) -> List[dict]:
            q = f"{base_q} topic:{topic}" if topic else base_q
            params = {
                "q": q,
                "sort": "stars",
                "order": "desc",
                "per_page": min(config.max_results, 100),
            }
            try:
                r = await client.get(search_url, params=params)
                r.raise_for_status()
                return r.json().get("items", [])
            except Exception as e:
                print(f"GitHub search error (topic={topic}): {e}")
                return []

        results = await asyncio.gather(*(search_one(t) for t in topics))

        # Flatten and deduplicate by repo ID
        seen: set[int] = set()
        deduped: List[dict] = []
        for repo in (r for sub in results for r in sub):
            if repo["id"] not in seen:
                seen.add(repo["id"])
                deduped.append(repo)

        return deduped

    def _apply_filters(self, repos: List[dict], config) -> List[dict]:
        """Apply language, stars, forks, and license filters that the GitHub API cannot handle natively."""
        allowed_langs = {lang.lower() for lang in config.selected_languages} if config.selected_languages else set()
        filtered = []
        for repo in repos:
            if config.require_license and not repo.get("license"):
                continue
            if allowed_langs and (repo.get("language") or "").lower() not in allowed_langs:
                continue
            filtered.append(repo)
        return filtered[:config.max_results]

    async def _fetch_readmes_and_map(self, client: httpx.AsyncClient, repos: List[dict]) -> List[GitHubDataEntity]:
        """Fetch README for each repo concurrently and map to domain entities."""

        async def fetch_one(repo: dict) -> GitHubDataEntity:
            readme = ""
            try:
                readme_url = f"https://api.github.com/repos/{repo['full_name']}/readme"
                r = await client.get(
                    readme_url,
                    headers={"Accept": "application/vnd.github.v3.raw"}
                )
                if r.status_code == 200:
                    readme = r.text[:10000]  # Truncate to avoid huge blobs
            except Exception as e:
                print(f"README fetch error for {repo.get('full_name')}: {e}")

            license_name: str | None = None
            if repo.get("license") and isinstance(repo["license"], dict):
                license_name = repo["license"].get("spdx_id") or repo["license"].get("name")

            return GitHubDataEntity(
                id=repo["id"],
                name=repo["name"],
                full_name=repo["full_name"],
                html_url=repo["html_url"],
                description=repo.get("description") or "",
                stargazers_count=repo.get("stargazers_count", 0),
                language=repo.get("language") or "",
                updated_at=repo.get("updated_at", ""),
                topics=repo.get("topics", []),
                readme=readme,
                owner_avatar_url=repo.get("owner", {}).get("avatar_url"),
                forks_count=repo.get("forks_count"),
                open_issues_count=repo.get("open_issues_count"),
                license=license_name,
            )

        return list(await asyncio.gather(*(fetch_one(r) for r in repos)))
