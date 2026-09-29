import strawberry
from typing import List
from strawberry.types import Info

from ...domain.usecases.github_reader import ReadRecentGitHubReposUseCase
from ...domain.usecases.github_fetcher import GitHubFetcherUseCase
from ...domain.usecases.github_config_updater import UpdateGitHubConfigUseCase
from .types import GitHubRepoType, GitHubSearchConfigType, GitHubSearchConfigInput


@strawberry.type
class GitHubQuery:
    @strawberry.field(description="Retrieves the most recently fetched GitHub repositories previously saved in the local database.")
    async def get_recent_github_repos(self, info: Info, limit: int = 50, offset: int = 0) -> List[GitHubRepoType]:
        repo = info.context["github_repository"]
        use_case = ReadRecentGitHubReposUseCase(repository=repo)
        repos = await use_case.execute(limit=limit, offset=offset)
        return [GitHubRepoType.from_entity(r) for r in repos]

    @strawberry.field(description="Returns the current GitHub search configuration stored in the database.")
    async def get_github_config(self, info: Info) -> GitHubSearchConfigType:
        repo = info.context["github_repository"]
        config = await repo.get_config()
        return GitHubSearchConfigType.from_entity(config)


@strawberry.type
class GitHubMutation:
    @strawberry.field(description="Fetches GitHub repositories using the search config stored in the database, downloads READMEs, and saves them.")
    async def fetch_and_save_github_repos(self, info: Info) -> List[GitHubRepoType]:
        repo = info.context["github_repository"]
        token = info.context.get("github_token")
        use_case = GitHubFetcherUseCase(repository=repo, token=token)
        repos = await use_case.execute()
        return [GitHubRepoType.from_entity(r) for r in repos]

    @strawberry.field(description="Updates the GitHub search configuration in the database.")
    async def update_github_config(self, info: Info, config: GitHubSearchConfigInput) -> GitHubSearchConfigType:
        repo = info.context["github_repository"]
        use_case = UpdateGitHubConfigUseCase(repository=repo)
        updated = await use_case.execute(config.to_entity())
        return GitHubSearchConfigType.from_entity(updated)
