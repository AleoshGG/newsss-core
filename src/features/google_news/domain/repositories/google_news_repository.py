from abc import ABC, abstractmethod
from datetime import datetime

from ..entities.google_news_article_data_entity import GoogleNewsArticleDataEntity
from ..entities.google_news_config_entity import GoogleNewsConfigEntity


class GoogleNewsRepository(ABC):

    @abstractmethod
    async def save(self, article: GoogleNewsArticleDataEntity) -> GoogleNewsArticleDataEntity:
        pass

    @abstractmethod
    async def find_all(self) -> list[GoogleNewsArticleDataEntity]:
        pass

    @abstractmethod
    async def find_recent(self, limit: int = 50, offset: int = 0) -> list[GoogleNewsArticleDataEntity]:
        pass

    @abstractmethod
    async def delete_all_before_date(self, date: datetime) -> int:
        pass

    @abstractmethod
    async def get_config(self) -> GoogleNewsConfigEntity:
        """Returns the singleton search config (id=1), auto-creating it with defaults if it doesn't exist."""
        pass

    @abstractmethod
    async def save_config(self, config: GoogleNewsConfigEntity) -> GoogleNewsConfigEntity:
        """Upserts the singleton search config (id=1)."""
        pass
