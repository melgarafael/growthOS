"""Tests for cron scheduler and content calendar automation."""

from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
import yaml

from growthOS_shared.scheduler import (
    CalendarEntry,
    ContentStatus,
    PublishResult,
    RegisteredJob,
    RetryConfig,
    ScheduleAction,
    ScheduleConfig,
    ScheduleDefinition,
    ScheduledPublisher,
    build_cron_prompt,
    load_schedule_config,
    prepare_cron_jobs,
    retry_with_backoff,
)


# ---------------------------------------------------------------------------
# ContentStatus enum
# ---------------------------------------------------------------------------


class TestContentStatus:
    def test_enum_values(self) -> None:
        assert ContentStatus.DRAFT.value == "draft"
        assert ContentStatus.SCHEDULED.value == "scheduled"
        assert ContentStatus.PUBLISHING.value == "publishing"
        assert ContentStatus.PUBLISHED.value == "published"
        assert ContentStatus.FAILED.value == "failed"

    def test_all_statuses_count(self) -> None:
        assert len(ContentStatus) == 5


# ---------------------------------------------------------------------------
# CalendarEntry
# ---------------------------------------------------------------------------


def _make_entry(**overrides) -> CalendarEntry:
    defaults = {
        "title": "Test Post",
        "scheduled_date": "2026-04-01T10:00",
        "platform": "twitter",
    }
    defaults.update(overrides)
    return CalendarEntry(**defaults)


class TestCalendarEntry:
    def test_create_with_defaults(self) -> None:
        entry = _make_entry()
        assert entry.title == "Test Post"
        assert entry.platform == "twitter"
        assert entry.content_type == "social"
        assert entry.status == ContentStatus.DRAFT
        assert entry.author == ""
        assert entry.tags == []
        assert entry.retry_count == 0
        assert entry.last_error == ""

    def test_platform_lowercased(self) -> None:
        entry = _make_entry(platform="LinkedIn")
        assert entry.platform == "linkedin"

    def test_platform_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="platform is required"):
            _make_entry(platform="")

    def test_platform_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="platform is required"):
            _make_entry(platform="   ")

    def test_custom_fields(self) -> None:
        entry = _make_entry(
            content_type="blog",
            status=ContentStatus.SCHEDULED,
            author="Alice",
            tags=["growth", "ai"],
            retry_count=2,
            last_error="timeout",
        )
        assert entry.content_type == "blog"
        assert entry.status == ContentStatus.SCHEDULED
        assert entry.author == "Alice"
        assert entry.tags == ["growth", "ai"]
        assert entry.retry_count == 2
        assert entry.last_error == "timeout"

    def test_all_statuses_assignable(self) -> None:
        for status in ContentStatus:
            entry = _make_entry(status=status)
            assert entry.status == status


class TestCalendarEntryFrontmatter:
    def test_to_frontmatter_format(self) -> None:
        entry = _make_entry(tags=["test"])
        fm = entry.to_frontmatter()
        assert fm.startswith("---\n")
        assert fm.endswith("\n---")
        assert "title: Test Post" in fm
        assert "platform: twitter" in fm

    def test_to_frontmatter_contains_status(self) -> None:
        entry = _make_entry(status=ContentStatus.SCHEDULED)
        fm = entry.to_frontmatter()
        assert "status: scheduled" in fm

    def test_roundtrip(self) -> None:
        original = _make_entry(
            title="Roundtrip",
            platform="linkedin",
            content_type="article",
            author="Bob",
            tags=["seo"],
        )
        fm = original.to_frontmatter()
        restored = CalendarEntry.from_frontmatter(fm)
        assert restored.title == original.title
        assert restored.platform == original.platform
        assert restored.content_type == original.content_type
        assert restored.author == original.author
        assert restored.tags == original.tags

    def test_roundtrip_with_status(self) -> None:
        original = _make_entry(status=ContentStatus.SCHEDULED)
        fm = original.to_frontmatter()
        restored = CalendarEntry.from_frontmatter(fm)
        assert restored.status == original.status

    def test_from_frontmatter_missing_delimiters(self) -> None:
        with pytest.raises(ValueError, match="missing --- delimiters"):
            CalendarEntry.from_frontmatter("no delimiters here")

    def test_from_frontmatter_only_one_delimiter(self) -> None:
        with pytest.raises(ValueError, match="missing --- delimiters"):
            CalendarEntry.from_frontmatter("---\ntitle: foo\n")

    def test_from_frontmatter_invalid_yaml(self) -> None:
        with pytest.raises(ValueError, match="expected YAML mapping"):
            CalendarEntry.from_frontmatter("---\n- just a list\n---")


