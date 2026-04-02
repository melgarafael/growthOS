"""Twitter/X platform adapter stub."""

import os

from platforms.base import PlatformAdapter


class TwitterAdapter(PlatformAdapter):

    @property
    def platform_name(self) -> str:
        return "twitter"

    @property
    def max_length(self) -> int:
        return 280

    def validate_content(self, content: str) -> list[str]:
        errors: list[str] = []
        if not content.strip():
            errors.append("Content cannot be empty")
        if len(content) > self.max_length:
            errors.append(f"Content exceeds {self.max_length} characters ({len(content)})")
        return errors

    async def preview(self, content: str) -> str:
        text = content[:self.max_length]
        preview = "┌─ X (Twitter) Post Preview ─────────────┐\n"
        preview += "│ @you\n"
        preview += "│\n"
        for line in text.split("\n"):
            preview += f"│ {line[:60]}\n"
        preview += "│\n"
        preview += "│ 💬 Reply  🔁 Repost  ❤️ Like  📊 Views\n"
        preview += "└────────────────────────────────────────┘\n"
        preview += f"Characters: {len(content)}/{self.max_length}"
        return preview

    async def publish(self, content: str, media_urls: list[str] | None = None) -> dict:
        if not os.environ.get("GROWTHOS_TWITTER_TOKEN"):
            raise NotImplementedError(
                "API credentials not configured. Set GROWTHOS_TWITTER_TOKEN env var."
            )
        raise NotImplementedError("Twitter/X API integration pending.")
