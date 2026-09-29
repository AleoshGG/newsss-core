from datetime import datetime
from typing import List, Optional
import strawberry

from ...domain.entities.youtube_video_data_entity import YouTubeVideoDataEntity
from ...domain.entities.youtube_video_metrics import YouTubeVideoMetrics
from ...domain.entities.youtube_search_settings import YouTubeSearchSettings


@strawberry.type
class YouTubeVideoMetricsType:
    views: int
    likes: int
    comments: int
    
    @classmethod
    def from_entity(cls, entity: YouTubeVideoMetrics) -> "YouTubeVideoMetricsType":
        return cls(
            views=entity.views,
            likes=entity.likes,
            comments=entity.comments
        )


@strawberry.type
class YouTubeVideoType:
    id: str
    title: str
    channel: str
    published_at: datetime
    url: str
    metrics: YouTubeVideoMetricsType
    thumbnail_url: str
    transcript: str

    @classmethod
    def from_entity(cls, entity: YouTubeVideoDataEntity) -> "YouTubeVideoType":
        return cls(
            id=entity.id,
            title=entity.title,
            channel=entity.channel,
            published_at=entity.published_at,
            url=entity.url,
            metrics=YouTubeVideoMetricsType.from_entity(entity.metrics),
            thumbnail_url=entity.thumbnail_url,
            transcript=entity.transcript
        )


@strawberry.input
class YouTubeSearchSettingsInput:
    keywords: List[str]
    channel_ids: Optional[List[str]] = strawberry.field(default_factory=list)
    languages: Optional[List[str]] = strawberry.field(default_factory=lambda: ["any"])
    max_results: int = 50

    def to_entity(self) -> YouTubeSearchSettings:
        return YouTubeSearchSettings(
            keywords=self.keywords,
            channel_ids=self.channel_ids or [],
            languages=self.languages or ["any"],
            max_results=self.max_results
        )
