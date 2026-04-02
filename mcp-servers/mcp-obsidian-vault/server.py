"""GrowthOS MCP Obsidian Vault Server.

Obsidian-compatible markdown vault operations via MCP tools.
Integrates with shared-lib for audit logging.
"""

import sys
from pathlib import Path

from fastmcp import FastMCP

# Add current directory for local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from vault_ops import VaultOperations

# --- Initialization ---

mcp = FastMCP("growthos-obsidian-vault")
vault = VaultOperations()


# --- MCP Tools ---


@mcp.tool()
async def create_note(
    path: str,
    title: str,
    content: str,
    tags: list[str] | None = None,
    note_type: str = "",
    status: str = "",
    platform: str | None = None,
) -> dict:
    """Create a new markdown note in the Obsidian vault.

    Args:
        path: Relative path within the vault (e.g. "projects/my-note")
        title: Note title (stored in frontmatter)
        content: Markdown body content
        tags: Optional list of tags
        note_type: Optional note type (e.g. "idea", "article", "reference")
        status: Optional status (e.g. "draft", "published")
        platform: Optional platform identifier
    """
    try:
        frontmatter_data: dict = {}
        if tags:
            frontmatter_data["tags"] = tags
        if note_type:
            frontmatter_data["type"] = note_type
        if status:
            frontmatter_data["status"] = status
        if platform:
            frontmatter_data["platform"] = platform

        filepath = vault.create(path, title, content, frontmatter_data or None)
        return {
            "status": "success",
            "path": str(filepath),
            "message": f"Note created: {path}",
        }
    except FileExistsError as e:
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": f"Failed to create note: {e}"}


@mcp.tool()
async def read_note(path: str) -> dict:
    """Read a note from the Obsidian vault.

    Args:
        path: Relative path within the vault (e.g. "projects/my-note" or "projects/my-note.md")

    Returns:
        Note frontmatter and content.
    """
    try:
        data = vault.read(path)
        return {"status": "success", **data}
    except FileNotFoundError as e:
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": f"Failed to read note: {e}"}


@mcp.tool()
async def update_note(
    path: str,
    content: str | None = None,
    frontmatter_updates: dict | None = None,
) -> dict:
    """Update an existing note's content and/or frontmatter.

    Args:
        path: Relative path within the vault
        content: New markdown body (replaces existing content if provided)
        frontmatter_updates: Dict of frontmatter fields to update (merged with existing)
    """
    try:
        filepath = vault.update(path, content, frontmatter_updates)
        return {
            "status": "success",
            "path": str(filepath),
            "message": f"Note updated: {path}",
        }
    except FileNotFoundError as e:
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": f"Failed to update note: {e}"}


@mcp.tool()
async def delete_note(path: str) -> dict:
    """Delete a note from the Obsidian vault.

    Args:
        path: Relative path within the vault
    """
    try:
        vault.delete(path)
        return {"status": "success", "message": f"Note deleted: {path}"}
    except FileNotFoundError as e:
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": f"Failed to delete note: {e}"}


@mcp.tool()
async def search_notes(
    query: str,
    tags: list[str] | None = None,
    folder: str | None = None,
) -> dict:
    """Search notes by content, title, and optional filters.

    Args:
        query: Text to search for (case-insensitive substring match)
        tags: Optional list of tags to filter by (OR logic — matches if any tag present)
        folder: Optional folder to restrict search to
    """
    try:
        results = vault.search(query, tags, folder)
        return {
            "status": "success",
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        return {"status": "error", "error": f"Search failed: {e}"}


@mcp.tool()
async def list_notes(
    folder: str | None = None,
    recursive: bool = True,
) -> dict:
    """List all notes in the vault or a specific folder.

    Args:
        folder: Optional folder to list (relative to vault root)
        recursive: Whether to include notes in subfolders (default True)
    """
    try:
        results = vault.list_notes(folder, recursive)
        return {
            "status": "success",
            "notes": results,
            "count": len(results),
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to list notes: {e}"}


@mcp.tool()
async def get_frontmatter(path: str) -> dict:
    """Get only the frontmatter metadata for a note.

    Args:
        path: Relative path within the vault
    """
    try:
        fm = vault.get_frontmatter(path)
        return {"status": "success", "frontmatter": fm}
    except FileNotFoundError as e:
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": f"Failed to get frontmatter: {e}"}


if __name__ == "__main__":
    mcp.run()
