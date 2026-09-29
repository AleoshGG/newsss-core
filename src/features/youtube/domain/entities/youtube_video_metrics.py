from dataclasses import dataclass

@dataclass(frozen=True)
class YouTubeVideoMetrics:
    views: int
    likes: int
    comments: int