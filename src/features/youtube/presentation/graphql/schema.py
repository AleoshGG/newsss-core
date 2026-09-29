import strawberry
from typing import List
from strawberry.types import Info

from ...domain.usecases.youtube_reader import ReadRecentYouTubeVideosUseCase
from ...domain.usecases.youtube_fetcher import YouTubeFetcherUseCase
from .types import YouTubeVideoType, YouTubeSearchSettingsInput


@strawberry.type
class Query:
    @strawberry.field(description="Retrieves the most recently fetched YouTube videos previously saved in the local database.")
    async def get_recent_youtube_videos(self, info: Info, limit: int = 50, offset: int = 0) -> List[YouTubeVideoType]:
        repo = info.context["youtube_repository"]
        use_case = ReadRecentYouTubeVideosUseCase(repository=repo)
        videos = await use_case.execute(limit=limit, offset=offset)
        return [YouTubeVideoType.from_entity(video) for video in videos]


@strawberry.type
class Mutation:
    @strawberry.field(description="Searches for YouTube videos using filters, enriches their metrics, fetches transcripts, and saves them to the local database.")
    async def fetch_and_save_youtube_videos(self, info: Info, config: YouTubeSearchSettingsInput) -> List[YouTubeVideoType]:
        repo = info.context["youtube_repository"]

        api_key = info.context["youtube_api_key"]
        
        use_case = YouTubeFetcherUseCase(repository=repo, api_key=api_key)
        settings_entity = config.to_entity()
        
        videos = await use_case.execute(config=settings_entity)
        return [YouTubeVideoType.from_entity(video) for video in videos]


schema = strawberry.Schema(query=Query, mutation=Mutation)
