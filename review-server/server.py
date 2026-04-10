#!/usr/bin/env python3
"""
review-server/server.py — Flask local review dashboard for GrowthOS carousels

Run:
    python growthOS/review-server/server.py

Then open: http://localhost:5050

Features:
    - Lists all carousels-v*.html in design-system/
    - Renders each carousel HTML with review overlay (approve/reject + tags + notes)
    - Persists state to growthOS/output/reviews/reviews.json
    - On approve → triggers export-carousel.mjs + organize-approved.py + update-profile.py
    - On reject → appends to REJECTED.md + triggers update-profile.py
"""

import os
import json
import subprocess
import sys
from datetime import datetime, date
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, render_template_string, abort

REPO_ROOT = Path(__file__).resolve().parents[2]
GROWTHOS = REPO_ROOT / "growthOS"
DESIGN_SYSTEM = GROWTHOS / "design-system"
OUTPUT = GROWTHOS / "output"
APPROVED = OUTPUT / "approved"
REVIEWS_DIR = OUTPUT / "reviews"
REVIEWS_FILE = REVIEWS_DIR / "reviews.json"
PREFERENCES = GROWTHOS / "voice" / "preferences"
SCRIPTS = GROWTHOS / "scripts"

REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
PREFERENCES.mkdir(parents=True, exist_ok=True)

REJECTION_TAGS = [
    "tom_guru", "tom_motivacional", "copy_fraca", "hook_morno",
    "layout_apertado", "cta_generico", "cliche", "vocabulario_proibido",
    "visual_generico", "sem_dor_real", "nao_e_minha_voz", "outro",
]

REVISION_TAGS = [
    # COPY
    ("copy_hook", "copy", "Só a capa (slide 1) precisa mudar"),
    ("copy_texto", "copy", "Reescrever texto de slide(s)"),
    ("copy_cta", "copy", "Ajustar fechamento / CTA"),
    ("copy_numero", "copy", "Número / fato / stat errado ou inventado"),
    ("copy_tom", "copy", "Tom quase mas desviou"),
    # DESIGN
    ("design_layout", "design", "Mudar disposição dos elementos"),
    ("design_hierarquia", "design", "Tamanho de fonte / prioridade visual"),
    ("design_asset", "design", "Trocar / adicionar logo / screenshot"),
    # ESTRUTURA
    ("estrutura_ordem", "estrutura", "Reordenar slides"),
    ("estrutura_adicionar", "estrutura", "Falta um slide"),
    ("estrutura_cortar", "estrutura", "Sobra slide"),
    # FATO
    ("fonte_verificar", "fato", "Checar fato / pedir fonte"),
]

REVISIONS_FILE = PREFERENCES / "REVISIONS.md"
REVISIONS_QUEUE = OUTPUT / "revisions" / "queue.json"
REVISIONS_BRIEFS = DESIGN_SYSTEM / "revisions"
REVISIONS_BRIEFS.mkdir(parents=True, exist_ok=True)
(OUTPUT / "revisions").mkdir(parents=True, exist_ok=True)

# Posting queue
POSTING_QUEUE_FILE = OUTPUT / "approved" / "queue" / "queue.json"
POSTING_QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=str(Path(__file__).parent / "static"))


def load_reviews() -> dict:
    if REVIEWS_FILE.exists():
        try:
            return json.loads(REVIEWS_FILE.read_text())
        except Exception:
            return {}
    return {}


def save_reviews(data: dict) -> None:
    REVIEWS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def list_carousel_files() -> list:
    return sorted([f.name for f in DESIGN_SYSTEM.glob("carousels-v*.html")]) + \
           sorted([f.name for f in DESIGN_SYSTEM.glob("carousel-*.html")])


def run_script(cmd: list, cwd: Path = None) -> dict:
    """Run a script and capture output."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd or REPO_ROOT,
            capture_output=True, text=True, timeout=300,
        )
        return {
            "ok": result.returncode == 0,
            "stdout": result.stdout[-2000:],
            "stderr": result.stderr[-2000:],
            "code": result.returncode,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ─────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────

@app.route("/assets/<path:filename>")
def serve_asset(filename):
    """Serve assets (logos, icons) so carousel HTML relative paths work."""
    assets_dir = GROWTHOS / "assets"
    return send_from_directory(str(assets_dir), filename)


@app.route("/")
def index():
    files = list_carousel_files()
    reviews = load_reviews()

    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="utf-8">
      <title>GrowthOS — Review Dashboard</title>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;700;900&family=Geist+Mono:wght@400;500&display=swap');
        body { background:#0A0A0A; color:#F5F5F5; font-family:'Geist',sans-serif; padding:60px; margin:0; }
        h1 { font-size:48px; font-weight:900; margin:0 0 8px; letter-spacing:-1px; }
        .sub { color:#8A8A8A; font-family:'Geist Mono',monospace; font-size:14px; margin-bottom:40px; }
        .accent { color:#B0FF3C; }
        .list { list-style:none; padding:0; }
        .file-card { background:#111; border:1px solid rgba(255,255,255,0.08); padding:20px 24px; margin-bottom:12px; border-radius:2px; display:flex; justify-content:space-between; align-items:center; }
        .file-card a { color:#F5F5F5; text-decoration:none; font-weight:700; font-size:18px; }
        .file-card a:hover { color:#B0FF3C; }
        .stats { font-family:'Geist Mono',monospace; font-size:12px; color:#8A8A8A; }
        .stat-approved { color:#B0FF3C; }
        .stat-revised { color:#FFE600; }
        .stat-rejected { color:#FF6B6B; }
        .stat-pending { color:#8A8A8A; }
        .footer { margin-top:60px; color:#5A5A5A; font-family:'Geist Mono',monospace; font-size:12px; }
        .footer a { color:#8A8A8A; margin-right:20px; }
      </style>
    </head>
    <body>
      <h1>GrowthOS <span class="accent">Review</span></h1>
      <div class="sub">localhost:5050 · @melgarafael · ◉ approve · ⟲ revise · ✗ reject</div>
      <ul class="list">
    """
    for f in files:
        file_reviews = reviews.get(f, {})
        approved = sum(1 for r in file_reviews.values() if r.get("status") == "approved")
        rejected = sum(1 for r in file_reviews.values() if r.get("status") == "rejected")
        revised = sum(1 for r in file_reviews.values() if r.get("status") == "revision_requested")
        html += f"""
        <li class="file-card">
          <a href="/c/{f}">{f}</a>
          <div class="stats">
            <span class="stat-approved">✓ {approved}</span> ·
            <span class="stat-revised">⟲ {revised}</span> ·
            <span class="stat-rejected">✗ {rejected}</span>
          </div>
        </li>
        """
    html += """
      </ul>
      <div class="footer">
        <a href="/queue" style="color:#B0FF3C;font-weight:700;">🚢 posting queue</a>
        <a href="/api/regen-profile">⟳ regenerate PROFILE.md</a>
        <a href="/api/reviews">📄 reviews.json</a>
        <a href="/api/queue">⟲ revision queue</a>
      </div>
    </body>
    </html>
    """
    return html


