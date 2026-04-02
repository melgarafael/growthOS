"""Tests for TokenManager — sliding window rate limiter."""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from growthOS_shared.token_manager import (
    PlatformStatus,
    RateLimitExceeded,
    RateLimits,
    TokenManager,
)


@pytest.fixture
def manager() -> TokenManager:
    tm = TokenManager()
    tm.register_platform("twitter", RateLimits(max_requests=5, window_seconds=60))
    tm.register_platform("linkedin", RateLimits(max_requests=3, window_seconds=120))
    return tm


class TestRegistration:
    def test_register_platform(self, manager: TokenManager) -> None:
        assert manager.remaining("twitter") == 5
        assert manager.remaining("linkedin") == 3

    def test_unregistered_platform_raises(self) -> None:
        tm = TokenManager()
        with pytest.raises(ValueError, match="not registered"):
            tm.consume("unknown")

    def test_re_register_preserves_window(self, manager: TokenManager) -> None:
        manager.consume("twitter")
        assert manager.remaining("twitter") == 4
        # Re-register with higher limit — existing timestamps should remain
        manager.register_platform("twitter", RateLimits(max_requests=10, window_seconds=60))
        assert manager.remaining("twitter") == 9


class TestConsume:
    def test_single_consume(self, manager: TokenManager) -> None:
        assert manager.consume("twitter") is True
        assert manager.remaining("twitter") == 4

    def test_multi_token_consume(self, manager: TokenManager) -> None:
        manager.consume("twitter", tokens=3)
        assert manager.remaining("twitter") == 2

    def test_consume_exact_limit(self, manager: TokenManager) -> None:
        manager.consume("twitter", tokens=5)
        assert manager.remaining("twitter") == 0

    def test_exceeds_limit_raises(self, manager: TokenManager) -> None:
        manager.consume("twitter", tokens=5)
        with pytest.raises(RateLimitExceeded) as exc_info:
            manager.consume("twitter")
        assert exc_info.value.platform == "twitter"
        assert isinstance(exc_info.value.reset_at, datetime)

    def test_multi_token_exceeds_limit(self, manager: TokenManager) -> None:
        manager.consume("twitter", tokens=3)
        with pytest.raises(RateLimitExceeded):
            manager.consume("twitter", tokens=3)  # 3+3=6 > 5


class TestSlidingWindow:
    def test_expired_tokens_are_pruned(self, manager: TokenManager) -> None:
        now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        later = now + timedelta(seconds=61)  # past the 60s window

        with patch("growthOS_shared.token_manager.datetime") as mock_dt:
            mock_dt.now.return_value = now
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            manager.consume("twitter", tokens=5)

        with patch("growthOS_shared.token_manager.datetime") as mock_dt:
            mock_dt.now.return_value = later
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            # All 5 tokens should have expired
            assert manager.remaining("twitter") == 5
            # Should be able to consume again
            manager.consume("twitter", tokens=5)


class TestResetAt:
    def test_reset_at_empty_window(self, manager: TokenManager) -> None:
        reset = manager.reset_at("twitter")
        assert isinstance(reset, datetime)

    def test_reset_at_after_consume(self, manager: TokenManager) -> None:
        manager.consume("twitter")
        reset = manager.reset_at("twitter")
        # reset_at should be ~60s from now
        now = datetime.now(timezone.utc)
        assert reset > now
        assert reset <= now + timedelta(seconds=61)


class TestGetStatus:
    def test_returns_all_platforms(self, manager: TokenManager) -> None:
        status = manager.get_status()
        assert set(status.keys()) == {"twitter", "linkedin"}

    def test_status_values(self, manager: TokenManager) -> None:
        manager.consume("twitter", tokens=2)
        status = manager.get_status()
        tw = status["twitter"]
        assert isinstance(tw, PlatformStatus)
        assert tw.platform == "twitter"
        assert tw.remaining == 3
        assert tw.limit == 5

    def test_empty_manager(self) -> None:
        tm = TokenManager()
        assert tm.get_status() == {}
