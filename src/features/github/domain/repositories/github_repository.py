from abc import ABC, abstractmethod
from datetime import datetime

from ..entities.github_data_entity import GitHubDataEntity


class GitHubRepository(ABC):

    @abstractmethod
    async def save(self, data: GitHubDataEntity) -> GitHubDataEntity:
        pass

    @abstractmethod
    async def find_all(self) -> list[GitHubDataEntity]:
        pass

    @abstractmethod
    async def delete_all_before_date(self, date: datetime) -> int:
        pass