@app.route("/c/<path:filename>")
def render_carousel(filename: str):
    file_path = DESIGN_SYSTEM / filename
    if not file_path.exists() or not filename.endswith(".html"):
        abort(404)

    html = file_path.read_text()
    reviews = load_reviews().get(filename, {})

    # Build the revision tags HTML (grouped by family)
    revision_tags_html = ""
    families = {}
    for tag, family, desc in REVISION_TAGS:
        families.setdefault(family, []).append((tag, desc))
    family_labels = {"copy": "COPY", "design": "DESIGN", "estrutura": "ESTRUTURA", "fato": "FATO"}
    for fam_key, items in families.items():
        revision_tags_html += f'<div class="rev-fam"><div class="rev-fam-label">{family_labels[fam_key]}</div>'
        for tag, desc in items:
            revision_tags_html += f'<label class="rev-tag" title="{desc}"><input type="checkbox" value="{tag}">{tag}</label>'
        revision_tags_html += '</div>'

    rejection_tags_options = "".join(f'<option value="{t}">{t}</option>' for t in REJECTION_TAGS)

    overlay = """
    <style>
      .review-bar { position:fixed; bottom:24px; right:24px; background:#0A0A0A; border:2px solid #B0FF3C;
        padding:20px; z-index:9999; font-family:'Geist Mono',monospace; font-size:13px; color:#F5F5F5;
        width:400px; max-height:85vh; overflow-y:auto; box-shadow:0 20px 60px rgba(176,255,60,0.2); }
      .review-bar h4 { margin:0 0 12px; font-size:14px; font-weight:900; color:#B0FF3C; text-transform:uppercase; letter-spacing:1px; }
      .review-bar select, .review-bar textarea, .review-bar input[type=text] { width:100%; padding:8px; background:#111; color:#F5F5F5;
        border:1px solid rgba(255,255,255,0.2); font-family:inherit; font-size:12px; margin-bottom:8px; box-sizing:border-box; }
      .review-bar textarea { min-height:80px; resize:vertical; }
      .review-bar .btn-row { display:flex; gap:6px; margin-top:8px; }
      .review-bar button { flex:1; padding:10px 8px; border:none; font-weight:900; font-family:inherit;
        text-transform:uppercase; cursor:pointer; font-size:11px; letter-spacing:0.5px; }
      .review-bar .btn-approve { background:#B0FF3C; color:#0A0A0A; }
      .review-bar .btn-revise { background:#FFE600; color:#0A0A0A; }
      .review-bar .btn-reject { background:#FF6B6B; color:#0A0A0A; }
      .review-bar .btn-skip { background:#333; color:#F5F5F5; }
      .review-bar .status { margin-top:8px; padding:6px 8px; font-size:11px; }
      .review-bar .status.approved { background:rgba(176,255,60,0.1); color:#B0FF3C; }
      .review-bar .status.revision_requested { background:rgba(255,230,0,0.1); color:#FFE600; }
      .review-bar .status.rejected { background:rgba(255,107,107,0.1); color:#FF6B6B; }

      /* Reject panel (hidden by default) */
      .panel { display:none; padding:12px; margin-top:10px; border:1px solid rgba(255,255,255,0.15); background:#0E0E0E; }
      .panel.open { display:block; }
      .panel h5 { margin:0 0 8px; font-size:11px; color:#8A8A8A; text-transform:uppercase; }

      /* Revise panel */
      .rev-fam { margin-bottom:10px; }
      .rev-fam-label { font-size:10px; color:#B0FF3C; font-weight:900; margin-bottom:4px; letter-spacing:1px; }
      .rev-tag { display:block; font-size:11px; padding:4px 6px; cursor:pointer; color:#F5F5F5; }
      .rev-tag:hover { background:rgba(255,230,0,0.08); }
      .rev-tag input { margin-right:6px; }
      .slide-picker { display:flex; gap:4px; flex-wrap:wrap; margin-bottom:8px; }
      .slide-picker label { display:inline-block; width:28px; height:28px; line-height:26px; text-align:center;
        border:1px solid rgba(255,255,255,0.2); cursor:pointer; font-size:11px; }
      .slide-picker label:has(input:checked) { background:#FFE600; color:#0A0A0A; border-color:#FFE600; font-weight:900; }
      .slide-picker input { display:none; }

      section[data-cid] { position:relative; }
      section[data-cid]::before { content:attr(data-review-status); position:absolute; top:8px; right:8px;
        font-family:'Geist Mono',monospace; font-size:10px; padding:4px 8px; border-radius:2px; z-index:100; }
      section[data-cid][data-review-status="approved"]::before { background:#B0FF3C; color:#0A0A0A; }
      section[data-cid][data-review-status="revision_requested"]::before { background:#FFE600; color:#0A0A0A; }
      section[data-cid][data-review-status="rejected"]::before { background:#FF6B6B; color:#0A0A0A; }
    </style>
    <div class="review-bar" id="reviewBar">
      <h4>◉ Review · <span id="currentCid">—</span></h4>

      <div class="btn-row">
        <button class="btn-approve" onclick="submitReview('approved')">✓ APPROVE</button>
        <button class="btn-revise" onclick="togglePanel('revise')">⟲ REVISE</button>
        <button class="btn-reject" onclick="togglePanel('reject')">✗ REJECT</button>
      </div>
      <div class="btn-row" style="margin-top:6px;">
        <button class="btn-skip" onclick="navCarousel(-1)">← prev</button>
        <button class="btn-skip" onclick="navCarousel(1)">next →</button>
      </div>
      <div class="status" id="statusBadge"></div>

      <!-- REJECT panel -->
      <div class="panel" id="rejectPanel">
        <h5>rejeitar · motivo</h5>
        <select id="rejectTag"><option value="">— tag —</option>__REJECTION_TAGS__</select>
        <textarea id="rejectReason" placeholder="razão livre (recomendado)"></textarea>
        <button class="btn-reject" onclick="submitReview('rejected')">confirmar rejeição</button>
      </div>

      <!-- REVISE panel -->
      <div class="panel" id="revisePanel">
        <h5>revisar · o que mudar?</h5>
        <textarea id="reviseInstructions" placeholder="ex: não construí 100 agentes. muda capa + slide 2, mantém 3-8."></textarea>

        <h5 style="margin-top:10px;">tags (marca uma ou mais)</h5>
        __REVISION_TAGS__

        <h5 style="margin-top:10px;">slides afetados</h5>
        <div class="slide-picker" id="slidePicker">
          <label><input type="checkbox" value="1" checked>1</label>
          <label><input type="checkbox" value="2" checked>2</label>
          <label><input type="checkbox" value="3" checked>3</label>
          <label><input type="checkbox" value="4" checked>4</label>
          <label><input type="checkbox" value="5" checked>5</label>
          <label><input type="checkbox" value="6" checked>6</label>
          <label><input type="checkbox" value="7" checked>7</label>
          <label><input type="checkbox" value="8" checked>8</label>
        </div>

        <button class="btn-revise" onclick="submitRevise()">enviar revisão</button>
      </div>
    </div>
    <script>
      const FILENAME = %FILENAME%;
      const EXISTING_REVIEWS = %REVIEWS%;
      let currentIdx = 0;
      let sections = [];

      window.addEventListener('DOMContentLoaded', () => {
        sections = Array.from(document.querySelectorAll('section')).filter(s => {
          return s.querySelector('.slide') || s.id?.match(/^c\\d+/) || s.dataset.carousel;
        });
        sections.forEach((s, i) => {
          const cid = s.dataset.carousel || s.id || `c${String(i+1).padStart(2,'0')}`;
          s.dataset.cid = cid;
          if (EXISTING_REVIEWS[cid]) {
            s.dataset.reviewStatus = EXISTING_REVIEWS[cid].status;
          }
        });
        focusCarousel(0);
      });

      function focusCarousel(i) {
        if (i < 0 || i >= sections.length) return;
        currentIdx = i;
        const s = sections[i];
        s.scrollIntoView({ behavior: 'smooth', block: 'start' });
        document.getElementById('currentCid').textContent = s.dataset.cid;
        const existing = EXISTING_REVIEWS[s.dataset.cid];
        const badge = document.getElementById('statusBadge');
        if (existing) {
          badge.className = 'status ' + existing.status;
          const extras = [];
          if (existing.tag) extras.push(existing.tag);
          if (existing.tags && existing.tags.length) extras.push(existing.tags.join(','));
          if (existing.reason || existing.instructions) extras.push((existing.reason || existing.instructions).slice(0, 60));
          badge.textContent = existing.status.toUpperCase() + (extras.length ? ' · ' + extras.join(' — ') : '');
        } else {
          badge.className = 'status';
          badge.textContent = 'pending review';
        }
        // Close any open panels when switching
        document.getElementById('rejectPanel').classList.remove('open');
        document.getElementById('revisePanel').classList.remove('open');
      }

      function navCarousel(delta) { focusCarousel(Math.max(0, Math.min(sections.length-1, currentIdx + delta))); }

      function togglePanel(which) {
        const reject = document.getElementById('rejectPanel');
        const revise = document.getElementById('revisePanel');
        if (which === 'reject') {
          reject.classList.toggle('open');
          revise.classList.remove('open');
        } else if (which === 'revise') {
          revise.classList.toggle('open');
          reject.classList.remove('open');
        }
      }

      async function submitReview(status) {
        const cid = sections[currentIdx].dataset.cid;
        let tag = '', reason = '';
        if (status === 'rejected') {
          tag = document.getElementById('rejectTag').value;
          reason = document.getElementById('rejectReason').value;
          if (!tag && !reason) {
            alert('rejeição exige tag OU razão');
            return;
          }
        }
        const r = await fetch('/api/review', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file: FILENAME, cid, status, tag, reason, timestamp: new Date().toISOString() }),
        });
        const j = await r.json();
        if (j.ok) {
          sections[currentIdx].dataset.reviewStatus = status;
          EXISTING_REVIEWS[cid] = { status, tag, reason };
          document.getElementById('rejectTag').value = '';
          document.getElementById('rejectReason').value = '';
          focusCarousel(currentIdx);
          setTimeout(() => navCarousel(1), 600);
        } else {
          alert('erro: ' + (j.error || 'unknown'));
        }
      }

      async function submitRevise() {
        const cid = sections[currentIdx].dataset.cid;
        const instructions = document.getElementById('reviseInstructions').value.trim();
        if (!instructions) {
          alert('instruções de revisão são obrigatórias');
          return;
        }
        const tags = Array.from(document.querySelectorAll('#revisePanel .rev-tag input:checked')).map(el => el.value);
        const slides = Array.from(document.querySelectorAll('#slidePicker input:checked')).map(el => parseInt(el.value));
        if (slides.length === 0) {
          alert('selecione ao menos 1 slide afetado');
          return;
        }
        const r = await fetch('/api/revise', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file: FILENAME, cid, instructions, tags, affected_slides: slides, timestamp: new Date().toISOString() }),
        });
        const j = await r.json();
        if (j.ok) {
          sections[currentIdx].dataset.reviewStatus = 'revision_requested';
          EXISTING_REVIEWS[cid] = { status: 'revision_requested', tags, instructions };
          document.getElementById('reviseInstructions').value = '';
          document.querySelectorAll('#revisePanel .rev-tag input').forEach(el => el.checked = false);
          focusCarousel(currentIdx);
          setTimeout(() => navCarousel(1), 600);
        } else {
          alert('erro: ' + (j.error || 'unknown'));
        }
      }

      document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
        if (e.key === 'a' || e.key === 'A') submitReview('approved');
        if (e.key === 'v' || e.key === 'V') togglePanel('revise');
        if (e.key === 'r' || e.key === 'R') togglePanel('reject');
        if (e.key === 'ArrowRight' || e.key === 'j') navCarousel(1);
        if (e.key === 'ArrowLeft' || e.key === 'k') navCarousel(-1);
        if (e.key === 'Escape') {
          document.getElementById('rejectPanel').classList.remove('open');
          document.getElementById('revisePanel').classList.remove('open');
        }
      });
    </script>
    """

    overlay = overlay.replace("__REJECTION_TAGS__", rejection_tags_options)
    overlay = overlay.replace("__REVISION_TAGS__", revision_tags_html)
    overlay = overlay.replace("%FILENAME%", json.dumps(filename))
    overlay = overlay.replace("%REVIEWS%", json.dumps(reviews))

    if "</body>" in html:
        html = html.replace("</body>", overlay + "</body>")
    else:
        html += overlay
    return html


