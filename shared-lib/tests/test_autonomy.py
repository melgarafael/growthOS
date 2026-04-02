"""Tests for GrowthOS autonomy level management."""

import json
from pathlib import Path


from growthOS_shared.autonomy import (
    CREATION_ACTIONS,
    EXTERNAL_ACTIONS,
    INTERNAL_ACTIONS,
    ActionType,
    AutonomyLevel,
    AutonomyManager,
)
from growthOS_shared.config import AutonomyConfig


def _make_config(
    level: str = "semi",
    dry_run_default: bool = True,
    kill_switch: bool = True,
) -> AutonomyConfig:
    return AutonomyConfig(
        level=level,
        require_preview=True,
        dry_run_default=dry_run_default,
        kill_switch=kill_switch,
    )


def _make_manager(
    tmp_path: Path,
    level: str = "semi",
    dry_run_default: bool = True,
    dry_run_override: bool | None = None,
) -> AutonomyManager:
    config = _make_config(level=level, dry_run_default=dry_run_default)
    return AutonomyManager(
        config=config,
        config_dir=str(tmp_path),
        dry_run_override=dry_run_override,
    )


# ── AutonomyLevel enum ────────────────────────────────────────────


class TestAutonomyLevel:
    def test_enum_values(self) -> None:
        assert AutonomyLevel.MANUAL.value == "manual"
        assert AutonomyLevel.SEMI.value == "semi"
        assert AutonomyLevel.AUTO.value == "auto"

    def test_from_string(self) -> None:
        assert AutonomyLevel("manual") == AutonomyLevel.MANUAL
        assert AutonomyLevel("semi") == AutonomyLevel.SEMI
        assert AutonomyLevel("auto") == AutonomyLevel.AUTO


# ── get_level ─────────────────────────────────────────────────────


class TestGetLevel:
    def test_returns_configured_level(self, tmp_path: Path) -> None:
        for level in ("manual", "semi", "auto"):
            mgr = _make_manager(tmp_path, level=level)
            assert mgr.get_level() == AutonomyLevel(level)

    def test_kill_switch_forces_manual(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="auto")
        mgr.activate_kill_switch()
        assert mgr.get_level() == AutonomyLevel.MANUAL


# ── Action classification ─────────────────────────────────────────


class TestActionClassification:
    def test_internal_actions(self) -> None:
        for action in INTERNAL_ACTIONS:
            assert AutonomyManager._classify_action(action) == ActionType.INTERNAL

    def test_creation_actions(self) -> None:
        for action in CREATION_ACTIONS:
            assert AutonomyManager._classify_action(action) == ActionType.CREATION

    def test_external_actions(self) -> None:
        for action in EXTERNAL_ACTIONS:
            assert AutonomyManager._classify_action(action) == ActionType.EXTERNAL

    def test_unknown_action_defaults_to_external(self) -> None:
        assert AutonomyManager._classify_action("some_unknown_action") == ActionType.EXTERNAL

    def test_no_overlap_between_sets(self) -> None:
        assert not (INTERNAL_ACTIONS & CREATION_ACTIONS)
        assert not (INTERNAL_ACTIONS & EXTERNAL_ACTIONS)
        assert not (CREATION_ACTIONS & EXTERNAL_ACTIONS)


# ── requires_approval: MANUAL mode ───────────────────────────────


class TestRequiresApprovalManual:
    def test_internal_never_needs_approval(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="manual")
        for action in INTERNAL_ACTIONS:
            assert mgr.requires_approval(action) is False

    def test_creation_needs_approval(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="manual")
        for action in CREATION_ACTIONS:
            assert mgr.requires_approval(action) is True

    def test_external_needs_approval(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="manual")
        for action in EXTERNAL_ACTIONS:
            assert mgr.requires_approval(action) is True

    def test_unknown_action_needs_approval(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="manual")
        assert mgr.requires_approval("unknown_thing") is True


# ── requires_approval: SEMI mode ─────────────────────────────────


class TestRequiresApprovalSemi:
    def test_internal_no_approval(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="semi")
        for action in INTERNAL_ACTIONS:
            assert mgr.requires_approval(action) is False

    def test_creation_auto_approved(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="semi")
        for action in CREATION_ACTIONS:
            assert mgr.requires_approval(action) is False

    def test_external_needs_approval(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="semi")
        for action in EXTERNAL_ACTIONS:
            assert mgr.requires_approval(action) is True


# ── requires_approval: AUTO mode ─────────────────────────────────


class TestRequiresApprovalAuto:
    def test_nothing_needs_approval(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="auto")
        all_actions = INTERNAL_ACTIONS | CREATION_ACTIONS | EXTERNAL_ACTIONS
        for action in all_actions:
            assert mgr.requires_approval(action) is False


