from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.github_data_entity import GitHubDataEntity
from ...domain.entities.github_search_config_entity import GitHubSearchConfigEntity
from ...domain.repositories.github_repository import GitHubRepository
from ..models.github_data_model import GitHubDataModel
from ..models.github_search_config_model import GitHubSearchConfigModel
from ..mappers.github_mapper import to_entity, to_model
from ..mappers.github_config_mapper import to_config_entity, to_config_model


class GitHubRepositoryImpl(GitHubRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, data: GitHubDataEntity) -> GitHubDataEntity:
        model = to_model(data)
        model = await self.session.merge(model)
        await self.session.commit()
        return to_entity(model)

    async def save_many(self, entities: list[GitHubDataEntity]) -> list[GitHubDataEntity]:
        models = [to_model(e) for e in entities]
        merged_models = []
        for model in models:
            merged_models.append(await self.session.merge(model))
        await self.session.commit()
        return [to_entity(m) for m in merged_models]

    async def find_all(self) -> list[GitHubDataEntity]:
        stmt = select(GitHubDataModel)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [to_entity(m) for m in models]

    async def find_recent(self, limit: int = 50, offset: int = 0) -> list[GitHubDataEntity]:
        stmt = (
            select(GitHubDataModel)
            .order_by(GitHubDataModel.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [to_entity(m) for m in models]

    async def delete_all_before_date(self, date: datetime) -> int:
        stmt = delete(GitHubDataModel).where(GitHubDataModel.updated_at < date.isoformat())
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount

    async def get_config(self) -> GitHubSearchConfigEntity:
        """Returns the singleton config (id=1). Auto-creates with defaults on first call."""
        stmt = select(GitHubSearchConfigModel).where(GitHubSearchConfigModel.id == 1)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            model = GitHubSearchConfigModel(
                id=1,
                keywords=["openai", "llm", "claude"],
                days_active=7,
                min_stars=50,
                min_forks=5,
                require_license=False,
                selected_topics=["ai", "llm"],
                selected_languages=["python", "typescript"],
                max_results=30,
            )
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
        return to_config_entity(model)

    async def save_config(self, config: GitHubSearchConfigEntity) -> GitHubSearchConfigEntity:
        """Upserts the singleton config (id=1)."""
        model = to_config_model(config)
        model = await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_config_entity(model)
