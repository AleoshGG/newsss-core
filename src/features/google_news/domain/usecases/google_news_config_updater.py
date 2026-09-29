from ..entities.google_news_config_entity import GoogleNewsConfigEntity
from ..repositories.google_news_repository import GoogleNewsRepository


class UpdateGoogleNewsConfigUseCase:
    """Use case to update the Google News search configuration singleton in the database."""

    def __init__(self, repository: GoogleNewsRepository):
        self.repository = repository

    async def execute(self, new_config: GoogleNewsConfigEntity) -> GoogleNewsConfigEntity:
        new_config.id = 1  # Always enforce singleton
        return await self.repository.save_config(new_config)