@app.route("/api/review", methods=["POST"])
def api_review():
    data = request.get_json()
    file = data.get("file")
    cid = data.get("cid")
    status = data.get("status")
    tag = data.get("tag", "")
    reason = data.get("reason", "")
    ts = data.get("timestamp", datetime.now().isoformat())

    if not file or not cid or status not in {"approved", "rejected"}:
        return jsonify({"ok": False, "error": "missing/invalid fields"}), 400

    reviews = load_reviews()
    reviews.setdefault(file, {})[cid] = {
        "status": status, "tag": tag, "reason": reason, "timestamp": ts,
    }
    save_reviews(reviews)

    # Auto-log to APPROVED.md or REJECTED.md
    log_file = PREFERENCES / ("APPROVED.md" if status == "approved" else "REJECTED.md")
    log_entry = f"\n## {ts[:19]} · {file} · {cid}\n"
    if tag:
        log_entry += f"- **tag:** `{tag}`\n"
    if reason:
        log_entry += f"- **razão:** {reason}\n"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(log_entry)

    # Trigger pipelines
    pipeline_results = {}
    if status == "approved":
        export_res = run_script([
            "node", str(SCRIPTS / "export-carousel.mjs"),
            str(DESIGN_SYSTEM / file), "--carousel", cid,
        ])
        pipeline_results["export"] = export_res
        if export_res.get("ok"):
            org_res = run_script([
                sys.executable, str(SCRIPTS / "organize-approved.py"),
                "--carousel", cid, "--source", Path(file).stem,
            ])
            pipeline_results["organize"] = org_res

    profile_res = run_script([sys.executable, str(SCRIPTS / "update-profile.py")])
    pipeline_results["profile"] = profile_res

    return jsonify({"ok": True, "pipeline": pipeline_results})


