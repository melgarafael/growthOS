"""Tests for mcp-social-discover server tools and platform adapters."""

import sys
from pathlib import Path

import pytest

# Setup paths so imports work from test context
_server_dir = str(Path(__file__).resolve().parent.parent)
_shared_lib = str(Path(__file__).resolve().parent.parent.parent.parent / "shared-lib")
sys.path.insert(0, _server_dir)
sys.path.insert(0, _shared_lib)

from platforms import get_adapter, list_available  # noqa: E402
from platforms.base import DiscoveryAdapter  # noqa: E402
from platforms.linkedin import LinkedInDiscoveryAdapter  # noqa: E402
from platforms.twitter import TwitterDiscoveryAdapter  # noqa: E402
from platforms.reddit import RedditDiscoveryAdapter  # noqa: E402


# --- Platform Registry Tests ---


class TestPlatformRegistry:
    def test_list_available_returns_all_platforms(self):
        platforms = list_available()
        assert set(platforms) == {"linkedin", "reddit", "twitter"}

    def test_get_adapter_returns_correct_type(self):
        assert isinstance(get_adapter("linkedin"), LinkedInDiscoveryAdapter)
        assert isinstance(get_adapter("twitter"), TwitterDiscoveryAdapter)
        assert isinstance(get_adapter("reddit"), RedditDiscoveryAdapter)

    def test_get_adapter_case_insensitive(self):
        assert isinstance(get_adapter("LinkedIn"), LinkedInDiscoveryAdapter)
        assert isinstance(get_adapter("TWITTER"), TwitterDiscoveryAdapter)
        assert isinstance(get_adapter("Reddit"), RedditDiscoveryAdapter)

    def test_get_adapter_unknown_platform_raises(self):
        with pytest.raises(ValueError, match="Unknown platform"):
            get_adapter("tiktok")

    def test_list_available_is_sorted(self):
        platforms = list_available()
        assert platforms == sorted(platforms)


# --- Platform Adapter Tests ---


class TestPlatformAdapters:
    ADAPTERS = [
        LinkedInDiscoveryAdapter,
        TwitterDiscoveryAdapter,
        RedditDiscoveryAdapter,
    ]

    @pytest.mark.parametrize("cls", ADAPTERS)
    def test_adapter_is_discovery_adapter(self, cls):
        assert issubclass(cls, DiscoveryAdapter)

    @pytest.mark.parametrize("cls", ADAPTERS)
    def test_platform_name_is_string(self, cls):
        adapter = cls()
        assert isinstance(adapter.platform_name, str)
        assert len(adapter.platform_name) > 0

    @pytest.mark.parametrize("cls", ADAPTERS)
    def test_platform_name_is_lowercase(self, cls):
        adapter = cls()
        assert adapter.platform_name == adapter.platform_name.lower()


# --- Analytics Tests ---


class TestGetAnalytics:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_returns_required_fields(self, cls):
        adapter = cls()
        result = await adapter.get_analytics("2026-03-01", "2026-03-31")
        assert result["platform"] == adapter.platform_name
        assert "impressions" in result
        assert "clicks" in result
        assert "shares" in result
        assert "comments" in result
        assert "engagement_rate" in result
        assert "top_posts" in result
        assert result["_mock"] is True

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_period_matches_input(self, cls):
        adapter = cls()
        result = await adapter.get_analytics("2026-01-01", "2026-01-31")
        assert result["period"]["from"] == "2026-01-01"
        assert result["period"]["to"] == "2026-01-31"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_metrics_are_positive(self, cls):
        adapter = cls()
        result = await adapter.get_analytics("2026-03-01", "2026-03-31")
        assert result["impressions"] > 0
        assert result["clicks"] > 0
        assert result["engagement_rate"] > 0

    @pytest.mark.asyncio
    async def test_deterministic_output(self):
        adapter = LinkedInDiscoveryAdapter()
        r1 = await adapter.get_analytics("2026-03-01", "2026-03-31")
        r2 = await adapter.get_analytics("2026-03-01", "2026-03-31")
        assert r1 == r2


# --- Discover Trends Tests ---


