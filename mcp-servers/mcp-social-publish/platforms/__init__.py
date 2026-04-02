"""Platform adapter registry for mcp-social-publish."""

from platforms.base import PlatformAdapter
from platforms.linkedin import LinkedInAdapter
from platforms.twitter import TwitterAdapter
from platforms.reddit import RedditAdapter
from platforms.github import GitHubAdapter
from platforms.threads import ThreadsAdapter

PLATFORM_REGISTRY: dict[str, type[PlatformAdapter]] = {
    "linkedin": LinkedInAdapter,
    "twitter": TwitterAdapter,
    "reddit": RedditAdapter,
    "github": GitHubAdapter,
    "threads": ThreadsAdapter,
}


def get_adapter(platform: str) -> PlatformAdapter:
    """Instantiate and return the adapter for the given platform name."""
    cls = PLATFORM_REGISTRY.get(platform.lower())
    if cls is None:
        raise ValueError(
            f"Unknown platform '{platform}'. "
            f"Available: {', '.join(sorted(PLATFORM_REGISTRY.keys()))}"
        )
    return cls()


def list_available() -> list[str]:
    """Return sorted list of registered platform names."""
    return sorted(PLATFORM_REGISTRY.keys())


__all__ = [
    "PlatformAdapter",
    "PLATFORM_REGISTRY",
    "get_adapter",
    "list_available",
]
