from datetime import datetime, timezone

from ..entities.normalized_item_entity import NormalizedItem, ScoredItem


# ---------------------------------------------------------------------------
# B2B / Consulting-oriented intent keyword taxonomy
# ---------------------------------------------------------------------------

B2B_INTENT_KEYWORDS: dict[str, list[str]] = {
    "high": [
        # Product launches and strong trends
        "launch", "release", "released", "announced", "trending", "viral",
        "case study", "roi", "revenue", "growth hacking", "growth strategy",
        # Enterprise / B2B signals
        "enterprise", "saas", "b2b", "automation", "productivity", "efficiency",
        "digital transformation", "consulting", "strategy", "competitive advantage",
        # AI / LLM (current high-value topics for tech consultancies)
        "ai agent", "llm", "copilot", "workflow", "integration", "platform",
        "generative ai", "gpt", "gemini", "claude", "anthropic", "openai",
    ],
    "medium": [
        # Educational / demonstrative value
        "tutorial", "how to", "guide", "best practices", "framework",
        "open source", "tool", "comparison", "benchmark", "overview",
        "getting started", "introduction", "explained",
        # Business context
        "market", "industry", "trend", "adoption", "deployment", "scalable",
    ],
    "low": [
        # Technical noise with low marketing value
        "bugfix", "bug fix", "hotfix", "refactor", "deprecated", "changelog",
        "docs update", "ci/cd", "dependency", "version bump", "minor update",
        "wip", "todo", "draft",
    ],
}

_RECENCY_DECAY_DAYS: int = 30  # Score decays linearly to 0 over 30 days


# ---------------------------------------------------------------------------
# Scoring function
# ---------------------------------------------------------------------------

def _compute_intent_score(
    body: str,
    title: str,
    engagement: float,
    published_at: datetime,
    max_engagement: float,
) -> tuple[float, str]:
    """
    Computes a composite B2B intent score in [0, 1] and assigns a tier.

    Formula:
        score = keyword_score * 0.50 + engagement_score * 0.30 + recency_score * 0.20

    Returns (score, tier) where tier is "high" | "medium" | "low".
    """
    text = f"{title} {body}".lower()

    # --- Keyword scoring (0-1) ---
    kw_score = 0.0
    for word in B2B_INTENT_KEYWORDS["high"]:
        if word in text:
            kw_score = min(kw_score + 0.15, 1.0)
    for word in B2B_INTENT_KEYWORDS["medium"]:
        if word in text:
            kw_score = min(kw_score + 0.08, 1.0)
    for word in B2B_INTENT_KEYWORDS["low"]:
        if word in text:
            kw_score = max(kw_score - 0.12, 0.0)

    # --- Normalized engagement (0-1) ---
    eng_score = min(engagement / (max_engagement + 1.0), 1.0)

    # --- Recency score (0-1, linear decay over RECENCY_DECAY_DAYS) ---
    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=timezone.utc)
    days_old = (datetime.now(timezone.utc) - published_at).days
    recency_score = max(0.0, 1.0 - (days_old / _RECENCY_DECAY_DAYS))

    # --- Weighted combination ---
    score = (kw_score * 0.50) + (eng_score * 0.30) + (recency_score * 0.20)

    # --- Tier assignment ---
    if score >= 0.55:
        tier = "high"
    elif score >= 0.30:
        tier = "medium"
    else:
        tier = "low"

    return round(score, 4), tier


# ---------------------------------------------------------------------------
# IntentFilterUseCase — Stage 2
# ---------------------------------------------------------------------------

class IntentFilterUseCase:
    """
    Stage 2 of the marketing pipeline.

    Scores each NormalizedItem for B2B marketing intent using a weighted
    combination of keyword matching, normalized engagement, and recency.
    Items below the minimum score threshold are discarded.

    Keyword taxonomy is calibrated for tech consultancies targeting CTOs,
    IT directors, and enterprise decision-makers.
    """

    def execute(
        self,
        items: list[NormalizedItem],
        min_score: float = 0.25,
    ) -> list[ScoredItem]:
        """
        Scores and filters items. Returns ScoredItems sorted by intent_score desc.
        """
        if not items:
            return []

        max_engagement = max(i.engagement_score for i in items) if items else 1.0

        scored: list[ScoredItem] = []
        for item in items:
            score, tier = _compute_intent_score(
                body=item.body,
                title=item.title,
                engagement=item.engagement_score,
                published_at=item.published_at,
                max_engagement=max_engagement,
            )
            if score < min_score:
                continue
            scored.append(ScoredItem(
                id=item.id,
                raw_id=item.raw_id,
                source=item.source,
                title=item.title,
                body=item.body,
                url=item.url,
                tags=item.tags,
                engagement_score=item.engagement_score,
                published_at=item.published_at,
                original_language=item.original_language,
                intent_score=score,
                intent_tier=tier,
            ))

        return sorted(scored, key=lambda x: x.intent_score, reverse=True)
