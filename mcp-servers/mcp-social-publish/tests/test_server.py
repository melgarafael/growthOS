"""Tests for mcp-social-publish server tools."""

import sys
from pathlib import Path

import pytest

# Setup paths so imports work from test context
_server_dir = str(Path(__file__).resolve().parent.parent)
_shared_lib = str(Path(__file__).resolve().parent.parent.parent.parent / "shared-lib")
sys.path.insert(0, _server_dir)
sys.path.insert(0, _shared_lib)

from platforms import get_adapter, list_available  # noqa: E402
from platforms.base import PlatformAdapter  # noqa: E402
from platforms.linkedin import LinkedInAdapter  # noqa: E402
from platforms.twitter import TwitterAdapter  # noqa: E402
from platforms.reddit import RedditAdapter  # noqa: E402
from platforms.github import GitHubAdapter  # noqa: E402
from platforms.threads import ThreadsAdapter  # noqa: E402


# --- Platform Registry Tests ---


class TestPlatformRegistry:
    def test_list_available_returns_all_platforms(self):
        platforms = list_available()
        assert set(platforms) == {"github", "linkedin", "reddit", "threads", "twitter"}

    def test_get_adapter_returns_correct_type(self):
        assert isinstance(get_adapter("linkedin"), LinkedInAdapter)
        assert isinstance(get_adapter("twitter"), TwitterAdapter)
        assert isinstance(get_adapter("reddit"), RedditAdapter)
        assert isinstance(get_adapter("github"), GitHubAdapter)
        assert isinstance(get_adapter("threads"), ThreadsAdapter)

    def test_get_adapter_case_insensitive(self):
        assert isinstance(get_adapter("LinkedIn"), LinkedInAdapter)
        assert isinstance(get_adapter("TWITTER"), TwitterAdapter)

    def test_get_adapter_unknown_platform_raises(self):
        with pytest.raises(ValueError, match="Unknown platform"):
            get_adapter("tiktok")


# --- Platform Adapter Tests ---


class TestPlatformAdapters:
    ADAPTERS = [
        LinkedInAdapter,
        TwitterAdapter,
        RedditAdapter,
        GitHubAdapter,
        ThreadsAdapter,
    ]

    @pytest.mark.parametrize("cls", ADAPTERS)
    def test_adapter_is_platform_adapter(self, cls):
        assert issubclass(cls, PlatformAdapter)

    @pytest.mark.parametrize("cls", ADAPTERS)
    def test_platform_name_is_string(self, cls):
        adapter = cls()
        assert isinstance(adapter.platform_name, str)
        assert len(adapter.platform_name) > 0

    @pytest.mark.parametrize("cls", ADAPTERS)
    def test_max_length_is_positive(self, cls):
        adapter = cls()
        assert adapter.max_length > 0

    @pytest.mark.parametrize("cls", ADAPTERS)
    def test_validate_empty_content(self, cls):
        adapter = cls()
        errors = adapter.validate_content("")
        assert any("empty" in e.lower() for e in errors)

    @pytest.mark.parametrize("cls", ADAPTERS)
    def test_validate_content_too_long(self, cls):
        adapter = cls()
        long_content = "x" * (adapter.max_length + 1)
        errors = adapter.validate_content(long_content)
        assert any("exceeds" in e.lower() for e in errors)

    @pytest.mark.parametrize("cls", ADAPTERS)
    def test_validate_valid_content(self, cls):
        adapter = cls()
        errors = adapter.validate_content("Hello world!")
        assert errors == []


# --- Preview Tests ---


class TestPreviews:
    @pytest.mark.asyncio
    async def test_linkedin_preview_format(self):
        adapter = LinkedInAdapter()
        preview = await adapter.preview("My LinkedIn Post\n\nWith body content")
        assert "LinkedIn" in preview
        assert "My LinkedIn Post" in preview
        assert "Characters:" in preview

    @pytest.mark.asyncio
    async def test_twitter_preview_format(self):
        adapter = TwitterAdapter()
        preview = await adapter.preview("Short tweet!")
        assert "Twitter" in preview or "X" in preview
        assert "Short tweet!" in preview
        assert "Characters:" in preview

    @pytest.mark.asyncio
    async def test_reddit_preview_format(self):
        adapter = RedditAdapter()
        preview = await adapter.preview("Post Title\n\nPost body here")
        assert "Reddit" in preview
        assert "Post Title" in preview

    @pytest.mark.asyncio
    async def test_github_preview_format(self):
        adapter = GitHubAdapter()
        preview = await adapter.preview("Discussion Title\n\nBody text")
        assert "GitHub" in preview
        assert "Discussion Title" in preview

    @pytest.mark.asyncio
    async def test_threads_preview_format(self):
        adapter = ThreadsAdapter()
        preview = await adapter.preview("Threads post content")
        assert "Threads" in preview
        assert "Threads post content" in preview


