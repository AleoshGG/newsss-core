from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from src.core.db.session import async_session
from src.core.config import settings
from src.features.youtube.data.repositories.youtube_repository_impl import YouTubeRepositoryImpl
from .schema import schema

async def get_context():
    async with async_session() as session:
        youtube_repository = YouTubeRepositoryImpl(session=session)
        # We pass dependencies to the context
        yield {
            "youtube_repository": youtube_repository,
            "youtube_api_key": settings.YOUTUBE_API_KEY
        }

graphql_app = GraphQLRouter(schema, context_getter=get_context)
