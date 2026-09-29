from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.youtube_video_data_entity import YouTubeVideoDataEntity
from ...domain.entities.youtube_search_config_entity import YouTubeSearchConfigEntity
from ...domain.repositories.youtube_repository import YouTubeRepository
from ..models.youtube_video_model import YouTubeVideoModel
from ..models.youtube_search_config_model import YouTubeSearchConfigModel
from ..mappers.youtube_mapper import to_entity, to_model
from ..mappers.youtube_config_mapper import to_config_entity, to_config_model


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

    async def find_recent(self, limit: int = 50, offset: int = 0) -> list[YouTubeVideoDataEntity]:
        stmt = (
            select(YouTubeVideoModel)
            .order_by(YouTubeVideoModel.published_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [to_entity(m) for m in models]

    async def delete_all_before_date(self, date: datetime) -> int:
        stmt = delete(YouTubeVideoModel).where(YouTubeVideoModel.published_at < date)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount

    async def get_config(self) -> YouTubeSearchConfigEntity:
        """Returns the singleton config (id=1). Auto-creates with defaults on first call."""
        stmt = select(YouTubeSearchConfigModel).where(YouTubeSearchConfigModel.id == 1)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            model = YouTubeSearchConfigModel(
                id=1,
                keywords=["OpenAI", "Anthropic", "Claude", "ChatGPT"],
                channel_ids=["@googledeepmind", "@OpenAI"],
                languages=["es", "en"],
                max_results=5,
            )
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
        return to_config_entity(model)

    async def save_config(self, config: YouTubeSearchConfigEntity) -> YouTubeSearchConfigEntity:
        """Upserts the singleton config (id=1)."""
        model = to_config_model(config)
        model = await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_config_entity(model)
