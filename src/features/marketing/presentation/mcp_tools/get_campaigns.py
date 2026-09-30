from typing import Optional

from src.mcp_server import mcp
from src.core.db.session import async_session
from src.features.marketing.data.repositories.marketing_repository_impl import MarketingRepositoryImpl


@mcp.tool()
async def get_marketing_campaigns(limit: int = 20, status: Optional[str] = None) -> list[dict]:
    """
    Retrieves previously generated marketing campaigns from the database.

    Args:
        limit: Maximum number of campaigns to return (most recent first). Default 20.
        status: Optional filter. One of: 'draft', 'approved', 'published'.
                If omitted, returns campaigns of all statuses.

    Returns:
        A list of campaign dicts with fields: id, topic_label, campaign_type,
        hook, body, cta, hashtags, status, created_at.
    """
    async with async_session() as session:
        repo = MarketingRepositoryImpl(session=session)
        campaigns = await repo.find_recent_campaigns(limit=limit, status=status)

    return [
        {
            "id": c.id,
            "topic_label": c.topic_label,
            "campaign_type": c.campaign_type,
            "hook": c.hook,
            "body": c.body,
            "cta": c.cta,
            "hashtags": c.hashtags,
            "status": c.status,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in campaigns
    ]
