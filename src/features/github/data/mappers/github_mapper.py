from ...domain.entities.github_data_entity import GitHubDataEntity
from ..models.github_data_model import GitHubDataModel

def to_entity(model: GitHubDataModel) -> GitHubDataEntity:
    return GitHubDataEntity(
        id=model.id, name=model.name, full_name=model.full_name, html_url=model.html_url,
        description=model.description, stargazers_count=model.stargazers_count,
        language=model.language, updated_at=model.updated_at, topics=model.topics,
        readme=model.readme, owner_avatar_url=model.owner_avatar_url,
        forks_count=model.forks_count, open_issues_count=model.open_issues_count,
        license=model.license, is_processed=model.is_processed
    )

def to_model(entity: GitHubDataEntity) -> GitHubDataModel:
    return GitHubDataModel(
        id=entity.id, name=entity.name, full_name=entity.full_name, html_url=entity.html_url,
        description=entity.description, stargazers_count=entity.stargazers_count,
        language=entity.language, updated_at=entity.updated_at, topics=entity.topics,
        readme=entity.readme, owner_avatar_url=entity.owner_avatar_url,
        forks_count=entity.forks_count, open_issues_count=entity.open_issues_count,
        license=entity.license, is_processed=entity.is_processed
    )
