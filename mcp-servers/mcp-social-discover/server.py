"""GrowthOS MCP Social Discover Server.

Analytics, trends, and social listening across multiple platforms via MCP tools.
Integrates with shared-lib for rate limiting, circuit breaking, and audit logging.
"""

import hashlib
import sys
from pathlib import Path

from fastmcp import FastMCP

# Add shared-lib and current dir to path
_shared_lib = str(Path(__file__).resolve().parent.parent.parent / "shared-lib")
sys.path.insert(0, _shared_lib)
sys.path.insert(0, str(Path(__file__).resolve().parent))

from growthOS_shared import (  # noqa: E402
    AuditLogger,
    CircuitBreaker,
    RateLimits,
    TokenManager,
)
from platforms import get_adapter, list_available  # noqa: E402

# --- Initialization ---

mcp = FastMCP("growthos-social-discover")

token_manager = TokenManager()
audit_logger = AuditLogger()

_circuit_breakers: dict[str, CircuitBreaker] = {}

_DEFAULT_RATE_LIMITS: dict[str, int] = {
    "linkedin": 200,
    "twitter": 500,
    "reddit": 300,
}

for _platform_name in list_available():
    limit = _DEFAULT_RATE_LIMITS.get(_platform_name, 200)
    token_manager.register_platform(_platform_name, RateLimits(max_requests=limit))
    _circuit_breakers[_platform_name] = CircuitBreaker(
        failure_threshold=3, recovery_timeout=300
    )


def _query_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _resolve_platforms(platforms: list[str] | None) -> list[str]:
    """Resolve platform list — None means all available."""
    if platforms:
        for p in platforms:
            if p.lower() not in [a.lower() for a in list_available()]:
                raise ValueError(
                    f"Unknown platform '{p}'. Available: {', '.join(list_available())}"
                )
        return [p.lower() for p in platforms]
    return list_available()


# --- MCP Tools ---


@mcp.tool()
async def get_analytics(
    platform: str,
    date_from: str,
    date_to: str,
) -> dict:
    """Get engagement metrics for a platform over a date range.

    Args:
        platform: Target platform (linkedin, twitter, reddit)
        date_from: Start date (YYYY-MM-DD)
        date_to: End date (YYYY-MM-DD)

    Returns metrics: impressions, clicks, shares, comments, engagement_rate, top_posts.
    """
    adapter = get_adapter(platform)
    name = adapter.platform_name
    cb = _circuit_breakers[name]

    token_manager.consume(name)
    audit_logger.log_action(
        action="get_analytics",
        platform=name,
        content_hash=_query_hash(f"{date_from}-{date_to}"),
        status="success",
        metadata={"date_from": date_from, "date_to": date_to},
    )

    result = await cb.call(adapter.get_analytics, date_from, date_to)
    return {"status": "ok", "data": result}


@mcp.tool()
async def discover_trends(
    topic: str,
    platforms: list[str] | None = None,
) -> dict:
    """Discover trending topics, hashtags, and content formats.

    Args:
        topic: Topic to research (e.g. "AI marketing", "developer tools")
        platforms: Optional list of platforms to search. None = all platforms.

    Returns trending hashtags, topics, popular formats, and insights per platform.
    """
    target_platforms = _resolve_platforms(platforms)
    results = {}

    for p in target_platforms:
        adapter = get_adapter(p)
        cb = _circuit_breakers[p]
        token_manager.consume(p)
        results[p] = await cb.call(adapter.discover_trends, topic)

    audit_logger.log_action(
        action="discover_trends",
        platform=",".join(target_platforms),
        content_hash=_query_hash(topic),
        status="success",
        metadata={"topic": topic, "platforms": target_platforms},
    )

    return {"status": "ok", "topic": topic, "platforms": results}


@mcp.tool()
async def search_mentions(
    query: str,
    platforms: list[str] | None = None,
    limit: int = 50,
) -> dict:
    """Search for brand or keyword mentions with sentiment analysis.

    Args:
        query: Search query (brand name, keyword, etc.)
        platforms: Optional list of platforms. None = all platforms.
        limit: Max mentions per platform (default 50)

    Returns mentions with sentiment breakdown per platform.
    """
    target_platforms = _resolve_platforms(platforms)
    results = {}
    total_mentions = 0

    for p in target_platforms:
        adapter = get_adapter(p)
        cb = _circuit_breakers[p]
        token_manager.consume(p)
        data = await cb.call(adapter.search_mentions, query, limit)
        results[p] = data
        total_mentions += data.get("total_count", 0)

    audit_logger.log_action(
        action="search_mentions",
        platform=",".join(target_platforms),
        content_hash=_query_hash(query),
        status="success",
        metadata={"query": query, "limit": limit, "total_found": total_mentions},
    )

    return {
        "status": "ok",
        "query": query,
        "total_mentions": total_mentions,
        "platforms": results,
    }


@mcp.tool()
async def get_competitor_activity(
    competitor: str,
    platforms: list[str] | None = None,
) -> dict:
    """Analyze a competitor's recent activity and engagement across platforms.

    Args:
        competitor: Competitor name or handle
        platforms: Optional list of platforms. None = all platforms.

    Returns competitor posts, engagement metrics, and content strategy insights.
    """
    target_platforms = _resolve_platforms(platforms)
    results = {}

    for p in target_platforms:
        adapter = get_adapter(p)
        cb = _circuit_breakers[p]
        token_manager.consume(p)
        results[p] = await cb.call(adapter.get_competitor_activity, competitor)

    audit_logger.log_action(
        action="get_competitor_activity",
        platform=",".join(target_platforms),
        content_hash=_query_hash(competitor),
        status="success",
        metadata={"competitor": competitor, "platforms": target_platforms},
    )

    return {"status": "ok", "competitor": competitor, "platforms": results}


@mcp.tool()
async def get_hashtag_performance(
    hashtag: str,
    platform: str,
) -> dict:
    """Get reach and engagement metrics for a specific hashtag on a platform.

    Args:
        hashtag: Hashtag to analyze (with or without #)
        platform: Target platform (linkedin, twitter, reddit)

    Returns reach, post count, engagement rate, peak hours, and related hashtags.
    """
    adapter = get_adapter(platform)
    name = adapter.platform_name
    cb = _circuit_breakers[name]

    token_manager.consume(name)

    result = await cb.call(adapter.get_hashtag_performance, hashtag)

    audit_logger.log_action(
        action="get_hashtag_performance",
        platform=name,
        content_hash=_query_hash(hashtag),
        status="success",
        metadata={"hashtag": hashtag},
    )

    return {"status": "ok", "data": result}


if __name__ == "__main__":
    mcp.run()
