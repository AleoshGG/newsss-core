from ...domain.entities.github_search_config_entity import GitHubSearchConfigEntity
from ..models.github_search_config_model import GitHubSearchConfigModel


def to_config_entity(model: GitHubSearchConfigModel) -> GitHubSearchConfigEntity:
    return GitHubSearchConfigEntity(
        id=model.id,
        keywords=list(model.keywords or []),
        days_active=model.days_active or 7,
        min_stars=model.min_stars or 50,
        min_forks=model.min_forks or 5,
        require_license=model.require_license or False,
        selected_topics=list(model.selected_topics or []),
        selected_languages=list(model.selected_languages or []),
        max_results=model.max_results or 30,
        last_search_at=model.last_search_at,
    )


def to_config_model(entity: GitHubSearchConfigEntity) -> GitHubSearchConfigModel:
    return GitHubSearchConfigModel(
        id=entity.id,
        keywords=entity.keywords,
        days_active=entity.days_active,
        min_stars=entity.min_stars,
        min_forks=entity.min_forks,
        require_license=entity.require_license,
        selected_topics=entity.selected_topics,
        selected_languages=entity.selected_languages,
        max_results=entity.max_results,
        last_search_at=entity.last_search_at,
    )
