"""GrowthOS MCP Social Publish Server.

Multi-platform social media publishing via MCP tools.
Integrates with shared-lib for rate limiting, circuit breaking, and audit logging.
"""

import hashlib
import sys
from pathlib import Path

from fastmcp import FastMCP

# Add shared-lib to path for cross-package imports
_shared_lib = str(Path(__file__).resolve().parent.parent.parent / "shared-lib")
sys.path.insert(0, _shared_lib)

# Add current directory for platform imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from growthOS_shared import (  # noqa: E402
    AuditLogger,
    CircuitBreaker,
    RateLimits,
    TokenManager,
)
from platforms import get_adapter, list_available  # noqa: E402

# --- Initialization ---

mcp = FastMCP("growthos-social-publish")

token_manager = TokenManager()
audit_logger = AuditLogger()

# Per-platform circuit breakers
_circuit_breakers: dict[str, CircuitBreaker] = {}

# Default rate limits per platform (requests per day)
_DEFAULT_RATE_LIMITS: dict[str, int] = {
    "linkedin": 100,
    "twitter": 300,
    "reddit": 100,
    "github": 500,
    "threads": 200,
}

# Register all platforms with rate limits
for _platform_name in list_available():
    limit = _DEFAULT_RATE_LIMITS.get(_platform_name, 100)
    token_manager.register_platform(_platform_name, RateLimits(max_requests=limit))
    _circuit_breakers[_platform_name] = CircuitBreaker(
        failure_threshold=3, recovery_timeout=300
    )


def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


# --- MCP Tools ---


@mcp.tool()
async def publish_post(
    platform: str,
    content: str,
    media_urls: list[str] | None = None,
    dry_run: bool = True,
) -> dict:
    """Publish a post to a social media platform.

    Args:
        platform: Target platform (linkedin, twitter, reddit, github, threads)
        content: Post content text
        media_urls: Optional list of media URLs to attach
        dry_run: If True (default), simulates publishing without actually posting
    """
    adapter = get_adapter(platform)
    name = adapter.platform_name

    # Validate content
    errors = adapter.validate_content(content)
    if errors:
        return {"status": "error", "platform": name, "errors": errors}

    # Check rate limits
    status = token_manager.get_status().get(name)
    if status and status.remaining <= 0:
        audit_logger.log_action(
            action="publish_rejected",
            platform=name,
            content_hash=_content_hash(content),
            status="rate_limited",
            metadata={"dry_run": dry_run},
        )
        return {
            "status": "error",
            "platform": name,
            "errors": [f"Rate limit exceeded. Resets at {status.reset_at.isoformat()}"],
        }

    if dry_run:
        preview = await adapter.preview(content)
        audit_logger.log_action(
            action="publish_dry_run",
            platform=name,
            content_hash=_content_hash(content),
            status="simulated",
            metadata={"content_length": len(content), "media_count": len(media_urls or [])},
        )
        return {
            "status": "dry_run",
            "platform": name,
            "preview": preview,
            "message": "Dry run — content validated but NOT published. Set dry_run=False to publish.",
        }

    # Real publish with circuit breaker
    cb = _circuit_breakers[name]
    try:
        result = await cb.call(adapter.publish, content, media_urls)
        token_manager.consume(name)
        audit_logger.log_action(
            action="publish",
            platform=name,
            content_hash=_content_hash(content),
            status="success",
            metadata={"result": result},
        )
        return {"status": "success", "platform": name, "result": result}
    except NotImplementedError as e:
        audit_logger.log_action(
            action="publish_failed",
            platform=name,
            content_hash=_content_hash(content),
            status="not_implemented",
            metadata={"error": str(e)},
        )
        return {"status": "error", "platform": name, "errors": [str(e)]}
    except Exception as e:
        audit_logger.log_action(
            action="publish_failed",
            platform=name,
            content_hash=_content_hash(content),
            status="error",
            metadata={"error": str(e)},
        )
        return {"status": "error", "platform": name, "errors": [str(e)]}


@mcp.tool()
async def preview_post(platform: str, content: str) -> dict:
    """Preview how a post will look on a platform without publishing.

    Args:
        platform: Target platform (linkedin, twitter, reddit, github, threads)
        content: Post content text
    """
    adapter = get_adapter(platform)
    name = adapter.platform_name

    errors = adapter.validate_content(content)
    if errors:
        return {"status": "error", "platform": name, "errors": errors}

    preview = await adapter.preview(content)
    return {
        "status": "ok",
        "platform": name,
        "preview": preview,
        "content_length": len(content),
        "max_length": adapter.max_length,
        "remaining_chars": adapter.max_length - len(content),
    }


@mcp.tool()
async def list_platforms() -> dict:
    """List all configured platforms and their status."""
    platforms = {}
    for name in list_available():
        adapter = get_adapter(name)
        status = token_manager.get_status().get(name)
        cb = _circuit_breakers.get(name)

        platforms[name] = {
            "max_length": adapter.max_length,
            "rate_limit": {
                "remaining": status.remaining if status else "unknown",
                "limit": status.limit if status else "unknown",
                "reset_at": status.reset_at.isoformat() if status else "unknown",
            },
            "circuit_breaker": cb.state.value if cb else "unknown",
        }

    return {"status": "ok", "platforms": platforms, "count": len(platforms)}


@mcp.tool()
async def get_rate_limits() -> dict:
    """Get current rate limit status for all platforms."""
    limits = {}
    for name, status in token_manager.get_status().items():
        limits[name] = {
            "remaining": status.remaining,
            "limit": status.limit,
            "reset_at": status.reset_at.isoformat(),
            "usage_percent": round(
                (1 - status.remaining / status.limit) * 100, 1
            )
            if status.limit > 0
            else 0,
        }
    return {"status": "ok", "rate_limits": limits}


if __name__ == "__main__":
    mcp.run()
