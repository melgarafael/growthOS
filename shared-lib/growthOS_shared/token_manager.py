"""Per-platform rate limiter with sliding window."""

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class RateLimits:
    max_requests: int
    window_seconds: int = 86400  # default: 1 day


class RateLimitExceeded(Exception):
    def __init__(self, platform: str, reset_at: datetime):
        self.platform = platform
        self.reset_at = reset_at
        super().__init__(f"Rate limit exceeded for {platform}. Resets at {reset_at.isoformat()}")


@dataclass
class PlatformStatus:
    platform: str
    remaining: int
    limit: int
    reset_at: datetime


class TokenManager:
    """Manages per-platform rate limits using a sliding window algorithm.

    Each platform tracks request timestamps in a deque. On every consume/query,
    expired timestamps (older than the window) are pruned, giving accurate
    real-time remaining counts without fixed-window boundary bursts.
    """

    def __init__(self) -> None:
        self._platforms: dict[str, RateLimits] = {}
        self._windows: dict[str, deque[datetime]] = {}

    def register_platform(self, platform: str, limits: RateLimits) -> None:
        self._platforms[platform] = limits
        if platform not in self._windows:
            self._windows[platform] = deque()

    def _prune(self, platform: str, now: datetime) -> None:
        limits = self._platforms[platform]
        cutoff = now - timedelta(seconds=limits.window_seconds)
        window = self._windows[platform]
        while window and window[0] <= cutoff:
            window.popleft()

    def _ensure_registered(self, platform: str) -> None:
        if platform not in self._platforms:
            raise ValueError(f"Platform '{platform}' not registered. Call register_platform first.")

    def consume(self, platform: str, tokens: int = 1) -> bool:
        """Consume tokens from the platform's rate limit budget.

        Returns True on success. Raises RateLimitExceeded if budget is exhausted.
        """
        self._ensure_registered(platform)
        now = datetime.now(timezone.utc)
        self._prune(platform, now)

        limits = self._platforms[platform]
        window = self._windows[platform]

        if len(window) + tokens > limits.max_requests:
            reset_at = self.reset_at(platform)
            raise RateLimitExceeded(platform, reset_at)

        for _ in range(tokens):
            window.append(now)
        return True

    def remaining(self, platform: str) -> int:
        self._ensure_registered(platform)
        now = datetime.now(timezone.utc)
        self._prune(platform, now)
        limits = self._platforms[platform]
        return limits.max_requests - len(self._windows[platform])

    def reset_at(self, platform: str) -> datetime:
        """Return when the oldest request in the window expires."""
        self._ensure_registered(platform)
        now = datetime.now(timezone.utc)
        self._prune(platform, now)
        window = self._windows[platform]
        if not window:
            return now
        limits = self._platforms[platform]
        return window[0] + timedelta(seconds=limits.window_seconds)

    def get_status(self) -> dict[str, PlatformStatus]:
        result: dict[str, PlatformStatus] = {}
        for platform, limits in self._platforms.items():
            result[platform] = PlatformStatus(
                platform=platform,
                remaining=self.remaining(platform),
                limit=limits.max_requests,
                reset_at=self.reset_at(platform),
            )
        return result
