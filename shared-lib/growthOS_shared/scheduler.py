"""Cron scheduler and content calendar automation for GrowthOS.

Provides:
- Schedule definitions in YAML format (cron expressions)
- Content calendar frontmatter schema for Obsidian Dataview
- Scheduled publish orchestration (triggers Social Publisher agent)
- Autonomy-aware: respects manual/semi/auto mode
- Retry with exponential backoff on transient errors

Uses Claude Code CronCreate API pattern for portability.
"""

import asyncio
import logging
import random
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

import yaml
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Content Calendar Schema
# ---------------------------------------------------------------------------

class ContentStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"


class CalendarEntry(BaseModel):
    """Obsidian-compatible frontmatter schema for content calendar items."""

    title: str
    scheduled_date: str = Field(description="ISO date: YYYY-MM-DD or YYYY-MM-DDTHH:MM")
    platform: str
    content_type: str = "social"
    status: ContentStatus = ContentStatus.DRAFT
    author: str = ""
    tags: list[str] = Field(default_factory=list)
    retry_count: int = 0
    last_error: str = ""

    @field_validator("platform")
    @classmethod
    def platform_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("platform is required")
        return v.lower()

    def to_frontmatter(self) -> str:
        """Render as YAML frontmatter block for Obsidian."""
        data = {
            "title": self.title,
            "scheduled_date": self.scheduled_date,
            "platform": self.platform,
            "content_type": self.content_type,
            "status": self.status.value,
            "author": self.author,
            "tags": self.tags,
        }
        lines = yaml.dump(data, default_flow_style=False, sort_keys=False).strip()
        return f"---\n{lines}\n---"

    @classmethod
    def from_frontmatter(cls, text: str) -> "CalendarEntry":
        """Parse from Obsidian frontmatter (between --- delimiters)."""
        parts = text.split("---")
        if len(parts) < 3:
            raise ValueError("Invalid frontmatter: missing --- delimiters")
        raw = yaml.safe_load(parts[1])
        if not isinstance(raw, dict):
            raise ValueError("Invalid frontmatter: expected YAML mapping")
        return cls(**raw)


# ---------------------------------------------------------------------------
# Schedule Definitions
# ---------------------------------------------------------------------------

class ScheduleAction(str, Enum):
    """Built-in actions a schedule can trigger."""

    PUBLISH = "publish"
    REVIEW_CALENDAR = "review_calendar"
    STRATEGY_REVIEW = "strategy_review"
    CONTENT_CHECK = "content_check"


class ScheduleDefinition(BaseModel):
    """A single cron schedule entry from YAML config."""

    name: str
    cron: str = Field(description="5-field cron expression: M H DoM Mon DoW")
    action: str
    agent: str = "cmo"
    enabled: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("cron")
    @classmethod
    def validate_cron(cls, v: str) -> str:
        parts = v.strip().split()
        if len(parts) != 5:
            raise ValueError(
                f"cron must have exactly 5 fields (M H DoM Mon DoW), got {len(parts)}: '{v}'"
            )
        return v.strip()


class ScheduleConfig(BaseModel):
    """Root model for schedule YAML files."""

    schedules: list[ScheduleDefinition] = Field(default_factory=list)

    def get_enabled(self) -> list[ScheduleDefinition]:
        return [s for s in self.schedules if s.enabled]

    def get_by_name(self, name: str) -> Optional[ScheduleDefinition]:
        for s in self.schedules:
            if s.name == name:
                return s
        return None