# ---------------------------------------------------------------------------
# ScheduleAction enum
# ---------------------------------------------------------------------------


class TestScheduleAction:
    def test_enum_values(self) -> None:
        assert ScheduleAction.PUBLISH.value == "publish"
        assert ScheduleAction.REVIEW_CALENDAR.value == "review_calendar"
        assert ScheduleAction.STRATEGY_REVIEW.value == "strategy_review"
        assert ScheduleAction.CONTENT_CHECK.value == "content_check"

    def test_all_actions_count(self) -> None:
        assert len(ScheduleAction) == 4


# ---------------------------------------------------------------------------
# ScheduleDefinition
# ---------------------------------------------------------------------------


class TestScheduleDefinition:
    def test_valid_cron(self) -> None:
        sd = ScheduleDefinition(name="test", cron="0 9 * * 1", action="publish")
        assert sd.cron == "0 9 * * 1"

    def test_cron_stripped(self) -> None:
        sd = ScheduleDefinition(name="test", cron="  0 9 * * 1  ", action="publish")
        assert sd.cron == "0 9 * * 1"

    def test_cron_too_few_fields(self) -> None:
        with pytest.raises(ValueError, match="5 fields"):
            ScheduleDefinition(name="test", cron="0 9 *", action="publish")

    def test_cron_too_many_fields(self) -> None:
        with pytest.raises(ValueError, match="5 fields"):
            ScheduleDefinition(name="test", cron="0 9 * * 1 2", action="publish")

    def test_cron_single_field(self) -> None:
        with pytest.raises(ValueError, match="5 fields"):
            ScheduleDefinition(name="test", cron="*", action="publish")

    def test_defaults(self) -> None:
        sd = ScheduleDefinition(name="test", cron="0 9 * * 1", action="publish")
        assert sd.agent == "cmo"
        assert sd.enabled is True
        assert sd.metadata == {}

    def test_custom_metadata(self) -> None:
        sd = ScheduleDefinition(
            name="test",
            cron="0 9 * * 1",
            action="publish",
            agent="social",
            enabled=False,
            metadata={"platform": "twitter"},
        )
        assert sd.agent == "social"
        assert sd.enabled is False
        assert sd.metadata == {"platform": "twitter"}


# ---------------------------------------------------------------------------
# ScheduleConfig
# ---------------------------------------------------------------------------


class TestScheduleConfig:
    def _config_with_schedules(self) -> ScheduleConfig:
        return ScheduleConfig(
            schedules=[
                ScheduleDefinition(name="daily", cron="0 9 * * *", action="publish", enabled=True),
                ScheduleDefinition(name="weekly", cron="0 10 * * 1", action="review_calendar", enabled=True),
                ScheduleDefinition(name="disabled", cron="0 0 * * *", action="content_check", enabled=False),
            ]
        )

    def test_empty_config(self) -> None:
        cfg = ScheduleConfig()
        assert cfg.schedules == []
        assert cfg.get_enabled() == []

    def test_get_enabled(self) -> None:
        cfg = self._config_with_schedules()
        enabled = cfg.get_enabled()
        assert len(enabled) == 2
        names = [s.name for s in enabled]
        assert "daily" in names
        assert "weekly" in names
        assert "disabled" not in names

    def test_get_by_name_found(self) -> None:
        cfg = self._config_with_schedules()
        s = cfg.get_by_name("weekly")
        assert s is not None
        assert s.name == "weekly"

    def test_get_by_name_not_found(self) -> None:
        cfg = self._config_with_schedules()
        assert cfg.get_by_name("nonexistent") is None

    def test_get_enabled_all_disabled(self) -> None:
        cfg = ScheduleConfig(
            schedules=[
                ScheduleDefinition(name="a", cron="0 0 * * *", action="x", enabled=False),
                ScheduleDefinition(name="b", cron="0 0 * * *", action="y", enabled=False),
            ]
        )
        assert cfg.get_enabled() == []