class TestDiscoverTrends:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_returns_required_fields(self, cls):
        adapter = cls()
        result = await adapter.discover_trends("AI marketing")
        assert result["platform"] == adapter.platform_name
        assert result["topic"] == "AI marketing"
        assert "trending_hashtags" in result
        assert "trending_topics" in result
        assert "popular_formats" in result
        assert "insights" in result
        assert result["_mock"] is True

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_trending_topics_have_volume(self, cls):
        adapter = cls()
        result = await adapter.discover_trends("developer tools")
        for topic in result["trending_topics"]:
            assert "topic" in topic
            assert "volume" in topic
            assert topic["volume"] > 0

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_popular_formats_have_multiplier(self, cls):
        adapter = cls()
        result = await adapter.discover_trends("startup")
        for fmt in result["popular_formats"]:
            assert "format" in fmt
            assert "engagement_multiplier" in fmt
            assert fmt["engagement_multiplier"] > 0


# --- Search Mentions Tests ---


class TestSearchMentions:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_returns_required_fields(self, cls):
        adapter = cls()
        result = await adapter.search_mentions("GrowthOS")
        assert result["platform"] == adapter.platform_name
        assert result["query"] == "GrowthOS"
        assert "mentions" in result
        assert "total_count" in result
        assert "sentiment_breakdown" in result
        assert result["_mock"] is True

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_mentions_have_sentiment(self, cls):
        adapter = cls()
        result = await adapter.search_mentions("TestBrand")
        for mention in result["mentions"]:
            assert "sentiment" in mention
            assert mention["sentiment"] in {"positive", "neutral", "negative"}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_limit_caps_mentions(self, cls):
        adapter = cls()
        result = await adapter.search_mentions("TestBrand", limit=3)
        assert len(result["mentions"]) <= 3

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_sentiment_breakdown_has_all_categories(self, cls):
        adapter = cls()
        result = await adapter.search_mentions("TestBrand")
        breakdown = result["sentiment_breakdown"]
        assert "positive" in breakdown
        assert "neutral" in breakdown
        assert "negative" in breakdown


# --- Competitor Activity Tests ---


class TestGetCompetitorActivity:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_returns_required_fields(self, cls):
        adapter = cls()
        result = await adapter.get_competitor_activity("CompetitorCo")
        assert result["platform"] == adapter.platform_name
        assert result["competitor"] == "CompetitorCo"
        assert "recent_posts" in result
        assert "top_content" in result
        assert result["_mock"] is True

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_recent_posts_are_list(self, cls):
        adapter = cls()
        result = await adapter.get_competitor_activity("Rival")
        assert isinstance(result["recent_posts"], list)
        assert len(result["recent_posts"]) > 0


# --- Hashtag Performance Tests ---


class TestGetHashtagPerformance:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_returns_required_fields(self, cls):
        adapter = cls()
        result = await adapter.get_hashtag_performance("#AI")
        assert result["platform"] == adapter.platform_name
        assert result["hashtag"] == "#AI"
        assert "reach" in result
        assert "posts_count" in result
        assert "engagement_rate" in result
        assert "peak_hours" in result
        assert result["_mock"] is True

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_strips_leading_hash(self, cls):
        adapter = cls()
        r1 = await adapter.get_hashtag_performance("#Python")
        r2 = await adapter.get_hashtag_performance("Python")
        assert r1["hashtag"] == "#Python"
        assert r2["hashtag"] == "#Python"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cls", [LinkedInDiscoveryAdapter, TwitterDiscoveryAdapter, RedditDiscoveryAdapter])
    async def test_metrics_are_positive(self, cls):
        adapter = cls()
        result = await adapter.get_hashtag_performance("Tech")
        assert result["reach"] > 0
        assert result["posts_count"] > 0
        assert result["engagement_rate"] > 0


# --- Server Tool Integration Tests ---


