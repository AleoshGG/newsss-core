from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GitHubSearchConfigEntity:
    """Domain entity representing the GitHub search configuration (singleton, id=1)."""
    id: int = 1
    keywords: list[str] = field(default_factory=lambda: ["openai", "llm", "claude"])
    days_active: int = 7
    min_stars: int = 50
    min_forks: int = 5
    require_license: bool = False
    selected_topics: list[str] = field(default_factory=lambda: ["ai", "llm"])
    selected_languages: list[str] = field(default_factory=lambda: ["python", "typescript"])
    max_results: int = 30
    last_search_at: datetime | None = None
