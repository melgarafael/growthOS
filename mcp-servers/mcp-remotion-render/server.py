"""GrowthOS MCP Remotion Render Server.

Renders videos via Remotion CLI through MCP tools.
Supports 6 composition templates, preview stills, and raw CLI passthrough.

Security: All subprocess calls use asyncio.create_subprocess_exec (not shell=True)
to prevent command injection. Arguments are passed as a list, never interpolated
into a shell string.
"""

import asyncio
import json
import os
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP

# Add shared-lib to path for cross-package imports
_shared_lib = str(Path(__file__).resolve().parent.parent.parent / "shared-lib")
sys.path.insert(0, _shared_lib)

# --- Template Registry ---

TEMPLATE_REGISTRY = {
    "ReelTips": {
        "name": "ReelTips",
        "description": "Animated tips reel (vertical 9:16, 15-60s)",
        "aspect_ratio": "9:16",
        "default_fps": 30,
        "min_duration": 15,
        "max_duration": 60,
    },
    "ReelBeforeAfter": {
        "name": "ReelBeforeAfter",
        "description": "Before/after comparison (vertical 9:16, 15-30s)",
        "aspect_ratio": "9:16",
        "default_fps": 30,
        "min_duration": 15,
        "max_duration": 30,
    },
    "ReelNumbers": {
        "name": "ReelNumbers",
        "description": "Animated statistics (vertical 9:16, 15-30s)",
        "aspect_ratio": "9:16",
        "default_fps": 30,
        "min_duration": 15,
        "max_duration": 30,
    },
    "ExplainerSteps": {
        "name": "ExplainerSteps",
        "description": "Step-by-step tutorial (horizontal 16:9, 60-180s)",
        "aspect_ratio": "16:9",
        "default_fps": 30,
        "min_duration": 60,
        "max_duration": 180,
    },
    "ExplainerDemo": {
        "name": "ExplainerDemo",
        "description": "Product demo showcase (horizontal 16:9, 30-120s)",
        "aspect_ratio": "16:9",
        "default_fps": 30,
        "min_duration": 30,
        "max_duration": 120,
    },
    "CarouselAnimated": {
        "name": "CarouselAnimated",
        "description": "Animated carousel slides (4:5, 15-60s)",
        "aspect_ratio": "4:5",
        "default_fps": 30,
        "min_duration": 15,
        "max_duration": 60,
    },
}

# --- Initialization ---

mcp = FastMCP("growthos-remotion-render")


# --- Internal Helpers ---


def _get_remotion_project_dir() -> Path:
    """Find the remotion/ project directory relative to growthOS root."""
    # Navigate from mcp-servers/mcp-remotion-render/ up to growthOS/
    growthos_root = Path(__file__).resolve().parent.parent.parent
    remotion_dir = growthos_root / "remotion"
    if not remotion_dir.exists():
        raise FileNotFoundError(
            f"Remotion project directory not found at {remotion_dir}. "
            "Ensure the remotion/ directory exists inside growthOS/."
        )
    return remotion_dir


def _get_output_dir(timestamp: str | None = None) -> Path:
    """Get or create the output directory for rendered videos."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    growthos_root = Path(__file__).resolve().parent.parent.parent
    output_dir = growthos_root.parent / ".growthOS" / "output" / "videos" / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _write_temp_props(props: dict) -> Path:
    """Write props dict to a temporary JSON file and return the path."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", prefix="remotion_props_", delete=False
    )
    json.dump(props, tmp)
    tmp.close()
    return Path(tmp.name)


def _check_disk_space(min_mb: int = 500) -> bool:
    """Check if there is enough free disk space for rendering."""
    stat = os.statvfs("/")
    free_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)
    return free_mb >= min_mb


def _parse_render_output(stdout: str) -> dict:
    """Extract metadata from Remotion CLI stdout."""
    result = {}
    for line in stdout.splitlines():
        lower = line.lower()
        if "duration" in lower:
            parts = lower.split()
            for i, part in enumerate(parts):
                if part == "duration" and i + 1 < len(parts):
                    try:
                        result["duration_seconds"] = float(
                            parts[i + 1].rstrip("s").rstrip(",")
                        )
                    except ValueError:
                        pass
        if "rendered" in lower and "frame" in lower:
            result["render_completed"] = True
    return result


# --- MCP Tools ---


