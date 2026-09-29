from src.mcp_server import mcp
from src.core.db.session import async_session
from src.core.config import settings
from src.features.youtube.data.repositories.youtube_repository_impl import YouTubeRepositoryImpl
from src.features.youtube.domain.usecases.youtube_fetcher import YouTubeFetcherUseCase


@mcp.tool()
async def fetch_youtube_videos() -> str:
    """
    Fetches YouTube videos using the search configuration stored in the database,
    enriches them with metrics and transcripts, and saves them via UPSERT.
    No parameters needed — configuration is loaded automatically from the database.
    """
    async with async_session() as session:
        repo = YouTubeRepositoryImpl(session=session)
        use_case = YouTubeFetcherUseCase(repository=repo, api_key=settings.YOUTUBE_API_KEY)
        videos = await use_case.execute()
        return f"Successfully fetched and saved {len(videos)} YouTube videos."
