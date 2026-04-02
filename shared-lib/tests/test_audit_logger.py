"""Tests for AuditLogger — append-only JSONL audit trail."""

import json
from pathlib import Path

import pytest

from growthOS_shared.audit_logger import AuditEntry, AuditLogger


@pytest.fixture
def audit_dir(tmp_path: Path) -> Path:
    return tmp_path / "audit"


@pytest.fixture
def logger(audit_dir: Path) -> AuditLogger:
    return AuditLogger(log_dir=str(audit_dir))


class TestDirectorySetup:
    def test_creates_directory(self, audit_dir: Path) -> None:
        assert not audit_dir.exists()
        AuditLogger(log_dir=str(audit_dir))
        assert audit_dir.exists()

    def test_env_var_override(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        custom_dir = tmp_path / "custom_audit"
        monkeypatch.setenv("GROWTHOS_AUDIT_DIR", str(custom_dir))
        logger = AuditLogger()  # no explicit log_dir
        assert logger.log_dir == custom_dir
        assert custom_dir.exists()

    def test_default_fallback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("GROWTHOS_AUDIT_DIR", raising=False)
        logger = AuditLogger()
        assert str(logger.log_dir).endswith(".growthOS/audit")


class TestLogAction:
    def test_creates_daily_file(self, logger: AuditLogger, audit_dir: Path) -> None:
        logger.log_action("publish", "twitter", "abc123")
        files = list(audit_dir.glob("audit-*.jsonl"))
        assert len(files) == 1
        assert files[0].name.startswith("audit-")
        assert files[0].name.endswith(".jsonl")

    def test_jsonl_format(self, logger: AuditLogger, audit_dir: Path) -> None:
        logger.log_action("publish", "twitter", "hash1")
        logger.log_action("draft", "linkedin", "hash2")

        files = list(audit_dir.glob("audit-*.jsonl"))
        lines = files[0].read_text().strip().split("\n")
        assert len(lines) == 2

        for line in lines:
            data = json.loads(line)
            assert "timestamp" in data
            assert "action" in data
            assert "platform" in data
            assert "content_hash" in data

    def test_append_only(self, logger: AuditLogger, audit_dir: Path) -> None:
        logger.log_action("a1", "twitter", "h1")
        files = list(audit_dir.glob("audit-*.jsonl"))
        size_after_first = files[0].stat().st_size

        logger.log_action("a2", "twitter", "h2")
        size_after_second = files[0].stat().st_size
        assert size_after_second > size_after_first

    def test_default_values(self, logger: AuditLogger, audit_dir: Path) -> None:
        logger.log_action("test", "twitter", "hash")
        files = list(audit_dir.glob("audit-*.jsonl"))
        data = json.loads(files[0].read_text().strip())
        assert data["user"] == "system"
        assert data["status"] == "success"
        assert data["metadata"] == {}

    def test_custom_metadata(self, logger: AuditLogger, audit_dir: Path) -> None:
        logger.log_action(
            "publish", "twitter", "h1",
            user="rafael",
            status="pending",
            metadata={"tweet_id": "12345", "chars": 280},
        )
        files = list(audit_dir.glob("audit-*.jsonl"))
        data = json.loads(files[0].read_text().strip())
        assert data["user"] == "rafael"
        assert data["status"] == "pending"
        assert data["metadata"]["tweet_id"] == "12345"


class TestGetEntries:
    def test_returns_all_entries(self, logger: AuditLogger) -> None:
        logger.log_action("a1", "twitter", "h1")
        logger.log_action("a2", "linkedin", "h2")
        logger.log_action("a3", "twitter", "h3")

        entries = logger.get_entries()
        assert len(entries) == 3
        assert all(isinstance(e, AuditEntry) for e in entries)

    def test_filter_by_platform(self, logger: AuditLogger) -> None:
        logger.log_action("a1", "twitter", "h1")
        logger.log_action("a2", "linkedin", "h2")
        logger.log_action("a3", "twitter", "h3")

        entries = logger.get_entries(filters={"platform": "twitter"})
        assert len(entries) == 2
        assert all(e.platform == "twitter" for e in entries)

    def test_filter_by_action(self, logger: AuditLogger) -> None:
        logger.log_action("publish", "twitter", "h1")
        logger.log_action("draft", "twitter", "h2")

        entries = logger.get_entries(filters={"action": "publish"})
        assert len(entries) == 1
        assert entries[0].action == "publish"

    def test_combined_filters(self, logger: AuditLogger) -> None:
        logger.log_action("publish", "twitter", "h1")
        logger.log_action("publish", "linkedin", "h2")
        logger.log_action("draft", "twitter", "h3")

        entries = logger.get_entries(filters={"action": "publish", "platform": "twitter"})
        assert len(entries) == 1

    def test_no_match_returns_empty(self, logger: AuditLogger) -> None:
        logger.log_action("publish", "twitter", "h1")
        entries = logger.get_entries(filters={"platform": "nonexistent"})
        assert entries == []

    def test_empty_log_returns_empty(self, logger: AuditLogger) -> None:
        entries = logger.get_entries()
        assert entries == []
