from ..entities.github_search_config_entity import GitHubSearchConfigEntity
from ..repositories.github_repository import GitHubRepository


class UpdateGitHubConfigUseCase:
    """Use case to update the GitHub search configuration singleton in the database."""

    def __init__(self, repository: GitHubRepository):
        self.repository = repository

    async def execute(self, new_config: GitHubSearchConfigEntity) -> GitHubSearchConfigEntity:
        new_config.id = 1  # Always enforce singleton
        return await self.repository.save_config(new_config)
