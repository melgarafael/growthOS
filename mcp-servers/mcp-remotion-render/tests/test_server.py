"""Tests for mcp-remotion-render server tools."""

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Setup paths so imports work from test context
_server_dir = str(Path(__file__).resolve().parent.parent)
_shared_lib = str(Path(__file__).resolve().parent.parent.parent.parent / "shared-lib")
sys.path.insert(0, _server_dir)
sys.path.insert(0, _shared_lib)

import server  # noqa: E402


# --- Template Registry Tests ---


class TestListTemplates:
    @pytest.mark.asyncio
    async def test_returns_six_templates(self):
        result = await server.list_templates()
        assert result["count"] == 6
        assert len(result["templates"]) == 6

    @pytest.mark.asyncio
    async def test_templates_have_required_fields(self):
        result = await server.list_templates()
        required_fields = {
            "name",
            "aspect_ratio",
            "default_fps",
            "min_duration",
            "max_duration",
            "description",
        }
        for name, template in result["templates"].items():
            for field in required_fields:
                assert field in template, (
                    f"Template '{name}' missing field '{field}'"
                )

    @pytest.mark.asyncio
    async def test_template_names_match_keys(self):
        result = await server.list_templates()
        for key, template in result["templates"].items():
            assert key == template["name"]

    @pytest.mark.asyncio
    async def test_expected_template_names(self):
        result = await server.list_templates()
        expected = {
            "ReelTips",
            "ReelBeforeAfter",
            "ReelNumbers",
            "ExplainerSteps",
            "ExplainerDemo",
            "CarouselAnimated",
        }
        assert set(result["templates"].keys()) == expected


# --- Render Video Tests ---


class TestRenderVideo:
    @pytest.mark.asyncio
    async def test_invalid_template_raises_error(self):
        with pytest.raises(ValueError, match="Unknown template"):
            await server.render_video(
                template="NonExistent",
                props={"brand": {}, "scenes": []},
            )

    @pytest.mark.asyncio
    async def test_invalid_template_lists_available(self):
        with pytest.raises(ValueError, match="ReelTips"):
            await server.render_video(
                template="FakeTemplate",
                props={},
            )

    @pytest.mark.asyncio
    @patch("server._check_disk_space", return_value=False)
    async def test_insufficient_disk_space_raises(self, mock_disk):
        with pytest.raises(RuntimeError, match="disk space"):
            await server.render_video(
                template="ReelTips",
                props={"brand": {}, "scenes": []},
            )

    @pytest.mark.asyncio
    @patch("server._check_disk_space", return_value=True)
    @patch("server._get_remotion_project_dir")
    @patch("asyncio.create_subprocess_exec")
    async def test_render_video_calls_remotion_cli(
        self, mock_subprocess, mock_project_dir, mock_disk
    ):
        mock_project_dir.return_value = Path("/tmp/test_remotion")

        # Mock successful process
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (
            b"Rendered 900 frames. Duration: 30s",
            b"",
        )
        mock_process.returncode = 0
        mock_process.kill = MagicMock()
        mock_subprocess.return_value = mock_process

        # Create a fake output file so verification passes
        with patch.object(Path, "exists", return_value=True), \
             patch.object(Path, "stat") as mock_stat, \
             patch("builtins.open", MagicMock()):
            mock_stat.return_value = MagicMock(st_size=5 * 1024 * 1024)
            result = await server.render_video(
                template="ReelTips",
                props={"brand": {}, "scenes": []},
                output_name="test_output",
            )

        assert "path" in result
        assert "file_size_mb" in result
        assert "render_time_seconds" in result
        mock_subprocess.assert_called_once()

        # Verify npx remotion render was called
        call_args = mock_subprocess.call_args[0]
        assert call_args[0] == "npx"
        assert call_args[1] == "remotion"
        assert call_args[2] == "render"
        assert "ReelTips" in call_args

    @pytest.mark.asyncio
    @patch("server._check_disk_space", return_value=True)
    @patch("server._get_remotion_project_dir")
    @patch("asyncio.create_subprocess_exec")
    async def test_render_video_timeout_kills_process(
        self, mock_subprocess, mock_project_dir, mock_disk
    ):
        mock_project_dir.return_value = Path("/tmp/test_remotion")

        mock_process = AsyncMock()
        mock_process.communicate.side_effect = asyncio.TimeoutError()
        mock_process.kill = MagicMock()
        mock_subprocess.return_value = mock_process

        with pytest.raises(RuntimeError, match="timed out"):
            await server.render_video(
                template="ReelTips",
                props={},
            )
        mock_process.kill.assert_called_once()


# --- Preview Composition Tests ---


