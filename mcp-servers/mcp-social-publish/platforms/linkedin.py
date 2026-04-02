"""LinkedIn platform adapter stub."""

import os

from platforms.base import PlatformAdapter


class LinkedInAdapter(PlatformAdapter):

    @property
    def platform_name(self) -> str:
        return "linkedin"

    @property
    def max_length(self) -> int:
        return 3000

    def validate_content(self, content: str) -> list[str]:
        errors: list[str] = []
        if not content.strip():
            errors.append("Content cannot be empty")
        if len(content) > self.max_length:
            errors.append(f"Content exceeds {self.max_length} characters ({len(content)})")
        return errors

    async def preview(self, content: str) -> str:
        lines = content.strip().split("\n")
        header = lines[0] if lines else ""
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

        preview = "┌─ LinkedIn Post Preview ────────────────┐\n"
        preview += f"│ {header[:60]}\n"
        if body:
            for line in body.split("\n")[:5]:
                preview += f"│ {line[:60]}\n"
            if len(body.split("\n")) > 5:
                preview += "│ ... (truncated)\n"
        preview += "│\n"
        preview += "│ 👍 Like  💬 Comment  🔁 Repost  📤 Send\n"
        preview += "└────────────────────────────────────────┘\n"
        preview += f"Characters: {len(content)}/{self.max_length}"
        return preview

    async def publish(self, content: str, media_urls: list[str] | None = None) -> dict:
        if not os.environ.get("GROWTHOS_LINKEDIN_TOKEN"):
            raise NotImplementedError(
                "API credentials not configured. Set GROWTHOS_LINKEDIN_TOKEN env var."
            )
        raise NotImplementedError("LinkedIn API integration pending.")
