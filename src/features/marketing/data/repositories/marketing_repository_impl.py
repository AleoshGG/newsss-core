from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.content_cluster_entity import ContentCluster
from ...domain.entities.marketing_campaign_entity import MarketingCampaign
from ...domain.repositories.marketing_repository import MarketingRepository
from ..models.content_cluster_model import ContentClusterModel
from ..models.marketing_campaign_model import MarketingCampaignModel


class MarketingRepositoryImpl(MarketingRepository):
    """SQLAlchemy implementation of MarketingRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ------------------------------------------------------------------
    # Clusters
    # ------------------------------------------------------------------

    async def save_cluster(self, cluster: ContentCluster) -> ContentCluster:
        """Inserts a new ContentCluster row and returns the entity with db_id."""
        model = ContentClusterModel(
            topic_label=cluster.topic_label,
            keywords=cluster.keywords,
            sources=cluster.sources,
            avg_engagement_score=cluster.avg_engagement_score,
            item_ids=cluster.all_item_ids,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        cluster.db_id = model.id
        return cluster

    async def save_many_clusters(self, clusters: list[ContentCluster]) -> list[ContentCluster]:
        """Bulk inserts ContentClusters and returns them with db_ids."""
        models = [
            ContentClusterModel(
                topic_label=c.topic_label,
                keywords=c.keywords,
                sources=c.sources,
                avg_engagement_score=c.avg_engagement_score,
                item_ids=c.all_item_ids,
            )
            for c in clusters
        ]
        for model in models:
            self.session.add(model)
        await self.session.commit()
        for i, model in enumerate(models):
            await self.session.refresh(model)
            clusters[i].db_id = model.id
        return clusters

    async def find_recent_clusters(self, limit: int = 10) -> list[ContentCluster]:
        """Returns the most recently created content clusters."""
        stmt = (
            select(ContentClusterModel)
            .order_by(ContentClusterModel.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._cluster_to_entity(m) for m in models]

    # ------------------------------------------------------------------
    # Campaigns
    # ------------------------------------------------------------------

    async def save_campaign(self, campaign: MarketingCampaign) -> MarketingCampaign:
        """Upserts a MarketingCampaign by its UUID id."""
        model = MarketingCampaignModel(
            id=campaign.id,
            cluster_id=campaign.cluster_id,
            campaign_type=campaign.campaign_type,
            topic_label=campaign.topic_label,
            hook=campaign.hook,
            body=campaign.body,
            cta=campaign.cta,
            hashtags=campaign.hashtags,
            status=campaign.status,
        )
        model = await self.session.merge(model)
        await self.session.commit()
        return campaign

    async def save_many_campaigns(self, campaigns: list[MarketingCampaign]) -> list[MarketingCampaign]:
        """Bulk upserts MarketingCampaigns by their UUID ids."""
        models = [
            MarketingCampaignModel(
                id=c.id,
                cluster_id=c.cluster_id,
                campaign_type=c.campaign_type,
                topic_label=c.topic_label,
                hook=c.hook,
                body=c.body,
                cta=c.cta,
                hashtags=c.hashtags,
                status=c.status,
            )
            for c in campaigns
        ]
        for model in models:
            await self.session.merge(model)
        await self.session.commit()
        return campaigns

    async def find_recent_campaigns(
        self,
        limit: int = 20,
        status: str | None = None,
    ) -> list[MarketingCampaign]:
        """Returns recently generated campaigns, optionally filtered by status."""
        stmt = select(MarketingCampaignModel).order_by(
            MarketingCampaignModel.created_at.desc()
        )
        if status:
            stmt = stmt.where(MarketingCampaignModel.status == status)
        stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._campaign_to_entity(m) for m in models]

    # ------------------------------------------------------------------
    # Mappers
    # ------------------------------------------------------------------

    @staticmethod
    def _cluster_to_entity(model: ContentClusterModel) -> ContentCluster:
        return ContentCluster(
            cluster_id=model.id,
            topic_label=model.topic_label,
            representative_items=[],  # Not stored in DB, only transient during pipeline
            all_item_ids=model.item_ids or [],
            keywords=model.keywords or [],
            avg_engagement_score=model.avg_engagement_score,
            sources=model.sources or [],
            db_id=model.id,
        )

    @staticmethod
    def _campaign_to_entity(model: MarketingCampaignModel) -> MarketingCampaign:
        return MarketingCampaign(
            id=model.id,
            cluster_id=model.cluster_id,
            campaign_type=model.campaign_type,
            topic_label=model.topic_label,
            hook=model.hook,
            body=model.body,
            cta=model.cta,
            hashtags=model.hashtags or [],
            status=model.status,
            created_at=model.created_at,
        )
