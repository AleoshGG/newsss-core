"""
Unified GraphQL root schema and context getter for all features.
Merges YouTube, GitHub, Google News, and Marketing queries and mutations via
Strawberry's multiple inheritance pattern, and injects all repositories into a
shared context.
"""
import strawberry
from strawberry.fastapi import GraphQLRouter

from src.core.db.session import async_session
from src.core.config import settings

from src.features.youtube.data.repositories.youtube_repository_impl import YouTubeRepositoryImpl
from src.features.github.data.repositories.github_repository_impl import GitHubRepositoryImpl
from src.features.google_news.data.repositories.google_news_repository_impl import GoogleNewsRepositoryImpl
from src.features.marketing.data.repositories.marketing_repository_impl import MarketingRepositoryImpl

from src.features.youtube.presentation.graphql.schema import YouTubeQuery, YouTubeMutation
from src.features.github.presentation.graphql.schema import GitHubQuery, GitHubMutation
from src.features.google_news.presentation.graphql.schema import GoogleNewsQuery, GoogleNewsMutation
from src.features.marketing.presentation.graphql.schema import MarketingQuery, MarketingMutation


# --- Merged root types via multiple inheritance ---

@strawberry.type
class Query(YouTubeQuery, GitHubQuery, GoogleNewsQuery, MarketingQuery):
    pass


@strawberry.type
class Mutation(YouTubeMutation, GitHubMutation, GoogleNewsMutation, MarketingMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)


# --- Unified context: each repository gets its own independent DB session ---
# Using separate sessions avoids SQLAlchemy's "concurrent operations not permitted"
# error that occurs when multiple resolvers share a single AsyncSession.

async def get_context():
    async with async_session() as yt_session, \
               async_session() as gh_session, \
               async_session() as gn_session, \
               async_session() as mk_session:
        # Build LLM client lazily — only when GEMINI_API_KEY is configured.
        # Importing here keeps the server startable even before the package is installed.
        llm = None
        if settings.GEMINI_API_KEY:
            try:
                from src.core.llm.gemini_client import GeminiLLMClient
                llm = GeminiLLMClient(api_key=settings.GEMINI_API_KEY, model_name=settings.GEMINI_MODEL)
            except ImportError:
                pass  # google-generativeai not yet installed; pipeline will fail with a clear message

        yield {
            "youtube_repository": YouTubeRepositoryImpl(session=yt_session),
            "github_repository": GitHubRepositoryImpl(session=gh_session),
            "google_news_repository": GoogleNewsRepositoryImpl(session=gn_session),
            "marketing_repository": MarketingRepositoryImpl(session=mk_session),
            "youtube_api_key": settings.YOUTUBE_API_KEY,
            "github_token": settings.GITHUB_TOKEN,
            "llm": llm,
        }


graphql_app = GraphQLRouter(schema, context_getter=get_context)
