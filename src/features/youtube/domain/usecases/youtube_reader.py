from typing import List
from ..entities.youtube_video_data_entity import YouTubeVideoDataEntity
from ..repositories.youtube_repository import YouTubeRepository

class ReadRecentYouTubeVideosUseCase:
    """
    Use case to read YouTube videos stored in the database, ordered from newest to oldest.
    """
    def __init__(self, repository: YouTubeRepository):
        self.repository = repository
        
    async def execute(self, limit: int = 50, offset: int = 0) -> List[YouTubeVideoDataEntity]:
        return await self.repository.find_recent(limit=limit, offset=offset)
