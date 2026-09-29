import strawberry
from typing import List
from strawberry.types import Info

from ...domain.usecases.google_news_reader import ReadRecentNewsArticlesUseCase
from ...domain.usecases.google_news_fetcher import GoogleNewsFetcherUseCase
from ...domain.usecases.google_news_config_updater import UpdateGoogleNewsConfigUseCase
from .types import NewsArticleType, GoogleNewsConfigType, GoogleNewsConfigInput


@strawberry.type
class GoogleNewsQuery:
    @strawberry.field(description="Retrieves the most recently fetched news articles previously saved in the local database.")
    async def get_recent_news_articles(self, info: Info, limit: int = 50, offset: int = 0) -> List[NewsArticleType]:
        repo = info.context["google_news_repository"]
        use_case = ReadRecentNewsArticlesUseCase(repository=repo)
        articles = await use_case.execute(limit=limit, offset=offset)
        return [NewsArticleType.from_entity(a) for a in articles]

    @strawberry.field(description="Returns the current Google News search configuration stored in the database.")
    async def get_google_news_config(self, info: Info) -> GoogleNewsConfigType:
        repo = info.context["google_news_repository"]
        config = await repo.get_config()
        return GoogleNewsConfigType.from_entity(config)


@strawberry.type
class GoogleNewsMutation:
    @strawberry.field(description="Fetches Google News articles using the search config stored in the database, scrapes content and images, and saves them.")
    async def fetch_and_save_news_articles(self, info: Info) -> List[NewsArticleType]:
        repo = info.context["google_news_repository"]
        use_case = GoogleNewsFetcherUseCase(repository=repo)
        articles = await use_case.execute()
        return [NewsArticleType.from_entity(a) for a in articles]

    @strawberry.field(description="Updates the Google News search configuration in the database.")
    async def update_google_news_config(self, info: Info, config: GoogleNewsConfigInput) -> GoogleNewsConfigType:
        repo = info.context["google_news_repository"]
        use_case = UpdateGoogleNewsConfigUseCase(repository=repo)
        updated = await use_case.execute(config.to_entity())
        return GoogleNewsConfigType.from_entity(updated)
