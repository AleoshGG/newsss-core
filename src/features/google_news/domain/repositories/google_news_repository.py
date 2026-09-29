from abc import ABC, abstractmethod
from datetime import datetime

from ..entities.google_news_article_data_entity import GoogleNewsArticleDataEntity


class GoogleNewsRepository(ABC):

    @abstractmethod
    async def save(self, article: GoogleNewsArticleDataEntity) -> GoogleNewsArticleDataEntity:
        pass

    @abstractmethod
    async def find_all(self) -> list[GoogleNewsArticleDataEntity]:
        pass

    @abstractmethod
    async def delete_all_before_date(self, date: datetime) -> int:
        pass
