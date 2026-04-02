"""Abstract base class for social media discovery/analytics adapters."""

from abc import ABC, abstractmethod
from typing import Any


class DiscoveryAdapter(ABC):
    """Base interface for all social media discovery adapters.

    Each platform must implement analytics retrieval, trend discovery,
    mention search, competitor tracking, and hashtag performance.
    Stubs return realistic mock data for agent testing.
    """

    @abstractmethod
    async def get_analytics(self, date_from: str, date_to: str) -> dict[str, Any]:
        """Get engagement metrics for a date range.

        Returns dict with: impressions, clicks, shares, comments, engagement_rate, top_posts.
        """
        ...

    @abstractmethod
    async def discover_trends(self, topic: str) -> dict[str, Any]:
        """Discover trending topics, hashtags, and content formats for a topic.

        Returns dict with: trending_hashtags, trending_topics, popular_formats, insights.
        """
        ...

    @abstractmethod
    async def search_mentions(self, query: str, limit: int = 50) -> dict[str, Any]:
        """Search for brand/keyword mentions with sentiment analysis.

        Returns dict with: mentions (list), total_count, sentiment_breakdown.
        """
        ...

    @abstractmethod
    async def get_competitor_activity(self, competitor: str) -> dict[str, Any]:
        """Analyze competitor's recent posts and engagement.

        Returns dict with: recent_posts, avg_engagement, posting_frequency, top_content.
        """
        ...

    @abstractmethod
    async def get_hashtag_performance(self, hashtag: str) -> dict[str, Any]:
        """Get reach and engagement metrics for a specific hashtag.

        Returns dict with: reach, posts_count, engagement_rate, peak_hours, related_hashtags.
        """
        ...

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Lowercase platform identifier."""
        ...
