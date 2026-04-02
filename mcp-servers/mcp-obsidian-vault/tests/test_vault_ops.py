"""Tests for VaultOperations — CRUD, search, and frontmatter handling."""

import os
import sys
from pathlib import Path

import pytest

# Ensure imports resolve correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
_shared_lib = str(Path(__file__).resolve().parent.parent.parent.parent / "shared-lib")
sys.path.insert(0, _shared_lib)

from vault_ops import VaultOperations  # noqa: E402


@pytest.fixture
def vault(tmp_path):
    """Create a VaultOperations instance backed by a temp directory."""
    vault_dir = tmp_path / "vault"
    vault_dir.mkdir()
    # Use a temp audit dir so audit logs don't pollute the real filesystem
    audit_dir = tmp_path / "audit"
    audit_dir.mkdir()
    os.environ["GROWTHOS_AUDIT_DIR"] = str(audit_dir)
    ops = VaultOperations(vault_path=str(vault_dir))
    yield ops
    os.environ.pop("GROWTHOS_AUDIT_DIR", None)


# ------------------------------------------------------------------
# CREATE
# ------------------------------------------------------------------


class TestCreate:
    def test_create_basic(self, vault):
        filepath = vault.create("hello", "Hello World", "Some content")
        assert filepath.exists()
        assert filepath.name == "hello.md"

    def test_create_with_md_extension(self, vault):
        filepath = vault.create("hello.md", "Hello", "Content")
        assert filepath.exists()
        assert filepath.name == "hello.md"

    def test_create_with_frontmatter(self, vault):
        vault.create(
            "note",
            "My Note",
            "Body text",
            frontmatter_data={"tags": ["ai", "growth"], "type": "idea", "status": "draft"},
        )
        data = vault.read("note")
        assert data["frontmatter"]["title"] == "My Note"
        assert data["frontmatter"]["tags"] == ["ai", "growth"]
        assert data["frontmatter"]["type"] == "idea"
        assert data["frontmatter"]["status"] == "draft"
        assert "date" in data["frontmatter"]

    def test_create_with_platform(self, vault):
        vault.create(
            "social",
            "Social Post",
            "Content",
            frontmatter_data={"platform": "linkedin"},
        )
        data = vault.read("social")
        assert data["frontmatter"]["platform"] == "linkedin"

    def test_create_in_subfolder(self, vault):
        filepath = vault.create("projects/deep/note", "Deep Note", "Deep content")
        assert filepath.exists()
        assert "projects" in str(filepath)

    def test_create_duplicate_raises(self, vault):
        vault.create("dup", "First", "First content")
        with pytest.raises(FileExistsError):
            vault.create("dup", "Second", "Second content")

    def test_create_path_traversal_blocked(self, vault):
        with pytest.raises(ValueError, match="Path traversal"):
            vault.create("../../etc/passwd", "Evil", "hack")


# ------------------------------------------------------------------
# READ
# ------------------------------------------------------------------


class TestRead:
    def test_read_existing(self, vault):
        vault.create("readable", "Readable", "Read me")
        data = vault.read("readable")
        assert data["content"] == "Read me"
        assert data["frontmatter"]["title"] == "Readable"

    def test_read_nonexistent_raises(self, vault):
        with pytest.raises(FileNotFoundError):
            vault.read("does-not-exist")

    def test_read_preserves_content(self, vault):
        long_content = "Line 1\n\nLine 2\n\n## Heading\n\n- item"
        vault.create("long", "Long", long_content)
        data = vault.read("long")
        assert data["content"] == long_content


# ------------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------------


class TestUpdate:
    def test_update_content(self, vault):
        vault.create("updatable", "Updatable", "Old content")
        vault.update("updatable", content="New content")
        data = vault.read("updatable")
        assert data["content"] == "New content"
        assert data["frontmatter"]["title"] == "Updatable"

    def test_update_frontmatter(self, vault):
        vault.create("updatable2", "Note", "Body")
        vault.update("updatable2", frontmatter_updates={"status": "published", "tags": ["new"]})
        data = vault.read("updatable2")
        assert data["frontmatter"]["status"] == "published"
        assert data["frontmatter"]["tags"] == ["new"]
        assert data["frontmatter"]["title"] == "Note"  # preserved

    def test_update_both(self, vault):
        vault.create("updatable3", "Note", "Old")
        vault.update("updatable3", content="New", frontmatter_updates={"type": "article"})
        data = vault.read("updatable3")
        assert data["content"] == "New"
        assert data["frontmatter"]["type"] == "article"

    def test_update_nonexistent_raises(self, vault):
        with pytest.raises(FileNotFoundError):
            vault.update("ghost", content="Nothing")


# ------------------------------------------------------------------
# DELETE
# ------------------------------------------------------------------


