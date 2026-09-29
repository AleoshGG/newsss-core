from sqlalchemy import Column, Integer, DateTime, ARRAY, String
from src.core.db.base_class import Base


class YouTubeSearchConfigModel(Base):
    __tablename__ = "youtube_search_config"

    id = Column(Integer, primary_key=True)
    keywords = Column(ARRAY(String), nullable=False)
    channel_ids = Column(ARRAY(String), nullable=False)
    languages = Column(ARRAY(String), nullable=False)
    max_results = Column(Integer, default=5)
    last_search_at = Column(DateTime(timezone=True), nullable=True)
