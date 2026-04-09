#!/usr/bin/env python3
"""
process-revision.py — Processa a queue de revisões pendentes

Usage:
    python process-revision.py                      # processa TUDO pending
    python process-revision.py --cid c02            # processa só um carousel
    python process-revision.py --file carousels-v1.html  # só revisões de um arquivo
    python process-revision.py --dry-run            # só mostra o que faria

Fluxo:
    1. Lê output/revisions/queue.json
    2. Agrupa revisões pendentes por arquivo original
    3. Pra cada arquivo, monta um MASTER BRIEF com:
         - lista de carrosséis aprovados (a serem copiados do original)
         - lista de revisões com instruções por carrossel
         - nome do arquivo de saída carousels-vN-rev{K}.html
    4. Despacha UiUX Expert via Maestri com o master brief
    5. Move revisões de pending → processing (estado intermediário)
    6. Quando UiUX Expert confirma conclusão, move pra done + atualiza REVISIONS.md

Nota: esse script NÃO aguarda o UiUX Expert por padrão. Ele só enfileira.
Rode `maestri check "UiUX Expert"` periodicamente OU passe --wait pra bloquear.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GROWTHOS = REPO_ROOT / "growthOS"
DESIGN_SYSTEM = GROWTHOS / "design-system"
OUTPUT = GROWTHOS / "output"
REVIEWS_FILE = OUTPUT / "reviews" / "reviews.json"
QUEUE_FILE = OUTPUT / "revisions" / "queue.json"
PREFERENCES = GROWTHOS / "voice" / "preferences"
REVISIONS_MD = PREFERENCES / "REVISIONS.md"


def load_queue() -> dict:
    if QUEUE_FILE.exists():
        return json.loads(QUEUE_FILE.read_text())
    return {"pending": [], "processing": [], "done": []}


def save_queue(q: dict):
    QUEUE_FILE.write_text(json.dumps(q, indent=2, ensure_ascii=False))


def load_reviews() -> dict:
    if REVIEWS_FILE.exists():
        return json.loads(REVIEWS_FILE.read_text())
    return {}


def next_rev_number(base_stem: str) -> int:
    """Figure out which rev number to use (increments if file already exists)."""
    existing = sorted(DESIGN_SYSTEM.glob(f"{base_stem}-rev*.html"))
    if not existing:
        return 1
    nums = [int(re.search(r"rev(\d+)", f.name).group(1)) for f in existing if re.search(r"rev(\d+)", f.name)]
    return (max(nums) + 1) if nums else 1


def build_master_brief(file: str, revisions: list, reviews: dict) -> Path:
    """Build a master brief listing approved + revisions for one source file."""
    base_stem = Path(file).stem
    rev_n = next_rev_number(base_stem)
    output_file = f"{base_stem}-rev{rev_n}.html"
    output_path = DESIGN_SYSTEM / output_file

    # Figure out which carousels are approved, which are revised, which are rejected
    file_reviews = reviews.get(file, {})
    approved_cids = sorted([cid for cid, r in file_reviews.items() if r.get("status") == "approved"])
    revised_cids = sorted([r["cid"] for r in revisions])
    rejected_cids = sorted([cid for cid, r in file_reviews.items() if r.get("status") == "rejected"])

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    brief_name = f"MASTER-REVISION-{base_stem}-rev{rev_n}-{ts}.md"
    brief_path = DESIGN_SYSTEM / "revisions" / brief_name

    lines = [
        f"# MASTER REVISION BRIEF — {base_stem} → {output_file}",
        "",
        f"> **Para:** UiUX Expert (via Maestri)",
        f"> **De:** /grow revise (process-revision.py)",
        f"> **Data:** {ts}",
        f"> **Fonte original:** `growthOS/design-system/{file}`",
        f"> **Output:** `growthOS/design-system/{output_file}`",
        f"> **Revision round:** {rev_n}",
        "",
        "---",
        "",
        "## Resumo do estado atual",
        "",
        f"- **Aprovados ({len(approved_cids)}):** {', '.join(approved_cids) or '(nenhum)'}",
        f"- **A revisar ({len(revised_cids)}):** {', '.join(revised_cids) or '(nenhum)'}",
        f"- **Rejeitados (excluídos) ({len(rejected_cids)}):** {', '.join(rejected_cids) or '(nenhum)'}",
        "",
        "---",
        "",
        "## Leituras obrigatórias ANTES de renderizar",
        "",
        "1. `growthOS/voice/GOLDEN-DOC.md` — voz real do Rafael (confessional, contrarian, anti-guru)",
        "2. `growthOS/voice/VOICE-GUIDE.md` — bordões literais e padrões de abertura/fechamento",
        "3. `growthOS/voice/preferences/PROFILE.md` — RLHF agregado",
        "4. `growthOS/voice/preferences/APPROVED.md` — padrões aprovados (replicar)",
        "5. `growthOS/voice/preferences/REJECTED.md` — padrões rejeitados (evitar)",
        "6. `growthOS/voice/preferences/REVISIONS.md` — histórico de ajustes pedidos",
        "7. `growthOS/design-system/DESIGN-SYSTEM.md` — DS canônico (lime-geist default)",
        f"8. `growthOS/design-system/{file}` — HTML original (pra copiar os aprovados exatos)",
        "",
        "---",
        "",
        "## Tarefa",
        "",
        f"Gere um novo arquivo HTML em `growthOS/design-system/{output_file}` contendo:",
        "",
        f"1. **TODOS os {len(approved_cids)} carrosséis APROVADOS** ({', '.join(approved_cids) or 'nenhum'}) — copiados EXATAMENTE do HTML original, sem mudanças. Use o mesmo wrapper `<section data-carousel=...>` e os mesmos slides.",
        f"2. **Os {len(revised_cids)} carrosséis REVISADOS** ({', '.join(revised_cids) or 'nenhum'}) — regenerados seguindo as instruções de cada um (listadas abaixo).",
        f"3. **EXCLUIR os {len(rejected_cids)} rejeitados** ({', '.join(rejected_cids) or 'nenhum'}).",
        "",
        f"O header do arquivo deve mostrar `rev{rev_n} · {len(approved_cids)} approved · {len(revised_cids)} revised · @melgarafael`.",
        "",
        "Reutilize TODO o CSS e estrutura do HTML original. Mesma paleta, mesmas fontes, mesmos slide-types.",
        "",
        "---",
        "",
        "## Revisões detalhadas",
        "",
    ]

    for rev in revisions:
        cid = rev["cid"]
        tags = ", ".join(f"`{t}`" for t in rev.get("tags", [])) or "(sem tags)"
        slides = rev.get("affected_slides", [])
        instructions = rev.get("instructions", "")
        brief_path_rel = rev.get("brief_path", "")
        lines.extend([
            f"### {cid}",
            "",
            f"- **tags:** {tags}",
            f"- **slides afetados:** {slides}",
            f"- **brief individual:** `{brief_path_rel}`",
            "",
            f"**Instruções do Rafael (literal):**",
            "",
            f"> {instructions}",
            "",
        ])

    lines.extend([
        "---",
        "",
        "## Quando terminar, responda com",
        "",
        f"1. Path do arquivo gerado: `growthOS/design-system/{output_file}`",
        f"2. Contagem final de carrosséis no arquivo (esperado: {len(approved_cids) + len(revised_cids)})",
        "3. Quais cids você manteve intactos vs regenerou",
        "4. Qualquer decisão criativa que tomou (especialmente nos slides revisados)",
    ])

    brief_path.write_text("\n".join(lines), encoding="utf-8")
    return brief_path, output_path, rev_n


def dispatch_to_maestri(brief_path: Path, output_path: Path):
    """Send a compact prompt to UiUX Expert via maestri ask."""
    prompt = (
        f"MASTER REVISION. Leia o brief em {brief_path.relative_to(REPO_ROOT)} e execute. "
        f"Output: {output_path.relative_to(REPO_ROOT)}. "
        f"Siga todas as leituras obrigatórias listadas no brief. Mantenha DS canônico. "
        f"Quando terminar: path + contagem de carrosséis + decisões criativas."
    )
    print(f"\n📤 dispatching to UiUX Expert via maestri...")
    print(f"   brief: {brief_path.name}")
    try:
        result = subprocess.run(
            ["maestri", "ask", "UiUX Expert", prompt],
            capture_output=True, text=True, timeout=30,
        )
        print(result.stdout[-500:] if result.stdout else "(no stdout)")
        if result.returncode != 0:
            print(f"   ⚠ maestri exit {result.returncode}: {result.stderr[-300:]}")
    except FileNotFoundError:
        print("   ❌ maestri CLI not found on PATH")
    except subprocess.TimeoutExpired:
        print("   ⏱ maestri ask dispatched (timeout but that's ok — it's async)")


def append_revisions_md(file: str, rev_n: int, output_path: Path, revisions: list):
    """Update REVISIONS.md entries for this batch with the resolved path."""
    if not REVISIONS_MD.exists():
        return
    content = REVISIONS_MD.read_text(encoding="utf-8")
    rel_output = str(output_path.relative_to(REPO_ROOT))
    ts = datetime.now().isoformat()[:19]
    footer = f"\n## BATCH RESOLVED · rev{rev_n} · {ts}\n"
    footer += f"- **source:** `{file}`\n"
    footer += f"- **output:** `{rel_output}`\n"
    footer += f"- **cids revised:** {', '.join(r['cid'] for r in revisions)}\n"
    footer += f"- **status:** dispatched (pending UiUX Expert completion)\n"
    REVISIONS_MD.write_text(content + footer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cid", help="process only this carousel id")
    parser.add_argument("--file", help="process only revisions for this source file")
    parser.add_argument("--dry-run", action="store_true", help="show what would happen, don't dispatch")
    args = parser.parse_args()

    queue = load_queue()
    reviews = load_reviews()
    pending = queue.get("pending", [])

    if not pending:
        print("📭 no pending revisions in queue")
        print(f"   queue: {QUEUE_FILE}")
        return

    # Apply filters
    filtered = pending
    if args.cid:
        filtered = [r for r in filtered if r["cid"] == args.cid]
    if args.file:
        filtered = [r for r in filtered if r["file"] == args.file]

    if not filtered:
        print(f"📭 no pending revisions match filters")
        return

    # Group by source file
    by_file = {}
    for rev in filtered:
        by_file.setdefault(rev["file"], []).append(rev)

    print(f"📋 processing {len(filtered)} revision(s) across {len(by_file)} source file(s)")

    for source_file, revs in by_file.items():
        print(f"\n━━ {source_file} ━━")
        print(f"   revisions: {len(revs)} ({', '.join(r['cid'] for r in revs)})")

        brief_path, output_path, rev_n = build_master_brief(source_file, revs, reviews)
        print(f"   ✅ master brief: {brief_path.relative_to(REPO_ROOT)}")
        print(f"   ✅ output target: {output_path.relative_to(REPO_ROOT)} (rev{rev_n})")

        if args.dry_run:
            print(f"   [DRY RUN] would dispatch to UiUX Expert now")
            continue

        dispatch_to_maestri(brief_path, output_path)
        append_revisions_md(source_file, rev_n, output_path, revs)

        # Move from pending to processing
        for rev in revs:
            queue["pending"].remove(rev)
            rev["dispatched_at"] = datetime.now().isoformat()
            rev["output_target"] = str(output_path.relative_to(REPO_ROOT))
            rev["brief_path_master"] = str(brief_path.relative_to(REPO_ROOT))
            queue["processing"].append(rev)

    if not args.dry_run:
        save_queue(queue)
        print(f"\n✅ queue updated — {len(queue['pending'])} still pending, {len(queue['processing'])} processing")
        print(f"\n   monitor with: maestri check 'UiUX Expert'")
        print(f"   when done, open: http://localhost:5050 to re-review the revN file")


if __name__ == "__main__":
    main()
