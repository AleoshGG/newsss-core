from ..entities.youtube_search_config_entity import YouTubeSearchConfigEntity
from ..repositories.youtube_repository import YouTubeRepository


class UpdateYouTubeConfigUseCase:
    """Use case to update the YouTube search configuration singleton in the database."""

    def __init__(self, repository: YouTubeRepository):
        self.repository = repository

    async def execute(self, new_config: YouTubeSearchConfigEntity) -> YouTubeSearchConfigEntity:
        new_config.id = 1  # Always enforce singleton
        return await self.repository.save_config(new_config)