class TestDelete:
    def test_delete_existing(self, vault):
        vault.create("deleteme", "Delete Me", "Goodbye")
        assert vault.delete("deleteme") is True
        with pytest.raises(FileNotFoundError):
            vault.read("deleteme")

    def test_delete_nonexistent_raises(self, vault):
        with pytest.raises(FileNotFoundError):
            vault.delete("nope")


# ------------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------------


class TestSearch:
    def test_search_by_content(self, vault):
        vault.create("s1", "Alpha", "This is about artificial intelligence")
        vault.create("s2", "Beta", "This is about cooking")
        results = vault.search("artificial")
        assert len(results) == 1
        assert "s1.md" in results[0]["path"]

    def test_search_by_title(self, vault):
        vault.create("s3", "Machine Learning Guide", "Body")
        results = vault.search("Machine Learning")
        assert len(results) == 1

    def test_search_case_insensitive(self, vault):
        vault.create("s4", "Title", "UPPERCASE content here")
        results = vault.search("uppercase")
        assert len(results) == 1

    def test_search_by_tags(self, vault):
        vault.create("t1", "Tagged", "Content", {"tags": ["python", "ai"]})
        vault.create("t2", "Other", "Content", {"tags": ["cooking"]})
        results = vault.search("Content", tags=["python"])
        assert len(results) == 1
        assert "t1.md" in results[0]["path"]

    def test_search_in_folder(self, vault):
        vault.create("projects/p1", "Project 1", "Work stuff")
        vault.create("personal/p2", "Personal", "Work stuff")
        results = vault.search("Work", folder="projects")
        assert len(results) == 1
        assert "projects" in results[0]["path"]

    def test_search_no_results(self, vault):
        vault.create("lonely", "Lonely Note", "Nothing matches")
        results = vault.search("zzzznotfound")
        assert len(results) == 0

    def test_search_nonexistent_folder(self, vault):
        results = vault.search("anything", folder="nonexistent")
        assert results == []


# ------------------------------------------------------------------
# LIST
# ------------------------------------------------------------------


class TestListNotes:
    def test_list_all(self, vault):
        vault.create("a", "A", "Content A")
        vault.create("b", "B", "Content B")
        notes = vault.list_notes()
        assert len(notes) == 2

    def test_list_folder(self, vault):
        vault.create("folder1/n1", "N1", "Content")
        vault.create("folder2/n2", "N2", "Content")
        notes = vault.list_notes(folder="folder1")
        assert len(notes) == 1

    def test_list_recursive(self, vault):
        vault.create("deep/a/b/note", "Deep", "Content")
        notes = vault.list_notes(recursive=True)
        assert len(notes) == 1

    def test_list_non_recursive(self, vault):
        vault.create("top", "Top", "Content")
        vault.create("sub/nested", "Nested", "Content")
        notes = vault.list_notes(recursive=False)
        assert len(notes) == 1
        assert "top.md" in notes[0]["path"]

    def test_list_empty_vault(self, vault):
        notes = vault.list_notes()
        assert notes == []

    def test_list_nonexistent_folder(self, vault):
        notes = vault.list_notes(folder="nonexistent")
        assert notes == []


# ------------------------------------------------------------------
# GET FRONTMATTER
# ------------------------------------------------------------------


class TestGetFrontmatter:
    def test_get_frontmatter(self, vault):
        vault.create("fm", "FM Note", "Body", {"tags": ["test"], "type": "idea"})
        fm = vault.get_frontmatter("fm")
        assert fm["title"] == "FM Note"
        assert fm["tags"] == ["test"]
        assert fm["type"] == "idea"
        assert "date" in fm

    def test_get_frontmatter_nonexistent(self, vault):
        with pytest.raises(FileNotFoundError):
            vault.get_frontmatter("missing")

    def test_frontmatter_defaults(self, vault):
        vault.create("defaults", "Defaults", "Body")
        fm = vault.get_frontmatter("defaults")
        assert fm["title"] == "Defaults"
        assert fm["tags"] == []
        assert fm["type"] == ""
        assert fm["status"] == ""
        assert "date" in fm


# ------------------------------------------------------------------
# ENV VAR VAULT PATH
# ------------------------------------------------------------------


class TestEnvVarPath:
    def test_vault_path_from_env(self, tmp_path):
        vault_dir = tmp_path / "env_vault"
        vault_dir.mkdir()
        audit_dir = tmp_path / "audit"
        audit_dir.mkdir()
        os.environ["GROWTHOS_VAULT_PATH"] = str(vault_dir)
        os.environ["GROWTHOS_AUDIT_DIR"] = str(audit_dir)
        try:
            ops = VaultOperations()
            assert ops.vault_path == Path(str(vault_dir))
        finally:
            os.environ.pop("GROWTHOS_VAULT_PATH", None)
            os.environ.pop("GROWTHOS_AUDIT_DIR", None)
