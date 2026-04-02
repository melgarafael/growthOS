# MCP Remotion Render Server

MCP server for rendering videos via the Remotion CLI. Part of the GrowthOS video production pipeline.

## Tools

| Tool | Description |
|------|-------------|
| `render_video` | Render a video from a template + props. Returns path, duration, file size, render time. |
| `list_templates` | List all 6 available composition templates with metadata. |
| `preview_composition` | Render a single-frame PNG still from a composition. |
| `render_custom` | Raw Remotion CLI passthrough for advanced rendering. |

## Templates

- **ReelTips** -- Animated tips reel (9:16, 15-60s)
- **ReelBeforeAfter** -- Before/after comparison (9:16, 15-30s)
- **ReelNumbers** -- Animated statistics (9:16, 15-30s)
- **ExplainerSteps** -- Step-by-step tutorial (16:9, 60-180s)
- **ExplainerDemo** -- Product demo showcase (16:9, 30-120s)
- **CarouselAnimated** -- Animated carousel slides (4:5, 15-60s)

## Requirements

- Python 3.11+
- Node.js 18+
- Remotion project at `growthOS/remotion/` with compositions installed

## Setup

```bash
pip install -r requirements.txt
cd ../../remotion && npm install
```

## Running

```bash
fastmcp run server.py
```

## Testing

```bash
pytest tests/
```
