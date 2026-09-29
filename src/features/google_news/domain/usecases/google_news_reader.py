from typing import List

from ..entities.google_news_article_data_entity import GoogleNewsArticleDataEntity
from ..repositories.google_news_repository import GoogleNewsRepository


class ReadRecentNewsArticlesUseCase:
    """Use case to read news articles stored in the database, ordered from newest to oldest."""

    def __init__(self, repository: GoogleNewsRepository):
        self.repository = repository

    async def execute(self, limit: int = 50, offset: int = 0) -> List[GoogleNewsArticleDataEntity]:
        return await self.repository.find_recent(limit=limit, offset=offset)
