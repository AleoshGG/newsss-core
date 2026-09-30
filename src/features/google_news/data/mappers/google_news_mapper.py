from datetime import datetime
from ...domain.entities.google_news_article_data_entity import GoogleNewsArticleDataEntity
from ..models.google_news_article_model import GoogleNewsArticleModel

def to_entity(model: GoogleNewsArticleModel) -> GoogleNewsArticleDataEntity:
    return GoogleNewsArticleDataEntity(
        id=model.id, title=model.title, link=model.link, pub_date=model.pub_date,
        source_name=model.source_name, source_url=model.source_url,
        fetched_at=model.fetched_at, image_url=model.image_url, content=model.content,
        is_processed=model.is_processed
    )

def to_model(entity: GoogleNewsArticleDataEntity) -> GoogleNewsArticleModel:
    pub_date_str = entity.pub_date.isoformat() if isinstance(entity.pub_date, datetime) else entity.pub_date
    return GoogleNewsArticleModel(
        id=entity.id, title=entity.title, link=entity.link, pub_date=pub_date_str,
        source_name=entity.source_name, source_url=entity.source_url,
        fetched_at=entity.fetched_at, image_url=entity.image_url, content=entity.content,
        is_processed=entity.is_processed
    )
