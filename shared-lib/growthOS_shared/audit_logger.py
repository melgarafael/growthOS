"""Append-only JSONL audit trail."""

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class AuditEntry:
    timestamp: str
    action: str
    platform: str
    content_hash: str
    user: str
    status: str
    metadata: dict = field(default_factory=dict)


class AuditLogger:
    """Writes one JSON object per line to daily JSONL files.

    File naming: audit-YYYY-MM-DD.jsonl
    Directory: GROWTHOS_AUDIT_DIR env var, fallback to .growthOS/audit/
    """

    def __init__(self, log_dir: Optional[str] = None) -> None:
        self.log_dir = Path(
            log_dir or os.environ.get("GROWTHOS_AUDIT_DIR", ".growthOS/audit/")
        )
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _log_path(self, date: datetime) -> Path:
        return self.log_dir / f"audit-{date.strftime('%Y-%m-%d')}.jsonl"

    def log_action(
        self,
        action: str,
        platform: str,
        content_hash: str,
        user: str = "system",
        status: str = "success",
        metadata: Optional[dict] = None,
    ) -> None:
        now = datetime.now(timezone.utc)
        entry = AuditEntry(
            timestamp=now.isoformat(),
            action=action,
            platform=platform,
            content_hash=content_hash,
            user=user,
            status=status,
            metadata=metadata or {},
        )
        path = self._log_path(now)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

    def get_entries(self, filters: Optional[dict] = None) -> list[AuditEntry]:
        """Read all entries, optionally filtering by field values.

        filters: dict of {field_name: value} — only entries matching ALL filters are returned.
        """
        entries: list[AuditEntry] = []
        for path in sorted(self.log_dir.glob("audit-*.jsonl")):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    if filters:
                        if not all(data.get(k) == v for k, v in filters.items()):
                            continue
                    entries.append(AuditEntry(**data))
        return entries
