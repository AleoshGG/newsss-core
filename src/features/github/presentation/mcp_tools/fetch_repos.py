from src.mcp_server import mcp
from src.core.db.session import async_session
from src.features.github.data.repositories.github_repository_impl import GitHubRepositoryImpl
from src.features.github.domain.usecases.github_fetcher import GitHubFetcherUseCase
from src.core.config import settings


@mcp.tool()
async def fetch_github_repos() -> str:
    """
    Fetches GitHub repositories using the search configuration stored in the database,
    applies filters, downloads README files, and saves them via UPSERT.
    No parameters needed — configuration is loaded automatically from the database.
    """
    async with async_session() as session:
        repo = GitHubRepositoryImpl(session=session)
        use_case = GitHubFetcherUseCase(repository=repo, token=settings.GITHUB_TOKEN)
        repos = await use_case.execute()
        return f"Successfully fetched and saved {len(repos)} GitHub repositories."
