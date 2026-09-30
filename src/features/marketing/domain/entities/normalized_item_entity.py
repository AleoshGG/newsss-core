from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


@dataclass
class NormalizedItem:
    """
    Unified representation of a content item from any data source.
    Body is always clean plain text in English — ready for ML processing.
    """

    id: str
    source: Literal["youtube", "github", "google_news"]
    title: str
    body: str                     # Clean plain text, always in English
    url: str
    tags: list[str]               # channel name, repo topics, source_name
    engagement_score: float       # Normalized score across sources
    published_at: datetime
    original_language: str = "en" # ISO 639-1 code — for traceability


@dataclass
class ScoredItem(NormalizedItem):
    """A NormalizedItem enriched with a B2B intent score and tier classification."""

    intent_score: float = 0.0
    intent_tier: Literal["high", "medium", "low"] = "low"


@dataclass
class CleaningStats:
    """Observability stats produced by the CleanAndNormalize stage."""

    total_fetched: int = 0
    discarded_empty_body: int = 0
    discarded_short_body: int = 0
    translated: int = 0
    passed: int = 0
    by_source: dict[str, int] = field(default_factory=dict)
