"""Platform adapter registry for mcp-social-discover."""

from platforms.base import DiscoveryAdapter
from platforms.linkedin import LinkedInDiscoveryAdapter
from platforms.twitter import TwitterDiscoveryAdapter
from platforms.reddit import RedditDiscoveryAdapter

PLATFORM_REGISTRY: dict[str, type[DiscoveryAdapter]] = {
    "linkedin": LinkedInDiscoveryAdapter,
    "twitter": TwitterDiscoveryAdapter,
    "reddit": RedditDiscoveryAdapter,
}


def get_adapter(platform: str) -> DiscoveryAdapter:
    """Instantiate and return the discovery adapter for the given platform."""
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
    "DiscoveryAdapter",
    "PLATFORM_REGISTRY",
    "get_adapter",
    "list_available",
]
