"""Threads (Meta) platform adapter stub."""

import os

from platforms.base import PlatformAdapter


class ThreadsAdapter(PlatformAdapter):

    @property
    def platform_name(self) -> str:
        return "threads"

    @property
    def max_length(self) -> int:
        return 500

    def validate_content(self, content: str) -> list[str]:
        errors: list[str] = []
        if not content.strip():
            errors.append("Content cannot be empty")
        if len(content) > self.max_length:
            errors.append(f"Content exceeds {self.max_length} characters ({len(content)})")
        return errors

    async def preview(self, content: str) -> str:
        text = content[:self.max_length]
        preview = "┌─ Threads Post Preview ────────────────┐\n"
        preview += "│ @you\n"
        preview += "│\n"
        for line in text.split("\n")[:5]:
            preview += f"│ {line[:58]}\n"
        if len(text.split("\n")) > 5:
            preview += "│ ... (truncated)\n"
        preview += "│\n"
        preview += "│ ❤️ Like  💬 Reply  🔁 Repost  📤 Share\n"
        preview += "└───────────────────────────────────────┘\n"
        preview += f"Characters: {len(content)}/{self.max_length}"
        return preview

    async def publish(self, content: str, media_urls: list[str] | None = None) -> dict:
        if not os.environ.get("GROWTHOS_THREADS_TOKEN"):
            raise NotImplementedError(
                "API credentials not configured. Set GROWTHOS_THREADS_TOKEN env var."
            )
        raise NotImplementedError("Threads API integration pending.")
