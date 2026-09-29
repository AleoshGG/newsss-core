from abc import ABC, abstractmethod
from datetime import datetime

from ..entities.youtube_video_data_entity import YouTubeVideoDataEntity
from ..entities.youtube_search_config_entity import YouTubeSearchConfigEntity


class YouTubeRepository(ABC):

    @abstractmethod
    async def save(self, video: YouTubeVideoDataEntity) -> YouTubeVideoDataEntity:
        pass

    @abstractmethod
    async def find_all(self) -> list[YouTubeVideoDataEntity]:
        pass

    @abstractmethod
    async def find_recent(self, limit: int = 50, offset: int = 0) -> list[YouTubeVideoDataEntity]:
        pass

    @abstractmethod
    async def delete_all_before_date(self, date: datetime) -> int:
        pass

    @abstractmethod
    async def get_config(self) -> YouTubeSearchConfigEntity:
        """Returns the singleton search config (id=1), auto-creating it with defaults if it doesn't exist."""
        pass

    @abstractmethod
    async def save_config(self, config: YouTubeSearchConfigEntity) -> YouTubeSearchConfigEntity:
        """Upserts the singleton search config (id=1)."""
        pass
