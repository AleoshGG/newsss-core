from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.entities.github_data_entity import GitHubDataEntity
from ...domain.repositories.github_repository import GitHubRepository
from ..models.github_data_model import GitHubDataModel
from ..mappers.github_mapper import to_entity, to_model

class GitHubRepositoryImpl(GitHubRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, data: GitHubDataEntity) -> GitHubDataEntity:
        model = to_model(data)
        model = await self.session.merge(model)
        await self.session.commit()
        return to_entity(model)

    async def find_all(self) -> list[GitHubDataEntity]:
        stmt = select(GitHubDataModel)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [to_entity(m) for m in models]

    async def delete_all_before_date(self, date: datetime) -> int:
        stmt = delete(GitHubDataModel).where(GitHubDataModel.updated_at < date.isoformat())
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