@app.route("/api/reviews")
def api_reviews():
    return jsonify(load_reviews())


@app.route("/api/revise", methods=["POST"])
def api_revise():
    data = request.get_json()
    file = data.get("file")
    cid = data.get("cid")
    instructions = data.get("instructions", "").strip()
    tags = data.get("tags", [])
    affected_slides = data.get("affected_slides", [])
    ts = data.get("timestamp", datetime.now().isoformat())

    if not file or not cid or not instructions:
        return jsonify({"ok": False, "error": "file, cid, instructions are required"}), 400

    # 1. Update reviews.json — mark as revision_requested
    reviews = load_reviews()
    reviews.setdefault(file, {})[cid] = {
        "status": "revision_requested",
        "tags": tags,
        "instructions": instructions,
        "affected_slides": affected_slides,
        "timestamp": ts,
    }
    save_reviews(reviews)

    # 2. Append to REVISIONS.md
    log_entry = f"\n## {ts[:19]} · {file} · {cid}\n"
    if tags:
        log_entry += f"- **tags:** {', '.join(f'`{t}`' for t in tags)}\n"
    log_entry += f"- **slides afetados:** {affected_slides}\n"
    log_entry += f"- **instruções:** {instructions}\n"
    log_entry += f"- **status:** pending\n"
    log_entry += f"- **revision_round:** 1\n"
    with REVISIONS_FILE.open("a", encoding="utf-8") as f_out:
        f_out.write(log_entry)

    # 3. Generate revision brief file for carousel-designer to consume later
    ts_slug = ts.replace(":", "").replace("-", "")[:15]
    brief_name = f"REVISION-{cid}-{ts_slug}.md"
    brief_path = REVISIONS_BRIEFS / brief_name
    brief_content = f"""# REVISION BRIEF — {cid} · {ts}

> Para: carousel-designer (via /grow revise)
> Fonte original: `design-system/{file}`
> Carrossel: `{cid}`
> Slides afetados: {affected_slides}
> Tags: {', '.join(tags) if tags else '(nenhuma)'}

## Instruções do usuário (literal)

{instructions}

## Tarefa

1. Leia o HTML original em `growthOS/design-system/{file}` e localize a `<section>` do carrossel `{cid}`.
2. Regenere APENAS os slides afetados ({affected_slides}), preservando os demais tal qual no original.
3. Respeite as regras de voz em `growthOS/voice/GOLDEN-DOC.md` + `PROFILE.md` + `APPROVED.md` + `REJECTED.md`.
4. Se a revisão pede pra corrigir número/fato (`copy_numero` ou `fonte_verificar`), NÃO invente dado novo — peça ao usuário ou use valor placeholder com marcador `[VERIFICAR]`.
5. Saída: retorne o HTML COMPLETO da section `{cid}` revisada, pronto pra ser mergado no arquivo versionado `{Path(file).stem}-rev{{N}}.html`.

## Antes de começar

Leia também a última versão do PROFILE para entender padrões já aprovados e rejeitados.
"""
    brief_path.write_text(brief_content, encoding="utf-8")

    # 4. Append to revision queue
    queue = json.loads(REVISIONS_QUEUE.read_text()) if REVISIONS_QUEUE.exists() else {"pending": [], "processing": [], "done": []}
    queue["pending"].append({
        "file": file,
        "cid": cid,
        "brief_path": str(brief_path.relative_to(REPO_ROOT)),
        "tags": tags,
        "affected_slides": affected_slides,
        "instructions": instructions,
        "timestamp": ts,
    })
    REVISIONS_QUEUE.write_text(json.dumps(queue, indent=2, ensure_ascii=False))

    # 5. Trigger profile regen (lightweight)
    run_script([sys.executable, str(SCRIPTS / "update-profile.py")])

    return jsonify({
        "ok": True,
        "brief_path": str(brief_path.relative_to(REPO_ROOT)),
        "queue_pending": len(queue["pending"]),
    })


@app.route("/api/queue")
def api_queue():
    if REVISIONS_QUEUE.exists():
        return jsonify(json.loads(REVISIONS_QUEUE.read_text()))
    return jsonify({"pending": [], "processing": [], "done": []})


@app.route("/api/regen-profile")
def api_regen_profile():
    result = run_script([sys.executable, str(SCRIPTS / "update-profile.py")])
    return jsonify(result)


