from sqlalchemy import Column, DateTime, Float, Integer, String, ARRAY, func

from src.core.db.base_class import Base


class ContentClusterModel(Base):
    """
    Stores semantic topic clusters identified by the ML pipeline.
    Each row represents one K-Means cluster from a pipeline run.
    """

    __tablename__ = "content_clusters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_label = Column(String, nullable=False)
    keywords = Column(ARRAY(String), nullable=True)
    sources = Column(ARRAY(String), nullable=True)
    avg_engagement_score = Column(Float, nullable=False, default=0.0)
    item_ids = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
