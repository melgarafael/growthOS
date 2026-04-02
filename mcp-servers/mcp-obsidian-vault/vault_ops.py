"""Obsidian vault operations — CRUD, search, and frontmatter management."""

import hashlib
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import frontmatter

# Add shared-lib to path for cross-package imports
_shared_lib = str(Path(__file__).resolve().parent.parent.parent / "shared-lib")
sys.path.insert(0, _shared_lib)

from growthOS_shared import AuditLogger  # noqa: E402

# Default frontmatter schema fields
_FRONTMATTER_DEFAULTS = {
    "title": "",
    "date": "",
    "tags": [],
    "type": "",
    "status": "",
}

# Optional fields that are included only when provided
_OPTIONAL_FIELDS = {"platform"}


def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


class VaultOperations:
    """File-based CRUD operations on an Obsidian-compatible markdown vault.

    All paths are relative to ``vault_path`` and use ``.md`` extension.
    Frontmatter is stored as YAML at the top of each file.
    """

    def __init__(self, vault_path: Optional[str] = None) -> None:
        self.vault_path = Path(
            vault_path or os.environ.get("GROWTHOS_VAULT_PATH", "./vault/")
        )
        self.audit = AuditLogger()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve(self, path: str) -> Path:
        """Resolve a relative note path to an absolute path inside the vault.

        Ensures the resolved path does not escape the vault directory.
        Appends ``.md`` extension if missing.
        """
        if not path.endswith(".md"):
            path = f"{path}.md"
        resolved = (self.vault_path / path).resolve()
        vault_resolved = self.vault_path.resolve()
        if not str(resolved).startswith(str(vault_resolved)):
            raise ValueError(f"Path traversal detected: {path}")
        return resolved

    def _build_frontmatter(self, title: str, extra: Optional[dict] = None) -> dict:
        """Build a frontmatter dict with schema defaults."""
        fm: dict = {
            **_FRONTMATTER_DEFAULTS,
            "title": title,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }
        if extra:
            for key, value in extra.items():
                if key in _FRONTMATTER_DEFAULTS or key in _OPTIONAL_FIELDS:
                    fm[key] = value
                # Allow arbitrary extra keys — Obsidian is flexible
                else:
                    fm[key] = value
        return fm

    def _note_summary(self, filepath: Path) -> dict:
        """Return a lightweight summary dict for listing/search results."""
        post = frontmatter.load(str(filepath))
        rel = filepath.relative_to(self.vault_path.resolve())
        return {
            "path": str(rel),
            "frontmatter": dict(post.metadata),
            "content_preview": post.content[:200] if post.content else "",
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create(
        self,
        path: str,
        title: str,
        content: str,
        frontmatter_data: Optional[dict] = None,
    ) -> Path:
        """Create a new note at *path* (relative to vault root).

        Raises ``FileExistsError`` if the note already exists.
        Returns the absolute ``Path`` to the created file.
        """
        filepath = self._resolve(path)
        if filepath.exists():
            raise FileExistsError(f"Note already exists: {path}")

        filepath.parent.mkdir(parents=True, exist_ok=True)

        fm = self._build_frontmatter(title, frontmatter_data)
        post = frontmatter.Post(content, **fm)
        filepath.write_text(frontmatter.dumps(post), encoding="utf-8")

        self.audit.log_action(
            action="create_note",
            platform="obsidian-vault",
            content_hash=_content_hash(content),
            status="success",
            metadata={"path": path, "title": title},
        )
        return filepath

    def read(self, path: str) -> dict:
        """Read a note and return its frontmatter and content.

        Returns ``{"frontmatter": dict, "content": str}``.
        Raises ``FileNotFoundError`` if the note does not exist.
        """
        filepath = self._resolve(path)
        if not filepath.exists():
            raise FileNotFoundError(f"Note not found: {path}")

        post = frontmatter.load(str(filepath))

        self.audit.log_action(
            action="read_note",
            platform="obsidian-vault",
            content_hash=_content_hash(post.content),
            status="success",
            metadata={"path": path},
        )
        return {
            "frontmatter": dict(post.metadata),
            "content": post.content,
        }

    def update(
        self,
        path: str,
        content: Optional[str] = None,
        frontmatter_updates: Optional[dict] = None,
    ) -> Path:
        """Update an existing note's content and/or frontmatter.

        Only the fields supplied in *frontmatter_updates* are changed;
        existing fields are preserved.
        Raises ``FileNotFoundError`` if the note does not exist.
        Returns the absolute ``Path`` to the updated file.
        """
        filepath = self._resolve(path)
        if not filepath.exists():
            raise FileNotFoundError(f"Note not found: {path}")

        post = frontmatter.load(str(filepath))

        if content is not None:
            post.content = content
        if frontmatter_updates:
            for key, value in frontmatter_updates.items():
                post.metadata[key] = value

        filepath.write_text(frontmatter.dumps(post), encoding="utf-8")

        self.audit.log_action(
            action="update_note",
            platform="obsidian-vault",
            content_hash=_content_hash(post.content),
            status="success",
            metadata={
                "path": path,
                "content_updated": content is not None,
                "frontmatter_keys": list(frontmatter_updates.keys())
                if frontmatter_updates
                else [],
            },
        )
        return filepath

    def delete(self, path: str) -> bool:
        """Delete a note from the vault.

        Returns ``True`` on success.
        Raises ``FileNotFoundError`` if the note does not exist.
        """
        filepath = self._resolve(path)
        if not filepath.exists():
            raise FileNotFoundError(f"Note not found: {path}")

        filepath.unlink()

        self.audit.log_action(
            action="delete_note",
            platform="obsidian-vault",
            content_hash="deleted",
            status="success",
            metadata={"path": path},
        )
        return True

    def search(
        self,
        query: str,
        tags: Optional[list[str]] = None,
        folder: Optional[str] = None,
    ) -> list[dict]:
        """Search notes by content/title substring and optional tag/folder filters.

        Returns a list of summary dicts for matching notes.
        """
        results: list[dict] = []
        search_root = self.vault_path.resolve()
        if folder:
            search_root = (self.vault_path / folder).resolve()
            if not search_root.exists():
                return results

        pattern = re.compile(re.escape(query), re.IGNORECASE)

        for filepath in search_root.rglob("*.md"):
            try:
                post = frontmatter.load(str(filepath))
            except Exception:
                continue

            # Tag filter
            if tags:
                note_tags = post.metadata.get("tags", [])
                if isinstance(note_tags, str):
                    note_tags = [note_tags]
                if not any(t in note_tags for t in tags):
                    continue

            # Text search across title, content, and frontmatter values
            title = post.metadata.get("title", "")
            searchable = f"{title}\n{post.content}"
            if pattern.search(searchable):
                rel = filepath.relative_to(self.vault_path.resolve())
                results.append(
                    {
                        "path": str(rel),
                        "frontmatter": dict(post.metadata),
                        "content_preview": post.content[:200]
                        if post.content
                        else "",
                    }
                )

        self.audit.log_action(
            action="search_notes",
            platform="obsidian-vault",
            content_hash=_content_hash(query),
            status="success",
            metadata={
                "query": query,
                "tags": tags,
                "folder": folder,
                "results_count": len(results),
            },
        )
        return results

    def list_notes(
        self, folder: Optional[str] = None, recursive: bool = True
    ) -> list[dict]:
        """List all notes in the vault or a specific folder.

        Returns a list of summary dicts.
        """
        search_root = self.vault_path.resolve()
        if folder:
            search_root = (self.vault_path / folder).resolve()
            if not search_root.exists():
                return []

        glob_pattern = "**/*.md" if recursive else "*.md"
        results: list[dict] = []

        for filepath in sorted(search_root.glob(glob_pattern)):
            try:
                results.append(self._note_summary(filepath))
            except Exception:
                # Skip files that cannot be parsed
                continue

        self.audit.log_action(
            action="list_notes",
            platform="obsidian-vault",
            content_hash="list",
            status="success",
            metadata={
                "folder": folder,
                "recursive": recursive,
                "count": len(results),
            },
        )
        return results

    def get_frontmatter(self, path: str) -> dict:
        """Return only the frontmatter metadata for a note.

        Raises ``FileNotFoundError`` if the note does not exist.
        """
        filepath = self._resolve(path)
        if not filepath.exists():
            raise FileNotFoundError(f"Note not found: {path}")

        post = frontmatter.load(str(filepath))
        return dict(post.metadata)
