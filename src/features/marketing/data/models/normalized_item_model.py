from sqlalchemy import Column, String, Float, DateTime, Boolean, ARRAY, func
from src.core.db.base_class import Base

class NormalizedItemModel(Base):
    """
    Silver Layer: Cleaned, translated (English), and normalized content.
    """
    __tablename__ = "normalized_items"

    id = Column(String, primary_key=True)
    raw_id = Column(String, nullable=False)
    source = Column(String, nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    url = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=False)
    engagement_score = Column(Float, nullable=False, default=0.0)
    published_at = Column(DateTime(timezone=True), nullable=False)
    original_language = Column(String, nullable=False, default="en")
    
    is_used_for_marketing = Column(Boolean, default=False, server_default='false', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
