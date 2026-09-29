from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.google_news_article_data_entity import GoogleNewsArticleDataEntity
from ...domain.entities.google_news_config_entity import GoogleNewsConfigEntity
from ...domain.repositories.google_news_repository import GoogleNewsRepository
from ..models.google_news_article_model import GoogleNewsArticleModel
from ..models.google_news_config_model import GoogleNewsConfigModel
from ..mappers.google_news_mapper import to_entity, to_model
from ..mappers.google_news_config_mapper import to_config_entity, to_config_model


class GoogleNewsRepositoryImpl(GoogleNewsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, article: GoogleNewsArticleDataEntity) -> GoogleNewsArticleDataEntity:
        model = to_model(article)
        model = await self.session.merge(model)
        await self.session.commit()
        return to_entity(model)

    async def find_all(self) -> list[GoogleNewsArticleDataEntity]:
        stmt = select(GoogleNewsArticleModel)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [to_entity(m) for m in models]

    async def find_recent(self, limit: int = 50, offset: int = 0) -> list[GoogleNewsArticleDataEntity]:
        stmt = (
            select(GoogleNewsArticleModel)
            .order_by(GoogleNewsArticleModel.fetched_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [to_entity(m) for m in models]

    async def delete_all_before_date(self, date: datetime) -> int:
        stmt = delete(GoogleNewsArticleModel).where(GoogleNewsArticleModel.fetched_at < date)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount

    async def get_config(self) -> GoogleNewsConfigEntity:
        """Returns the singleton config (id=1). Auto-creates with defaults on first call."""
        stmt = select(GoogleNewsConfigModel).where(GoogleNewsConfigModel.id == 1)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            model = GoogleNewsConfigModel(
                id=1,
                q="Inteligencia Artificial OR IA",
                hl="es-419",
                gl="MX",
                ceid="MX:es-419",
                when="1d",
                max_results=30,
            )
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
        return to_config_entity(model)

    async def save_config(self, config: GoogleNewsConfigEntity) -> GoogleNewsConfigEntity:
        """Upserts the singleton config (id=1)."""
        model = to_config_model(config)
        model = await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_config_entity(model)
