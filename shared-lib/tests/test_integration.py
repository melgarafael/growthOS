"""Cross-module integration tests for GrowthOS shared-lib.

Tests verify that modules work correctly together across boundaries,
catching contract mismatches that unit tests miss.
"""

import asyncio
import json
import tempfile
from pathlib import Path

import pytest
import yaml

from growthOS_shared.audit_logger import AuditLogger
from growthOS_shared.autonomy import AutonomyLevel, AutonomyManager
from growthOS_shared.circuit_breaker import CircuitBreaker, CircuitOpenError, CircuitState
from growthOS_shared.config import AutonomyConfig, BrandVoiceConfig, load_brand_voice
from growthOS_shared.scheduler import (
    CalendarEntry,
    ContentStatus,
    RetryConfig,
    ScheduleConfig,
    ScheduledPublisher,
    load_schedule_config,
    prepare_cron_jobs,
)


# ── Fixtures ──────────────────────────────────────────────────────


@pytest.fixture
def brand_voice_path() -> str:
    """Path to the example brand voice config."""
    return str(Path(__file__).parent.parent.parent / "brand-voice.example.yaml")


@pytest.fixture
def tmp_dir(tmp_path: Path) -> Path:
    """Provide a clean temp directory for test artifacts."""
    return tmp_path


@pytest.fixture
def sample_calendar_entry() -> CalendarEntry:
    return CalendarEntry(
        title="Launch day post",
        scheduled_date="2026-04-15T10:00",
        platform="linkedin",
        content_type="social",
        status=ContentStatus.DRAFT,
        author="growth-engineer",
        tags=["launch", "product"],
    )


@pytest.fixture
def schedule_yaml(tmp_dir: Path) -> Path:
    """Create a temporary schedule YAML file."""
    config = {
        "schedules": [
            {
                "name": "daily-publish",
                "cron": "0 9 * * 1-5",
                "action": "publish",
                "agent": "social-publisher",
                "enabled": True,
                "metadata": {"priority": "high"},
            },
            {
                "name": "weekly-review",
                "cron": "0 14 * * 5",
                "action": "review_calendar",
                "agent": "cmo",
                "enabled": True,
            },
            {
                "name": "disabled-job",
                "cron": "0 0 1 * *",
                "action": "strategy_review",
                "agent": "cmo",
                "enabled": False,
            },
        ]
    }
    path = tmp_dir / "schedules.yaml"
    path.write_text(yaml.dump(config), encoding="utf-8")
    return path


# ── Chain 1: Config -> Autonomy ───────────────────────────────────


class TestConfigAutonomyChain:
    """Verify config module feeds autonomy module correctly."""

    def test_load_brand_voice_provides_valid_autonomy_config(self, brand_voice_path: str):
        """Config loads and produces an AutonomyConfig that AutonomyManager accepts."""
        brand_config = load_brand_voice(brand_voice_path)

        assert isinstance(brand_config, BrandVoiceConfig)
        assert isinstance(brand_config.autonomy, AutonomyConfig)

        manager = AutonomyManager(
            config=brand_config.autonomy,
            config_dir=tempfile.mkdtemp(),
        )

        level = manager.get_level()
        assert isinstance(level, AutonomyLevel)
        assert level.value == brand_config.autonomy.level

    def test_all_autonomy_levels_from_config(self, tmp_dir: Path):
        """Each valid autonomy level in config maps to the correct AutonomyLevel enum."""
        for level_str in ("manual", "semi", "auto"):
            config = AutonomyConfig(
                level=level_str,
                require_preview=True,
                dry_run_default=True,
                kill_switch=True,
            )
            manager = AutonomyManager(
                config=config,
                config_dir=str(tmp_dir / level_str),
            )
            assert manager.get_level() == AutonomyLevel(level_str)

    def test_config_dry_run_propagates_to_manager(self, brand_voice_path: str):
        """dry_run_default from config is respected by AutonomyManager."""
        brand_config = load_brand_voice(brand_voice_path)
        manager = AutonomyManager(
            config=brand_config.autonomy,
            config_dir=tempfile.mkdtemp(),
        )
        assert manager.is_dry_run() == brand_config.autonomy.dry_run_default

    def test_config_kill_switch_overrides_level(self, tmp_dir: Path):
        """When kill switch activates, level reverts to MANUAL regardless of config."""
        config = AutonomyConfig(level="auto", dry_run_default=False, kill_switch=True)
        manager = AutonomyManager(config=config, config_dir=str(tmp_dir))

        assert manager.get_level() == AutonomyLevel.AUTO

        manager.activate_kill_switch()
        assert manager.get_level() == AutonomyLevel.MANUAL

        manager.deactivate_kill_switch()
        assert manager.get_level() == AutonomyLevel.AUTO


