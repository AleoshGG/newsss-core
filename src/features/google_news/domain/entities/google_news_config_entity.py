from dataclasses import dataclass
from datetime import datetime


@dataclass
class GoogleNewsConfigEntity:
    """Domain entity representing the Google News search configuration (singleton, id=1)."""
    id: int = 1
    q: str = "Inteligencia Artificial OR IA"
    hl: str = "es-419"
    gl: str = "MX"
    ceid: str = "MX:es-419"
    when: str = "1d"  # '1h', '1d', '7d', '1y'
    site: str | None = None
    intitle: str | None = None
    max_results: int = 30
    last_search_at: datetime | None = None
