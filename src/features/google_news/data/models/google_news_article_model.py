from sqlalchemy import Column, String, DateTime
from src.core.db.base_class import Base

class GoogleNewsArticleModel(Base):
    __tablename__ = "google_news_articles"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    pub_date = Column(String, nullable=False)
    source_name = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    fetched_at = Column(DateTime(timezone=True), nullable=True)
    image_url = Column(String, nullable=True)
    content = Column(String, nullable=True)
