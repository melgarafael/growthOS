#!/usr/bin/env python3
"""
asset-vision.py — Lista assets pendentes de análise visual

NOTA: NÃO chama API do Claude. Claude Code (via plano Max) tem vision nativo
através do tool Read — o carousel-designer agent (ou você na conversa) lê a
imagem diretamente e escreve a análise no sidecar. Zero custo de API, zero
API key necessária.

Este script tem 2 funções:
    1. Listar assets sem análise visual (pendentes)
    2. Criar o sidecar skeleton pronto pra Claude Code preencher

Usage:
    .venv/bin/python asset-vision.py --pending          # lista pendentes
    .venv/bin/python asset-vision.py --prepare PATH     # cria skeleton no sidecar
    .venv/bin/python asset-vision.py --prepare-all      # skeleton pra todos

Como fazer a análise depois:
    Na conversa do Claude Code, só pedir:
        "analisa os assets pendentes e preenche os sidecars"
    Claude usa Read tool em cada imagem, analisa, e escreve no sidecar.
"""

import argparse
import hashlib
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GROWTHOS = REPO_ROOT / "growthOS"
ASSETS = GROWTHOS / "assets"
META_DIR = ASSETS / "_meta"
CATEGORIES = ["logos", "screenshots", "icons", "photos"]

SKELETON_VISION = {
    "_status": "pending",
    "_instructions": (
        "Claude Code: leia a imagem via Read tool e preencha este bloco com análise "
        "visual. Estrutura esperada abaixo. Depois de preencher, mude _status pra 'done' "
        "e adicione _cached_hash + _analyzed_at."
    ),
    "subject": "",
    "visual_type": "",
    "dominant_elements": [],
    "dominant_colors": [],
    "mood": "",
    "brand_fit_score": 0.0,
    "brand_fit_reason": "",
    "best_placement": [],
    "suggested_topics": [],
    "do_not_use_when": [],
    "contrast_considerations": "",
    "text_overlay_ok": True,
    "crop_hint": "",
    "accessibility_alt": "",
}

SCHEMA_REFERENCE = """
## Schema a preencher (via Read tool + escrita no sidecar)

subject: "descrição objetiva em 1 frase do que a imagem mostra"
visual_type: logo_monochrome | logo_colored | screenshot_ui | photo_person | photo_object | icon | diagram | chart | illustration | abstract
dominant_elements: [lista, de, elementos, principais]
dominant_colors: ["#HEX1", "#HEX2"]
mood: "3-5 adjetivos (ex: technical, minimal, futuristic)"
brand_fit_score: 0.0-1.0  # quanto combina com @melgarafael (dark lime-geist, confessional, anti-guru)
brand_fit_reason: "por que combina ou não"
best_placement:
  - slide_type: "cover | hook | demo | framework | stat | cta | filosofico"
    position: "top-right | top-left | centered_small | centered_large | full_bleed | side_panel"
    size: "small | medium | large"
    reason: "justificativa curta"
suggested_topics: [lista de temas de carrossel onde brilha]
do_not_use_when: [lista de contextos a evitar]
contrast_considerations: "nota sobre legibilidade em dark mode lime-geist"
text_overlay_ok: true | false
crop_hint: "se precisar cortar, onde fica o foco"
accessibility_alt: "alt text curto"
_cached_hash: "sha256 truncado"
_analyzed_at: "ISO timestamp"
_status: "done"
"""


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def load_sidecar(asset_path: Path):
    import yaml
    sidecar = META_DIR / f"{asset_path.name}.meta.yaml"
    if not sidecar.exists():
        return sidecar, {}
    try:
        return sidecar, yaml.safe_load(sidecar.read_text()) or {}
    except Exception:
        return sidecar, {}


def save_sidecar(sidecar_path: Path, data: dict):
    import yaml
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    sidecar_path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))


def iter_all_assets():
    for cat in CATEGORIES:
        cat_dir = ASSETS / cat
        if not cat_dir.exists():
            continue
        for asset in sorted(cat_dir.iterdir()):
            if asset.is_file() and not asset.name.startswith("."):
                yield asset


def is_pending(meta: dict, asset_path: Path) -> bool:
    vision = meta.get("vision")
    if not vision:
        return True
    status = vision.get("_status")
    if status != "done":
        return True
    # If sidecar has _cached_hash, verify against current file (detect modified files)
    cached = vision.get("_cached_hash")
    if cached and cached != hash_file(asset_path):
        return True
    return False


def list_pending():
    pending = []
    for asset in iter_all_assets():
        _, meta = load_sidecar(asset)
        if is_pending(meta, asset):
            pending.append(asset)

    if not pending:
        print("📭 nenhum asset pendente de análise visual")
        return

    print(f"📋 {len(pending)} asset(s) pendente(s) de análise visual:\n")
    for i, asset in enumerate(pending, 1):
        rel = asset.relative_to(GROWTHOS)
        print(f"  {i}. {rel}")

    print()
    print("─" * 60)
    print("PRÓXIMO PASSO — peça ao Claude Code na conversa:")
    print()
    print('  "analisa os assets pendentes e preenche os sidecars"')
    print()
    print("Claude vai usar Read tool em cada imagem (vision nativo do plano Max),")
    print("analisar, e escrever o bloco vision no sidecar YAML correspondente.")
    print("─" * 60)


def prepare_skeleton(asset_path: Path):
    """Cria o sidecar skeleton com vision pendente, preservando dados existentes."""
    sidecar, meta = load_sidecar(asset_path)

    if not meta:
        print(f"⚠ {asset_path.name} sem sidecar ainda — rode asset-indexer.py primeiro")
        return

    skeleton = dict(SKELETON_VISION)
    skeleton["_cached_hash"] = hash_file(asset_path)
    skeleton["_prepared_at"] = datetime.now().isoformat()

    meta["vision"] = skeleton
    save_sidecar(sidecar, meta)
    rel_sidecar = sidecar.relative_to(GROWTHOS)
    print(f"✅ skeleton preparado: {rel_sidecar}")
    print(f"   asset: {asset_path.relative_to(GROWTHOS)}")
    print(f"   status: pending")


def prepare_all():
    count = 0
    for asset in iter_all_assets():
        _, meta = load_sidecar(asset)
        if is_pending(meta, asset):
            prepare_skeleton(asset)
            count += 1
    print(f"\n✅ {count} skeleton(s) preparado(s)")


def print_schema():
    print(SCHEMA_REFERENCE)


def main():
    parser = argparse.ArgumentParser(description="Asset vision pending manager")
    parser.add_argument("--pending", action="store_true", help="lista assets pendentes de análise")
    parser.add_argument("--prepare", metavar="PATH", help="cria skeleton no sidecar de 1 asset")
    parser.add_argument("--prepare-all", action="store_true", help="cria skeleton pra todos os pendentes")
    parser.add_argument("--schema", action="store_true", help="imprime o schema esperado pro bloco vision")
    args = parser.parse_args()

    if args.pending:
        list_pending()
    elif args.prepare:
        prepare_skeleton(Path(args.prepare).resolve())
    elif args.prepare_all:
        prepare_all()
    elif args.schema:
        print_schema()
    else:
        parser.print_help()
        print()
        list_pending()


if __name__ == "__main__":
    main()