@mcp.tool()
async def render_video(
    template: str,
    props: dict,
    output_name: str | None = None,
    format: str = "mp4",
) -> dict:
    """Render a video using a Remotion composition template.

    Args:
        template: Remotion composition name (e.g. ReelTips, ExplainerSteps)
        props: Composition props (brand, scenes, etc.) as a dictionary
        output_name: Optional output filename (without extension)
        format: Output format, default "mp4"
    """
    # Validate template
    if template not in TEMPLATE_REGISTRY:
        available = ", ".join(sorted(TEMPLATE_REGISTRY.keys()))
        raise ValueError(
            f"Unknown template '{template}'. Available templates: {available}"
        )

    # Check disk space
    if not _check_disk_space():
        raise RuntimeError(
            "Insufficient disk space. At least 500MB free space required for rendering."
        )

    # Prepare paths
    remotion_dir = _get_remotion_project_dir()
    props_path = _write_temp_props(props)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = _get_output_dir(timestamp)

    if output_name is None:
        output_name = f"{template.lower()}_{timestamp}"
    output_file = output_dir / f"{output_name}.{format}"

    # Build CLI command as argument list (safe from injection)
    cmd = [
        "npx",
        "remotion",
        "render",
        "src/Root.tsx",
        template,
        str(output_file),
        "--props",
        str(props_path),
        "--codec",
        "h264",
    ]

    start_time = time.time()
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(remotion_dir),
        )
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=300
        )
    except asyncio.TimeoutError:
        process.kill()
        raise RuntimeError(
            f"Render timed out after 300 seconds for template '{template}'. "
            "Consider reducing video duration or complexity."
        )
    except FileNotFoundError:
        raise RuntimeError(
            "npx command not found. Ensure Node.js is installed and in PATH."
        )
    finally:
        # Clean up temp props file
        props_path.unlink(missing_ok=True)

    render_time = time.time() - start_time

    if process.returncode != 0:
        error_msg = stderr.decode() if stderr else "Unknown error"
        raise RuntimeError(
            f"Remotion render failed (exit code {process.returncode}): {error_msg}"
        )

    # Verify output exists
    if not output_file.exists():
        raise RuntimeError(
            f"Render completed but output file not found at {output_file}"
        )

    # Get file metadata
    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    parsed = _parse_render_output(stdout.decode() if stdout else "")

    # Save storyboard and composition alongside video
    composition_path = output_dir / "composition.json"
    with open(composition_path, "w") as f:
        json.dump(
            {"template": template, "props": props, "format": format},
            f,
            indent=2,
        )

    return {
        "path": str(output_file),
        "duration_seconds": parsed.get("duration_seconds"),
        "file_size_mb": round(file_size_mb, 2),
        "render_time_seconds": round(render_time, 2),
    }


@mcp.tool()
async def list_templates() -> dict:
    """List all available Remotion composition templates with metadata.

    Returns registry of 6 templates including name, aspect ratio,
    default FPS, duration range, and description.
    """
    return {
        "templates": TEMPLATE_REGISTRY,
        "count": len(TEMPLATE_REGISTRY),
    }


@mcp.tool()
async def preview_composition(
    template: str,
    props: dict,
    frame: int = 0,
) -> dict:
    """Render a single frame preview (PNG still) from a composition.

    Args:
        template: Remotion composition name
        props: Composition props as a dictionary
        frame: Frame number to render (default: 0, first frame)
    """
    # Validate template
    if template not in TEMPLATE_REGISTRY:
        available = ", ".join(sorted(TEMPLATE_REGISTRY.keys()))
        raise ValueError(
            f"Unknown template '{template}'. Available templates: {available}"
        )

    if frame < 0:
        raise ValueError(f"Frame number must be non-negative, got {frame}")

    remotion_dir = _get_remotion_project_dir()
    props_path = _write_temp_props(props)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = _get_output_dir(timestamp)
    output_file = output_dir / "preview.png"

    # Build CLI command as argument list (safe from injection)
    cmd = [
        "npx",
        "remotion",
        "still",
        "src/Root.tsx",
        template,
        str(output_file),
        "--props",
        str(props_path),
        "--frame",
        str(frame),
    ]

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(remotion_dir),
        )
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=120
        )
    except asyncio.TimeoutError:
        process.kill()
        raise RuntimeError(
            f"Preview render timed out after 120 seconds for template '{template}'."
        )
    except FileNotFoundError:
        raise RuntimeError(
            "npx command not found. Ensure Node.js is installed and in PATH."
        )
    finally:
        props_path.unlink(missing_ok=True)

    if process.returncode != 0:
        error_msg = stderr.decode() if stderr else "Unknown error"
        raise RuntimeError(
            f"Remotion still render failed (exit code {process.returncode}): {error_msg}"
        )

    if not output_file.exists():
        raise RuntimeError(
            f"Preview render completed but output file not found at {output_file}"
        )

    return {"path": str(output_file)}


@mcp.tool()
async def render_custom(
    composition_id: str,
    output_path: str,
    extra_args: list[str] | None = None,
) -> dict:
    """Raw Remotion CLI passthrough for advanced rendering control.

    Args:
        composition_id: Remotion composition ID to render
        output_path: Full output file path
        extra_args: Optional extra CLI arguments (e.g. ["--codec", "prores"])
    """
    remotion_dir = _get_remotion_project_dir()

    # Build CLI command as argument list (safe from injection)
    cmd = [
        "npx",
        "remotion",
        "render",
        "src/Root.tsx",
        composition_id,
        output_path,
    ]
    if extra_args:
        cmd.extend(extra_args)

    start_time = time.time()
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(remotion_dir),
        )
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=300
        )
    except asyncio.TimeoutError:
        process.kill()
        raise RuntimeError(
            f"Custom render timed out after 300 seconds for composition '{composition_id}'."
        )
    except FileNotFoundError:
        raise RuntimeError(
            "npx command not found. Ensure Node.js is installed and in PATH."
        )

    render_time = time.time() - start_time

    if process.returncode != 0:
        error_msg = stderr.decode() if stderr else "Unknown error"
        raise RuntimeError(
            f"Custom render failed (exit code {process.returncode}): {error_msg}"
        )

    return {
        "path": output_path,
        "render_time_seconds": round(render_time, 2),
    }