# ── Chain 2: Autonomy -> Scheduler ────────────────────────────────


class TestAutonomySchedulerChain:
    """Verify ScheduledPublisher respects autonomy levels."""

    @pytest.fixture
    def entry(self) -> CalendarEntry:
        return CalendarEntry(
            title="Test post",
            scheduled_date="2026-04-15",
            platform="twitter",
        )

    def test_auto_mode_publishes(self, entry: CalendarEntry):
        """Auto mode calls publish handler and returns 'published'."""
        published = []

        async def mock_publish(e: CalendarEntry):
            published.append(e.title)

        publisher = ScheduledPublisher(
            autonomy_level="auto",
            publish_handler=mock_publish,
            retry_config=RetryConfig(max_retries=0, base_delay=0),
        )
        result = asyncio.run(publisher.execute(entry))

        assert result.success is True
        assert result.action_taken == "published"
        assert len(published) == 1
        assert entry.status == ContentStatus.PUBLISHED

    def test_semi_mode_creates_draft(self, entry: CalendarEntry):
        """Semi mode calls draft handler and returns 'draft_created'."""
        drafts = []

        async def mock_draft(e: CalendarEntry):
            drafts.append(e.title)

        publisher = ScheduledPublisher(
            autonomy_level="semi",
            draft_handler=mock_draft,
            retry_config=RetryConfig(max_retries=0, base_delay=0),
        )
        result = asyncio.run(publisher.execute(entry))

        assert result.success is True
        assert result.action_taken == "draft_created"
        assert len(drafts) == 1
        assert entry.status == ContentStatus.DRAFT

    def test_manual_mode_notifies(self, entry: CalendarEntry):
        """Manual mode calls notify handler and returns 'notification_sent'."""
        notifications = []

        async def mock_notify(e: CalendarEntry):
            notifications.append(e.title)

        publisher = ScheduledPublisher(
            autonomy_level="manual",
            notify_handler=mock_notify,
            retry_config=RetryConfig(max_retries=0, base_delay=0),
        )
        result = asyncio.run(publisher.execute(entry))

        assert result.success is True
        assert result.action_taken == "notification_sent"
        assert len(notifications) == 1

    def test_auto_without_handler_fails_gracefully(self, entry: CalendarEntry):
        """Auto mode without a publish handler returns failed, not crash."""
        publisher = ScheduledPublisher(autonomy_level="auto")
        result = asyncio.run(publisher.execute(entry))

        assert result.success is False
        assert result.action_taken == "failed"
        assert "No publish handler" in result.error

    def test_autonomy_manager_drives_publisher_level(self, tmp_dir: Path):
        """End-to-end: AutonomyManager level feeds into ScheduledPublisher behavior."""
        config = AutonomyConfig(level="auto", dry_run_default=False, kill_switch=True)
        manager = AutonomyManager(config=config, config_dir=str(tmp_dir))

        published = []

        async def mock_publish(e: CalendarEntry):
            published.append(e.title)

        entry = CalendarEntry(
            title="E2E test",
            scheduled_date="2026-04-15",
            platform="linkedin",
        )

        publisher = ScheduledPublisher(
            autonomy_level=manager.get_level().value,
            publish_handler=mock_publish,
            retry_config=RetryConfig(max_retries=0, base_delay=0),
        )
        result = asyncio.run(publisher.execute(entry))
        assert result.action_taken == "published"

        # Now activate kill switch -> level becomes manual
        manager.activate_kill_switch()
        entry2 = CalendarEntry(
            title="E2E test 2",
            scheduled_date="2026-04-16",
            platform="twitter",
        )
        notified = []

        async def mock_notify(e: CalendarEntry):
            notified.append(e.title)

        publisher2 = ScheduledPublisher(
            autonomy_level=manager.get_level().value,
            notify_handler=mock_notify,
            retry_config=RetryConfig(max_retries=0, base_delay=0),
        )
        result2 = asyncio.run(publisher2.execute(entry2))
        assert result2.action_taken == "notification_sent"


