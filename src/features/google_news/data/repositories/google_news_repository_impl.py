from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.entities.google_news_article_data_entity import GoogleNewsArticleDataEntity
from ...domain.repositories.google_news_repository import GoogleNewsRepository
from ..models.google_news_article_model import GoogleNewsArticleModel
from ..mappers.google_news_mapper import to_entity, to_model

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

    async def delete_all_before_date(self, date: datetime) -> int:
        stmt = delete(GoogleNewsArticleModel).where(GoogleNewsArticleModel.fetched_at < date)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
