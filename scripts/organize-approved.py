#!/usr/bin/env python3
"""
organize-approved.py — Organiza um carrossel aprovado em output/approved/{data}/{id}/

Usage:
    python organize-approved.py --carousel c04 --source carousels-v3

Pipeline:
    1. Localiza os PNGs em output/carousels/{source}/{carousel}/slides/
    2. Cria output/approved/{YYYY-MM-DD}/{carousel}-{slug}/
    3. Copia os PNGs pra slides/
    4. Extrai metadata do brief (se existir) → metadata.json
    5. Dispara caption-writer (via simple prompt stub ou agent)
    6. Cria post-status.json (status: draft)
"""

import argparse
import json
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GROWTHOS = REPO_ROOT / "growthOS"
OUTPUT = GROWTHOS / "output"
DESIGN_SYSTEM = GROWTHOS / "design-system"
PREFERENCES = GROWTHOS / "voice" / "preferences"


def find_brief_for_source(source: str) -> Path | None:
    """Try to locate the brief file matching the carousel source."""
    candidates = [
        DESIGN_SYSTEM / f"BRIEF-{source.upper()}.md",
        DESIGN_SYSTEM / f"BRIEF-10-CAROUSELS-{source.upper().replace('CAROUSELS-', '')}.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    # fallback: glob
    for f in DESIGN_SYSTEM.glob("BRIEF-*.md"):
        if source.lower() in f.name.lower():
            return f
    return None


def extract_carousel_info(brief: Path, cid: str) -> dict:
    """Parse the brief markdown to extract info for this carousel."""
    if not brief:
        return {"title": cid, "category": "unknown", "code": "", "bonus": ""}

    text = brief.read_text(encoding="utf-8")
    lines = text.split("\n")

    # match "### 04 — SOMETHING" or "### C04 ..." or "### 4 — ..."
    num_pattern = re.compile(rf"^###\s+0?{cid.lstrip('c').lstrip('C').lstrip('0') or '0'}\b")
    alt_pattern = re.compile(rf"^###\s+{cid}\b", re.IGNORECASE)

    start = None
    for i, line in enumerate(lines):
        if num_pattern.match(line) or alt_pattern.match(line):
            start = i
            break

    if start is None:
        return {"title": cid, "category": "unknown", "code": "", "bonus": ""}

    # Read until next ### or EOF
    chunk = []
    for line in lines[start + 1:]:
        if line.startswith("### "):
            break
        chunk.append(line)

    chunk_text = "\n".join(chunk)
    info = {"title": cid, "category": "unknown", "code": "", "bonus": ""}

    # Try to extract: Tema, Code, Bônus, Variant, Categoria
    for key, pattern in [
        ("title", r"\*\*Tema:\*\*\s*(.+)"),
        ("code", r"\*\*Code:\*\*\s*(\S+)"),
        ("bonus", r"\*\*Bônus:\*\*\s*(.+)"),
        ("variant", r"Variant:\s*`?(\S+?)`?\s*—"),
        ("category", r"Cat:\s*(\S+)"),
    ]:
        m = re.search(pattern, chunk_text)
        if m:
            info[key] = m.group(1).strip()

    return info


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[áàâã]", "a", s)
    s = re.sub(r"[éèê]", "e", s)
    s = re.sub(r"[íì]", "i", s)
    s = re.sub(r"[óòôõ]", "o", s)
    s = re.sub(r"[úù]", "u", s)
    s = re.sub(r"ç", "c", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:40]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--carousel", required=True, help="carousel id e.g. c04")
    parser.add_argument("--source", required=True, help="source stem e.g. carousels-v3")
    parser.add_argument("--date", default=str(date.today()), help="target date YYYY-MM-DD")
    args = parser.parse_args()

    cid = args.carousel
    source = args.source

    # 1. Locate PNGs
    src_slides = OUTPUT / "carousels" / source / cid / "slides"
    if not src_slides.exists():
        print(f"❌ PNGs not found at {src_slides}")
        print("   Run export-carousel.mjs first.")
        sys.exit(1)

    pngs = sorted(src_slides.glob("*.png"))
    if not pngs:
        print(f"❌ no PNGs in {src_slides}")
        sys.exit(1)

    # 2. Extract brief info
    brief = find_brief_for_source(source)
    info = extract_carousel_info(brief, cid) if brief else {"title": cid, "category": "unknown", "code": "", "bonus": ""}
    slug = slugify(info.get("title", cid))

    # 3. Create approved folder
    approved_dir = OUTPUT / "approved" / args.date / f"{cid}-{slug}"
    slides_dir = approved_dir / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    # 4. Copy PNGs
    for png in pngs:
        dest = slides_dir / png.name
        shutil.copy2(png, dest)

    # 5. Write metadata.json
    metadata = {
        "schema_version": 1,
        "carousel_id": cid,
        "source": source,
        "brief": str(brief.relative_to(GROWTHOS)) if brief else None,
        "title": info.get("title", cid),
        "slug": slug,
        "category": info.get("category", "unknown"),
        "variant": info.get("variant", "lime-geist"),
        "code": info.get("code", ""),
        "bonus": info.get("bonus", ""),
        "slide_count": len(pngs),
        "slides": [p.name for p in pngs],
        "approved_at": datetime.now().isoformat(),
        "approved_date": args.date,
    }
    (approved_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    # 6. Write post-status.json
    post_status = {
        "status": "draft",
        "caption_written": False,
        "published": False,
        "post_url": None,
        "scheduled_for": None,
        "metrics": {},
    }
    (approved_dir / "post-status.json").write_text(json.dumps(post_status, indent=2))

    # 7. Empty caption.md placeholder (will be filled by caption-writer agent)
    caption_placeholder = f"""# Caption — {info.get("title", cid)}

<!-- pending caption-writer agent generation -->

**status:** draft
**code:** {info.get("code", "")}
**category:** {info.get("category", "")}
"""
    (approved_dir / "caption.md").write_text(caption_placeholder)

    print(f"✅ organized {cid} → {approved_dir.relative_to(GROWTHOS)}")
    print(f"   {len(pngs)} slides")
    print(f"   metadata.json ✓")
    print(f"   post-status.json ✓ (draft)")
    print(f"   caption.md placeholder ✓")


if __name__ == "__main__":
    main()