class TestPreviewComposition:
    @pytest.mark.asyncio
    async def test_invalid_template_raises_error(self):
        with pytest.raises(ValueError, match="Unknown template"):
            await server.preview_composition(
                template="BadTemplate",
                props={},
            )

    @pytest.mark.asyncio
    async def test_negative_frame_raises_error(self):
        with pytest.raises(ValueError, match="non-negative"):
            await server.preview_composition(
                template="ReelTips",
                props={},
                frame=-1,
            )

    @pytest.mark.asyncio
    @patch("server._get_remotion_project_dir")
    @patch("asyncio.create_subprocess_exec")
    async def test_preview_calls_remotion_still(
        self, mock_subprocess, mock_project_dir
    ):
        mock_project_dir.return_value = Path("/tmp/test_remotion")

        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b"", b"")
        mock_process.returncode = 0
        mock_process.kill = MagicMock()
        mock_subprocess.return_value = mock_process

        with patch.object(Path, "exists", return_value=True):
            result = await server.preview_composition(
                template="ExplainerSteps",
                props={"brand": {}, "scenes": []},
                frame=10,
            )

        assert "path" in result

        call_args = mock_subprocess.call_args[0]
        assert call_args[0] == "npx"
        assert call_args[1] == "remotion"
        assert call_args[2] == "still"
        assert "ExplainerSteps" in call_args
        assert "10" in call_args


# --- Render Custom Tests ---


class TestRenderCustom:
    @pytest.mark.asyncio
    @patch("server._get_remotion_project_dir")
    @patch("asyncio.create_subprocess_exec")
    async def test_render_custom_basic(self, mock_subprocess, mock_project_dir):
        mock_project_dir.return_value = Path("/tmp/test_remotion")

        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b"", b"")
        mock_process.returncode = 0
        mock_process.kill = MagicMock()
        mock_subprocess.return_value = mock_process

        result = await server.render_custom(
            composition_id="MyCustomComp",
            output_path="/tmp/output.mp4",
        )

        assert result["path"] == "/tmp/output.mp4"
        assert "render_time_seconds" in result

    @pytest.mark.asyncio
    @patch("server._get_remotion_project_dir")
    @patch("asyncio.create_subprocess_exec")
    async def test_render_custom_with_extra_args(
        self, mock_subprocess, mock_project_dir
    ):
        mock_project_dir.return_value = Path("/tmp/test_remotion")

        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b"", b"")
        mock_process.returncode = 0
        mock_process.kill = MagicMock()
        mock_subprocess.return_value = mock_process

        await server.render_custom(
            composition_id="MyComp",
            output_path="/tmp/out.mp4",
            extra_args=["--codec", "prores", "--scale", "2"],
        )

        call_args = mock_subprocess.call_args[0]
        assert "--codec" in call_args
        assert "prores" in call_args
        assert "--scale" in call_args
        assert "2" in call_args

    @pytest.mark.asyncio
    @patch("server._get_remotion_project_dir")
    @patch("asyncio.create_subprocess_exec")
    async def test_render_custom_failure_raises(
        self, mock_subprocess, mock_project_dir
    ):
        mock_project_dir.return_value = Path("/tmp/test_remotion")

        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b"", b"Some error occurred")
        mock_process.returncode = 1
        mock_process.kill = MagicMock()
        mock_subprocess.return_value = mock_process

        with pytest.raises(RuntimeError, match="Custom render failed"):
            await server.render_custom(
                composition_id="BadComp",
                output_path="/tmp/out.mp4",
            )


# --- Internal Helper Tests ---


class TestHelpers:
    def test_get_remotion_project_dir_not_found(self):
        with patch.object(Path, "exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="Remotion project"):
                server._get_remotion_project_dir()

    def test_write_temp_props_creates_valid_json(self):
        props = {"brand": {"name": "Test"}, "scenes": [{"type": "hook"}]}
        props_path = server._write_temp_props(props)
        try:
            assert props_path.exists()
            with open(props_path) as f:
                loaded = json.load(f)
            assert loaded == props
        finally:
            props_path.unlink(missing_ok=True)

    def test_write_temp_props_file_has_json_extension(self):
        props_path = server._write_temp_props({"test": True})
        try:
            assert props_path.suffix == ".json"
        finally:
            props_path.unlink(missing_ok=True)

    def test_check_disk_space_returns_bool(self):
        result = server._check_disk_space(min_mb=500)
        assert isinstance(result, bool)

    def test_check_disk_space_low_threshold(self):
        # With min_mb=0, should always return True
        assert server._check_disk_space(min_mb=0) is True

    def test_parse_render_output_extracts_duration(self):
        stdout = "Rendering...\nDuration 30s\nRendered 900 frames."
        result = server._parse_render_output(stdout)
        assert result.get("duration_seconds") == 30.0

    def test_parse_render_output_empty(self):
        result = server._parse_render_output("")
        assert isinstance(result, dict)

    def test_get_output_dir_creates_directory(self, tmp_path):
        with patch.object(
            Path, "resolve", return_value=tmp_path / "mcp-servers" / "mcp-remotion-render" / "server.py"
        ):
            # Just verify the function doesn't crash with a custom timestamp
            output_dir = server._get_output_dir("20260401_120000")
            assert "20260401_120000" in str(output_dir)