# ─────────────────────────────────────────────────────────────────
# POSTING QUEUE
# ─────────────────────────────────────────────────────────────────

def load_posting_queue() -> dict:
    if POSTING_QUEUE_FILE.exists():
        try:
            return json.loads(POSTING_QUEUE_FILE.read_text())
        except Exception:
            pass
    return {"items": [], "updated_at": None}


def save_posting_queue(q: dict):
    q["updated_at"] = datetime.now().isoformat()
    POSTING_QUEUE_FILE.write_text(json.dumps(q, indent=2, ensure_ascii=False))


def _parse_cid_title_from_html(source_html: Path, cid: str) -> str:
    """Quick & dirty extraction of a title for a carousel inside an HTML file."""
    if not source_html.exists():
        return cid
    try:
        text = source_html.read_text(encoding="utf-8")
        # find the section with id=cid
        import re
        m = re.search(rf'<section[^>]*id="{cid}"[^>]*>(.*?)</section>', text, re.DOTALL)
        if not m:
            return cid
        chunk = m.group(1)
        # find first non-empty heading
        head = re.search(r'<(?:h1|h2|div[^>]*class="[^"]*(?:display|cover|headline)[^"]*")[^>]*>(.*?)</', chunk, re.DOTALL)
        if head:
            raw = re.sub(r'<[^>]+>', '', head.group(1))
            raw = re.sub(r'\s+', ' ', raw).strip()
            return raw[:80] or cid
        return cid
    except Exception:
        return cid


def rebuild_posting_queue() -> dict:
    """Scan reviews.json, pull all approved, merge with existing queue, return fresh dict."""
    reviews = load_reviews()
    existing = load_posting_queue()
    existing_by_key = {(it["source"], it["cid"]): it for it in existing.get("items", [])}

    # Dedupe by (family, cid) where family strips -revN suffix
    # E.g., carousels-v1.html and carousels-v1-rev1.html belong to same "v1" family
    # But carousels-v4.html is a different family (separate carousel set)
    import re
    def family_of(source: str) -> str:
        stem = Path(source).stem
        return re.sub(r'-rev\d+$', '', stem)

    best_by_family_cid = {}  # (family, cid) -> best source
    for source, cids in reviews.items():
        fam = family_of(source)
        for cid, rev in cids.items():
            if rev.get("status") != "approved":
                continue
            key = (fam, cid)
            current_best = best_by_family_cid.get(key)
            if current_best is None:
                best_by_family_cid[key] = source
            else:
                # Prefer rev (revN > base within same family)
                if "-rev" in source and "-rev" not in current_best:
                    best_by_family_cid[key] = source
                elif "-rev" in source and "-rev" in current_best:
                    # Higher rev number wins
                    cur_n = int(re.search(r"-rev(\d+)", current_best).group(1))
                    new_n = int(re.search(r"-rev(\d+)", source).group(1))
                    if new_n > cur_n:
                        best_by_family_cid[key] = source

    items = []
    order_idx = 0
    for (fam, cid), source in sorted(best_by_family_cid.items()):
        key = (source, cid)
        if key in existing_by_key:
            item = existing_by_key[key]
        else:
            title = _parse_cid_title_from_html(DESIGN_SYSTEM / source, cid)
            item = {
                "source": source,
                "cid": cid,
                "title": title,
                "status": "pending",
                "order": order_idx,
                "added_at": datetime.now().isoformat(),
                "approved_date": str(date.today()),
                "scheduled_for": None,
                "post_url": None,
            }
        items.append(item)
        order_idx += 1

    # Preserve manual ordering if exists
    items.sort(key=lambda it: it.get("order", 9999))
    queue = {"items": items}
    save_posting_queue(queue)
    return queue


