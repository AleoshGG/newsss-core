from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.entities.youtube_video_data_entity import YouTubeVideoDataEntity
from ...domain.repositories.youtube_repository import YouTubeRepository
from ..models.youtube_video_model import YouTubeVideoModel
from ..mappers.youtube_mapper import to_entity, to_model

class YouTubeRepositoryImpl(YouTubeRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, video: YouTubeVideoDataEntity) -> YouTubeVideoDataEntity:
        model = to_model(video)
        model = await self.session.merge(model)
        await self.session.commit()
        return to_entity(model)

    async def find_all(self) -> list[YouTubeVideoDataEntity]:
        stmt = select(YouTubeVideoModel)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [to_entity(m) for m in models]

    async def delete_all_before_date(self, date: datetime) -> int:
        stmt = delete(YouTubeVideoModel).where(YouTubeVideoModel.published_at < date)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
