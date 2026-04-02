"""Autonomy level management with kill switch and dry-run orchestration."""

import json
import os
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

from growthOS_shared.config import AutonomyConfig, load_brand_voice


class AutonomyLevel(str, Enum):
    MANUAL = "manual"
    SEMI = "semi"
    AUTO = "auto"


class ActionType(str, Enum):
    """Classification of actions by their external impact."""

    INTERNAL = "internal"
    CREATION = "creation"
    EXTERNAL = "external"


# Actions classified by tier — used to decide approval requirements.
INTERNAL_ACTIONS = frozenset({
    "read_note",
    "search_notes",
    "get_analytics",
    "list_drafts",
    "get_config",
})

CREATION_ACTIONS = frozenset({
    "create_note",
    "generate_content",
    "create_draft",
    "edit_draft",
})

EXTERNAL_ACTIONS = frozenset({
    "publish_post",
    "schedule_post",
    "delete_post",
    "update_post",
    "send_notification",
})


class KillSwitchActiveError(Exception):
    """Raised when an action is attempted while the kill switch is active."""


class AutonomyManager:
    """Manages autonomy levels, action approval, kill switch, and dry-run state.

    Reads configuration from brand-voice.yaml via AutonomyConfig.
    Kill switch state persists to disk so it survives container restarts.
    """

    def __init__(
        self,
        config: Optional[AutonomyConfig] = None,
        config_dir: Optional[str] = None,
        dry_run_override: Optional[bool] = None,
    ) -> None:
        if config is not None:
            self._config = config
        else:
            brand_config = load_brand_voice()
            self._config = brand_config.autonomy

        self._config_dir = Path(
            config_dir
            or os.environ.get("GROWTHOS_CONFIG_DIR", ".growthOS")
        )
        self._config_dir.mkdir(parents=True, exist_ok=True)

        self._kill_switch_path = self._config_dir / "kill-switch.json"
        self._dry_run_override = dry_run_override

        # Load persisted kill switch state on init
        self._kill_switch_active = self._load_kill_switch_state()

    # ── Public API ────────────────────────────────────────────────

    def get_level(self) -> AutonomyLevel:
        """Return the current effective autonomy level.

        If the kill switch is active, always returns MANUAL regardless of config.
        """
        if self._kill_switch_active:
            return AutonomyLevel.MANUAL
        return AutonomyLevel(self._config.level)

    def requires_approval(self, action_type: str) -> bool:
        """Determine if the given action requires user approval.

        Args:
            action_type: The action name (e.g. 'publish_post', 'read_note').

        Returns:
            True if the action should pause for user confirmation.
        """
        if self._kill_switch_active:
            return action_type not in INTERNAL_ACTIONS

        classification = self._classify_action(action_type)
        level = self.get_level()

        if classification == ActionType.INTERNAL:
            return False

        if level == AutonomyLevel.MANUAL:
            return True

        if level == AutonomyLevel.SEMI:
            return classification == ActionType.EXTERNAL

        # AUTO: no approval needed (circuit breaker protects externally)
        return False

    def is_dry_run(self) -> bool:
        """Check if operations should run in dry-run (simulation) mode.

        Per-invocation --dry-run flag overrides the config value.
        """
        if self._dry_run_override is not None:
            return self._dry_run_override
        return self._config.dry_run_default

    def activate_kill_switch(self) -> None:
        """Halt all operations and revert to manual mode.

        Persists state to disk so it survives container restarts.
        """
        self._kill_switch_active = True
        self._persist_kill_switch_state(activated=True)

    def deactivate_kill_switch(self) -> None:
        """Restore normal operation (returns to configured autonomy level)."""
        self._kill_switch_active = False
        self._persist_kill_switch_state(activated=False)

    def is_kill_switch_active(self) -> bool:
        """Check if the kill switch is currently engaged."""
        return self._kill_switch_active

    # ── Action Classification ─────────────────────────────────────

    @staticmethod
    def _classify_action(action_type: str) -> ActionType:
        """Classify an action into its approval tier.

        Unknown actions default to EXTERNAL (most restrictive) for safety.
        """
        if action_type in INTERNAL_ACTIONS:
            return ActionType.INTERNAL
        if action_type in CREATION_ACTIONS:
            return ActionType.CREATION
        if action_type in EXTERNAL_ACTIONS:
            return ActionType.EXTERNAL
        # Unknown actions are treated as external for safety
        return ActionType.EXTERNAL

    # ── Kill Switch Persistence ───────────────────────────────────

    def _persist_kill_switch_state(self, activated: bool) -> None:
        """Write kill switch state to disk as JSON."""
        state = {
            "activated": activated,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "previous_level": self._config.level,
        }
        self._kill_switch_path.write_text(
            json.dumps(state, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def _load_kill_switch_state(self) -> bool:
        """Load kill switch state from disk. Returns False if no state file."""
        if not self._kill_switch_path.exists():
            return False
        try:
            data = json.loads(self._kill_switch_path.read_text(encoding="utf-8"))
            return bool(data.get("activated", False))
        except (json.JSONDecodeError, OSError):
            return False
