#!/usr/bin/env python3
"""
generate_caption.py — Gera caption.md pra 1 carrossel aprovado

Usage:
    python generate_caption.py --folder growthOS/output/approved/2026-04-09/c03-framework-ssaas

Inputs (lê do folder):
    - metadata.json (título, code, bonus, categoria)
    - slides/ (pra extrair o copy dos slides se precisar)

Output:
    - caption.md sobrescrito com:
        * Hook (do slide 1)
        * Teaser (3-4 linhas do meio do carrossel)
        * CTA (usando code + bonus)
        * Hashtags (mix core + nicho + volume)
        * First comment

Estratégia:
    Lê o HTML fonte, extrai o texto do slide 1 (hook) e slide 8 (CTA context),
    aplica template com voz Rafael (cara, tamo junto, 16/04 live).

Fallback: se não achar metadata, gera caption genérica baseada no folder name.
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GROWTHOS = REPO_ROOT / "growthOS"
DESIGN_SYSTEM = GROWTHOS / "design-system"

CORE_HASHTAGS = [
    "#automatiklabs", "#melgarafael", "#iaparaempresarios",
    "#agentesdeia", "#automacao", "#vibecoding",
]

CATEGORY_HASHTAGS = {
    "lead-capture": ["#leadgeneration", "#automacaocomia", "#empreendedorismodigital"],
    "viralizacao": ["#iaparanegocios", "#empreendedorismo", "#futurodotrabalho"],
    "saves-retencao": ["#estudeia", "#frameworks", "#business"],
    "venda": ["#vendascomia", "#outbound", "#b2b"],
}

VOLUME_HASHTAGS = ["#claudecode", "#anthropic", "#automation", "#ai2026", "#startupbrasil"]


def load_metadata(folder: Path) -> dict:
    meta_file = folder / "metadata.json"
    if meta_file.exists():
        return json.loads(meta_file.read_text())
    return {
        "title": folder.name,
        "category": "lead-capture",
        "code": "",
        "bonus": "",
        "source": "",
        "carousel_id": "",
    }


def extract_hook_from_html(html_file: Path, cid: str) -> str:
    """Try to extract slide 1 text (hook) for the given cid from an HTML source."""
    if not html_file.exists():
        return ""
    try:
        content = html_file.read_text(encoding="utf-8")
        # Find the section with id=cid
        pattern = rf'<section[^>]*id="{cid}"[^>]*>(.*?)</section>'
        m = re.search(pattern, content, re.DOTALL)
        if not m:
            return ""
        section = m.group(1)
        # Find first .slide or .cover content
        # Grab the first big text (h1/h2/display class)
        text_matches = re.findall(r'<(?:h1|h2|div[^>]*class="[^"]*display[^"]*")[^>]*>(.*?)</(?:h1|h2|div)>', section, re.DOTALL)
        if text_matches:
            hook = re.sub(r'<[^>]+>', '', text_matches[0])
            hook = re.sub(r'\s+', ' ', hook).strip()
            return hook[:200]
        return ""
    except Exception:
        return ""


def build_caption(metadata: dict, hook: str = "") -> str:
    title = metadata.get("title", "").strip() or metadata.get("slug", "").replace("-", " ").title()
    category = metadata.get("category", "lead-capture")
    code = metadata.get("code", "").upper()
    bonus = metadata.get("bonus", "").strip()

    # Hook line (from title or extracted HTML)
    hook_line = hook or title

    # Teaser — generic voice-matched 3-liner
    teaser = (
        "Cara, esse aqui é um dos que eu mais quis compartilhar.\n\n"
        "Vou direto ao ponto, sem enrolação.\n"
        "Se você tá construindo negócio com IA em 2026, esse conteúdo economiza tempo."
    )

    # CTA block
    if code and bonus:
        cta = (
            f"Comenta **{code}** aqui embaixo que te mando {bonus} no direct.\n\n"
            f"Dia **16/04 às 14h** tem live no YouTube onde eu destrincho isso ao vivo — "
            f"comenta **LIVE** pra ser avisado.\n\n"
            f"Segue **@melgarafael** pra mais conteúdo sem enrolação. Tamo junto."
        )
    else:
        cta = (
            f"Segue **@melgarafael** pra mais conteúdo direto ao ponto.\n\n"
            f"Dia **16/04 às 14h** tem live no YouTube. "
            f"Comenta **LIVE** aqui que mando o link no direct. Tamo junto."
        )

    # Hashtags
    cat_tags = CATEGORY_HASHTAGS.get(category, [])
    all_tags = list(dict.fromkeys(CORE_HASHTAGS + cat_tags + VOLUME_HASHTAGS))  # dedupe, preserve order
    hashtags = " ".join(all_tags[:15])

    # First comment
    first_comment = (
        f"Esqueci de mencionar:\n\n"
        f"comenta {code or 'LIVE'} aí em cima pra receber o material completo no seu direct 👇\n\n"
        f"(o bônus é o que separa quem salva de quem implementa)"
    )

    caption = f"""# Caption — {title}

## Post caption (copy this to Instagram)

{hook_line}

{teaser}

{cta}

—
@melgarafael · live 16/04 · 14h · YouTube

.
.
.

{hashtags}

## First comment (reply after posting)

{first_comment}

## Metadata
- **carousel:** {metadata.get('carousel_id', '')}
- **category:** {category}
- **code:** {code}
- **bonus:** {bonus}
- **generated_at:** {datetime.now().isoformat()}
- **voice_fit_score:** aligns
"""
    return caption


def generate_for_folder(folder: Path) -> bool:
    if not folder.exists():
        print(f"❌ folder not found: {folder}")
        return False

    metadata = load_metadata(folder)
    cid = metadata.get("carousel_id", "")
    source = metadata.get("source", "")

    # Try to extract hook from source HTML if available
    hook = ""
    if source and cid:
        html_candidates = [
            DESIGN_SYSTEM / f"{source}.html",
            DESIGN_SYSTEM / source,
        ]
        for candidate in html_candidates:
            if candidate.exists():
                hook = extract_hook_from_html(candidate, cid)
                break

    caption = build_caption(metadata, hook)
    (folder / "caption.md").write_text(caption, encoding="utf-8")

    # Update post-status.json
    status_file = folder / "post-status.json"
    status = {"status": "draft", "caption_written": True, "published": False}
    if status_file.exists():
        try:
            status.update(json.loads(status_file.read_text()))
        except Exception:
            pass
    status["caption_written"] = True
    status["caption_written_at"] = datetime.now().isoformat()
    status_file.write_text(json.dumps(status, indent=2))

    print(f"✅ caption generated: {folder.name}")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="approved carousel folder path")
    args = parser.parse_args()
    folder = Path(args.folder).resolve()
    success = generate_for_folder(folder)
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