# ── Chain 3: CalendarEntry Frontmatter Roundtrip ──────────────────


class TestCalendarEntryRoundtrip:
    """Verify serialize -> deserialize produces identical entries."""

    def test_basic_roundtrip(self, sample_calendar_entry: CalendarEntry):
        """All standard fields survive frontmatter roundtrip."""
        frontmatter = sample_calendar_entry.to_frontmatter()
        restored = CalendarEntry.from_frontmatter(frontmatter)

        assert restored.title == sample_calendar_entry.title
        assert restored.scheduled_date == sample_calendar_entry.scheduled_date
        assert restored.platform == sample_calendar_entry.platform
        assert restored.content_type == sample_calendar_entry.content_type
        assert restored.status == sample_calendar_entry.status
        assert restored.author == sample_calendar_entry.author
        assert restored.tags == sample_calendar_entry.tags

    def test_roundtrip_with_empty_tags(self):
        """Entry with no tags roundtrips correctly."""
        entry = CalendarEntry(
            title="Minimal post",
            scheduled_date="2026-05-01",
            platform="twitter",
        )
        frontmatter = entry.to_frontmatter()
        restored = CalendarEntry.from_frontmatter(frontmatter)

        assert restored.title == entry.title
        assert restored.tags == []

    def test_roundtrip_preserves_status_enum(self):
        """ContentStatus enum survives YAML string serialization."""
        for status in ContentStatus:
            entry = CalendarEntry(
                title=f"Status test {status.value}",
                scheduled_date="2026-06-01",
                platform="reddit",
                status=status,
            )
            frontmatter = entry.to_frontmatter()
            restored = CalendarEntry.from_frontmatter(frontmatter)
            assert restored.status == status

    def test_frontmatter_has_yaml_delimiters(self, sample_calendar_entry: CalendarEntry):
        """Frontmatter output starts and ends with --- delimiters."""
        fm = sample_calendar_entry.to_frontmatter()
        assert fm.startswith("---\n")
        assert fm.endswith("\n---")

    def test_platform_normalized_on_roundtrip(self):
        """Platform name is lowercased during validation."""
        entry = CalendarEntry(
            title="Case test",
            scheduled_date="2026-07-01",
            platform="LinkedIn",
        )
        assert entry.platform == "linkedin"
        fm = entry.to_frontmatter()
        restored = CalendarEntry.from_frontmatter(fm)
        assert restored.platform == "linkedin"


# ── Chain 4: ScheduleConfig -> CronJobs ───────────────────────────


