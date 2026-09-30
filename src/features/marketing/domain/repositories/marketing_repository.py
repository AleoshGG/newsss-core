from abc import ABC, abstractmethod

from ..entities.content_cluster_entity import ContentCluster
from ..entities.marketing_campaign_entity import MarketingCampaign


class MarketingRepository(ABC):
    """Abstract repository for persisting and reading marketing pipeline outputs."""

    @abstractmethod
    async def save_cluster(self, cluster: ContentCluster) -> ContentCluster:
        """Persists a ContentCluster and returns the entity with its assigned db_id."""
        ...

    @abstractmethod
    async def save_many_clusters(self, clusters: list[ContentCluster]) -> list[ContentCluster]:
        """Bulk persists ContentClusters and returns the entities with their assigned db_ids."""
        ...

    @abstractmethod
    async def save_campaign(self, campaign: MarketingCampaign) -> MarketingCampaign:
        """Persists a MarketingCampaign (UPSERT by id)."""
        ...

    @abstractmethod
    async def save_many_campaigns(self, campaigns: list[MarketingCampaign]) -> list[MarketingCampaign]:
        """Bulk persists MarketingCampaigns (UPSERT by id)."""
        ...

    @abstractmethod
    async def find_recent_campaigns(
        self,
        limit: int = 20,
        status: str | None = None,
    ) -> list[MarketingCampaign]:
        """
        Retrieves recently generated campaigns ordered by created_at desc.
        Optionally filter by status: 'draft', 'approved', or 'published'.
        """
        ...

    @abstractmethod
    async def find_recent_clusters(self, limit: int = 10) -> list[ContentCluster]:
        """Retrieves recently generated content clusters ordered by created_at desc."""
        ...
