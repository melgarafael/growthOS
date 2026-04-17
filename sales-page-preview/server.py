#!/usr/bin/env python3
"""
sales-page-preview/server.py — Flask preview server for Sales Page Pipeline

Run:
    python growthOS/sales-page-preview/server.py

Then open: http://localhost:8061

Features:
    - Serves preview HTML for each phase of the sales page pipeline
    - Shows pipeline progress with phase navigation
    - Approval/revision controls per phase
    - Persists state to growthOS/output/sales-pages/{slug}/state.json
    - Live reload for build phase (Phase 7)
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, render_template_string, abort, redirect

REPO_ROOT = Path(__file__).resolve().parents[2]
GROWTHOS = REPO_ROOT / "growthOS"
OUTPUT = GROWTHOS / "output" / "sales-pages"
DESIGN_INTEL = GROWTHOS / "design-intelligence"
TEMPLATES = GROWTHOS / "templates" / "sales-pages"

OUTPUT.mkdir(parents=True, exist_ok=True)

PHASES = [
    {"num": 1, "id": "discovery", "label": "Discovery", "icon": "🔍"},
    {"num": 2, "id": "research", "label": "Research", "icon": "📊"},
    {"num": 3, "id": "briefing", "label": "Briefing", "icon": "📋"},
    {"num": 4, "id": "visual-design", "label": "Visual Design", "icon": "🎨"},
    {"num": 5, "id": "narrative", "label": "Narrative", "icon": "✍️"},
    {"num": 6, "id": "fusion", "label": "Fusion", "icon": "⚡"},
    {"num": 7, "id": "build", "label": "Build", "icon": "🔧"},
    {"num": 8, "id": "qa", "label": "QA", "icon": "✅"},
]

app = Flask(__name__, static_folder=str(Path(__file__).parent / "static"))


def list_projects() -> list:
    """List all sales page projects by scanning output directory."""
    projects = []
    if OUTPUT.exists():
        for d in sorted(OUTPUT.iterdir()):
            if d.is_dir() and (d / "state.json").exists():
                state = json.loads((d / "state.json").read_text())
                projects.append({
                    "slug": d.name,
                    "name": state.get("project", {}).get("name", d.name),
                    "status": state.get("project", {}).get("status", "unknown"),
                    "current_phase": state.get("project", {}).get("current_phase", "discovery"),
                    "phases_completed": state.get("metadata", {}).get("total_phases_completed", 0),
                })
    return projects


def load_state(slug: str) -> dict:
    state_file = OUTPUT / slug / "state.json"
    if state_file.exists():
        return json.loads(state_file.read_text())
    return {}


def save_state(slug: str, state: dict) -> None:
    state_file = OUTPUT / slug / "state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state["project"]["updated"] = datetime.now().isoformat()
    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))


# ─────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    projects = list_projects()

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>GrowthOS — Sales Page Studio</title>
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #09090B; color: #FAFAFA; font-family: system-ui, -apple-system, sans-serif; }
        .container { max-width: 960px; margin: 0 auto; padding: 80px 24px; }
        h1 { font-size: 42px; font-weight: 800; letter-spacing: -1.5px; margin-bottom: 4px; }
        h1 span { background: linear-gradient(135deg, #3B82F6, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .sub { color: #71717A; font-family: monospace; font-size: 13px; margin-bottom: 48px; }
        .empty { color: #52525B; font-size: 15px; padding: 40px; border: 1px dashed #27272A; border-radius: 8px; text-align: center; }
        .project-card {
          background: #18181B; border: 1px solid #27272A; border-radius: 8px;
          padding: 24px; margin-bottom: 12px; display: flex; justify-content: space-between;
          align-items: center; transition: border-color 0.2s;
        }
        .project-card:hover { border-color: #3B82F6; }
        .project-card a { color: #FAFAFA; text-decoration: none; font-weight: 700; font-size: 18px; }
        .project-meta { font-family: monospace; font-size: 12px; color: #71717A; }
        .badge {
          display: inline-block; padding: 2px 8px; border-radius: 4px;
          font-size: 11px; font-weight: 600; text-transform: uppercase;
        }
        .badge-active { background: #1E3A5F; color: #60A5FA; }
        .badge-completed { background: #14532D; color: #4ADE80; }
        .badge-paused { background: #422006; color: #FB923C; }
        .phases-bar { display: flex; gap: 4px; margin-top: 8px; }
        .phase-dot { width: 24px; height: 4px; border-radius: 2px; background: #27272A; }
        .phase-dot.done { background: #4ADE80; }
        .phase-dot.active { background: #3B82F6; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Sales Page <span>Studio</span></h1>
        <div class="sub">localhost:8061 · 8-phase pipeline · design intelligence directed</div>
    """

    if not projects:
        html += '<div class="empty">No projects yet. Run the growthOS-sales-page skill to start.</div>'
    else:
        for p in projects:
            status_class = "active" if p["status"] == "in-progress" else p["status"]
            phase_dots = ""
            phase_idx = next((i for i, ph in enumerate(PHASES) if ph["id"] == p["current_phase"]), 0)
            for i in range(8):
                cls = "done" if i < p["phases_completed"] else ("active" if i == phase_idx else "")
                phase_dots += f'<div class="phase-dot {cls}"></div>'

            html += f"""
            <div class="project-card">
              <div>
                <a href="/project/{p['slug']}">{p['name']}</a>
                <div class="phases-bar">{phase_dots}</div>
              </div>
              <div class="project-meta">
                <span class="badge badge-{status_class}">{p['status']}</span>
                <br>Phase {p['phases_completed']}/8
              </div>
            </div>
            """

    html += """
      </div>
    </body>
    </html>
    """
    return html


