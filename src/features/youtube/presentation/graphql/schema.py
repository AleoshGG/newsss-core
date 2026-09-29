import strawberry
from typing import List
from strawberry.types import Info

from ...domain.usecases.youtube_reader import ReadRecentYouTubeVideosUseCase
from ...domain.usecases.youtube_fetcher import YouTubeFetcherUseCase
from ...domain.usecases.youtube_config_updater import UpdateYouTubeConfigUseCase
from .types import YouTubeVideoType, YouTubeSearchConfigType, YouTubeSearchConfigInput


@strawberry.type
class YouTubeQuery:
    @strawberry.field(description="Retrieves the most recently fetched YouTube videos previously saved in the local database.")
    async def get_recent_youtube_videos(self, info: Info, limit: int = 50, offset: int = 0) -> List[YouTubeVideoType]:
        repo = info.context["youtube_repository"]
        use_case = ReadRecentYouTubeVideosUseCase(repository=repo)
        videos = await use_case.execute(limit=limit, offset=offset)
        return [YouTubeVideoType.from_entity(video) for video in videos]

    @strawberry.field(description="Returns the current YouTube search configuration stored in the database.")
    async def get_youtube_config(self, info: Info) -> YouTubeSearchConfigType:
        repo = info.context["youtube_repository"]
        config = await repo.get_config()
        return YouTubeSearchConfigType.from_entity(config)


@strawberry.type
class YouTubeMutation:
    @strawberry.field(description="Fetches YouTube videos using the search config stored in the database, enriches metrics and transcripts, and saves them.")
    async def fetch_and_save_youtube_videos(self, info: Info) -> List[YouTubeVideoType]:
        repo = info.context["youtube_repository"]
        api_key = info.context["youtube_api_key"]
        use_case = YouTubeFetcherUseCase(repository=repo, api_key=api_key)
        videos = await use_case.execute()
        return [YouTubeVideoType.from_entity(video) for video in videos]

    @strawberry.field(description="Updates the YouTube search configuration in the database.")
    async def update_youtube_config(self, info: Info, config: YouTubeSearchConfigInput) -> YouTubeSearchConfigType:
        repo = info.context["youtube_repository"]
        use_case = UpdateYouTubeConfigUseCase(repository=repo)
        updated = await use_case.execute(config.to_entity())
        return YouTubeSearchConfigType.from_entity(updated)
