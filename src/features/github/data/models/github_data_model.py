from sqlalchemy import Column, Integer, String, ARRAY
from src.core.db.base_class import Base

class GitHubDataModel(Base):
    __tablename__ = "github_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    html_url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    stargazers_count = Column(Integer, default=0)
    language = Column(String, nullable=True)
    updated_at = Column(String, nullable=False)
    topics = Column(ARRAY(String), nullable=True)
    readme = Column(String, nullable=True)
    owner_avatar_url = Column(String, nullable=True)
    forks_count = Column(Integer, nullable=True)
    open_issues_count = Column(Integer, nullable=True)
    license = Column(String, nullable=True)
