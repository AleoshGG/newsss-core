from sqlalchemy import Column, Integer, DateTime, String
from src.core.db.base_class import Base


class GoogleNewsConfigModel(Base):
    __tablename__ = "google_news_config"

    id = Column(Integer, primary_key=True)
    q = Column(String, nullable=False)
    hl = Column(String, default="es-419")
    gl = Column(String, default="MX")
    ceid = Column(String, default="MX:es-419")
    when = Column(String, default="1d")  # '1h', '1d', '7d', '1y'
    site = Column(String, nullable=True)
    intitle = Column(String, nullable=True)
    max_results = Column(Integer, default=30)
    last_search_at = Column(DateTime(timezone=True), nullable=True)
