from ...domain.entities.youtube_video_data_entity import YouTubeVideoDataEntity
from ...domain.entities.youtube_video_metrics import YouTubeVideoMetrics
from ..models.youtube_video_model import YouTubeVideoModel

def to_entity(model: YouTubeVideoModel) -> YouTubeVideoDataEntity:
    metrics = YouTubeVideoMetrics(views=model.views, likes=model.likes, comments=model.comments)
    return YouTubeVideoDataEntity(
        id=model.id, title=model.title, channel=model.channel,
        published_at=model.published_at, url=model.url,
        metrics=metrics, thumbnail_url=model.thumbnail_url, transcript=model.transcript
    )

def to_model(entity: YouTubeVideoDataEntity) -> YouTubeVideoModel:
    return YouTubeVideoModel(
        id=entity.id, title=entity.title, channel=entity.channel,
        published_at=entity.published_at, url=entity.url,
        thumbnail_url=entity.thumbnail_url, transcript=entity.transcript,
        views=entity.metrics.views, likes=entity.metrics.likes, comments=entity.metrics.comments
    )
