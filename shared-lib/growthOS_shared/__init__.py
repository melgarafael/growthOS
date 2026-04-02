"""GrowthOS shared library — brand voice models, content types, and utilities."""

__version__ = "1.0.0"

from growthOS_shared.token_manager import (
    TokenManager,
    RateLimits,
    RateLimitExceeded,
    PlatformStatus,
)
from growthOS_shared.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
    CircuitOpenError,
)
from growthOS_shared.audit_logger import AuditLogger, AuditEntry
from growthOS_shared.config import (
    BrandVoiceConfig,
    load_brand_voice,
)
from growthOS_shared.autonomy import (
    AutonomyManager,
    AutonomyLevel,
    ActionType,
    KillSwitchActiveError,
)
from growthOS_shared.html_generator import (
    generate_landing_page,
    list_available_styles,
)
from growthOS_shared.carousel_generator import (
    CarouselOutput,
    SlideContent,
    generate_carousel,
    list_carousel_styles,
)
from growthOS_shared.intent_router import (
    Intent,
    RouteResult,
    SubcommandResult,
    check_first_run,
    classify_intent,
    parse_subcommand,
    route,
)
from growthOS_shared.scheduler import (
    CalendarEntry,
    ContentStatus,
    ScheduleConfig,
    ScheduleDefinition,
    ScheduledPublisher,
    PublishResult,
    RetryConfig,
    load_schedule_config,
    prepare_cron_jobs,
    retry_with_backoff,
)

__all__ = [
    "TokenManager",
    "RateLimits",
    "RateLimitExceeded",
    "PlatformStatus",
    "CircuitBreaker",
    "CircuitState",
    "CircuitOpenError",
    "AuditLogger",
    "AuditEntry",
    "BrandVoiceConfig",
    "load_brand_voice",
    "AutonomyManager",
    "AutonomyLevel",
    "ActionType",
    "KillSwitchActiveError",
    "CalendarEntry",
    "ContentStatus",
    "ScheduleConfig",
    "ScheduleDefinition",
    "ScheduledPublisher",
    "PublishResult",
    "RetryConfig",
    "load_schedule_config",
    "prepare_cron_jobs",
    "retry_with_backoff",
    "generate_landing_page",
    "list_available_styles",
    "CarouselOutput",
    "SlideContent",
    "generate_carousel",
    "list_carousel_styles",
    "Intent",
    "RouteResult",
    "SubcommandResult",
    "check_first_run",
    "classify_intent",
    "parse_subcommand",
    "route",
]
