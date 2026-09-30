from datetime import datetime
from typing import List, Optional
import strawberry

from ...domain.entities.content_cluster_entity import ContentCluster
from ...domain.entities.marketing_campaign_entity import MarketingCampaign
from ...domain.entities.normalized_item_entity import CleaningStats as CleaningStatsEntity
from ...domain.usecases.run_marketing_pipeline import PipelineResult


@strawberry.type
class CleaningStatsType:
    total_fetched: int = strawberry.field(description="Total raw items fetched from all sources.")
    discarded_empty_body: int = strawberry.field(description="Items discarded due to empty or unusable body (no transcript, captcha, etc.).")
    discarded_short_body: int = strawberry.field(description="Items discarded because the body was below the minimum length threshold.")
    translated: int = strawberry.field(description="Items translated from a non-English language to English.")
    passed: int = strawberry.field(description="Items that passed all cleaning checks and entered the ML pipeline.")
    by_source: strawberry.scalars.JSON = strawberry.field(description="Item count that passed cleaning, broken down by source (youtube, github, google_news).")

    @classmethod
    def from_entity(cls, entity: CleaningStatsEntity) -> "CleaningStatsType":
        return cls(
            total_fetched=entity.total_fetched,
            discarded_empty_body=entity.discarded_empty_body,
            discarded_short_body=entity.discarded_short_body,
            translated=entity.translated,
            passed=entity.passed,
            by_source=entity.by_source,
        )


@strawberry.type
class MarketingCampaignType:
    id: str = strawberry.field(description="Unique UUID of the campaign.")
    cluster_id: Optional[int] = strawberry.field(description="ID of the content cluster that originated this campaign.")
    topic_label: str = strawberry.field(description="Auto-generated topic label from the cluster's TF-IDF keywords.")
    campaign_type: str = strawberry.field(description="Format of the campaign: linkedin_post | twitter_thread | email_newsletter.")
    hook: Optional[str] = strawberry.field(description="Attention-grabbing first line or subject line.")
    body: str = strawberry.field(description="Main campaign content.")
    cta: Optional[str] = strawberry.field(description="Call to action.")
    hashtags: List[str] = strawberry.field(description="Relevant hashtags for the campaign.")
    status: str = strawberry.field(description="Current status: draft | approved | published.")
    created_at: Optional[datetime] = strawberry.field(description="Timestamp when the campaign was generated.")

    @classmethod
    def from_entity(cls, entity: MarketingCampaign) -> "MarketingCampaignType":
        return cls(
            id=entity.id,
            cluster_id=entity.cluster_id,
            topic_label=entity.topic_label,
            campaign_type=entity.campaign_type,
            hook=entity.hook,
            body=entity.body,
            cta=entity.cta,
            hashtags=entity.hashtags or [],
            status=entity.status,
            created_at=entity.created_at,
        )


@strawberry.type
class ContentClusterType:
    cluster_id: int = strawberry.field(description="Numeric identifier of the cluster.")
    topic_label: str = strawberry.field(description="Auto-generated topic label from TF-IDF keywords.")
    keywords: List[str] = strawberry.field(description="Top TF-IDF keywords characterizing this cluster.")
    sources: List[str] = strawberry.field(description="Data sources that contributed items to this cluster.")
    avg_engagement_score: float = strawberry.field(description="Average engagement score of items in this cluster.")
    all_item_ids: List[str] = strawberry.field(description="IDs of all items assigned to this cluster.")

    @classmethod
    def from_entity(cls, entity: ContentCluster) -> "ContentClusterType":
        return cls(
            cluster_id=entity.cluster_id,
            topic_label=entity.topic_label,
            keywords=entity.keywords or [],
            sources=entity.sources or [],
            avg_engagement_score=entity.avg_engagement_score,
            all_item_ids=entity.all_item_ids or [],
        )


@strawberry.type
class PipelineResultType:
    campaigns: List[MarketingCampaignType] = strawberry.field(description="Generated marketing campaigns, one per topic cluster.")
    clusters_found: int = strawberry.field(description="Number of topic clusters identified by the ML stage.")
    items_processed: int = strawberry.field(description="Number of items that passed cleaning and normalization.")
    items_after_filter: int = strawberry.field(description="Number of items that passed the B2B intent filter.")
    cleaning_stats: CleaningStatsType = strawberry.field(description="Detailed breakdown of the data cleaning stage.")

    @classmethod
    def from_entity(cls, entity: PipelineResult) -> "PipelineResultType":
        return cls(
            campaigns=[MarketingCampaignType.from_entity(c) for c in entity.campaigns],
            clusters_found=entity.clusters_found,
            items_processed=entity.items_processed,
            items_after_filter=entity.items_after_filter,
            cleaning_stats=CleaningStatsType.from_entity(entity.cleaning_stats),
        )
