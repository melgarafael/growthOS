"""Tests for MCP server tool responses."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
_shared_lib = str(Path(__file__).resolve().parent.parent.parent.parent / "shared-lib")
sys.path.insert(0, _shared_lib)

# We test the server tools by importing them and calling directly (they are async).
import server as srv  # noqa: E402


@pytest.fixture(autouse=True)
def setup_vault(tmp_path, monkeypatch):
    """Point the server's VaultOperations at a temp directory."""
    vault_dir = tmp_path / "vault"
    vault_dir.mkdir()
    audit_dir = tmp_path / "audit"
    audit_dir.mkdir()
    monkeypatch.setenv("GROWTHOS_AUDIT_DIR", str(audit_dir))

    from vault_ops import VaultOperations

    new_vault = VaultOperations(vault_path=str(vault_dir))
    monkeypatch.setattr(srv, "vault", new_vault)


# ------------------------------------------------------------------
# CREATE
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_note_success():
    result = await srv.create_note(
        path="test-note",
        title="Test Note",
        content="Hello world",
        tags=["test"],
        note_type="idea",
        status="draft",
    )
    assert result["status"] == "success"
    assert "test-note" in result["message"]


@pytest.mark.asyncio
async def test_create_note_duplicate():
    await srv.create_note(path="dup", title="Dup", content="First")
    result = await srv.create_note(path="dup", title="Dup", content="Second")
    assert result["status"] == "error"


@pytest.mark.asyncio
async def test_create_note_with_platform():
    result = await srv.create_note(
        path="social",
        title="Social",
        content="Post",
        platform="twitter",
    )
    assert result["status"] == "success"


# ------------------------------------------------------------------
# READ
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_read_note_success():
    await srv.create_note(path="readable", title="Readable", content="Body")
    result = await srv.read_note(path="readable")
    assert result["status"] == "success"
    assert result["content"] == "Body"
    assert result["frontmatter"]["title"] == "Readable"


@pytest.mark.asyncio
async def test_read_note_not_found():
    result = await srv.read_note(path="missing")
    assert result["status"] == "error"


# ------------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_update_note_content():
    await srv.create_note(path="upd", title="Upd", content="Old")
    result = await srv.update_note(path="upd", content="New")
    assert result["status"] == "success"
    read_result = await srv.read_note(path="upd")
    assert read_result["content"] == "New"


@pytest.mark.asyncio
async def test_update_note_frontmatter():
    await srv.create_note(path="upd2", title="Upd2", content="Body")
    result = await srv.update_note(
        path="upd2", frontmatter_updates={"status": "published"}
    )
    assert result["status"] == "success"
    read_result = await srv.read_note(path="upd2")
    assert read_result["frontmatter"]["status"] == "published"


@pytest.mark.asyncio
async def test_update_note_not_found():
    result = await srv.update_note(path="ghost", content="Nothing")
    assert result["status"] == "error"


# ------------------------------------------------------------------
# DELETE
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_delete_note_success():
    await srv.create_note(path="del", title="Del", content="Gone")
    result = await srv.delete_note(path="del")
    assert result["status"] == "success"
    read_result = await srv.read_note(path="del")
    assert read_result["status"] == "error"


@pytest.mark.asyncio
async def test_delete_note_not_found():
    result = await srv.delete_note(path="nope")
    assert result["status"] == "error"


# ------------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_search_notes():
    await srv.create_note(path="s1", title="AI Note", content="About AI")
    await srv.create_note(path="s2", title="Cooking", content="About food")
    result = await srv.search_notes(query="AI")
    assert result["status"] == "success"
    assert result["count"] == 1


@pytest.mark.asyncio
async def test_search_with_tags():
    await srv.create_note(
        path="tag1", title="T1", content="Content", tags=["python"]
    )
    await srv.create_note(
        path="tag2", title="T2", content="Content", tags=["cooking"]
    )
    result = await srv.search_notes(query="Content", tags=["python"])
    assert result["count"] == 1


@pytest.mark.asyncio
async def test_search_no_results():
    result = await srv.search_notes(query="nonexistent-xyz")
    assert result["status"] == "success"
    assert result["count"] == 0


# ------------------------------------------------------------------
# LIST
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_notes_all():
    await srv.create_note(path="l1", title="L1", content="C1")
    await srv.create_note(path="l2", title="L2", content="C2")
    result = await srv.list_notes()
    assert result["status"] == "success"
    assert result["count"] == 2


@pytest.mark.asyncio
async def test_list_notes_folder():
    await srv.create_note(path="f1/n1", title="N1", content="C")
    await srv.create_note(path="f2/n2", title="N2", content="C")
    result = await srv.list_notes(folder="f1")
    assert result["count"] == 1


@pytest.mark.asyncio
async def test_list_notes_empty():
    result = await srv.list_notes()
    assert result["status"] == "success"
    assert result["count"] == 0


# ------------------------------------------------------------------
# GET FRONTMATTER
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_frontmatter_success():
    await srv.create_note(
        path="fm", title="FM", content="Body", tags=["a"], note_type="ref"
    )
    result = await srv.get_frontmatter(path="fm")
    assert result["status"] == "success"
    assert result["frontmatter"]["title"] == "FM"
    assert result["frontmatter"]["tags"] == ["a"]
    assert result["frontmatter"]["type"] == "ref"


@pytest.mark.asyncio
async def test_get_frontmatter_not_found():
    result = await srv.get_frontmatter(path="missing")
    assert result["status"] == "error"
