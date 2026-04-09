#!/usr/bin/env python3
"""
ship-queue.py — Orchestrator que publica a fila de aprovados no Instagram

Usage:
    python ship-queue.py                     # publica a fila inteira na ordem definida
    python ship-queue.py --dry-run           # simula sem publicar
    python ship-queue.py --delay 1800        # espera 30 min entre posts (default 900s = 15 min)
    python ship-queue.py --max 3             # limita a 3 posts por execução
    python ship-queue.py --item <idx>        # publica só 1 item específico (índice 0-based)

Fluxo pra cada item da fila:
    1. Verifica se existe folder em output/approved/<date>/<slug>/
    2. Se não: roda export-carousel.mjs + organize-approved.py pra criar
    3. Verifica se caption.md tem conteúdo (não placeholder) — se não: gera via generate_caption.py
    4. Roda ig_publisher.py --folder <path> (usa sessão Chrome persistida)
    5. Atualiza queue.json com status (pending → exporting → captioning → publishing → done / failed)
    6. Aguarda `delay` segundos antes do próximo
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GROWTHOS = REPO_ROOT / "growthOS"
OUTPUT = GROWTHOS / "output"
APPROVED = OUTPUT / "approved"
QUEUE_FILE = APPROVED / "queue" / "queue.json"
DESIGN_SYSTEM = GROWTHOS / "design-system"
SCRIPTS = GROWTHOS / "scripts"
PUBLISHER = GROWTHOS / "publisher" / "ig_publisher.py"
VENV_PY = GROWTHOS / ".venv" / "bin" / "python"


def load_queue() -> dict:
    if not QUEUE_FILE.exists():
        return {"items": [], "updated_at": None}
    return json.loads(QUEUE_FILE.read_text())


def save_queue(q: dict):
    q["updated_at"] = datetime.now().isoformat()
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(q, indent=2, ensure_ascii=False))


def slugify(s: str) -> str:
    import re
    s = s.lower()
    for a, b in [("á", "a"), ("à", "a"), ("ã", "a"), ("â", "a"),
                 ("é", "e"), ("ê", "e"), ("í", "i"), ("ó", "o"),
                 ("ô", "o"), ("õ", "o"), ("ú", "u"), ("ç", "c")]:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:40] or "untitled"


def update_status(queue: dict, idx: int, status: str, **extra):
    if 0 <= idx < len(queue["items"]):
        queue["items"][idx]["status"] = status
        queue["items"][idx]["last_update"] = datetime.now().isoformat()
        queue["items"][idx].update(extra)
        save_queue(queue)


def ensure_export(item: dict, idx: int, queue: dict) -> Path | None:
    """Garante que output/approved/<date>/<cid>-<slug>/ exists com PNGs + metadata."""
    source = item["source"]
    cid = item["cid"]
    title = item.get("title", cid)
    slug = slugify(title)
    today = item.get("approved_date", str(date.today()))

    approved_folder = APPROVED / today / f"{cid}-{slug}"
    slides_folder = approved_folder / "slides"

    if slides_folder.exists() and any(slides_folder.glob("*.png")):
        return approved_folder

    update_status(queue, idx, "exporting")
    print(f"  📸 exporting {cid}...")

    stem = Path(source).stem
    src_html = DESIGN_SYSTEM / source

    # Run export (Python playwright — no npm install needed)
    export_cmd = [str(VENV_PY), str(SCRIPTS / "export_carousel.py"), str(src_html), "--carousel", cid]
    res = subprocess.run(export_cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=300)
    if res.returncode != 0:
        print(f"  ❌ export failed: {res.stderr[-300:]}")
        update_status(queue, idx, "failed", error="export failed")
        return None

    # Run organize
    update_status(queue, idx, "organizing")
    print(f"  📂 organizing {cid}...")
    org_cmd = [
        str(VENV_PY), str(SCRIPTS / "organize-approved.py"),
        "--carousel", cid, "--source", stem, "--date", today,
    ]
    res = subprocess.run(org_cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)
    if res.returncode != 0:
        print(f"  ❌ organize failed: {res.stderr[-300:]}")
        update_status(queue, idx, "failed", error="organize failed")
        return None

    # Find the folder the organizer created (may have different slug from ours)
    date_dir = APPROVED / today
    candidates = list(date_dir.glob(f"{cid}-*")) if date_dir.exists() else []
    if candidates:
        return candidates[0]
    return None


def ensure_caption(folder: Path, queue: dict, idx: int) -> bool:
    """Garante que caption.md tem conteúdo real (não só placeholder)."""
    caption_file = folder / "caption.md"
    if caption_file.exists():
        content = caption_file.read_text()
        # Heuristic: placeholder has "pending caption-writer" comment
        if "pending caption-writer" not in content and "## Post caption" in content:
            return True

    update_status(queue, idx, "captioning")
    print(f"  ✏ generating caption...")

    cmd = [str(VENV_PY), str(SCRIPTS / "generate_caption.py"), "--folder", str(folder)]
    res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=60)
    if res.returncode != 0:
        print(f"  ❌ caption generation failed: {res.stderr[-300:]}")
        return False
    return True


def publish(folder: Path, queue: dict, idx: int, dry_run: bool) -> bool:
    update_status(queue, idx, "publishing")
    print(f"  🚀 publishing {folder.name}...")

    cmd = [str(VENV_PY), str(PUBLISHER), "--folder", str(folder)]
    if dry_run:
        cmd.append("--dry-run")

    res = subprocess.run(cmd, cwd=REPO_ROOT, timeout=600)
    if res.returncode != 0:
        update_status(queue, idx, "failed", error="publish failed")
        return False

    update_status(queue, idx, "done", published_at=datetime.now().isoformat())
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delay", type=int, default=900, help="seconds between posts (default 900 = 15 min)")
    parser.add_argument("--max", type=int, default=10, help="max items per run")
    parser.add_argument("--item", type=int, help="publish only 1 item (0-based idx)")
    args = parser.parse_args()

    queue = load_queue()
    items = queue.get("items", [])
    if not items:
        print("📭 queue is empty")
        sys.exit(0)

    # Determine which items to process
    if args.item is not None:
        indices = [args.item] if 0 <= args.item < len(items) else []
    else:
        indices = [i for i, it in enumerate(items) if it.get("status") not in {"done", "skipped"}][:args.max]

    if not indices:
        print("✅ nothing pending in queue")
        sys.exit(0)

    print(f"🚢 shipping {len(indices)} item(s) in order")
    if args.dry_run:
        print("   [DRY RUN]")
    print()

    for n, idx in enumerate(indices, 1):
        item = items[idx]
        cid = item["cid"]
        source = item["source"]
        print(f"━━ [{n}/{len(indices)}] {source} · {cid} ━━")

        # 1. Ensure export
        folder = ensure_export(item, idx, queue)
        if not folder:
            continue

        # 2. Ensure caption
        if not ensure_caption(folder, queue, idx):
            update_status(queue, idx, "failed", error="caption failed")
            continue

        # 3. Publish
        if not publish(folder, queue, idx, args.dry_run):
            continue

        print(f"  ✅ {cid} done")

        # 4. Delay before next
        if n < len(indices) and not args.dry_run:
            print(f"\n  ⏱ aguardando {args.delay}s antes do próximo...")
            time.sleep(args.delay)
        print()

    # Final report
    done = sum(1 for it in items if it.get("status") == "done")
    failed = sum(1 for it in items if it.get("status") == "failed")
    print(f"\n✅ ship complete: {done} done, {failed} failed, {len(items) - done - failed} remaining")


if __name__ == "__main__":
    main()
