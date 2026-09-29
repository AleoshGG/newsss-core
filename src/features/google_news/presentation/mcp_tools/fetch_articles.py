from src.mcp_server import mcp
from src.core.db.session import async_session
from src.features.google_news.data.repositories.google_news_repository_impl import GoogleNewsRepositoryImpl
from src.features.google_news.domain.usecases.google_news_fetcher import GoogleNewsFetcherUseCase


@mcp.tool()
async def fetch_google_news_articles() -> str:
    """
    Fetches Google News articles using the search configuration stored in the database,
    scrapes article content and og:image from each article URL, and saves them via UPSERT.
    No parameters needed — configuration is loaded automatically from the database.
    """
    async with async_session() as session:
        repo = GoogleNewsRepositoryImpl(session=session)
        use_case = GoogleNewsFetcherUseCase(repository=repo)
        articles = await use_case.execute()
        return f"Successfully fetched and saved {len(articles)} news articles."