# ── Dry-run ───────────────────────────────────────────────────────


class TestDryRun:
    def test_config_dry_run_true(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, dry_run_default=True)
        assert mgr.is_dry_run() is True

    def test_config_dry_run_false(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, dry_run_default=False)
        assert mgr.is_dry_run() is False

    def test_override_true_overrides_config_false(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, dry_run_default=False, dry_run_override=True)
        assert mgr.is_dry_run() is True

    def test_override_false_overrides_config_true(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, dry_run_default=True, dry_run_override=False)
        assert mgr.is_dry_run() is False

    def test_override_none_uses_config(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, dry_run_default=True, dry_run_override=None)
        assert mgr.is_dry_run() is True


# ── Kill switch ───────────────────────────────────────────────────


class TestKillSwitch:
    def test_initially_inactive(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path)
        assert mgr.is_kill_switch_active() is False

    def test_activate(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="auto")
        mgr.activate_kill_switch()
        assert mgr.is_kill_switch_active() is True
        assert mgr.get_level() == AutonomyLevel.MANUAL

    def test_deactivate(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="auto")
        mgr.activate_kill_switch()
        mgr.deactivate_kill_switch()
        assert mgr.is_kill_switch_active() is False
        assert mgr.get_level() == AutonomyLevel.AUTO

    def test_kill_switch_requires_approval_for_non_internal(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="auto")
        mgr.activate_kill_switch()
        assert mgr.requires_approval("publish_post") is True
        assert mgr.requires_approval("create_note") is True
        assert mgr.requires_approval("read_note") is False

    def test_persists_to_disk(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="auto")
        mgr.activate_kill_switch()

        state_file = tmp_path / "kill-switch.json"
        assert state_file.exists()
        data = json.loads(state_file.read_text(encoding="utf-8"))
        assert data["activated"] is True
        assert "timestamp" in data
        assert data["previous_level"] == "auto"

    def test_survives_reinit(self, tmp_path: Path) -> None:
        """Kill switch state persists across AutonomyManager instances."""
        mgr1 = _make_manager(tmp_path, level="auto")
        mgr1.activate_kill_switch()

        # New instance reads persisted state
        mgr2 = _make_manager(tmp_path, level="auto")
        assert mgr2.is_kill_switch_active() is True
        assert mgr2.get_level() == AutonomyLevel.MANUAL

    def test_deactivate_persists(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="semi")
        mgr.activate_kill_switch()
        mgr.deactivate_kill_switch()

        mgr2 = _make_manager(tmp_path, level="semi")
        assert mgr2.is_kill_switch_active() is False

    def test_corrupted_state_file_defaults_to_inactive(self, tmp_path: Path) -> None:
        state_file = tmp_path / "kill-switch.json"
        state_file.write_text("not valid json", encoding="utf-8")

        mgr = _make_manager(tmp_path)
        assert mgr.is_kill_switch_active() is False


# ── Integration: all levels + kill switch + dry-run ───────────────


class TestIntegration:
    def test_full_manual_flow(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="manual", dry_run_default=True)
        assert mgr.get_level() == AutonomyLevel.MANUAL
        assert mgr.is_dry_run() is True
        assert mgr.requires_approval("publish_post") is True
        assert mgr.requires_approval("create_note") is True
        assert mgr.requires_approval("read_note") is False

    def test_full_semi_flow(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="semi", dry_run_default=False)
        assert mgr.get_level() == AutonomyLevel.SEMI
        assert mgr.is_dry_run() is False
        assert mgr.requires_approval("publish_post") is True
        assert mgr.requires_approval("create_note") is False
        assert mgr.requires_approval("read_note") is False

    def test_full_auto_flow(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="auto", dry_run_default=False)
        assert mgr.get_level() == AutonomyLevel.AUTO
        assert mgr.is_dry_run() is False
        assert mgr.requires_approval("publish_post") is False
        assert mgr.requires_approval("create_note") is False

    def test_auto_with_kill_switch_reverts_to_manual(self, tmp_path: Path) -> None:
        mgr = _make_manager(tmp_path, level="auto", dry_run_default=False)
        mgr.activate_kill_switch()
        assert mgr.get_level() == AutonomyLevel.MANUAL
        assert mgr.requires_approval("publish_post") is True
        assert mgr.requires_approval("create_note") is True

        mgr.deactivate_kill_switch()
        assert mgr.get_level() == AutonomyLevel.AUTO
        assert mgr.requires_approval("publish_post") is False

    def test_dry_run_override_with_kill_switch(self, tmp_path: Path) -> None:
        mgr = _make_manager(
            tmp_path, level="auto", dry_run_default=False, dry_run_override=True
        )
        mgr.activate_kill_switch()
        assert mgr.is_dry_run() is True
        assert mgr.get_level() == AutonomyLevel.MANUAL
