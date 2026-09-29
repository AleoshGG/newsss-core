from typing import List, Optional

from src.mcp_server import mcp
from src.core.db.session import async_session
from src.core.config import settings
from src.features.youtube.data.repositories.youtube_repository_impl import YouTubeRepositoryImpl
from src.features.youtube.domain.usecases.youtube_fetcher import YouTubeFetcherUseCase
from src.features.youtube.domain.entities.youtube_search_settings import YouTubeSearchSettings

@mcp.tool()
async def fetch_youtube_videos(keywords: List[str], channel_ids: Optional[List[str]] = None, languages: Optional[List[str]] = None, max_results: int = 5) -> str:
    """
    Searches for YouTube videos using filters, enriches their metrics, fetches transcripts, and saves them to the local database.
    """
    async with async_session() as session:
        repo = YouTubeRepositoryImpl(session=session)
        use_case = YouTubeFetcherUseCase(repository=repo, api_key=settings.YOUTUBE_API_KEY)
        
        config = YouTubeSearchSettings(
            keywords=keywords,
            channel_ids=channel_ids or [],
            languages=languages or ["any"],
            max_results=max_results
        )
        
        videos = await use_case.execute(config)
        return f"Successfully fetched and saved {len(videos)} videos."
