from ...domain.entities.youtube_search_config_entity import YouTubeSearchConfigEntity
from ..models.youtube_search_config_model import YouTubeSearchConfigModel


def to_config_entity(model: YouTubeSearchConfigModel) -> YouTubeSearchConfigEntity:
    return YouTubeSearchConfigEntity(
        id=model.id,
        keywords=list(model.keywords or []),
        channel_ids=list(model.channel_ids or []),
        languages=list(model.languages or ["es", "en"]),
        max_results=model.max_results or 5,
        last_search_at=model.last_search_at,
    )


def to_config_model(entity: YouTubeSearchConfigEntity) -> YouTubeSearchConfigModel:
    return YouTubeSearchConfigModel(
        id=entity.id,
        keywords=entity.keywords,
        channel_ids=entity.channel_ids,
        languages=entity.languages,
        max_results=entity.max_results,
        last_search_at=entity.last_search_at,
    )
