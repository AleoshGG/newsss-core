from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, ARRAY, func

from src.core.db.base_class import Base


class MarketingCampaignModel(Base):
    """
    Stores LLM-generated marketing campaigns.
    Each row corresponds to one campaign generated for a content cluster.
    """

    __tablename__ = "marketing_campaigns"

    id = Column(String, primary_key=True)                                     # UUID4
    cluster_id = Column(Integer, ForeignKey("content_clusters.id"), nullable=True)
    campaign_type = Column(String, nullable=False)                            # linkedin_post | twitter_thread | email_newsletter
    topic_label = Column(String, nullable=False)
    hook = Column(String, nullable=True)
    body = Column(String, nullable=False)
    cta = Column(String, nullable=True)
    hashtags = Column(ARRAY(String), nullable=True)
    status = Column(String, default="draft", nullable=False)                  # draft | approved | published
    created_at = Column(DateTime(timezone=True), server_default=func.now())
