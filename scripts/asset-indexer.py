#!/usr/bin/env python3
"""
asset-indexer.py — indexador de assets do GrowthOS

Usage:
    python asset-indexer.py <path-to-asset>     # indexa 1 arquivo
    python asset-indexer.py --reindex           # reindexa tudo, regenera INDEX.md

O indexador:
    1. Extrai paleta dominante (usa Pillow + colorthief se instalado)
    2. Infere tipo pela pasta (logos/screenshots/icons/photos)
    3. Gera sidecar .meta.yaml em assets/_meta/
    4. Atualiza INDEX.md agregando todos os sidecars

Dependencies (auto-install no primeiro run):
    - PyYAML
    - Pillow (opcional, pra paleta de PNG/JPG)
    - colorthief (opcional, pra paleta rica)

SVG: lê paleta por regex simples dos fills/strokes.
"""

import sys
import os
import re
import json
import subprocess
from pathlib import Path
from datetime import date, datetime

REPO_ROOT = Path(__file__).resolve().parents[2]
GROWTHOS = REPO_ROOT / "growthOS"
ASSETS = GROWTHOS / "assets"
META_DIR = ASSETS / "_meta"
INDEX_FILE = ASSETS / "INDEX.md"

CATEGORIES = ["logos", "screenshots", "icons", "photos"]
DS_ACCENTS = {"lime": "#B0FF3C", "yellow": "#FFE600", "cyan": "#00F0FF"}


def ensure_deps():
    try:
        import yaml  # noqa
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pyyaml"], check=False)


def infer_type(asset_path: Path) -> str:
    for cat in CATEGORIES:
        if f"/{cat}/" in str(asset_path):
            return cat[:-1] if cat.endswith("s") else cat
    return "unknown"


def extract_svg_palette(svg_path: Path) -> list:
    try:
        content = svg_path.read_text()
        colors = set(re.findall(r"#[0-9A-Fa-f]{6}", content))
        return sorted(colors)[:5]
    except Exception:
        return []


def extract_image_palette(img_path: Path) -> list:
    try:
        from PIL import Image
        img = Image.open(img_path).convert("RGB")
        img.thumbnail((200, 200))
        pixels = list(img.getdata())
        from collections import Counter
        common = Counter(pixels).most_common(5)
        return ["#{:02X}{:02X}{:02X}".format(*rgb) for rgb, _ in common]
    except Exception:
        return []


def derive_tags(filename: str, asset_type: str) -> list:
    stem = Path(filename).stem.lower()
    tags = {asset_type}
    tags.update(re.split(r"[-_\s]+", stem))
    tags.discard("")
    return sorted(tags)


def voice_fit_from_palette(palette: list) -> str:
    if not palette:
        return "neutral"
    palette_up = [c.upper() for c in palette]
    if any(c in palette_up for c in DS_ACCENTS.values()):
        return "aligns"
    if "#000000" in palette_up or "#0A0A0A" in palette_up:
        return "aligns"
    return "neutral"


def index_one(asset_path: Path, skip_vision: bool = False) -> dict:
    import yaml
    META_DIR.mkdir(parents=True, exist_ok=True)
    asset_type = infer_type(asset_path)
    filename = asset_path.name
    ext = asset_path.suffix.lower()

    if ext == ".svg":
        palette = extract_svg_palette(asset_path)
    elif ext in {".png", ".jpg", ".jpeg", ".webp"}:
        palette = extract_image_palette(asset_path)
    else:
        palette = []

    rel_path = str(asset_path.relative_to(GROWTHOS))
    meta_file = META_DIR / f"{filename}.meta.yaml"

    # Preserve existing vision data if present
    existing = {}
    if meta_file.exists():
        try:
            existing = yaml.safe_load(meta_file.read_text()) or {}
        except Exception:
            existing = {}

    meta = {
        "asset": filename,
        "path": rel_path,
        "type": asset_type,
        "tags": derive_tags(filename, asset_type),
        "suggested_use": ["hook", "demo"] if asset_type == "logo" else ["evidence", "demo"],
        "palette": palette,
        "dominant_color": palette[0] if palette else None,
        "voice_fit": voice_fit_from_palette(palette),
        "position_hint": "top-right" if asset_type == "logo" else "center",
        "size_category": "small" if asset_type == "logo" else "medium",
        "format": ext.lstrip("."),
        "added": str(date.today()),
    }

    # Preserve vision block from existing sidecar
    if "vision" in existing:
        meta["vision"] = existing["vision"]

    # Vision skeleton (Claude Code with native Read tool will fill it later)
    # NOTA: não chamamos API aqui. O carousel-designer agente (ou você na conversa)
    # usa Read tool direto na imagem pra analisar — plano Max, sem custo extra.
    if not skip_vision and "vision" not in meta:
        meta["vision"] = {
            "_status": "pending",
            "_instructions": "Claude Code: leia a imagem via Read e preencha este bloco. Veja scripts/asset-vision.py --schema",
            "_prepared_at": str(datetime.now().isoformat()),
        }

    meta_file.write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True))
    print(f"✅ indexed {rel_path} → {meta_file.relative_to(GROWTHOS)}")
    return meta