class TestScheduleConfigCronJobs:
    """Verify schedule YAML -> cron job preparation pipeline."""

    def test_load_and_prepare_jobs(self, schedule_yaml: Path):
        """Load YAML config and prepare cron jobs — only enabled jobs appear."""
        config = load_schedule_config(schedule_yaml)

        assert isinstance(config, ScheduleConfig)
        assert len(config.schedules) == 3

        jobs = prepare_cron_jobs(config)

        # Only enabled schedules become jobs
        assert len(jobs) == 2
        job_names = [j.name for j in jobs]
        assert "daily-publish" in job_names
        assert "weekly-review" in job_names
        assert "disabled-job" not in job_names

    def test_jobs_have_valid_cron_expressions(self, schedule_yaml: Path):
        """Each job has a 5-field cron expression."""
        config = load_schedule_config(schedule_yaml)
        jobs = prepare_cron_jobs(config)

        for job in jobs:
            parts = job.cron.strip().split()
            assert len(parts) == 5, f"Job '{job.name}' has invalid cron: {job.cron}"

    def test_jobs_have_non_empty_prompts(self, schedule_yaml: Path):
        """Each job has a prompt that references the action and agent."""
        config = load_schedule_config(schedule_yaml)
        jobs = prepare_cron_jobs(config)

        for job in jobs:
            assert len(job.prompt) > 0
            assert "GrowthOS scheduler" in job.prompt

    def test_job_prompt_includes_metadata(self, schedule_yaml: Path):
        """Jobs with metadata include it in the prompt string."""
        config = load_schedule_config(schedule_yaml)
        jobs = prepare_cron_jobs(config)

        daily_job = next(j for j in jobs if j.name == "daily-publish")
        assert "priority=high" in daily_job.prompt

    def test_job_prompt_includes_agent(self, schedule_yaml: Path):
        """Job prompt references the target agent."""
        config = load_schedule_config(schedule_yaml)
        jobs = prepare_cron_jobs(config)

        daily_job = next(j for j in jobs if j.name == "daily-publish")
        assert "@social-publisher" in daily_job.prompt

    def test_empty_schedule_produces_no_jobs(self, tmp_dir: Path):
        """An empty schedule config produces zero jobs."""
        path = tmp_dir / "empty.yaml"
        path.write_text(yaml.dump({"schedules": []}), encoding="utf-8")

        config = load_schedule_config(path)
        jobs = prepare_cron_jobs(config)
        assert jobs == []


# ── Chain 5: CircuitBreaker State Transitions ─────────────────────


class TestCircuitBreakerStateTransitions:
    """Verify circuit breaker state machine through failure/recovery cycles."""

    def test_closes_to_open_after_threshold(self):
        """Circuit opens after failure_threshold consecutive failures."""
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60)

        assert cb.state == CircuitState.CLOSED

        async def failing():
            raise ConnectionError("service down")

        for i in range(3):
            with pytest.raises(ConnectionError):
                asyncio.run(cb.call(failing))

        assert cb.state == CircuitState.OPEN

    def test_open_circuit_rejects_calls(self):
        """Open circuit raises CircuitOpenError immediately."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=9999)

        async def failing():
            raise ConnectionError("down")

        with pytest.raises(ConnectionError):
            asyncio.run(cb.call(failing))

        assert cb.state == CircuitState.OPEN

        with pytest.raises(CircuitOpenError):
            asyncio.run(cb.call(failing))

    def test_success_resets_failure_count(self):
        """Successful calls reset the failure counter — intermittent failures don't trip."""
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60)

        async def success():
            return "ok"

        async def fail():
            raise ConnectionError("blip")

        # 2 failures, then success
        for _ in range(2):
            with pytest.raises(ConnectionError):
                asyncio.run(cb.call(fail))

        asyncio.run(cb.call(success))
        assert cb.state == CircuitState.CLOSED
        assert cb._failure_count == 0

    def test_half_open_success_closes_circuit(self):
        """After recovery timeout, one success closes the circuit."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0)

        async def fail():
            raise ConnectionError("down")

        async def success():
            return "recovered"

        # Trip the circuit
        with pytest.raises(ConnectionError):
            asyncio.run(cb.call(fail))
        assert cb._state == CircuitState.OPEN

        # recovery_timeout=0 means immediate transition to HALF_OPEN
        assert cb.state == CircuitState.HALF_OPEN

        result = asyncio.run(cb.call(success))
        assert result == "recovered"
        assert cb.state == CircuitState.CLOSED

    def test_half_open_failure_reopens_circuit(self):
        """A failure during HALF_OPEN sends circuit back to OPEN."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0)

        async def fail():
            raise ConnectionError("still down")

        # Trip to OPEN
        with pytest.raises(ConnectionError):
            asyncio.run(cb.call(fail))

        # Now HALF_OPEN (recovery_timeout=0)
        assert cb.state == CircuitState.HALF_OPEN

        # Failure in HALF_OPEN -> back to OPEN
        with pytest.raises(ConnectionError):
            asyncio.run(cb.call(fail))
        assert cb._state == CircuitState.OPEN


