from ...domain.entities.google_news_config_entity import GoogleNewsConfigEntity
from ..models.google_news_config_model import GoogleNewsConfigModel


def to_config_entity(model: GoogleNewsConfigModel) -> GoogleNewsConfigEntity:
    return GoogleNewsConfigEntity(
        id=model.id,
        q=model.q or "Inteligencia Artificial OR IA",
        hl=model.hl or "es-419",
        gl=model.gl or "MX",
        ceid=model.ceid or "MX:es-419",
        when=model.when or "1d",
        site=model.site,
        intitle=model.intitle,
        max_results=model.max_results or 30,
        last_search_at=model.last_search_at,
    )


def to_config_model(entity: GoogleNewsConfigEntity) -> GoogleNewsConfigModel:
    return GoogleNewsConfigModel(
        id=entity.id,
        q=entity.q,
        hl=entity.hl,
        gl=entity.gl,
        ceid=entity.ceid,
        when=entity.when,
        site=entity.site,
        intitle=entity.intitle,
        max_results=entity.max_results,
        last_search_at=entity.last_search_at,
    )