@app.route("/project/<slug>")
def project_overview(slug):
    state = load_state(slug)
    if not state:
        abort(404)

    project = state.get("project", {})
    current_phase = project.get("current_phase", "discovery")
    current_idx = next((i for i, ph in enumerate(PHASES) if ph["id"] == current_phase), 0)

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>{project.get('name', slug)} — Sales Page Studio</title>
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: #09090B; color: #FAFAFA; font-family: system-ui, -apple-system, sans-serif; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 24px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }}
        .header h1 {{ font-size: 32px; font-weight: 800; letter-spacing: -1px; }}
        .header a {{ color: #71717A; text-decoration: none; font-size: 14px; }}
        .header a:hover {{ color: #FAFAFA; }}
        .pipeline {{ display: flex; gap: 8px; margin-bottom: 40px; overflow-x: auto; padding-bottom: 8px; }}
        .phase-card {{
          flex: 1; min-width: 120px; padding: 16px; border-radius: 8px;
          border: 1px solid #27272A; background: #18181B; text-align: center;
          cursor: pointer; transition: all 0.2s;
        }}
        .phase-card.done {{ border-color: #166534; background: #052e16; }}
        .phase-card.active {{ border-color: #3B82F6; background: #1E3A5F; }}
        .phase-card:hover {{ border-color: #52525B; }}
        .phase-icon {{ font-size: 24px; margin-bottom: 4px; }}
        .phase-label {{ font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
        .phase-num {{ font-family: monospace; font-size: 10px; color: #71717A; }}
        .preview-frame {{
          width: 100%; min-height: 70vh; border: 1px solid #27272A;
          border-radius: 8px; background: #FFF;
        }}
        .no-preview {{
          display: flex; align-items: center; justify-content: center;
          min-height: 400px; color: #52525B; font-size: 15px;
          border: 1px dashed #27272A; border-radius: 8px;
        }}
        .actions {{ display: flex; gap: 12px; margin-top: 16px; }}
        .btn {{
          padding: 10px 24px; border: none; border-radius: 6px;
          font-weight: 700; font-size: 14px; cursor: pointer; transition: all 0.2s;
        }}
        .btn-approve {{ background: #166534; color: #4ADE80; }}
        .btn-approve:hover {{ background: #14532D; }}
        .btn-revise {{ background: #422006; color: #FB923C; }}
        .btn-revise:hover {{ background: #451A03; }}
        .btn-reject {{ background: #450A0A; color: #FCA5A5; }}
        .btn-reject:hover {{ background: #7F1D1D; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>{project.get('name', slug)}</h1>
          <a href="/">← All Projects</a>
        </div>

        <div class="pipeline">
    """

    for i, phase in enumerate(PHASES):
        phase_key = f"phase_{phase['num']}_{phase['id'].replace('-', '_')}"
        phase_state = state.get(phase_key, {})
        phase_status = phase_state.get("status", "pending")

        cls = ""
        if phase_status in ("approved", "pass"):
            cls = "done"
        elif i == current_idx:
            cls = "active"

        html += f"""
          <a href="/project/{slug}/phase/{phase['num']}" style="text-decoration:none;color:inherit;flex:1;min-width:120px;">
            <div class="phase-card {cls}">
              <div class="phase-icon">{phase['icon']}</div>
              <div class="phase-label">{phase['label']}</div>
              <div class="phase-num">Phase {phase['num']}</div>
            </div>
          </a>
        """

    html += """
        </div>
    """

    # Show current phase preview
    preview_file = OUTPUT / slug / "previews" / f"phase-{current_idx + 1}-{PHASES[current_idx]['id']}.html"
    if preview_file.exists():
        html += f'<iframe class="preview-frame" src="/project/{slug}/preview/{current_idx + 1}"></iframe>'
    else:
        html += f'<div class="no-preview">Phase {current_idx + 1} ({PHASES[current_idx]["label"]}) — No preview generated yet</div>'

    html += """
        <div class="actions">
          <button class="btn btn-approve" onclick="approve()">Approve Phase</button>
          <button class="btn btn-revise" onclick="revise()">Request Revision</button>
        </div>
      </div>

      <script>
        function approve() {
          const slug = window.location.pathname.split('/')[2];
          fetch(`/api/project/${slug}/approve`, { method: 'POST' })
            .then(r => r.json())
            .then(d => { if(d.ok) location.reload(); else alert(d.error); });
        }
        function revise() {
          const note = prompt('What needs to change?');
          if (!note) return;
          const slug = window.location.pathname.split('/')[2];
          fetch(`/api/project/${slug}/revise`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ note })
          }).then(r => r.json())
            .then(d => { if(d.ok) location.reload(); else alert(d.error); });
        }
      </script>
    </body>
    </html>
    """
    return html


@app.route("/project/<slug>/phase/<int:phase_num>")
def phase_detail(slug, phase_num):
    """Redirect to project overview focused on specific phase."""
    return redirect(f"/project/{slug}")


@app.route("/project/<slug>/preview/<int:phase_num>")
def serve_preview(slug, phase_num):
    """Serve the preview HTML for a specific phase."""
    if phase_num < 1 or phase_num > 8:
        abort(404)
    phase = PHASES[phase_num - 1]
    preview_dir = OUTPUT / slug / "previews"
    filename = f"phase-{phase_num}-{phase['id']}.html"
    if not (preview_dir / filename).exists():
        abort(404)
    return send_from_directory(str(preview_dir), filename)


@app.route("/project/<slug>/build")
def serve_build(slug):
    """Serve the final built page (Phase 7 output)."""
    build_dir = OUTPUT / slug
    # Look for the final HTML file
    for candidate in ["index.html", f"{slug}.html"]:
        if (build_dir / candidate).exists():
            return send_from_directory(str(build_dir), candidate)
    abort(404)


# ─────────────────────────────────────────────────────────────────
# API Routes
# ─────────────────────────────────────────────────────────────────

@app.route("/api/projects")
def api_list_projects():
    return jsonify(list_projects())


@app.route("/api/project/<slug>/state")
def api_get_state(slug):
    state = load_state(slug)
    if not state:
        abort(404)
    return jsonify(state)


@app.route("/api/project/<slug>/state", methods=["POST"])
def api_update_state(slug):
    """Update project state (used by skills during pipeline execution)."""
    state = request.json
    if not state:
        return jsonify({"ok": False, "error": "No state provided"}), 400
    save_state(slug, state)
    return jsonify({"ok": True})


@app.route("/api/project/<slug>/approve", methods=["POST"])
def api_approve_phase(slug):
    state = load_state(slug)
    if not state:
        return jsonify({"ok": False, "error": "Project not found"}), 404

    current_phase = state["project"]["current_phase"]
    phase_key = f"phase_{next(p['num'] for p in PHASES if p['id'] == current_phase)}_{current_phase.replace('-', '_')}"

    if phase_key in state:
        state[phase_key]["status"] = "approved"
        state[phase_key]["approved_at"] = datetime.now().isoformat()

    # Advance to next phase
    current_idx = next(i for i, p in enumerate(PHASES) if p["id"] == current_phase)
    if current_idx < len(PHASES) - 1:
        state["project"]["current_phase"] = PHASES[current_idx + 1]["id"]
        state["metadata"]["total_phases_completed"] = current_idx + 1

    save_state(slug, state)
    return jsonify({"ok": True, "next_phase": state["project"]["current_phase"]})


@app.route("/api/project/<slug>/revise", methods=["POST"])
def api_revise_phase(slug):
    state = load_state(slug)
    if not state:
        return jsonify({"ok": False, "error": "Project not found"}), 404

    current_phase = state["project"]["current_phase"]
    phase_key = f"phase_{next(p['num'] for p in PHASES if p['id'] == current_phase)}_{current_phase.replace('-', '_')}"

    note = request.json.get("note", "") if request.json else ""

    if phase_key in state:
        state[phase_key]["status"] = "revision-requested"
        if "revision_notes" not in state[phase_key]:
            state[phase_key]["revision_notes"] = []
        state[phase_key]["revision_notes"].append({
            "note": note,
            "timestamp": datetime.now().isoformat()
        })

    state["metadata"]["total_revisions"] = state.get("metadata", {}).get("total_revisions", 0) + 1
    save_state(slug, state)
    return jsonify({"ok": True})


@app.route("/api/project/<slug>/init", methods=["POST"])
def api_init_project(slug):
    """Initialize a new project with empty state."""
    data = request.json or {}
    name = data.get("name", slug)

    state = {
        "project": {
            "slug": slug,
            "name": name,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "current_phase": "discovery",
            "status": "in-progress"
        },
        "metadata": {
            "total_phases_completed": 0,
            "total_revisions": 0,
            "design_intelligence_files_consulted": [],
            "skills_invoked": [],
            "build_duration_minutes": None
        }
    }

    # Create directories
    project_dir = OUTPUT / slug
    (project_dir / "previews").mkdir(parents=True, exist_ok=True)

    save_state(slug, state)
    return jsonify({"ok": True, "state": state})


# ─────────────────────────────────────────────────────────────────
# Static assets
# ─────────────────────────────────────────────────────────────────

@app.route("/assets/<path:filename>")
def serve_asset(filename):
    assets_dir = GROWTHOS / "assets"
    return send_from_directory(str(assets_dir), filename)


# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("─" * 50)
    print("  GrowthOS — Sales Page Studio")
    port = int(os.environ.get("SP_PORT", 5061))
    print(f"  http://localhost:{port}")
    print("─" * 50)
    app.run(host="0.0.0.0", port=port, debug=True)