@app.route("/queue")
def queue_page():
    queue = rebuild_posting_queue()

    rows_html = ""
    for i, item in enumerate(queue["items"]):
        status = item.get("status", "pending")
        status_color = {
            "pending": "#8A8A8A", "exporting": "#FFE600", "organizing": "#FFE600",
            "captioning": "#FFE600", "publishing": "#00F0FF", "done": "#B0FF3C",
            "failed": "#FF6B6B", "skipped": "#5A5A5A", "scheduled": "#FF9F43",
        }.get(status, "#8A8A8A")
        title = item.get("title", "")[:70]
        source = item["source"]
        cid = item["cid"]
        post_url = item.get("post_url") or ""
        post_link = f'<a href="{post_url}" target="_blank" style="color:#B0FF3C;font-size:10px;">📎 post</a>' if post_url else ""
        scheduled = item.get("scheduled_for") or ""
        sched_badge = f'<span class="q-sched">🕐 {scheduled[:16].replace("T"," ")}</span>' if scheduled else ""
        rows_html += f"""
        <li class="q-item" data-idx="{i}" draggable="true">
          <div class="q-drag">⋮⋮</div>
          <div class="q-order">{i+1:02d}</div>
          <div class="q-main" onclick="toggleDetail({i}, event)">
            <div class="q-title">{title} <span class="q-expand-icon">▸</span></div>
            <div class="q-sub">{source} · {cid} {sched_badge}</div>
          </div>
          <div class="q-status" style="color:{status_color};">● {status}</div>
          <div class="q-actions">{post_link}</div>
        </li>
        <li class="q-detail" id="detail-{i}" style="display:none;">
          <div class="q-detail-inner">
            <div class="q-detail-loading">carregando...</div>
          </div>
        </li>
        """

    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="utf-8">
      <title>GrowthOS — Posting Queue</title>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;700;900&family=Geist+Mono:wght@400;500;700&display=swap');
        body { background:#0A0A0A; color:#F5F5F5; font-family:'Geist',sans-serif; padding:60px; margin:0; }
        .back { color:#8A8A8A; text-decoration:none; font-family:'Geist Mono',monospace; font-size:12px; }
        .back:hover { color:#B0FF3C; }
        h1 { font-size:48px; font-weight:900; margin:12px 0 4px; letter-spacing:-1px; }
        .sub { color:#8A8A8A; font-family:'Geist Mono',monospace; font-size:13px; margin-bottom:32px; }
        .accent { color:#B0FF3C; }
        .bar { display:flex; gap:8px; margin-bottom:24px; align-items:center; flex-wrap:wrap; }
        .bar button { padding:12px 20px; border:none; font-weight:900; font-family:inherit; text-transform:uppercase;
          cursor:pointer; font-size:12px; letter-spacing:1px; }
        .btn-prepare { background:#FFE600; color:#0A0A0A; }
        .btn-ship { background:#B0FF3C; color:#0A0A0A; }
        .btn-dry { background:#00F0FF; color:#0A0A0A; }
        .btn-reload { background:#333; color:#F5F5F5; }
        .bar .delay { margin-left:auto; font-family:'Geist Mono',monospace; font-size:12px; color:#8A8A8A; }
        .bar .delay input { width:80px; padding:8px; background:#111; color:#F5F5F5; border:1px solid rgba(255,255,255,0.2); font-family:inherit; }
        .q-list { list-style:none; padding:0; }
        .q-item { background:#111; border:1px solid rgba(255,255,255,0.08); padding:16px 20px; margin-bottom:8px;
          display:flex; align-items:center; gap:16px; cursor:grab; transition:transform 120ms,border-color 120ms; }
        .q-item:hover { border-color:rgba(176,255,60,0.3); }
        .q-item.dragging { opacity:0.5; transform:scale(0.98); }
        .q-item.drag-over { border-color:#B0FF3C; background:rgba(176,255,60,0.05); }
        .q-drag { color:#5A5A5A; font-family:'Geist Mono',monospace; font-size:16px; cursor:grab; }
        .q-order { font-family:'Geist Mono',monospace; color:#B0FF3C; font-weight:700; font-size:14px; min-width:32px; }
        .q-main { flex:1; min-width:0; }
        .q-title { font-weight:700; font-size:16px; margin-bottom:4px; }
        .q-sub { font-family:'Geist Mono',monospace; font-size:11px; color:#5A5A5A; }
        .q-status { font-family:'Geist Mono',monospace; font-size:11px; text-transform:uppercase; min-width:120px; text-align:right; }
        .q-actions { min-width:60px; text-align:right; }
        .q-main { cursor:pointer; }
        .q-expand-icon { font-size:10px; color:#5A5A5A; transition:transform 200ms; display:inline-block; }
        .q-expand-icon.open { transform:rotate(90deg); color:#B0FF3C; }
        .q-sched { font-size:10px; color:#FF9F43; margin-left:8px; }
        .q-detail { list-style:none; margin-bottom:8px; }
        .q-detail-inner { background:#0E0E0E; border:1px solid rgba(255,255,255,0.08); border-top:none; padding:20px; }
        .q-detail-loading { color:#5A5A5A; font-family:'Geist Mono',monospace; font-size:12px; }
        .q-slides-row { display:flex; gap:8px; overflow-x:auto; padding:8px 0; }
        .q-slides-row img { width:120px; height:120px; object-fit:cover; border:1px solid rgba(255,255,255,0.1); flex-shrink:0; }
        .q-caption-box { margin-top:12px; background:#111; border:1px solid rgba(255,255,255,0.06); padding:12px; font-family:'Geist Mono',monospace;
          font-size:11px; color:#CCC; max-height:180px; overflow-y:auto; white-space:pre-wrap; line-height:1.5; }
        .q-schedule-row { margin-top:16px; display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
        .q-schedule-row label { font-family:'Geist Mono',monospace; font-size:12px; color:#8A8A8A; }
        .q-schedule-row input[type="datetime-local"] { padding:8px 12px; background:#111; color:#F5F5F5; border:1px solid rgba(255,255,255,0.2);
          font-family:'Geist Mono',monospace; font-size:12px; }
        .q-schedule-row button { padding:8px 16px; border:none; font-weight:700; font-family:inherit; font-size:11px; cursor:pointer; text-transform:uppercase; }
        .q-schedule-row .btn-sched { background:#FF9F43; color:#0A0A0A; }
        .q-schedule-row .btn-unsched { background:#333; color:#F5F5F5; }
        .q-meta-row { margin-top:8px; font-family:'Geist Mono',monospace; font-size:10px; color:#5A5A5A; }
        .empty { color:#5A5A5A; font-family:'Geist Mono',monospace; font-size:13px; padding:40px; text-align:center; border:1px dashed rgba(255,255,255,0.1); }
        .log { margin-top:32px; background:#0E0E0E; border:1px solid rgba(255,255,255,0.1); padding:16px; font-family:'Geist Mono',monospace; font-size:11px; color:#8A8A8A; max-height:200px; overflow-y:auto; white-space:pre-wrap; }
        .log .ok { color:#B0FF3C; }
        .log .err { color:#FF6B6B; }
      </style>
    </head>
    <body>
      <a href="/" class="back">← dashboard</a>
      <h1>Posting <span class="accent">Queue</span></h1>
      <div class="sub">{count} aprovados · arraste pra reordenar · clique SHIP quando a ordem estiver certa</div>

      <div class="bar">
        <button class="btn-reload" onclick="location.reload()">↻ reload</button>
        <button class="btn-prepare" onclick="prepare()">⚙ prepare all (export + captions)</button>
        <button class="btn-dry" onclick="ship(true)">◉ dry-run ship</button>
        <button class="btn-ship" onclick="ship(false)">🚀 SHIP TO INSTAGRAM</button>
        <div class="delay">
          delay entre posts: <input type="number" id="delay" value="900" min="300" max="7200"> segundos
        </div>
      </div>

      <ul class="q-list" id="qlist">
        {rows}
      </ul>

      {empty}

      <div class="log" id="log">waiting for action...</div>

      <script>
        const list = document.getElementById('qlist');
        const log = document.getElementById('log');
        let dragged = null;

        function logLine(msg, cls='') {
          const line = document.createElement('div');
          if (cls) line.className = cls;
          line.textContent = '[' + new Date().toLocaleTimeString() + '] ' + msg;
          log.insertBefore(line, log.firstChild);
        }

        // Drag & drop reorder
        list.querySelectorAll('.q-item').forEach(item => {
          item.addEventListener('dragstart', () => {
            dragged = item;
            item.classList.add('dragging');
          });
          item.addEventListener('dragend', async () => {
            item.classList.remove('dragging');
            list.querySelectorAll('.drag-over').forEach(x => x.classList.remove('drag-over'));
            const newOrder = Array.from(list.querySelectorAll('.q-item')).map(el => parseInt(el.dataset.idx));
            logLine('saving new order...');
            const r = await fetch('/api/queue/reorder', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({order: newOrder}),
            });
            const j = await r.json();
            if (j.ok) {
              logLine('✓ order saved', 'ok');
              // Update order numbers visually
              list.querySelectorAll('.q-order').forEach((el, i) => el.textContent = String(i+1).padStart(2,'0'));
              // Update data-idx to new positions
              list.querySelectorAll('.q-item').forEach((el, i) => el.dataset.idx = i);
            } else {
              logLine('✗ reorder failed: ' + (j.error || 'unknown'), 'err');
            }
          });
          item.addEventListener('dragover', e => {
            e.preventDefault();
            if (dragged && dragged !== item) {
              item.classList.add('drag-over');
              const rect = item.getBoundingClientRect();
              const after = (e.clientY - rect.top) > rect.height / 2;
              if (after) {
                item.parentNode.insertBefore(dragged, item.nextSibling);
              } else {
                item.parentNode.insertBefore(dragged, item);
              }
            }
          });
          item.addEventListener('dragleave', () => item.classList.remove('drag-over'));
        });

        // --- Expand / collapse detail panel ---
        const detailCache = {};
        async function toggleDetail(idx, event) {
          if (event && event.target.closest('.q-drag')) return;
          const panel = document.getElementById('detail-' + idx);
          const icon = panel.previousElementSibling.querySelector('.q-expand-icon');
          if (panel.style.display === 'none') {
            panel.style.display = 'list-item';
            if (icon) icon.classList.add('open');
            if (!detailCache[idx]) {
              try {
                const r = await fetch('/api/queue/item/' + idx);
                detailCache[idx] = await r.json();
              } catch(e) {
                panel.querySelector('.q-detail-inner').textContent = 'erro ao carregar';
                return;
              }
            }
            renderDetail(idx, detailCache[idx]);
          } else {
            panel.style.display = 'none';
            if (icon) icon.classList.remove('open');
          }
        }

        function renderDetail(idx, data) {
          const panel = document.getElementById('detail-' + idx);
          const inner = panel.querySelector('.q-detail-inner');
          // Clear previous content safely
          inner.textContent = '';

          if (!data.ok) {
            const err = document.createElement('div');
            err.className = 'q-detail-loading';
            err.style.color = '#FF6B6B';
            err.textContent = 'dados não encontrados — rode PREPARE primeiro';
            inner.appendChild(err);
            return;
          }

          // Slides row
          if (data.slides && data.slides.length) {
            const row = document.createElement('div');
            row.className = 'q-slides-row';
            data.slides.forEach(url => {
              const img = document.createElement('img');
              img.src = url;
              img.alt = 'slide';
              img.loading = 'lazy';
              row.appendChild(img);
            });
            inner.appendChild(row);
          } else {
            const noSlides = document.createElement('div');
            noSlides.className = 'q-meta-row';
            noSlides.textContent = 'nenhum slide exportado — rode PREPARE';
            inner.appendChild(noSlides);
          }

          // Caption box (server already extracts "Post caption" section)
          const captionBox = document.createElement('div');
          captionBox.className = 'q-caption-box';
          captionBox.textContent = data.caption || '(sem caption — rode PREPARE)';
          inner.appendChild(captionBox);

          // Schedule row
          const schedRow = document.createElement('div');
          schedRow.className = 'q-schedule-row';

          const lbl = document.createElement('label');
          lbl.textContent = 'agendar post:';
          schedRow.appendChild(lbl);

          const dtInput = document.createElement('input');
          dtInput.type = 'datetime-local';
          dtInput.id = 'sched-input-' + idx;
          if (data.scheduled_for) dtInput.value = data.scheduled_for.slice(0, 16);
          schedRow.appendChild(dtInput);

          const btnSave = document.createElement('button');
          btnSave.className = 'btn-sched';
          btnSave.textContent = 'salvar agendamento';
          btnSave.addEventListener('click', () => saveSchedule(idx));
          schedRow.appendChild(btnSave);

          const btnClear = document.createElement('button');
          btnClear.className = 'btn-unsched';
          btnClear.textContent = 'limpar';
          btnClear.addEventListener('click', () => clearSchedule(idx));
          schedRow.appendChild(btnClear);

          inner.appendChild(schedRow);

          // Meta row
          const meta = document.createElement('div');
          meta.className = 'q-meta-row';
          meta.textContent = data.slide_count + ' slides · ' + data.source + ' · ' + data.cid;
          inner.appendChild(meta);
        }

        async function saveSchedule(idx) {
          const input = document.getElementById('sched-input-' + idx);
          const val = input.value;
          if (!val) { logLine('selecione data/hora primeiro', 'err'); return; }
          const iso = new Date(val).toISOString();
          const r = await fetch('/api/queue/schedule', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({idx: idx, scheduled_for: iso}),
          });
          const j = await r.json();
          if (j.ok) {
            logLine('✓ agendamento salvo: ' + val, 'ok');
            detailCache[idx] = null;
            setTimeout(() => location.reload(), 800);
          } else {
            logLine('✗ erro: ' + (j.error || 'unknown'), 'err');
          }
        }

        async function clearSchedule(idx) {
          const r = await fetch('/api/queue/schedule', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({idx: idx, scheduled_for: null}),
          });
          const j = await r.json();
          if (j.ok) {
            logLine('✓ agendamento removido', 'ok');
            detailCache[idx] = null;
            setTimeout(() => location.reload(), 800);
          } else {
            logLine('✗ erro: ' + (j.error || 'unknown'), 'err');
          }
        }

        async function prepare() {
          logLine('preparing queue: exporting PNGs + generating captions...');
          const r = await fetch('/api/queue/prepare', {method: 'POST'});
          const j = await r.json();
          if (j.ok) {
            logLine('✓ prepare complete: ' + j.prepared + ' items ready', 'ok');
            setTimeout(() => location.reload(), 1500);
          } else {
            logLine('✗ prepare failed: ' + (j.error || 'unknown'), 'err');
          }
        }

        async function ship(dry) {
          const delay = document.getElementById('delay').value || 900;
          const label = dry ? 'DRY-RUN' : 'LIVE SHIP';
          if (!dry && !confirm('Vai publicar de verdade no Instagram. Confirma a ordem atual?')) return;
          logLine('🚢 ' + label + ' started — delay ' + delay + 's between posts');
          const r = await fetch('/api/queue/ship', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({dry_run: dry, delay: parseInt(delay)}),
          });
          const j = await r.json();
          if (j.ok) {
            logLine('✓ ship dispatched in background — monitor terminal OR reload page', 'ok');
            setTimeout(() => location.reload(), 3000);
          } else {
            logLine('✗ ship failed: ' + (j.error || 'unknown'), 'err');
          }
        }
      </script>
    </body>
    </html>
    """
    empty_msg = '<div class="empty">fila vazia — aprove carrosséis no dashboard primeiro</div>' if not queue["items"] else ""
    return html.replace("{count}", str(len(queue["items"]))).replace("{rows}", rows_html).replace("{empty}", empty_msg)


@app.route("/api/queue/posting")
def api_queue_posting_get():
    return jsonify(rebuild_posting_queue())


@app.route("/api/queue/item/<int:idx>")
def api_queue_item_detail(idx):
    """Return detail for a single queue item: slides (as URLs), caption text, metadata."""
    queue = load_posting_queue()
    items = queue.get("items", [])
    if idx < 0 or idx >= len(items):
        return jsonify({"ok": False, "error": "index out of range"}), 404

    item = items[idx]
    source = item["source"]
    cid = item["cid"]
    approved_date = item.get("approved_date", str(date.today()))

    # Find the approved folder
    date_dir = APPROVED / approved_date
    candidates = list(date_dir.glob(f"{cid}-*")) if date_dir.exists() else []
    folder = candidates[0] if candidates else None

    detail = {
        "ok": True,
        "source": source,
        "cid": cid,
        "title": item.get("title", cid),
        "status": item.get("status", "pending"),
        "scheduled_for": item.get("scheduled_for"),
        "slides": [],
        "caption": "",
        "metadata": {},
        "slide_count": 0,
    }

    if folder and folder.exists():
        slides_dir = folder / "slides"
        if slides_dir.exists():
            slides = sorted(slides_dir.glob("*.png"))
            detail["slides"] = [f"/api/queue/slide/{approved_date}/{folder.name}/{s.name}" for s in slides]
            detail["slide_count"] = len(slides)

        caption_file = folder / "caption.md"
        if caption_file.exists():
            import re as _re
            raw = caption_file.read_text()
            detail["caption_raw"] = raw
            # Extract just the "Post caption" section for display
            m = _re.search(r"## Post caption[^\n]*\n+(.+?)(?=\n## |\Z)", raw, _re.DOTALL)
            detail["caption"] = m.group(1).strip() if m else raw[:800]

        meta_file = folder / "metadata.json"
        if meta_file.exists():
            try:
                detail["metadata"] = json.loads(meta_file.read_text())
            except Exception:
                pass

    return jsonify(detail)


@app.route("/api/queue/slide/<date_str>/<folder_name>/<filename>")
def api_queue_slide(date_str, folder_name, filename):
    """Serve a slide PNG from the approved folder."""
    slides_dir = APPROVED / date_str / folder_name / "slides"
    if not slides_dir.exists():
        abort(404)
    return send_from_directory(str(slides_dir), filename)


@app.route("/api/queue/schedule", methods=["POST"])
def api_queue_schedule():
    """Set scheduled_for datetime on a queue item."""
    data = request.get_json() or {}
    idx = data.get("idx")
    scheduled_for = data.get("scheduled_for")  # ISO string or null

    if idx is None:
        return jsonify({"ok": False, "error": "idx required"}), 400

    queue = load_posting_queue()
    items = queue.get("items", [])
    if idx < 0 or idx >= len(items):
        return jsonify({"ok": False, "error": "index out of range"}), 404

    items[idx]["scheduled_for"] = scheduled_for
    items[idx]["last_update"] = datetime.now().isoformat()
    save_posting_queue(queue)

    return jsonify({"ok": True, "idx": idx, "scheduled_for": scheduled_for})


@app.route("/api/queue/reorder", methods=["POST"])
def api_queue_reorder():
    data = request.get_json() or {}
    order = data.get("order", [])
    queue = load_posting_queue()
    items = queue.get("items", [])
    if len(order) != len(items):
        return jsonify({"ok": False, "error": f"order length mismatch ({len(order)} vs {len(items)})"}), 400
    try:
        new_items = [items[i] for i in order]
    except IndexError:
        return jsonify({"ok": False, "error": "invalid index in order"}), 400
    for i, it in enumerate(new_items):
        it["order"] = i
    queue["items"] = new_items
    save_posting_queue(queue)
    return jsonify({"ok": True, "count": len(new_items)})


@app.route("/api/queue/prepare", methods=["POST"])
def api_queue_prepare():
    """Export PNGs + generate captions for all pending items."""
    queue = rebuild_posting_queue()
    prepared = 0
    errors = []

    for idx, item in enumerate(queue["items"]):
        if item.get("status") in {"done", "skipped"}:
            continue

        # Only prepare items that need export/caption (don't ship here)
        cmd = [
            sys.executable, str(SCRIPTS / "ship-queue.py"),
            "--dry-run", "--delay", "0", "--item", str(idx),
        ]
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=600)
        if res.returncode == 0:
            prepared += 1
        else:
            errors.append({"idx": idx, "cid": item["cid"], "error": res.stderr[-300:]})

    return jsonify({"ok": True, "prepared": prepared, "errors": errors})


@app.route("/api/queue/ship", methods=["POST"])
def api_queue_ship():
    """Dispatch the ship-queue orchestrator in background."""
    data = request.get_json() or {}
    dry_run = data.get("dry_run", False)
    delay = int(data.get("delay", 900))

    cmd = [sys.executable, str(SCRIPTS / "ship-queue.py"), "--delay", str(delay)]
    if dry_run:
        cmd.append("--dry-run")

    log_file = OUTPUT / "approved" / "queue" / "ship.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_fh = open(log_file, "a")
    log_fh.write(f"\n\n━━ ship started at {datetime.now().isoformat()} (dry_run={dry_run}) ━━\n")
    log_fh.flush()

    try:
        subprocess.Popen(cmd, cwd=REPO_ROOT, stdout=log_fh, stderr=subprocess.STDOUT)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

    return jsonify({"ok": True, "log_file": str(log_file.relative_to(REPO_ROOT)), "dry_run": dry_run, "delay": delay})


if __name__ == "__main__":
    port = int(os.environ.get("GROWTHOS_REVIEW_PORT", "5050"))
    print(f"\n🎬 GrowthOS Review Dashboard")
    print(f"   http://localhost:{port}")
    print(f"   design-system: {DESIGN_SYSTEM}")
    print(f"   reviews: {REVIEWS_FILE}\n")
    app.run(host="127.0.0.1", port=port, debug=False)
