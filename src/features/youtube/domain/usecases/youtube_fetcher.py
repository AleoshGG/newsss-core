import re
import asyncio
from datetime import datetime, timedelta, timezone
from typing import List

import httpx
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from ..entities.youtube_video_data_entity import YouTubeVideoDataEntity
from ..entities.youtube_video_metrics import YouTubeVideoMetrics
from ..entities.youtube_search_settings import YouTubeSearchSettings
from ..repositories.youtube_repository import YouTubeRepository


def parse_iso_duration(duration: str) -> int:
    if not duration:
        return 0
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


class YouTubeFetcherUseCase:
    """
    Use case to fetch, filter, and save YouTube videos based on configuration.
    """

    def __init__(self, repository: YouTubeRepository, api_key: str):
        self.repository = repository
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY configuration is missing")

    async def execute(self, config: YouTubeSearchSettings) -> List[YouTubeVideoDataEntity]:
        # We use a single client to maintain an open connection pool
        # limits=httpx.Limits(max_connections=50) helps to manage concurrency
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=50)
        async with httpx.AsyncClient(limits=limits) as client:
            # Phase 1: Channel handles resolution
            channel_ids = await self._resolve_channel_handles(client, config.channel_ids)
            
            # Phase 2: Search candidates
            search_items = await self._fetch_search_candidates(client, config, channel_ids)
            if not search_items:
                return []
            
            # Phase 3: Enrich details
            enriched_videos = await self._enrich_video_details_in_batch(client, search_items)
            
            # Phase 4: Filter and fetch transcripts
            final_videos = await self._filter_and_fetch_transcripts(client, enriched_videos, config)
            
            # Phase 5: Concurrent DB saving
            if final_videos:
                save_tasks = [self.repository.save(video) for video in final_videos]
                await asyncio.gather(*save_tasks)
                
            return final_videos

    async def _resolve_channel_handles(self, client: httpx.AsyncClient, channel_ids: List[str]) -> List[str]:
        if not channel_ids:
            return []

        async def resolve(raw_id: str) -> str | None:
            if raw_id.startswith("@"):
                handle = raw_id.replace("@", "")
                try:
                    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=id&forHandle={handle}&key={self.api_key}"
                    response = await client.get(url)
                    response.raise_for_status()
                    data = response.json()
                    if data.get("items"):
                        return data["items"][0]["id"]
                except Exception as e:
                    print(f"Error resolving channel {handle}: {e}")
                return None
            return raw_id

        resolved = await asyncio.gather(*(resolve(raw_id) for raw_id in channel_ids))
        return [id_ for id_ in resolved if id_ is not None]

    async def _fetch_search_candidates(self, client: httpx.AsyncClient, config: YouTubeSearchSettings, channel_ids: List[str]) -> List[dict]:
        query = " | ".join(config.keywords)
        query = f"{query} -shorts -#shorts" if query else "-shorts -#shorts"

        search_base_url = "https://youtube.googleapis.com/youtube/v3/search"
        two_days_ago = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        
        base_params = {
            "part": "snippet",
            "type": "video",
            "maxResults": "50",
            "order": "date",
            "key": self.api_key,
            "publishedAfter": two_days_ago,
        }

        languages_to_search = config.languages if config.languages else ["any"]
        search_promises = []

        async def fetch_search(params: dict) -> List[dict]:
            try:
                response = await client.get(search_base_url, params=params)
                response.raise_for_status()
                data = response.json()
                return data.get("items", [])
            except Exception as e:
                print(f"Error in YouTube API search: {e}")
                return []

        # 1. Search in specific channels
        for channel_id in channel_ids:
            params = base_params.copy()
            params["channelId"] = channel_id
            search_promises.append(fetch_search(params))

        # 2. Global search by keywords
        if config.keywords:
            for lang in languages_to_search:
                params = base_params.copy()
                params["q"] = query
                if lang != "any":
                    params["relevanceLanguage"] = lang
                    if lang == "en":
                        params["regionCode"] = "US"
                    elif lang == "es":
                        params["regionCode"] = "MX"
                search_promises.append(fetch_search(params))

        results_matrix = await asyncio.gather(*search_promises)
        search_items = [item for sublist in results_matrix for item in sublist]

        # Deduplicate
        seen_ids = set()
        deduped_items = []
        for item in search_items:
            video_id = item.get("id", {}).get("videoId")
            if video_id and video_id not in seen_ids:
                seen_ids.add(video_id)
                deduped_items.append(item)

        # Sort from newest to oldest
        deduped_items.sort(
            key=lambda x: datetime.fromisoformat(x["snippet"]["publishedAt"].replace("Z", "+00:00")),
            reverse=True
        )

        return deduped_items

    async def _enrich_video_details_in_batch(self, client: httpx.AsyncClient, search_items: List[dict]) -> List[dict]:
        valid_items = [item for item in search_items if item.get("id", {}).get("videoId")]
        if not valid_items:
            return []

        chunk_size = 50
        enriched_videos = []
        stats_url = "https://youtube.googleapis.com/youtube/v3/videos"

        async def fetch_chunk(chunk) -> List[dict]:
            video_ids = ",".join([item["id"]["videoId"] for item in chunk])
            params = {
                "part": "statistics,contentDetails,snippet",
                "id": video_ids,
                "key": self.api_key
            }
            try:
                response = await client.get(stats_url, params=params)
                response.raise_for_status()
                data = response.json()
                return data.get("items", [])
            except Exception as e:
                print(f"Error enriching videos in batch: {e}")
                return []

        chunks = [valid_items[i:i + chunk_size] for i in range(0, len(valid_items), chunk_size)]
        results = await asyncio.gather(*(fetch_chunk(chunk) for chunk in chunks))
        
        for res in results:
            enriched_videos.extend(res)

        # Maintain original order
        order_map = {item["id"]["videoId"]: i for i, item in enumerate(valid_items)}
        enriched_videos.sort(key=lambda x: order_map.get(x["id"], 999))

        return enriched_videos

    async def _filter_and_fetch_transcripts(self, client: httpx.AsyncClient, videos_details: List[dict], config: YouTubeSearchSettings) -> List[YouTubeVideoDataEntity]:
        final_videos = []
        pushed_per_channel = {}
        total_pushed = 0
        
        is_global_search = not config.channel_ids
        langs_to_try = config.languages if (config.languages and "any" not in config.languages) else ["es", "en"]
        foreign_chars_regex = re.compile(r'[\u0900-\u097F\u0E00-\u0E7F\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uAC00-\uD7AF\u0400-\u04FF\u0600-\u06FF]')

        # Parallel transcript fetching to maximize speed
        # First identify which videos pass the filters
        passed_videos = []
        for item in videos_details:
            video_id = item["id"]
            snippet = item["snippet"]
            channel_id = snippet["channelId"]

            if is_global_search:
                if total_pushed >= config.max_results:
                    break
            else:
                if pushed_per_channel.get(channel_id, 0) >= config.max_results:
                    continue

            audio_lang = snippet.get("defaultAudioLanguage") or snippet.get("defaultLanguage")
            if audio_lang:
                is_allowed = any(audio_lang.lower().startswith(lang.lower()) for lang in langs_to_try)
                if not is_allowed:
                    continue
            else:
                if foreign_chars_regex.search(snippet.get("title", "")):
                    continue

            content_details = item.get("contentDetails", {})
            duration_seconds = parse_iso_duration(content_details.get("duration", ""))
            if duration_seconds <= 120:
                continue

            passed_videos.append(item)
            pushed_per_channel[channel_id] = pushed_per_channel.get(channel_id, 0) + 1
            total_pushed += 1

        async def fetch_transcript_and_map(item: dict) -> YouTubeVideoDataEntity:
            video_id = item["id"]
            snippet = item["snippet"]
            stats = item.get("statistics", {})

            transcript = 'Transcript not available'
            
            # youtube_transcript_api is synchronous by default, we wrap in to_thread
            def fetch_t():
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=langs_to_try)
                    formatter = TextFormatter()
                    return formatter.format_transcript(transcript_list).replace('\n', ' ').strip()
                except Exception:
                    return 'Transcript not available'
            
            transcript = await asyncio.to_thread(fetch_t)
            
            thumbnails = snippet.get("thumbnails", {})
            thumbnail_url = thumbnails.get("high", {}).get("url") or thumbnails.get("default", {}).get("url") or ""
            
            return YouTubeVideoDataEntity(
                id=video_id,
                title=snippet.get("title", ""),
                channel=snippet.get("channelTitle", ""),
                published_at=datetime.fromisoformat(snippet["publishedAt"].replace("Z", "+00:00")),
                url=f"https://www.youtube.com/watch?v={video_id}",
                metrics=YouTubeVideoMetrics(
                    views=int(stats.get("viewCount", "0")),
                    likes=int(stats.get("likeCount", "0")),
                    comments=int(stats.get("commentCount", "0"))
                ),
                thumbnail_url=thumbnail_url,
                transcript=transcript
            )

        if passed_videos:
            final_videos = await asyncio.gather(*(fetch_transcript_and_map(item) for item in passed_videos))
            
        return list(final_videos)
