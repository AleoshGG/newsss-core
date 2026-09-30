from dataclasses import dataclass
from datetime import datetime

from .youtube_video_metrics import YouTubeVideoMetrics

@dataclass(frozen=True)
class YouTubeVideoDataEntity:
    id: str
    title: str
    channel: str
    published_at: datetime
    url: str
    metrics: YouTubeVideoMetrics
    thumbnail_url: str
    transcript: str
    is_processed: bool = False
