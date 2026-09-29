from src.mcp_server import mcp
from src.core.db.session import async_session
from src.features.youtube.data.repositories.youtube_repository_impl import YouTubeRepositoryImpl
from src.features.youtube.domain.usecases.youtube_reader import ReadRecentYouTubeVideosUseCase

@mcp.tool()
async def get_recent_youtube_videos(limit: int = 10, offset: int = 0) -> str:
    """
    Retrieves the most recently fetched YouTube videos previously saved in the local database.
    """
    async with async_session() as session:
        repo = YouTubeRepositoryImpl(session=session)
        use_case = ReadRecentYouTubeVideosUseCase(repository=repo)
        
        videos = await use_case.execute(limit=limit, offset=offset)
        
        resultado = []
        for v in videos:
            resultado.append(f"- ID: {v.id} | Title: {v.title} | Channel: {v.channel} | Transcript: {v.transcript[:200]}...")
            
        return "\n".join(resultado) if resultado else "No videos have been saved yet."

