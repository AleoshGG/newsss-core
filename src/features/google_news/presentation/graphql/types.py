from datetime import datetime
from typing import List, Optional
import strawberry

from ...domain.entities.google_news_article_data_entity import GoogleNewsArticleDataEntity
from ...domain.entities.google_news_config_entity import GoogleNewsConfigEntity


@strawberry.type
class NewsArticleType:
    id: str
    title: str
    link: str
    pub_date: str
    source_name: str
    source_url: str
    fetched_at: Optional[datetime]
    image_url: Optional[str]
    content: Optional[str]

    @classmethod
    def from_entity(cls, entity: GoogleNewsArticleDataEntity) -> "NewsArticleType":
        pub_date_str = (
            entity.pub_date.isoformat()
            if isinstance(entity.pub_date, datetime)
            else str(entity.pub_date or "")
        )
        return cls(
            id=entity.id,
            title=entity.title,
            link=entity.link,
            pub_date=pub_date_str,
            source_name=entity.source_name,
            source_url=entity.source_url,
            fetched_at=entity.fetched_at,
            image_url=entity.image_url,
            content=entity.content,
        )


@strawberry.type
class GoogleNewsConfigType:
    id: int
    q: str
    hl: str
    gl: str
    ceid: str
    when: str
    site: Optional[str]
    intitle: Optional[str]
    max_results: int
    last_search_at: Optional[datetime]

    @classmethod
    def from_entity(cls, entity: GoogleNewsConfigEntity) -> "GoogleNewsConfigType":
        return cls(
            id=entity.id,
            q=entity.q,
            hl=entity.hl,
            gl=entity.gl,
            ceid=entity.ceid,
            when=entity.when,
            site=entity.site,
            intitle=entity.intitle,
            max_results=entity.max_results,
            last_search_at=entity.last_search_at,
        )


@strawberry.input(description="Configuration settings for fetching Google News articles.")
class GoogleNewsConfigInput:
    q: str = strawberry.field(description="Main search query (e.g. 'Inteligencia Artificial OR IA').")
    hl: str = strawberry.field(default="es-419", description="Interface language code (e.g. 'es-419', 'en-US').")
    gl: str = strawberry.field(default="MX", description="Geolocation country code (e.g. 'MX', 'US').")
    ceid: str = strawberry.field(default="MX:es-419", description="Edition identifier (e.g. 'MX:es-419').")
    when: str = strawberry.field(default="1d", description="Time window: '1h', '1d', '7d', or '1y'.")
    site: Optional[str] = strawberry.field(default=None, description="Restrict results to a specific domain.")
    intitle: Optional[str] = strawberry.field(default=None, description="Require this word in article titles.")
    max_results: int = strawberry.field(default=30, description="Maximum number of articles to fetch and save.")

    def to_entity(self) -> GoogleNewsConfigEntity:
        return GoogleNewsConfigEntity(
            id=1,
            q=self.q,
            hl=self.hl,
            gl=self.gl,
            ceid=self.ceid,
            when=self.when,
            site=self.site,
            intitle=self.intitle,
            max_results=self.max_results,
        )
