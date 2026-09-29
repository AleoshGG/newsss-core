from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class YouTubeSearchConfigEntity:
    """Domain entity representing the YouTube search configuration (singleton, id=1)."""
    id: int = 1
    keywords: list[str] = field(default_factory=lambda: ["OpenAI", "Anthropic", "Claude", "ChatGPT"])
    channel_ids: list[str] = field(default_factory=lambda: ["@googledeepmind", "@OpenAI"])
    languages: list[str] = field(default_factory=lambda: ["es", "en"])
    max_results: int = 5
    last_search_at: datetime | None = None
