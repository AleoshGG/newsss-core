from datetime import datetime
from typing import List, Optional
import strawberry

from ...domain.entities.youtube_video_data_entity import YouTubeVideoDataEntity
from ...domain.entities.youtube_video_metrics import YouTubeVideoMetrics
from ...domain.entities.youtube_search_config_entity import YouTubeSearchConfigEntity


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


@strawberry.type
class YouTubeSearchConfigType:
    id: int
    keywords: List[str]
    channel_ids: List[str]
    languages: List[str]
    max_results: int
    last_search_at: Optional[datetime]

    @classmethod
    def from_entity(cls, entity: YouTubeSearchConfigEntity) -> "YouTubeSearchConfigType":
        return cls(
            id=entity.id,
            keywords=entity.keywords,
            channel_ids=entity.channel_ids,
            languages=entity.languages,
            max_results=entity.max_results,
            last_search_at=entity.last_search_at,
        )


@strawberry.input(description="Configuration settings for searching YouTube videos.")
class YouTubeSearchConfigInput:
    keywords: List[str] = strawberry.field(description="List of keywords to search for.")
    channel_ids: Optional[List[str]] = strawberry.field(default_factory=list, description="Optional list of channel handles or IDs (e.g. '@googledeepmind').")
    languages: Optional[List[str]] = strawberry.field(default_factory=lambda: ["es", "en"], description="List of language codes (e.g. 'en', 'es', or 'any').")
    max_results: int = strawberry.field(default=5, description="Maximum number of videos to fetch per channel or globally.")

    def to_entity(self) -> YouTubeSearchConfigEntity:
        return YouTubeSearchConfigEntity(
            id=1,
            keywords=self.keywords,
            channel_ids=self.channel_ids or [],
            languages=self.languages or ["es", "en"],
            max_results=self.max_results,
        )
