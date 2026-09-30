import strawberry
from typing import List, Optional
from strawberry.types import Info

from ...domain.usecases.run_marketing_pipeline import RunMarketingPipelineUseCase, PipelineConfig
from ...domain.repositories.marketing_repository import MarketingRepository
from .types import MarketingCampaignType, ContentClusterType, PipelineResultType


@strawberry.type
class MarketingQuery:
    @strawberry.field(
        description=(
            "Retrieves previously generated marketing campaigns from the database. "
            "Optionally filter by status: 'draft', 'approved', or 'published'."
        )
    )
    async def get_marketing_campaigns(
        self,
        info: Info,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> List[MarketingCampaignType]:
        repo: MarketingRepository = info.context["marketing_repository"]
        campaigns = await repo.find_recent_campaigns(limit=limit, status=status)
        return [MarketingCampaignType.from_entity(c) for c in campaigns]

    @strawberry.field(
        description="Retrieves the most recently generated content clusters from the database."
    )
    async def get_content_clusters(
        self,
        info: Info,
        limit: int = 10,
    ) -> List[ContentClusterType]:
        repo: MarketingRepository = info.context["marketing_repository"]
        clusters = await repo.find_recent_clusters(limit=limit)
        return [ContentClusterType.from_entity(c) for c in clusters]


@strawberry.type
class MarketingMutation:
    @strawberry.field(
        description=(
            "Runs the full 5-stage ML marketing pipeline: "
            "(1) Cleans and normalizes data from YouTube, GitHub, and Google News — "
            "strips markdown, detects language, and translates non-English content to English. "
            "(2) Filters items by B2B intent score. "
            "(3) Clusters items semantically using local sentence-transformers + K-Means. "
            "(4) Generates marketing campaigns per cluster using Gemini LLM, "
            "calibrated for B2B / consulting firm audiences. "
            "Returns the generated campaigns and pipeline observability stats."
        )
    )
    async def run_marketing_pipeline(
        self,
        info: Info,
        limit_per_source: int = 50,
        n_clusters: int = 5,
        min_intent_score: float = 0.25,
        campaign_type: str = "linkedin_post",
        translate_non_english: bool = True,
    ) -> PipelineResultType:
        ctx = info.context
        use_case = RunMarketingPipelineUseCase(
            youtube_repo=ctx["youtube_repository"],
            github_repo=ctx["github_repository"],
            google_news_repo=ctx["google_news_repository"],
            marketing_repo=ctx["marketing_repository"],
            llm=ctx["llm"],
        )
        config = PipelineConfig(
            limit_per_source=limit_per_source,
            n_clusters=n_clusters,
            min_intent_score=min_intent_score,
            campaign_type=campaign_type,
            translate_non_english=translate_non_english,
        )
        result = await use_case.execute(config)
        return PipelineResultType.from_entity(result)