# --- Publish Stub Tests ---


class TestPublishStubs:
    @pytest.mark.asyncio
    async def test_linkedin_publish_raises_not_implemented(self):
        adapter = LinkedInAdapter()
        with pytest.raises(NotImplementedError, match="GROWTHOS_LINKEDIN_TOKEN"):
            await adapter.publish("test")

    @pytest.mark.asyncio
    async def test_twitter_publish_raises_not_implemented(self):
        adapter = TwitterAdapter()
        with pytest.raises(NotImplementedError, match="GROWTHOS_TWITTER_TOKEN"):
            await adapter.publish("test")

    @pytest.mark.asyncio
    async def test_reddit_publish_raises_not_implemented(self):
        adapter = RedditAdapter()
        with pytest.raises(NotImplementedError, match="GROWTHOS_REDDIT_TOKEN"):
            await adapter.publish("test")

    @pytest.mark.asyncio
    async def test_github_publish_raises_not_implemented(self):
        adapter = GitHubAdapter()
        with pytest.raises(NotImplementedError, match="GROWTHOS_GITHUB_TOKEN"):
            await adapter.publish("test")

    @pytest.mark.asyncio
    async def test_threads_publish_raises_not_implemented(self):
        adapter = ThreadsAdapter()
        with pytest.raises(NotImplementedError, match="GROWTHOS_THREADS_TOKEN"):
            await adapter.publish("test")


# --- Server Tool Integration Tests ---


class TestServerTools:
    """Test the MCP server tools via direct import."""

    @pytest.fixture(autouse=True)
    def _setup_server(self):
        """Import server module for tool testing."""
        import server

        self.server = server

    @pytest.mark.asyncio
    async def test_publish_post_dry_run(self):
        result = await self.server.publish_post(
            platform="linkedin",
            content="Test post for LinkedIn",
            dry_run=True,
        )
        assert result["status"] == "dry_run"
        assert result["platform"] == "linkedin"
        assert "preview" in result

    @pytest.mark.asyncio
    async def test_publish_post_validation_error(self):
        result = await self.server.publish_post(
            platform="twitter",
            content="",
            dry_run=True,
        )
        assert result["status"] == "error"
        assert len(result["errors"]) > 0

    @pytest.mark.asyncio
    async def test_publish_post_content_too_long(self):
        result = await self.server.publish_post(
            platform="twitter",
            content="x" * 300,
            dry_run=True,
        )
        assert result["status"] == "error"
        assert any("exceeds" in e.lower() for e in result["errors"])

    @pytest.mark.asyncio
    async def test_publish_post_real_raises_not_implemented(self):
        result = await self.server.publish_post(
            platform="linkedin",
            content="Test post",
            dry_run=False,
        )
        assert result["status"] == "error"
        assert any("credentials" in e.lower() or "not configured" in e.lower() for e in result["errors"])

    @pytest.mark.asyncio
    async def test_preview_post(self):
        result = await self.server.preview_post(
            platform="linkedin",
            content="My awesome post",
        )
        assert result["status"] == "ok"
        assert result["platform"] == "linkedin"
        assert "preview" in result
        assert result["content_length"] == len("My awesome post")
        assert result["remaining_chars"] > 0

    @pytest.mark.asyncio
    async def test_preview_post_validation_error(self):
        result = await self.server.preview_post(platform="twitter", content="")
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_list_platforms(self):
        result = await self.server.list_platforms()
        assert result["status"] == "ok"
        assert result["count"] == 5
        assert "linkedin" in result["platforms"]
        assert "twitter" in result["platforms"]
        for name, info in result["platforms"].items():
            assert "max_length" in info
            assert "rate_limit" in info
            assert "circuit_breaker" in info

    @pytest.mark.asyncio
    async def test_get_rate_limits(self):
        result = await self.server.get_rate_limits()
        assert result["status"] == "ok"
        assert "rate_limits" in result
        for name, limits in result["rate_limits"].items():
            assert "remaining" in limits
            assert "limit" in limits
            assert "reset_at" in limits
            assert "usage_percent" in limits
            assert limits["usage_percent"] >= 0

    @pytest.mark.asyncio
    async def test_publish_unknown_platform(self):
        with pytest.raises(ValueError, match="Unknown platform"):
            await self.server.publish_post(
                platform="tiktok",
                content="test",
                dry_run=True,
            )