# ── Chain 6: AuditLogger Integration ─────────────────────────────


class TestAuditLoggerIntegration:
    """Verify audit logger writes valid JSONL and reads it back."""

    def test_log_and_read_entries(self, tmp_dir: Path):
        """Log multiple entries and read them back with correct fields."""
        logger = AuditLogger(log_dir=str(tmp_dir))

        logger.log_action(
            action="publish_post",
            platform="linkedin",
            content_hash="abc123",
            user="growth-engineer",
            status="success",
            metadata={"post_id": "123"},
        )
        logger.log_action(
            action="create_draft",
            platform="twitter",
            content_hash="def456",
            user="system",
            status="success",
        )

        entries = logger.get_entries()
        assert len(entries) == 2
        assert entries[0].action == "publish_post"
        assert entries[0].platform == "linkedin"
        assert entries[0].content_hash == "abc123"
        assert entries[0].metadata == {"post_id": "123"}
        assert entries[1].action == "create_draft"

    def test_jsonl_format_valid(self, tmp_dir: Path):
        """Each line in the log file is valid JSON."""
        logger = AuditLogger(log_dir=str(tmp_dir))

        logger.log_action(
            action="publish_post",
            platform="reddit",
            content_hash="ghi789",
        )
        logger.log_action(
            action="schedule_post",
            platform="instagram",
            content_hash="jkl012",
        )

        log_files = list(tmp_dir.glob("audit-*.jsonl"))
        assert len(log_files) == 1

        with open(log_files[0], "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        assert len(lines) == 2
        for line in lines:
            data = json.loads(line)  # Must not raise
            assert "timestamp" in data
            assert "action" in data
            assert "platform" in data
            assert "content_hash" in data
            assert "user" in data
            assert "status" in data
            assert "metadata" in data

    def test_filter_entries(self, tmp_dir: Path):
        """Filtering by field values returns matching entries only."""
        logger = AuditLogger(log_dir=str(tmp_dir))

        logger.log_action(action="publish_post", platform="linkedin", content_hash="a")
        logger.log_action(action="create_draft", platform="twitter", content_hash="b")
        logger.log_action(action="publish_post", platform="twitter", content_hash="c")

        linkedin_entries = logger.get_entries(filters={"platform": "linkedin"})
        assert len(linkedin_entries) == 1
        assert linkedin_entries[0].content_hash == "a"

        publish_entries = logger.get_entries(filters={"action": "publish_post"})
        assert len(publish_entries) == 2

    def test_empty_log_returns_empty_list(self, tmp_dir: Path):
        """Reading from an empty audit directory returns no entries."""
        logger = AuditLogger(log_dir=str(tmp_dir))
        entries = logger.get_entries()
        assert entries == []

    def test_log_file_naming_convention(self, tmp_dir: Path):
        """Log files follow audit-YYYY-MM-DD.jsonl naming."""
        logger = AuditLogger(log_dir=str(tmp_dir))
        logger.log_action(action="test", platform="test", content_hash="x")

        log_files = list(tmp_dir.glob("audit-*.jsonl"))
        assert len(log_files) == 1

        name = log_files[0].name
        assert name.startswith("audit-")
        assert name.endswith(".jsonl")
        # Verify date format: audit-YYYY-MM-DD.jsonl
        date_part = name.replace("audit-", "").replace(".jsonl", "")
        parts = date_part.split("-")
        assert len(parts) == 3
        assert len(parts[0]) == 4  # year
        assert len(parts[1]) == 2  # month
        assert len(parts[2]) == 2  # day
