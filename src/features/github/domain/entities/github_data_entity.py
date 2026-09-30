from dataclasses import dataclass

@dataclass(frozen=True)
class GitHubDataEntity:
    id: int
    name: str
    full_name: str
    html_url: str
    description: str
    stargazers_count: int
    language: str
    updated_at: str
    topics: list[str]
    readme: str
    owner_avatar_url: str | None = None
    forks_count: int | None = None
    open_issues_count: int | None = None
    license: str | None = None
    is_processed: bool = False
