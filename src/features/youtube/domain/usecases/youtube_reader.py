from typing import List
from ..entities.youtube_video_data_entity import YouTubeVideoDataEntity
from ..repositories.youtube_repository import YouTubeRepository

class ReadRecentYouTubeVideosUseCase:
    """
    Caso de uso para leer los videos guardados en la base de datos
    ordenados del más reciente al más viejo.
    """
    def __init__(self, repository: YouTubeRepository):
        self.repository = repository
        
    async def execute(self, limit: int = 50, offset: int = 0) -> List[YouTubeVideoDataEntity]:
        return await self.repository.find_recent(limit=limit, offset=offset)
