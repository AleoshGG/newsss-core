from dataclasses import dataclass
from datetime import datetime

@dataclass
class GoogleNewsArticleDataEntity:
    id: str
    title: str
    link: str
    pub_date: datetime | str
    source_name: str
    source_url: str
    fetched_at: datetime | None = None
    image_url: str | None = None
    content: str | None = None
    is_processed: bool = False
