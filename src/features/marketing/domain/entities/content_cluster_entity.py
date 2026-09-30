from dataclasses import dataclass, field


@dataclass
class ContentCluster:
    """
    A semantic topic cluster identified by K-Means over item embeddings.
    Contains the top representative items (by engagement) and TF-IDF keywords
    that characterize the cluster topic.
    """

    cluster_id: int
    topic_label: str                       # Auto-generated from top TF-IDF keywords
    representative_items: list             # Top NormalizedItems by engagement (max 5)
    all_item_ids: list[str]                # IDs of all items in this cluster
    keywords: list[str]                    # TF-IDF top keywords for the cluster
    avg_engagement_score: float
    sources: list[str]                     # Which sources contributed (youtube, github, google_news)
    db_id: int | None = None               # Set after persistence