def load_schedule_config(path: str | Path) -> ScheduleConfig:
    """Load schedule definitions from a YAML file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Schedule config not found: {p}")
    raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid schedule config: expected YAML mapping in {p}")
    return ScheduleConfig(**raw)


# ---------------------------------------------------------------------------
# Retry with Exponential Backoff
# ---------------------------------------------------------------------------

TRANSIENT_EXCEPTIONS = (
    TimeoutError,
    ConnectionError,
    OSError,
)


@dataclass
class RetryConfig:
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    jitter: bool = True
    transient_exceptions: tuple = field(default_factory=lambda: TRANSIENT_EXCEPTIONS)


async def retry_with_backoff(
    func: Callable,
    *args: Any,
    config: Optional[RetryConfig] = None,
    **kwargs: Any,
) -> Any:
    """Execute an async function with exponential backoff on transient errors.

    Returns the function result on success.
    Raises the last exception after all retries are exhausted.
    """
    cfg = config or RetryConfig()
    last_error: Optional[Exception] = None

    for attempt in range(cfg.max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except cfg.transient_exceptions as exc:
            last_error = exc
            if attempt >= cfg.max_retries:
                logger.error(
                    "All %d retries exhausted for %s: %s",
                    cfg.max_retries, func.__name__, exc,
                )
                raise
            delay = min(cfg.base_delay * (2 ** attempt), cfg.max_delay)
            if cfg.jitter:
                delay *= 0.5 + random.random()
            logger.warning(
                "Transient error (attempt %d/%d) in %s: %s — retrying in %.1fs",
                attempt + 1, cfg.max_retries, func.__name__, exc, delay,
            )
            await asyncio.sleep(delay)

    raise last_error  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Publish Orchestration
# ---------------------------------------------------------------------------

@dataclass
class PublishResult:
    """Outcome of a scheduled publish attempt."""

    entry: CalendarEntry
    success: bool
    action_taken: str  # "published" | "draft_created" | "notification_sent" | "failed"
    error: str = ""
    attempts: int = 1


PublishHandler = Callable[[CalendarEntry], Any]


class ScheduledPublisher:
    """Orchestrates content publishing based on autonomy level.

    - auto: publishes directly via the handler
    - semi: creates draft/notification instead of publishing
    - manual: creates notification only, no draft
    """

    def __init__(
        self,
        autonomy_level: str = "semi",
        publish_handler: Optional[PublishHandler] = None,
        draft_handler: Optional[PublishHandler] = None,
        notify_handler: Optional[PublishHandler] = None,
        retry_config: Optional[RetryConfig] = None,
    ) -> None:
        if autonomy_level not in {"manual", "semi", "auto"}:
            raise ValueError(f"Invalid autonomy level: {autonomy_level}")
        self.autonomy_level = autonomy_level
        self.publish_handler = publish_handler
        self.draft_handler = draft_handler
        self.notify_handler = notify_handler
        self.retry_config = retry_config or RetryConfig()

    async def execute(self, entry: CalendarEntry) -> PublishResult:
        """Execute a scheduled publish based on the autonomy level."""
        if self.autonomy_level == "auto":
            return await self._publish(entry)
        elif self.autonomy_level == "semi":
            return await self._create_draft(entry)
        else:
            return await self._notify(entry)

    async def _publish(self, entry: CalendarEntry) -> PublishResult:
        if not self.publish_handler:
            return PublishResult(
                entry=entry, success=False,
                action_taken="failed", error="No publish handler configured",
            )
        try:
            await retry_with_backoff(
                self.publish_handler, entry, config=self.retry_config,
            )
            entry.status = ContentStatus.PUBLISHED
            return PublishResult(entry=entry, success=True, action_taken="published")
        except Exception as exc:
            entry.status = ContentStatus.FAILED
            entry.retry_count = self.retry_config.max_retries
            entry.last_error = str(exc)
            return PublishResult(
                entry=entry, success=False, action_taken="failed",
                error=str(exc), attempts=self.retry_config.max_retries + 1,
            )

    async def _create_draft(self, entry: CalendarEntry) -> PublishResult:
        if self.draft_handler:
            try:
                await retry_with_backoff(
                    self.draft_handler, entry, config=self.retry_config,
                )
            except Exception as exc:
                return PublishResult(
                    entry=entry, success=False, action_taken="failed",
                    error=f"Draft creation failed: {exc}",
                )
        entry.status = ContentStatus.DRAFT
        return PublishResult(entry=entry, success=True, action_taken="draft_created")

    async def _notify(self, entry: CalendarEntry) -> PublishResult:
        if self.notify_handler:
            try:
                await retry_with_backoff(
                    self.notify_handler, entry, config=self.retry_config,
                )
            except Exception as exc:
                return PublishResult(
                    entry=entry, success=False, action_taken="failed",
                    error=f"Notification failed: {exc}",
                )
        return PublishResult(entry=entry, success=True, action_taken="notification_sent")


# ---------------------------------------------------------------------------
# CronCreate Integration
# ---------------------------------------------------------------------------

@dataclass
class RegisteredJob:
    """Represents a schedule registered via CronCreate."""

    name: str
    cron: str
    prompt: str
    job_id: Optional[str] = None


def build_cron_prompt(schedule: ScheduleDefinition) -> str:
    """Build the prompt string that CronCreate will enqueue."""
    action = schedule.action
    agent = schedule.agent
    meta = schedule.metadata

    prompt = f"GrowthOS scheduler: execute '{action}' via @{agent}"
    if meta:
        details = ", ".join(f"{k}={v}" for k, v in meta.items())
        prompt += f" [{details}]"
    return prompt


def prepare_cron_jobs(config: ScheduleConfig) -> list[RegisteredJob]:
    """Convert enabled schedule definitions into CronCreate-ready jobs.

    Returns a list of RegisteredJob instances ready for registration.
    The caller should pass each job's cron and prompt to CronCreate.
    """
    jobs: list[RegisteredJob] = []
    for sched in config.get_enabled():
        jobs.append(RegisteredJob(
            name=sched.name,
            cron=sched.cron,
            prompt=build_cron_prompt(sched),
        ))
    return jobs
