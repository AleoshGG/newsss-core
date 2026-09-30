import asyncio

from ..entities.content_cluster_entity import ContentCluster
from ..entities.normalized_item_entity import ScoredItem


class ClusterContentUseCase:
    """
    Stage 3 of the marketing pipeline.

    Generates semantic embeddings for each ScoredItem using sentence-transformers
    (model: all-MiniLM-L6-v2, ~90MB, downloaded once and cached by HuggingFace)
    and groups them into topic clusters using K-Means. Representative keywords
    per cluster are extracted with TF-IDF for automatic topic labeling.

    Everything runs locally on CPU — no external API calls.
    CPU-bound work is offloaded to a thread pool via asyncio.to_thread to avoid
    blocking FastAPI's event loop (same pattern as YouTubeTranscriptApi).

    Model note: all-MiniLM-L6-v2 produces 384-dimensional embeddings, is optimized
    for semantic textual similarity, and performs well on short paragraphs.
    """

    DEFAULT_MODEL = "all-MiniLM-L6-v2"

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        n_clusters: int = 5,
    ) -> None:
        self._model_name = model_name
        self._n_clusters = n_clusters

    async def execute(self, items: list[ScoredItem]) -> list[ContentCluster]:
        """
        Clusters items semantically. Returns clusters sorted by avg engagement desc.
        Auto-reduces n_clusters if there are fewer items than requested clusters.
        """
        if not items:
            return []

        n = min(self._n_clusters, len(items))
        texts = [f"{item.title}. {item.body[:600]}" for item in items]

        labels, keywords_per_cluster = await asyncio.to_thread(
            self._fit_and_cluster, texts, n
        )

        return self._build_cluster_entities(items, labels, keywords_per_cluster)

    # ------------------------------------------------------------------
    # CPU-bound — runs in thread pool
    # ------------------------------------------------------------------

    def _fit_and_cluster(
        self,
        texts: list[str],
        n_clusters: int,
    ) -> tuple[list[int], dict[int, list[str]]]:
        """
        1. Encode texts to dense embeddings with sentence-transformers.
        2. Cluster with K-Means (n_init=10, random_state=42 for reproducibility).
        3. Extract top TF-IDF keywords per cluster for topic labeling.
        Returns (cluster_labels, {cluster_id: [keyword, ...]}).
        """
        # Import here so the heavy libraries are only loaded when the pipeline runs,
        # not at server startup (keeps cold-start fast).
        from sentence_transformers import SentenceTransformer
        from sklearn.cluster import KMeans
        from sklearn.feature_extraction.text import TfidfVectorizer

        # --- Embeddings ---
        encoder = SentenceTransformer(self._model_name)
        embeddings = encoder.encode(texts, show_progress_bar=False, batch_size=32)

        # --- K-Means ---
        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels: list[int] = km.fit_predict(embeddings).tolist()

        # --- TF-IDF keywords per cluster ---
        keywords_per_cluster: dict[int, list[str]] = {}
        tfidf = TfidfVectorizer(
            max_features=30,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
        )

        for cluster_id in range(n_clusters):
            cluster_texts = [t for t, lbl in zip(texts, labels) if lbl == cluster_id]
            if not cluster_texts:
                keywords_per_cluster[cluster_id] = []
                continue
            try:
                tfidf.fit(cluster_texts)
                # Sort features by their mean TF-IDF score across docs in the cluster
                feature_names = tfidf.get_feature_names_out()
                scores = tfidf.transform(cluster_texts).mean(axis=0).A1
                top_indices = scores.argsort()[::-1][:8]
                keywords_per_cluster[cluster_id] = [feature_names[i] for i in top_indices]
            except Exception as e:
                print(f"TF-IDF error for cluster {cluster_id}: {e}")
                keywords_per_cluster[cluster_id] = []

        return labels, keywords_per_cluster

    # ------------------------------------------------------------------
    # Entity assembly
    # ------------------------------------------------------------------

    def _build_cluster_entities(
        self,
        items: list[ScoredItem],
        labels: list[int],
        keywords_per_cluster: dict[int, list[str]],
    ) -> list[ContentCluster]:
        """Groups items by cluster label and builds ContentCluster entities."""
        cluster_buckets: dict[int, list[ScoredItem]] = {}
        for item, label in zip(items, labels):
            cluster_buckets.setdefault(label, []).append(item)

        clusters: list[ContentCluster] = []
        for cluster_id, cluster_items in cluster_buckets.items():
            # Top 5 items by engagement score for the LLM prompt context
            top_items = sorted(
                cluster_items, key=lambda x: x.engagement_score, reverse=True
            )[:5]

            sources = list({item.source for item in cluster_items})
            avg_eng = sum(i.engagement_score for i in cluster_items) / len(cluster_items)
            keywords = keywords_per_cluster.get(cluster_id, [])

            # Auto-generate a human-readable topic label from top 3 keywords
            topic_label = " · ".join(keywords[:3]) if keywords else f"Topic {cluster_id + 1}"

            clusters.append(ContentCluster(
                cluster_id=cluster_id,
                topic_label=topic_label,
                representative_items=top_items,
                all_item_ids=[i.id for i in cluster_items],
                keywords=keywords,
                avg_engagement_score=round(avg_eng, 4),
                sources=sources,
            ))

        # Return clusters ordered from most to least engaging
        return sorted(clusters, key=lambda c: c.avg_engagement_score, reverse=True)
