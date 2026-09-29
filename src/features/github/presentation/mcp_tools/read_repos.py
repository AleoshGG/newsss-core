from src.mcp_server import mcp
from src.core.db.session import async_session
from src.features.github.data.repositories.github_repository_impl import GitHubRepositoryImpl
from src.features.github.domain.usecases.github_reader import ReadRecentGitHubReposUseCase


@mcp.tool()
async def get_recent_github_repos(limit: int = 10, offset: int = 0) -> str:
    """
    Retrieves the most recently fetched GitHub repositories from the local database.
    Returns name, full_name, stars, language, description, and URL for each repository.
    """
    async with async_session() as session:
        repo = GitHubRepositoryImpl(session=session)
        use_case = ReadRecentGitHubReposUseCase(repository=repo)
        repos = await use_case.execute(limit=limit, offset=offset)

        if not repos:
            return "No GitHub repositories have been saved yet."

        lines = []
        for r in repos:
            lines.append(
                f"- [{r.name}]({r.html_url}) | ⭐ {r.stargazers_count} | "
                f"Lang: {r.language or 'N/A'} | {(r.description or '')[:120]}"
            )
        return "\n".join(lines)
