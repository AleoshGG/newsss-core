from src.mcp_server import mcp
from src.core.db.session import async_session
from src.features.google_news.data.repositories.google_news_repository_impl import GoogleNewsRepositoryImpl
from src.features.google_news.domain.usecases.google_news_reader import ReadRecentNewsArticlesUseCase


@mcp.tool()
async def get_recent_news_articles(limit: int = 10, offset: int = 0) -> str:
    """
    Retrieves the most recently fetched news articles from the local database.
    Returns title, source, publication date, link, and a content snippet for each article.
    """
    async with async_session() as session:
        repo = GoogleNewsRepositoryImpl(session=session)
        use_case = ReadRecentNewsArticlesUseCase(repository=repo)
        articles = await use_case.execute(limit=limit, offset=offset)

        if not articles:
            return "No news articles have been saved yet."

        lines = []
        for a in articles:
            snippet = (a.content or "")[:200].replace("\n", " ")
            lines.append(
                f"- [{a.title}]({a.link})\n"
                f"  Source: {a.source_name} | Published: {a.pub_date}\n"
                f"  {snippet}..."
            )
        return "\n\n".join(lines)
