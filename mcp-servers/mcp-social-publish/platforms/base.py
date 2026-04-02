"""Abstract base class for social media platform adapters."""

from abc import ABC, abstractmethod


class PlatformAdapter(ABC):
    """Base interface for all social media platform adapters.

    Each platform must implement publish, preview, and content validation.
    Stubs raise NotImplementedError for publish until API credentials are configured.
    """

    @abstractmethod
    async def publish(self, content: str, media_urls: list[str] | None = None) -> dict:
        """Publish content to the platform. Returns result dict with post URL/ID."""
        ...

    @abstractmethod
    async def preview(self, content: str) -> str:
        """Return a formatted preview of how the content will appear on the platform."""
        ...

    @abstractmethod
    def validate_content(self, content: str) -> list[str]:
        """Validate content against platform constraints. Returns list of error strings."""
        ...

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Lowercase platform identifier (e.g. 'linkedin', 'twitter')."""
        ...

    @property
    @abstractmethod
    def max_length(self) -> int:
        """Maximum character count for a single post on this platform."""
        ...
