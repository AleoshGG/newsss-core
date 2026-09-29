"""
Unified GraphQL root schema and context getter for all features.
Merges YouTube, GitHub, and Google News queries and mutations via Strawberry's
multiple inheritance pattern, and injects all repositories into a shared context.
"""
import strawberry
from strawberry.fastapi import GraphQLRouter

from src.core.db.session import async_session
from src.core.config import settings

from src.features.youtube.data.repositories.youtube_repository_impl import YouTubeRepositoryImpl
from src.features.github.data.repositories.github_repository_impl import GitHubRepositoryImpl
from src.features.google_news.data.repositories.google_news_repository_impl import GoogleNewsRepositoryImpl

from src.features.youtube.presentation.graphql.schema import YouTubeQuery, YouTubeMutation
from src.features.github.presentation.graphql.schema import GitHubQuery, GitHubMutation
from src.features.google_news.presentation.graphql.schema import GoogleNewsQuery, GoogleNewsMutation


# --- Merged root types via multiple inheritance ---

@strawberry.type
class Query(YouTubeQuery, GitHubQuery, GoogleNewsQuery):
    pass


@strawberry.type
class Mutation(YouTubeMutation, GitHubMutation, GoogleNewsMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)


# --- Unified context: each repository gets its own independent DB session ---
# Using separate sessions avoids SQLAlchemy's "concurrent operations not permitted"
# error that occurs when multiple resolvers share a single AsyncSession.

async def get_context():
    async with async_session() as yt_session, \
               async_session() as gh_session, \
               async_session() as gn_session:
        yield {
            "youtube_repository": YouTubeRepositoryImpl(session=yt_session),
            "github_repository": GitHubRepositoryImpl(session=gh_session),
            "google_news_repository": GoogleNewsRepositoryImpl(session=gn_session),
            "youtube_api_key": settings.YOUTUBE_API_KEY,
            "github_token": settings.GITHUB_TOKEN,
        }


graphql_app = GraphQLRouter(schema, context_getter=get_context)
