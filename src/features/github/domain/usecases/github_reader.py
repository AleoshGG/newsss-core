from typing import List

from ..entities.github_data_entity import GitHubDataEntity
from ..repositories.github_repository import GitHubRepository


class ReadRecentGitHubReposUseCase:
    """Use case to read GitHub repositories stored in the database, ordered by update date."""

    def __init__(self, repository: GitHubRepository):
        self.repository = repository

    async def execute(self, limit: int = 50, offset: int = 0) -> List[GitHubDataEntity]:
        return await self.repository.find_recent(limit=limit, offset=offset)
