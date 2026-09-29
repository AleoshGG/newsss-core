from abc import ABC, abstractmethod
from datetime import datetime

from ..entities.youtube_video_data_entity import YouTubeVideoDataEntity


class YouTubeRepository(ABC):

    @abstractmethod
    async def save(self, video: YouTubeVideoDataEntity) -> YouTubeVideoDataEntity:
        pass

    @abstractmethod
    async def find_all(self) -> list[YouTubeVideoDataEntity]:
        pass

    @abstractmethod
    async def delete_all_before_date(self, date: datetime) -> int:
        pass
