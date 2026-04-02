"""Reddit platform adapter stub."""

import os

from platforms.base import PlatformAdapter


class RedditAdapter(PlatformAdapter):

    @property
    def platform_name(self) -> str:
        return "reddit"

    @property
    def max_length(self) -> int:
        return 40000

    def validate_content(self, content: str) -> list[str]:
        errors: list[str] = []
        if not content.strip():
            errors.append("Content cannot be empty")
        if len(content) > self.max_length:
            errors.append(f"Content exceeds {self.max_length} characters ({len(content)})")
        return errors

    async def preview(self, content: str) -> str:
        lines = content.strip().split("\n")
        title = lines[0] if lines else "Untitled"
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

        preview = "┌─ Reddit Post Preview ─────────────────┐\n"
        preview += "│ r/subreddit\n"
        preview += "│\n"
        preview += f"│ ▲  {title[:55]}\n"
        preview += "│ ▼\n"
        if body:
            for line in body.split("\n")[:6]:
                preview += f"│    {line[:55]}\n"
            if len(body.split("\n")) > 6:
                preview += "│    ... (truncated)\n"
        preview += "│\n"
        preview += "│ 💬 Comments  🔗 Share  ⭐ Save\n"
        preview += "└───────────────────────────────────────┘\n"
        preview += f"Characters: {len(content)}/{self.max_length}"
        return preview

    async def publish(self, content: str, media_urls: list[str] | None = None) -> dict:
        if not os.environ.get("GROWTHOS_REDDIT_TOKEN"):
            raise NotImplementedError(
                "API credentials not configured. Set GROWTHOS_REDDIT_TOKEN env var."
            )
        raise NotImplementedError("Reddit API integration pending.")
