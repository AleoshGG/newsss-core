from datetime import datetime
from typing import List, Optional
import strawberry

from ...domain.entities.github_data_entity import GitHubDataEntity
from ...domain.entities.github_search_config_entity import GitHubSearchConfigEntity


@strawberry.type
class GitHubRepoType:
    id: int
    name: str
    full_name: str
    html_url: str
    description: Optional[str]
    stargazers_count: int
    language: Optional[str]
    updated_at: str
    topics: List[str]
    readme: str
    owner_avatar_url: Optional[str]
    forks_count: Optional[int]
    open_issues_count: Optional[int]
    license: Optional[str]

    @classmethod
    def from_entity(cls, entity: GitHubDataEntity) -> "GitHubRepoType":
        return cls(
            id=entity.id,
            name=entity.name,
            full_name=entity.full_name,
            html_url=entity.html_url,
            description=entity.description,
            stargazers_count=entity.stargazers_count,
            language=entity.language,
            updated_at=entity.updated_at,
            topics=entity.topics or [],
            readme=entity.readme or "",
            owner_avatar_url=entity.owner_avatar_url,
            forks_count=entity.forks_count,
            open_issues_count=entity.open_issues_count,
            license=entity.license,
        )


@strawberry.type
class GitHubSearchConfigType:
    id: int
    keywords: List[str]
    days_active: int
    min_stars: int
    min_forks: int
    require_license: bool
    selected_topics: List[str]
    selected_languages: List[str]
    max_results: int
    last_search_at: Optional[datetime]

    @classmethod
    def from_entity(cls, entity: GitHubSearchConfigEntity) -> "GitHubSearchConfigType":
        return cls(
            id=entity.id,
            keywords=entity.keywords,
            days_active=entity.days_active,
            min_stars=entity.min_stars,
            min_forks=entity.min_forks,
            require_license=entity.require_license,
            selected_topics=entity.selected_topics,
            selected_languages=entity.selected_languages,
            max_results=entity.max_results,
            last_search_at=entity.last_search_at,
        )


@strawberry.input(description="Configuration settings for searching GitHub repositories.")
class GitHubSearchConfigInput:
    keywords: List[str] = strawberry.field(description="Keywords to search for (combined with OR).")
    days_active: int = strawberry.field(default=7, description="Only include repos with activity in the last N days.")
    min_stars: int = strawberry.field(default=50, description="Minimum number of stars.")
    min_forks: int = strawberry.field(default=5, description="Minimum number of forks.")
    require_license: bool = strawberry.field(default=False, description="If true, exclude repos without a license.")
    selected_topics: Optional[List[str]] = strawberry.field(default_factory=list, description="Required topics (one request per topic, then merged).")
    selected_languages: Optional[List[str]] = strawberry.field(default_factory=list, description="Filter by programming language (post-API).")
    max_results: int = strawberry.field(default=30, description="Maximum number of repositories to fetch and save.")

    def to_entity(self) -> GitHubSearchConfigEntity:
        return GitHubSearchConfigEntity(
            id=1,
            keywords=self.keywords,
            days_active=self.days_active,
            min_stars=self.min_stars,
            min_forks=self.min_forks,
            require_license=self.require_license,
            selected_topics=self.selected_topics or [],
            selected_languages=self.selected_languages or [],
            max_results=self.max_results,
        )
