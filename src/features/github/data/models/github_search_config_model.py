from sqlalchemy import Column, Integer, DateTime, Boolean, ARRAY, String
from src.core.db.base_class import Base


class GitHubSearchConfigModel(Base):
    __tablename__ = "github_search_config"

    id = Column(Integer, primary_key=True)
    keywords = Column(ARRAY(String), nullable=False)
    days_active = Column(Integer, default=7)
    min_stars = Column(Integer, default=50)
    min_forks = Column(Integer, default=5)
    require_license = Column(Boolean, default=False)
    selected_topics = Column(ARRAY(String), nullable=False)
    selected_languages = Column(ARRAY(String), nullable=False)
    max_results = Column(Integer, default=30)
    last_search_at = Column(DateTime(timezone=True), nullable=True)