def reindex_all(skip_vision: bool = False):
    import yaml
    all_assets = []
    for cat in CATEGORIES:
        cat_dir = ASSETS / cat
        if not cat_dir.exists():
            continue
        for asset in sorted(cat_dir.iterdir()):
            if asset.is_file() and not asset.name.startswith("."):
                all_assets.append(index_one(asset, skip_vision=skip_vision))

    write_index(all_assets)
    print(f"\n📚 INDEX.md regenerated with {len(all_assets)} assets")


def _vision_summary(meta: dict) -> dict:
    """Pull key vision fields if present, falling back gracefully."""
    v = meta.get("vision") or {}
    if not v or v.get("_status") == "pending":
        return {
            "status": "⏳ pending",
            "subject": "(sem análise visual — drop no Claude Code pra analisar)",
            "fit_score": None,
            "topics": "",
        }
    score = v.get("brand_fit_score")
    fit_badge = "✓✓" if (score or 0) >= 0.9 else ("✓" if (score or 0) >= 0.7 else "~")
    return {
        "status": f"{fit_badge} done",
        "subject": (v.get("subject") or "")[:80],
        "fit_score": score,
        "topics": ", ".join((v.get("suggested_topics") or [])[:3]),
    }


def write_index(assets: list):
    lines = [
        "# Asset Library Index",
        "",
        f"> **Auto-gerado por:** `growthOS/scripts/asset-indexer.py`",
        f"> **Lido por:** `carousel-designer`, `content-creator`, `caption-writer`",
        f"> **Última atualização:** {date.today()}",
        f"> **Total assets:** {len(assets)}",
        "",
        "---",
        "",
        "## Como o agente usa",
        "",
        "Durante a Phase 2 do carousel-designer, o agente:",
        "",
        "1. Lê este INDEX.md + os sidecars completos em `_meta/*.meta.yaml`",
        "2. Pra cada slide, extrai 2-5 keywords e compara contra `vision.suggested_topics` (semantic match)",
        "3. Filtra por `vision.brand_fit_score >= 0.7`",
        "4. Posiciona usando `vision.best_placement` (position + size + reason)",
        "5. Respeita override explícito do brief",
        "",
        "---",
        "",
    ]
    by_type = {}
    for a in assets:
        by_type.setdefault(a["type"], []).append(a)

    icons = {"logo": "🎨 Logos", "screenshot": "📸 Screenshots", "icon": "🔣 Icons", "photo": "🖼 Photos"}
    for t in ["logo", "screenshot", "icon", "photo"]:
        lines.append(f"### {icons.get(t, t.title())}")
        lines.append("")
        if t in by_type:
            lines.append("| Asset | Fit | Subject | Suggested topics |")
            lines.append("|---|---|---|---|")
            for a in by_type[t]:
                v = _vision_summary(a)
                score_str = f"{v['fit_score']:.2f}" if v["fit_score"] is not None else "—"
                lines.append(
                    f"| `{a['asset']}` ({v['status']}) | {score_str} | {v['subject']} | {v['topics']} |"
                )
        else:
            lines.append("_(vazio — adicione arquivos em `assets/" + t + "s/`)_")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Assets por brand_fit_score (ordem decrescente)",
        "",
    ])
    ranked = []
    for a in assets:
        v = a.get("vision") or {}
        score = v.get("brand_fit_score")
        if score is not None:
            ranked.append((score, a["asset"], v.get("subject", "")[:70]))
    ranked.sort(reverse=True)
    if ranked:
        lines.append("| Score | Asset | Subject |")
        lines.append("|---|---|---|")
        for score, asset, subject in ranked:
            lines.append(f"| **{score:.2f}** | `{asset}` | {subject} |")
    else:
        lines.append("_(nenhum asset analisado por vision ainda)_")
    lines.append("")

    lines.extend([
        "---",
        "",
        "## Como adicionar um novo asset",
        "",
        "```bash",
        "cp ~/Downloads/asset.png growthOS/assets/logos/",
        ".venv/bin/python growthOS/scripts/asset-indexer.py growthOS/assets/logos/asset.png",
        "# depois, na conversa: 'analisa os assets pendentes'",
        ".venv/bin/python growthOS/scripts/asset-indexer.py --reindex  # regenera INDEX.md",
        "```",
    ])
    INDEX_FILE.write_text("\n".join(lines))


def main():
    ensure_deps()
    if len(sys.argv) < 2:
        print("usage:")
        print("  asset-indexer.py <path-to-asset>        # index + vision")
        print("  asset-indexer.py <path> --no-vision     # index only, skip Claude Vision")
        print("  asset-indexer.py --reindex              # reindex all + vision for new")
        print("  asset-indexer.py --reindex --no-vision  # reindex all, skip vision")
        sys.exit(1)

    skip_vision = "--no-vision" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--no-vision"]

    if not args:
        print("❌ no path or --reindex specified")
        sys.exit(1)

    arg = args[0]
    if arg == "--reindex":
        reindex_all(skip_vision=skip_vision)
    else:
        asset_path = Path(arg).resolve()
        if not asset_path.exists():
            print(f"❌ not found: {asset_path}")
            sys.exit(1)
        index_one(asset_path, skip_vision=skip_vision)
        reindex_all(skip_vision=skip_vision)


if __name__ == "__main__":
    main()
