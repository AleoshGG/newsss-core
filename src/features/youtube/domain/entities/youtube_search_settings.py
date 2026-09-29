from dataclasses import dataclass, field

@dataclass
class YouTubeSearchSettings:
    keywords: list[str] = field(default_factory=list)
    channel_ids: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=lambda: ["any"])
    max_results: int = 50