class TestServerTools:
    """Test the MCP server tools via direct import."""

    @pytest.fixture(autouse=True)
    def _setup_server(self):
        import server
        self.server = server

    @pytest.mark.asyncio
    async def test_get_analytics_success(self):
        result = await self.server.get_analytics(
            platform="linkedin",
            date_from="2026-03-01",
            date_to="2026-03-31",
        )
        assert result["status"] == "ok"
        assert "data" in result
        assert result["data"]["platform"] == "linkedin"

    @pytest.mark.asyncio
    async def test_get_analytics_unknown_platform(self):
        with pytest.raises(ValueError, match="Unknown platform"):
            await self.server.get_analytics(
                platform="tiktok",
                date_from="2026-03-01",
                date_to="2026-03-31",
            )

    @pytest.mark.asyncio
    async def test_discover_trends_all_platforms(self):
        result = await self.server.discover_trends(topic="AI marketing")
        assert result["status"] == "ok"
        assert result["topic"] == "AI marketing"
        assert "linkedin" in result["platforms"]
        assert "twitter" in result["platforms"]
        assert "reddit" in result["platforms"]

    @pytest.mark.asyncio
    async def test_discover_trends_single_platform(self):
        result = await self.server.discover_trends(
            topic="startup", platforms=["twitter"]
        )
        assert result["status"] == "ok"
        assert set(result["platforms"].keys()) == {"twitter"}

    @pytest.mark.asyncio
    async def test_discover_trends_unknown_platform(self):
        with pytest.raises(ValueError, match="Unknown platform"):
            await self.server.discover_trends(
                topic="test", platforms=["tiktok"]
            )

    @pytest.mark.asyncio
    async def test_search_mentions_all_platforms(self):
        result = await self.server.search_mentions(query="GrowthOS")
        assert result["status"] == "ok"
        assert result["query"] == "GrowthOS"
        assert result["total_mentions"] > 0
        assert len(result["platforms"]) == 3

    @pytest.mark.asyncio
    async def test_search_mentions_with_limit(self):
        result = await self.server.search_mentions(
            query="TestBrand", limit=2
        )
        assert result["status"] == "ok"
        for platform_data in result["platforms"].values():
            assert len(platform_data["mentions"]) <= 2

    @pytest.mark.asyncio
    async def test_search_mentions_single_platform(self):
        result = await self.server.search_mentions(
            query="brand", platforms=["reddit"]
        )
        assert result["status"] == "ok"
        assert set(result["platforms"].keys()) == {"reddit"}

    @pytest.mark.asyncio
    async def test_get_competitor_activity_all_platforms(self):
        result = await self.server.get_competitor_activity(competitor="Rival")
        assert result["status"] == "ok"
        assert result["competitor"] == "Rival"
        assert len(result["platforms"]) == 3

    @pytest.mark.asyncio
    async def test_get_competitor_activity_single_platform(self):
        result = await self.server.get_competitor_activity(
            competitor="Rival", platforms=["linkedin"]
        )
        assert result["status"] == "ok"
        assert set(result["platforms"].keys()) == {"linkedin"}

    @pytest.mark.asyncio
    async def test_get_hashtag_performance_success(self):
        result = await self.server.get_hashtag_performance(
            hashtag="#Python", platform="twitter"
        )
        assert result["status"] == "ok"
        assert "data" in result
        assert result["data"]["platform"] == "twitter"
        assert result["data"]["hashtag"] == "#Python"

    @pytest.mark.asyncio
    async def test_get_hashtag_performance_unknown_platform(self):
        with pytest.raises(ValueError, match="Unknown platform"):
            await self.server.get_hashtag_performance(
                hashtag="#test", platform="tiktok"
            )


# --- Helper Function Tests ---


class TestHelpers:
    @pytest.fixture(autouse=True)
    def _setup_server(self):
        import server
        self.server = server

    def test_query_hash_is_deterministic(self):
        h1 = self.server._query_hash("test")
        h2 = self.server._query_hash("test")
        assert h1 == h2
        assert len(h1) == 16

    def test_query_hash_different_inputs(self):
        h1 = self.server._query_hash("foo")
        h2 = self.server._query_hash("bar")
        assert h1 != h2

    def test_resolve_platforms_none_returns_all(self):
        result = self.server._resolve_platforms(None)
        assert set(result) == {"linkedin", "reddit", "twitter"}

    def test_resolve_platforms_specific(self):
        result = self.server._resolve_platforms(["LinkedIn", "Twitter"])
        assert result == ["linkedin", "twitter"]

    def test_resolve_platforms_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown platform"):
            self.server._resolve_platforms(["tiktok"])
