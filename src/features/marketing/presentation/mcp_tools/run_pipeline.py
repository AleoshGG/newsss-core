from src.mcp_server import mcp
from src.core.config import settings
from src.core.db.session import async_session
from src.core.llm.gemini_client import GeminiLLMClient
from src.features.github.data.repositories.github_repository_impl import GitHubRepositoryImpl
from src.features.google_news.data.repositories.google_news_repository_impl import GoogleNewsRepositoryImpl
from src.features.marketing.data.repositories.marketing_repository_impl import MarketingRepositoryImpl
from src.features.marketing.domain.usecases.run_marketing_pipeline import (
    PipelineConfig,
    RunMarketingPipelineUseCase,
)
from src.features.youtube.data.repositories.youtube_repository_impl import YouTubeRepositoryImpl


@mcp.tool()
async def run_marketing_pipeline(
    limit_per_source: int = 50,
    n_clusters: int = 5,
    campaign_type: str = "linkedin_post",
    translate_non_english: bool = True,
) -> dict:
    """
    Runs the full 5-stage ML marketing pipeline for B2B / consulting firm audiences.

    Stage 0+1 — Cleans and normalizes data from YouTube, GitHub, and Google News:
      strips markdown from READMEs, detects absent YouTube transcripts, handles
      captcha/paywall in news articles, and translates non-English content to English.
    Stage 2 — Filters items by B2B intent score (keyword matching + engagement + recency).
    Stage 3 — Clusters items semantically using local ML (sentence-transformers + K-Means).
    Stage 4 — Generates a marketing campaign per cluster using Google Gemini LLM.

    Args:
        limit_per_source: Max items to read per source (YouTube, GitHub, Google News). Default 50.
        n_clusters: Number of topic clusters to identify. Default 5.
        campaign_type: Format of generated campaigns. Options: linkedin_post (default),
                       twitter_thread, email_newsletter.
        translate_non_english: Whether to translate Spanish/other-language content to English
                               before clustering. Default True.

    Returns:
        A dict with 'campaigns' (list of generated campaigns) and 'stats' (pipeline metrics).
    """
    if not settings.GEMINI_API_KEY:
        return {"error": "GEMINI_API_KEY is not configured. Add it to your .env file."}

    async with (
        async_session() as yt_session,
        async_session() as gh_session,
        async_session() as gn_session,
        async_session() as mk_session,
    ):
        llm = GeminiLLMClient(api_key=settings.GEMINI_API_KEY)
        use_case = RunMarketingPipelineUseCase(
            youtube_repo=YouTubeRepositoryImpl(session=yt_session),
            github_repo=GitHubRepositoryImpl(session=gh_session),
            google_news_repo=GoogleNewsRepositoryImpl(session=gn_session),
            marketing_repo=MarketingRepositoryImpl(session=mk_session),
            llm=llm,
        )
        config = PipelineConfig(
            limit_per_source=limit_per_source,
            n_clusters=n_clusters,
            campaign_type=campaign_type,
            translate_non_english=translate_non_english,
        )
        result = await use_case.execute(config)

    campaigns_data = [
        {
            "id": c.id,
            "topic_label": c.topic_label,
            "campaign_type": c.campaign_type,
            "hook": c.hook,
            "body": c.body,
            "cta": c.cta,
            "hashtags": c.hashtags,
            "status": c.status,
        }
        for c in result.campaigns
    ]

    return {
        "campaigns": campaigns_data,
        "stats": {
            "clusters_found": result.clusters_found,
            "items_processed": result.items_processed,
            "items_after_filter": result.items_after_filter,
            "total_fetched": result.cleaning_stats.total_fetched,
            "discarded_empty_body": result.cleaning_stats.discarded_empty_body,
            "translated": result.cleaning_stats.translated,
            "passed_cleaning": result.cleaning_stats.passed,
            "by_source": result.cleaning_stats.by_source,
        },
    }