# ---------------------------------------------------------------------------
# load_schedule_config
# ---------------------------------------------------------------------------


class TestLoadScheduleConfig:
    def test_load_valid_file(self, tmp_path: Path) -> None:
        data = {
            "schedules": [
                {"name": "morning", "cron": "0 8 * * *", "action": "publish"},
            ]
        }
        p = tmp_path / "schedule.yaml"
        p.write_text(yaml.dump(data), encoding="utf-8")
        cfg = load_schedule_config(p)
        assert len(cfg.schedules) == 1
        assert cfg.schedules[0].name == "morning"

    def test_load_multiple_schedules(self, tmp_path: Path) -> None:
        data = {
            "schedules": [
                {"name": "daily", "cron": "0 9 * * *", "action": "publish"},
                {"name": "weekly", "cron": "0 10 * * 1", "action": "review_calendar"},
            ]
        }
        p = tmp_path / "schedule.yaml"
        p.write_text(yaml.dump(data), encoding="utf-8")
        cfg = load_schedule_config(p)
        assert len(cfg.schedules) == 2

    def test_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="not found"):
            load_schedule_config(tmp_path / "missing.yaml")

    def test_invalid_yaml_content(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.yaml"
        p.write_text("- just a list", encoding="utf-8")
        with pytest.raises(ValueError, match="expected YAML mapping"):
            load_schedule_config(p)

    def test_empty_schedules(self, tmp_path: Path) -> None:
        p = tmp_path / "empty.yaml"
        p.write_text(yaml.dump({"schedules": []}), encoding="utf-8")
        cfg = load_schedule_config(p)
        assert cfg.schedules == []

    def test_accepts_path_as_string(self, tmp_path: Path) -> None:
        data = {"schedules": [{"name": "x", "cron": "0 0 * * *", "action": "publish"}]}
        p = tmp_path / "str.yaml"
        p.write_text(yaml.dump(data), encoding="utf-8")
        cfg = load_schedule_config(str(p))
        assert len(cfg.schedules) == 1


# ---------------------------------------------------------------------------
# RetryConfig
# ---------------------------------------------------------------------------


class TestRetryConfig:
    def test_defaults(self) -> None:
        rc = RetryConfig()
        assert rc.max_retries == 3
        assert rc.base_delay == 1.0
        assert rc.max_delay == 30.0
        assert rc.jitter is True
        assert TimeoutError in rc.transient_exceptions
        assert ConnectionError in rc.transient_exceptions
        assert OSError in rc.transient_exceptions

    def test_custom_values(self) -> None:
        rc = RetryConfig(max_retries=5, base_delay=0.5, max_delay=10.0, jitter=False)
        assert rc.max_retries == 5
        assert rc.base_delay == 0.5
        assert rc.max_delay == 10.0
        assert rc.jitter is False

    def test_custom_transient_exceptions(self) -> None:
        rc = RetryConfig(transient_exceptions=(RuntimeError,))
        assert RuntimeError in rc.transient_exceptions
        assert TimeoutError not in rc.transient_exceptions


# ---------------------------------------------------------------------------
# retry_with_backoff
# ---------------------------------------------------------------------------


class TestRetryWithBackoff:
    @pytest.mark.asyncio
    async def test_success_on_first_try(self) -> None:
        func = AsyncMock(return_value="ok")
        result = await retry_with_backoff(func)
        assert result == "ok"
        assert func.call_count == 1

    @pytest.mark.asyncio
    async def test_retries_on_transient_error(self) -> None:
        func = AsyncMock(side_effect=[TimeoutError("t/o"), "ok"])
        cfg = RetryConfig(max_retries=3, base_delay=0.0, jitter=False)
        with patch("growthOS_shared.scheduler.asyncio.sleep", new_callable=AsyncMock):
            result = await retry_with_backoff(func, config=cfg)
        assert result == "ok"
        assert func.call_count == 2

    @pytest.mark.asyncio
    async def test_retries_connection_error(self) -> None:
        func = AsyncMock(side_effect=[ConnectionError("reset"), "recovered"])
        cfg = RetryConfig(max_retries=3, base_delay=0.0, jitter=False)
        with patch("growthOS_shared.scheduler.asyncio.sleep", new_callable=AsyncMock):
            result = await retry_with_backoff(func, config=cfg)
        assert result == "recovered"

    @pytest.mark.asyncio
    async def test_retries_os_error(self) -> None:
        func = AsyncMock(side_effect=[OSError("io"), "ok"])
        cfg = RetryConfig(max_retries=3, base_delay=0.0, jitter=False)
        with patch("growthOS_shared.scheduler.asyncio.sleep", new_callable=AsyncMock):
            result = await retry_with_backoff(func, config=cfg)
        assert result == "ok"

    @pytest.mark.asyncio
    async def test_exhausts_retries(self) -> None:
        func = AsyncMock(side_effect=ConnectionError("fail"))
        cfg = RetryConfig(max_retries=2, base_delay=0.0, jitter=False)
        with patch("growthOS_shared.scheduler.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(ConnectionError, match="fail"):
                await retry_with_backoff(func, config=cfg)
        # 1 initial + 2 retries = 3
        assert func.call_count == 3

    @pytest.mark.asyncio
    async def test_non_transient_error_not_retried(self) -> None:
        func = AsyncMock(side_effect=ValueError("bad input"))
        cfg = RetryConfig(max_retries=3, base_delay=0.0, jitter=False)
        with pytest.raises(ValueError, match="bad input"):
            await retry_with_backoff(func, config=cfg)
        assert func.call_count == 1

    @pytest.mark.asyncio
    async def test_passes_args_and_kwargs(self) -> None:
        func = AsyncMock(return_value="done")
        await retry_with_backoff(func, "a", "b", key="val")
        func.assert_called_once_with("a", "b", key="val")

    @pytest.mark.asyncio
    async def test_backoff_delay_capped_at_max(self) -> None:
        sleep_calls: list[float] = []

        async def mock_sleep(delay: float) -> None:
            sleep_calls.append(delay)

        func = AsyncMock(side_effect=[TimeoutError(), TimeoutError(), TimeoutError(), "ok"])
        cfg = RetryConfig(max_retries=3, base_delay=1.0, max_delay=5.0, jitter=False)
        with patch("growthOS_shared.scheduler.asyncio.sleep", side_effect=mock_sleep):
            await retry_with_backoff(func, config=cfg)

        assert len(sleep_calls) == 3
        for d in sleep_calls:
            assert d <= 5.0

    @pytest.mark.asyncio
    async def test_backoff_exponential_without_jitter(self) -> None:
        sleep_calls: list[float] = []

        async def mock_sleep(delay: float) -> None:
            sleep_calls.append(delay)

        func = AsyncMock(side_effect=[TimeoutError(), TimeoutError(), TimeoutError(), "ok"])
        cfg = RetryConfig(max_retries=3, base_delay=1.0, max_delay=100.0, jitter=False)
        with patch("growthOS_shared.scheduler.asyncio.sleep", side_effect=mock_sleep):
            await retry_with_backoff(func, config=cfg)

        # delays: 1*2^0=1, 1*2^1=2, 1*2^2=4
        assert sleep_calls == [1.0, 2.0, 4.0]

    @pytest.mark.asyncio
    async def test_zero_retries_fails_immediately(self) -> None:
        func = AsyncMock(side_effect=TimeoutError("boom"))
        cfg = RetryConfig(max_retries=0, base_delay=0.0, jitter=False)
        with pytest.raises(TimeoutError, match="boom"):
            await retry_with_backoff(func, config=cfg)
        assert func.call_count == 1

    @pytest.mark.asyncio
    async def test_uses_default_config_when_none(self) -> None:
        func = AsyncMock(return_value="ok")
        result = await retry_with_backoff(func, config=None)
        assert result == "ok"

    @pytest.mark.asyncio
    async def test_jitter_adds_randomness(self) -> None:
        sleep_calls: list[float] = []

        async def mock_sleep(delay: float) -> None:
            sleep_calls.append(delay)

        func = AsyncMock(side_effect=[TimeoutError(), "ok"])
        cfg = RetryConfig(max_retries=1, base_delay=1.0, max_delay=100.0, jitter=True)
        with patch("growthOS_shared.scheduler.asyncio.sleep", side_effect=mock_sleep):
            with patch("growthOS_shared.scheduler.random.random", return_value=0.5):
                await retry_with_backoff(func, config=cfg)

        # delay = min(1.0 * 2^0, 100) * (0.5 + 0.5) = 1.0
        assert len(sleep_calls) == 1
        assert sleep_calls[0] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# PublishResult
# ---------------------------------------------------------------------------


class TestPublishResult:
    def test_create_success(self) -> None:
        entry = _make_entry()
        pr = PublishResult(entry=entry, success=True, action_taken="published")
        assert pr.success is True
        assert pr.action_taken == "published"
        assert pr.error == ""
        assert pr.attempts == 1

    def test_create_failure(self) -> None:
        entry = _make_entry()
        pr = PublishResult(
            entry=entry, success=False, action_taken="failed",
            error="timeout", attempts=3,
        )
        assert pr.success is False
        assert pr.error == "timeout"
        assert pr.attempts == 3


# ---------------------------------------------------------------------------
# ScheduledPublisher — Init
# ---------------------------------------------------------------------------


class TestScheduledPublisherInit:
    def test_valid_levels(self) -> None:
        for level in ("manual", "semi", "auto"):
            sp = ScheduledPublisher(autonomy_level=level)
            assert sp.autonomy_level == level

    def test_invalid_level(self) -> None:
        with pytest.raises(ValueError, match="Invalid autonomy level"):
            ScheduledPublisher(autonomy_level="yolo")

    def test_default_retry_config(self) -> None:
        sp = ScheduledPublisher(autonomy_level="semi")
        assert sp.retry_config.max_retries == 3

    def test_custom_retry_config(self) -> None:
        cfg = RetryConfig(max_retries=5)
        sp = ScheduledPublisher(autonomy_level="semi", retry_config=cfg)
        assert sp.retry_config.max_retries == 5


# ---------------------------------------------------------------------------
# ScheduledPublisher — Auto mode
# ---------------------------------------------------------------------------


class TestScheduledPublisherAutoMode:
    @pytest.mark.asyncio
    async def test_publish_success(self) -> None:
        handler = AsyncMock()
        sp = ScheduledPublisher(
            autonomy_level="auto",
            publish_handler=handler,
            retry_config=RetryConfig(max_retries=0),
        )
        entry = _make_entry()
        result = await sp.execute(entry)
        assert result.success is True
        assert result.action_taken == "published"
        assert entry.status == ContentStatus.PUBLISHED
        handler.assert_called_once_with(entry)

    @pytest.mark.asyncio
    async def test_publish_no_handler(self) -> None:
        sp = ScheduledPublisher(autonomy_level="auto")
        entry = _make_entry()
        result = await sp.execute(entry)
        assert result.success is False
        assert result.action_taken == "failed"
        assert "No publish handler" in result.error

    @pytest.mark.asyncio
    async def test_publish_handler_fails(self) -> None:
        handler = AsyncMock(side_effect=ConnectionError("network"))
        cfg = RetryConfig(max_retries=1, base_delay=0.0, jitter=False)
        sp = ScheduledPublisher(
            autonomy_level="auto",
            publish_handler=handler,
            retry_config=cfg,
        )
        entry = _make_entry()
        with patch("growthOS_shared.scheduler.asyncio.sleep", new_callable=AsyncMock):
            result = await sp.execute(entry)
        assert result.success is False
        assert result.action_taken == "failed"
        assert entry.status == ContentStatus.FAILED
        assert entry.retry_count == cfg.max_retries
        assert "network" in entry.last_error
        assert result.attempts == cfg.max_retries + 1

    @pytest.mark.asyncio
    async def test_publish_retries_then_succeeds(self) -> None:
        handler = AsyncMock(side_effect=[TimeoutError("t/o"), None])
        cfg = RetryConfig(max_retries=3, base_delay=0.0, jitter=False)
        sp = ScheduledPublisher(
            autonomy_level="auto",
            publish_handler=handler,
            retry_config=cfg,
        )
        entry = _make_entry()
        with patch("growthOS_shared.scheduler.asyncio.sleep", new_callable=AsyncMock):
            result = await sp.execute(entry)
        assert result.success is True
        assert result.action_taken == "published"
        assert entry.status == ContentStatus.PUBLISHED

    @pytest.mark.asyncio
    async def test_publish_non_transient_error_fails(self) -> None:
        handler = AsyncMock(side_effect=RuntimeError("bug"))
        cfg = RetryConfig(max_retries=2, base_delay=0.0, jitter=False)
        sp = ScheduledPublisher(
            autonomy_level="auto",
            publish_handler=handler,
            retry_config=cfg,
        )
        entry = _make_entry()
        result = await sp.execute(entry)
        assert result.success is False
        assert entry.status == ContentStatus.FAILED


# ---------------------------------------------------------------------------
# ScheduledPublisher — Semi mode
# ---------------------------------------------------------------------------


class TestScheduledPublisherSemiMode:
    @pytest.mark.asyncio
    async def test_creates_draft(self) -> None:
        draft_handler = AsyncMock()
        sp = ScheduledPublisher(
            autonomy_level="semi",
            draft_handler=draft_handler,
            retry_config=RetryConfig(max_retries=0),
        )
        entry = _make_entry()
        result = await sp.execute(entry)
        assert result.success is True
        assert result.action_taken == "draft_created"
        assert entry.status == ContentStatus.DRAFT
        draft_handler.assert_called_once_with(entry)

    @pytest.mark.asyncio
    async def test_draft_no_handler_still_succeeds(self) -> None:
        sp = ScheduledPublisher(autonomy_level="semi")
        entry = _make_entry()
        result = await sp.execute(entry)
        assert result.success is True
        assert result.action_taken == "draft_created"

    @pytest.mark.asyncio
    async def test_draft_handler_fails(self) -> None:
        draft_handler = AsyncMock(side_effect=ConnectionError("fail"))
        cfg = RetryConfig(max_retries=0, base_delay=0.0, jitter=False)
        sp = ScheduledPublisher(
            autonomy_level="semi",
            draft_handler=draft_handler,
            retry_config=cfg,
        )
        entry = _make_entry()
        result = await sp.execute(entry)
        assert result.success is False
        assert result.action_taken == "failed"
        assert "Draft creation failed" in result.error

    @pytest.mark.asyncio
    async def test_semi_does_not_call_publish_handler(self) -> None:
        publish_handler = AsyncMock()
        sp = ScheduledPublisher(
            autonomy_level="semi",
            publish_handler=publish_handler,
            retry_config=RetryConfig(max_retries=0),
        )
        entry = _make_entry()
        await sp.execute(entry)
        publish_handler.assert_not_called()


# ---------------------------------------------------------------------------
# ScheduledPublisher — Manual mode
# ---------------------------------------------------------------------------


class TestScheduledPublisherManualMode:
    @pytest.mark.asyncio
    async def test_sends_notification(self) -> None:
        notify_handler = AsyncMock()
        sp = ScheduledPublisher(
            autonomy_level="manual",
            notify_handler=notify_handler,
            retry_config=RetryConfig(max_retries=0),
        )
        entry = _make_entry()
        result = await sp.execute(entry)
        assert result.success is True
        assert result.action_taken == "notification_sent"
        notify_handler.assert_called_once_with(entry)

    @pytest.mark.asyncio
    async def test_notify_no_handler_still_succeeds(self) -> None:
        sp = ScheduledPublisher(autonomy_level="manual")
        entry = _make_entry()
        result = await sp.execute(entry)
        assert result.success is True
        assert result.action_taken == "notification_sent"

    @pytest.mark.asyncio
    async def test_notify_handler_fails(self) -> None:
        notify_handler = AsyncMock(side_effect=OSError("fail"))
        cfg = RetryConfig(max_retries=0, base_delay=0.0, jitter=False)
        sp = ScheduledPublisher(
            autonomy_level="manual",
            notify_handler=notify_handler,
            retry_config=cfg,
        )
        entry = _make_entry()
        result = await sp.execute(entry)
        assert result.success is False
        assert result.action_taken == "failed"
        assert "Notification failed" in result.error

    @pytest.mark.asyncio
    async def test_manual_does_not_call_publish_or_draft(self) -> None:
        publish_handler = AsyncMock()
        draft_handler = AsyncMock()
        sp = ScheduledPublisher(
            autonomy_level="manual",
            publish_handler=publish_handler,
            draft_handler=draft_handler,
            retry_config=RetryConfig(max_retries=0),
        )
        entry = _make_entry()
        await sp.execute(entry)
        publish_handler.assert_not_called()
        draft_handler.assert_not_called()


# ---------------------------------------------------------------------------
# CronCreate integration helpers
# ---------------------------------------------------------------------------


class TestBuildCronPrompt:
    def test_basic_prompt(self) -> None:
        sd = ScheduleDefinition(name="daily", cron="0 9 * * *", action="publish")
        prompt = build_cron_prompt(sd)
        assert "publish" in prompt
        assert "@cmo" in prompt

    def test_custom_agent(self) -> None:
        sd = ScheduleDefinition(name="x", cron="0 9 * * *", action="review_calendar", agent="social")
        prompt = build_cron_prompt(sd)
        assert "@social" in prompt
        assert "review_calendar" in prompt

    def test_with_metadata(self) -> None:
        sd = ScheduleDefinition(
            name="x",
            cron="0 9 * * *",
            action="publish",
            metadata={"platform": "twitter", "priority": "high"},
        )
        prompt = build_cron_prompt(sd)
        assert "platform=twitter" in prompt
        assert "priority=high" in prompt
        assert "[" in prompt

    def test_no_metadata(self) -> None:
        sd = ScheduleDefinition(name="x", cron="0 9 * * *", action="publish")
        prompt = build_cron_prompt(sd)
        assert "[" not in prompt

    def test_prompt_contains_growthOS_prefix(self) -> None:
        sd = ScheduleDefinition(name="x", cron="0 9 * * *", action="publish")
        prompt = build_cron_prompt(sd)
        assert prompt.startswith("GrowthOS scheduler:")


class TestPrepareCronJobs:
    def test_converts_enabled_only(self) -> None:
        cfg = ScheduleConfig(
            schedules=[
                ScheduleDefinition(name="a", cron="0 9 * * *", action="publish", enabled=True),
                ScheduleDefinition(name="b", cron="0 10 * * *", action="review_calendar", enabled=False),
                ScheduleDefinition(name="c", cron="0 11 * * *", action="content_check", enabled=True),
            ]
        )
        jobs = prepare_cron_jobs(cfg)
        assert len(jobs) == 2
        names = [j.name for j in jobs]
        assert "a" in names
        assert "c" in names
        assert "b" not in names

    def test_job_attributes(self) -> None:
        cfg = ScheduleConfig(
            schedules=[
                ScheduleDefinition(name="daily", cron="0 9 * * *", action="publish"),
            ]
        )
        jobs = prepare_cron_jobs(cfg)
        assert len(jobs) == 1
        job = jobs[0]
        assert isinstance(job, RegisteredJob)
        assert job.name == "daily"
        assert job.cron == "0 9 * * *"
        assert "publish" in job.prompt
        assert job.job_id is None

    def test_empty_config(self) -> None:
        cfg = ScheduleConfig()
        jobs = prepare_cron_jobs(cfg)
        assert jobs == []

    def test_preserves_order(self) -> None:
        cfg = ScheduleConfig(
            schedules=[
                ScheduleDefinition(name="first", cron="0 1 * * *", action="a", enabled=True),
                ScheduleDefinition(name="second", cron="0 2 * * *", action="b", enabled=True),
                ScheduleDefinition(name="third", cron="0 3 * * *", action="c", enabled=True),
            ]
        )
        jobs = prepare_cron_jobs(cfg)
        assert [j.name for j in jobs] == ["first", "second", "third"]


class TestRegisteredJob:
    def test_defaults(self) -> None:
        job = RegisteredJob(name="test", cron="0 0 * * *", prompt="do something")
        assert job.job_id is None

    def test_with_job_id(self) -> None:
        job = RegisteredJob(name="test", cron="0 0 * * *", prompt="do something", job_id="abc-123")
        assert job.job_id == "abc-123"

    def test_fields(self) -> None:
        job = RegisteredJob(name="daily", cron="0 9 * * *", prompt="run publish")
        assert job.name == "daily"
        assert job.cron == "0 9 * * *"
        assert job.prompt == "run publish"
