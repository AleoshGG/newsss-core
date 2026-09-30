import asyncio
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def test_yt():
    video_id = "V0_PivD4Bws" # random
    try:
        tlist = YouTubeTranscriptApi.list_transcripts(video_id)
        for t in tlist:
            print(t.language_code, t.is_generated)
    except Exception as e:
        print(f"List error: {e}")

test_yt()
