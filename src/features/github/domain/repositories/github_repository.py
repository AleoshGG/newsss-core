from abc import ABC, abstractmethod
from datetime import datetime

from ..entities.github_data_entity import GitHubDataEntity
from ..entities.github_search_config_entity import GitHubSearchConfigEntity


class GitHubRepository(ABC):

    @abstractmethod
    async def save(self, data: GitHubDataEntity) -> GitHubDataEntity:
        pass

    @abstractmethod
    async def find_all(self) -> list[GitHubDataEntity]:
        pass

    @abstractmethod
    async def find_recent(self, limit: int = 50, offset: int = 0) -> list[GitHubDataEntity]:
        pass

    @abstractmethod
    async def delete_all_before_date(self, date: datetime) -> int:
        pass

    @abstractmethod
    async def get_config(self) -> GitHubSearchConfigEntity:
        """Returns the singleton search config (id=1), auto-creating it with defaults if it doesn't exist."""
        pass

    @abstractmethod
    async def save_config(self, config: GitHubSearchConfigEntity) -> GitHubSearchConfigEntity:
        """Upserts the singleton search config (id=1)."""
        pass
