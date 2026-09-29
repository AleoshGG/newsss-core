from sqlalchemy import Column, String, Integer, DateTime
from src.core.db.base_class import Base

class YouTubeVideoModel(Base):
    __tablename__ = "youtube_videos"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=False)
    url = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=False)
    transcript = Column(String, nullable=False)
    
    # Metrics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
