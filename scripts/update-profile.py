#!/usr/bin/env python3
"""
update-profile.py — Aggregates APPROVED.md + REJECTED.md into PROFILE.md

Called automatically by review-server after every approve/reject.
Can also be run manually: `python update-profile.py`

Strategy:
    1. Parse APPROVED.md → count entries, extract tags/templates/variants/categories
    2. Parse REJECTED.md → same + count rejection tags
    3. Compute approval rates per dimension
    4. Generate human-readable PROFILE.md with top patterns and insights
    5. Emit lessons learned (heuristic: if tag X appears 3+ times in rejected, emit avoid-rule)
"""

import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PREFERENCES = REPO_ROOT / "growthOS" / "voice" / "preferences"
APPROVED = PREFERENCES / "APPROVED.md"
REJECTED = PREFERENCES / "REJECTED.md"
REVISIONS = PREFERENCES / "REVISIONS.md"
PROFILE = PREFERENCES / "PROFILE.md"


def parse_entries(md_path: Path) -> list:
    """Parse entries from a markdown log file. Returns list of dicts."""
    if not md_path.exists():
        return []
    text = md_path.read_text(encoding="utf-8")
    # Split by `## {timestamp} ...`
    blocks = re.split(r"\n## (?=\d{4}-\d{2}-\d{2})", text)
    entries = []
    for block in blocks[1:]:  # skip preamble
        lines = block.split("\n")
        header = lines[0]
        m = re.match(r"(\S+)\s+·\s+(\S+)\s+·\s+(\S+)", header)
        if not m:
            continue
        entry = {
            "timestamp": m.group(1),
            "file": m.group(2),
            "cid": m.group(3),
            "raw": block,
        }
        for field in ["tema", "categoria", "template", "variant", "tag", "razão", "source"]:
            fm = re.search(rf"-\s+\*\*{field}:\*\*\s+(.+)", block)
            if fm:
                entry[field] = fm.group(1).strip("` ").strip()
        entries.append(entry)
    return entries


def parse_revision_tags(entry: dict) -> list:
    """REVISIONS entries have **tags:** `t1`, `t2` — parse them out."""
    raw = entry.get("tags", "")
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str):
        return [t.strip().strip("`") for t in raw.split(",") if t.strip()]
    return []


def compute_stats(approved: list, rejected: list, revisions: list) -> dict:
    total = len(approved) + len(rejected) + len(revisions)
    approval_rate = (len(approved) / total * 100) if total > 0 else 0
    revision_rate = (len(revisions) / total * 100) if total > 0 else 0

    # Aggregate by dimension
    def count_field(entries, field):
        return Counter(e.get(field, "unknown") for e in entries if field in e)

    # Flatten revision tags (they come as comma-separated list)
    revision_tag_counter = Counter()
    for entry in revisions:
        for t in parse_revision_tags(entry):
            revision_tag_counter[t] += 1

    stats = {
        "total_reviews": total,
        "total_approved": len(approved),
        "total_rejected": len(rejected),
        "total_revisions": len(revisions),
        "approval_rate": approval_rate,
        "revision_rate": revision_rate,
        "approved_by_template": count_field(approved, "template"),
        "approved_by_variant": count_field(approved, "variant"),
        "approved_by_category": count_field(approved, "categoria"),
        "rejected_tags": count_field(rejected, "tag"),
        "rejected_by_category": count_field(rejected, "categoria"),
        "rejected_by_template": count_field(rejected, "template"),
        "revision_tags": revision_tag_counter,
    }
    return stats


def detect_lessons(stats: dict, rejected: list) -> list:
    """Extract human-readable lessons from patterns."""
    lessons = []

    # If a rejection tag appears 3+ times → avoid-rule
    for tag, count in stats["rejected_tags"].most_common():
        if count >= 3:
            lessons.append(f"Tag `{tag}` rejeitada {count}x — **evitar sempre**.")
        elif count == 2:
            lessons.append(f"Tag `{tag}` rejeitada 2x — **cuidado**, revisar antes de finalizar.")

    # If a revision tag appears 3+ times → recurring-issue rule
    for tag, count in stats["revision_tags"].most_common():
        if count >= 3:
            lessons.append(f"Revisão `{tag}` pedida {count}x — **revisar preventivamente** antes de gerar.")
        elif count == 2:
            lessons.append(f"Revisão `{tag}` pedida 2x — padrão emergente, ficar atento.")

    # If a template has high approval rate and seen_count >= 5
    template_total = stats["approved_by_template"] + stats["rejected_by_template"]
    for template, approved_count in stats["approved_by_template"].most_common():
        total = template_total.get(template, approved_count)
        if total >= 5 and approved_count / total > 0.8:
            lessons.append(f"Template `{template}` tem {int(approved_count/total*100)}% de aprovação ({approved_count}/{total}) — **preferir**.")

    # If a variant dominates approvals
    for variant, count in stats["approved_by_variant"].most_common(1):
        total = stats["total_approved"]
        if total >= 5 and count / total > 0.6:
            lessons.append(f"Variant `{variant}` domina aprovações ({count}/{total}, {int(count/total*100)}%) — **default recomendado**.")

    if not lessons:
        lessons.append("_(insuficiente data — continue aprovando/rejeitando pra lições aparecerem)_")

    return lessons


def render_profile(stats: dict, lessons: list) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# PROFILE — Perfil Agregado de Preferências",
        "",
        f"> **Auto-gerado por:** `growthOS/scripts/update-profile.py`",
        "> **Lido por:** TODOS os agentes de conteúdo antes de gerar",
        "> **Propósito:** RLHF pessoal — agrega APPROVED + REVISIONS + REJECTED em insights acionáveis",
        f"> **Última atualização:** {now}",
        f"> **Base:** {stats['total_reviews']} reviews ({stats['total_approved']} approved, {stats['total_revisions']} revised, {stats['total_rejected']} rejected)",
        f"> **Approval rate:** {stats['approval_rate']:.1f}% · **Revision rate:** {stats['revision_rate']:.1f}%",
        "",
        "---",
        "",
        "## ⚠️ Instrução crítica pros agentes",
        "",
        "**Antes de gerar qualquer conteúdo**, leia este PROFILE + APPROVED.md + REJECTED.md.",
        "Se houver conflito entre o brief e o PROFILE, o PROFILE ganha.",
        "",
        "---",
        "",
        "## Lições aprendidas (acionável)",
        "",
    ]
    for lesson in lessons:
        lines.append(f"- {lesson}")
    lines.extend(["", "---", "", "## Padrões aprovados"])

    if stats["total_approved"] == 0:
        lines.extend(["", "_(sem aprovações ainda)_"])
    else:
        lines.extend([
            "",
            "### Por template",
            "",
            "| Template | Aprovações |",
            "|---|---|",
        ])
        for t, c in stats["approved_by_template"].most_common():
            lines.append(f"| `{t}` | {c} |")

        lines.extend([
            "",
            "### Por variant",
            "",
            "| Variant | Aprovações |",
            "|---|---|",
        ])
        for v, c in stats["approved_by_variant"].most_common():
            lines.append(f"| `{v}` | {c} |")

        lines.extend([
            "",
            "### Por categoria",
            "",
            "| Categoria | Aprovações |",
            "|---|---|",
        ])
        for cat, c in stats["approved_by_category"].most_common():
            lines.append(f"| `{cat}` | {c} |")

    lines.extend(["", "---", "", "## Padrões de revisão pedidos"])
    if stats["total_revisions"] == 0:
        lines.extend(["", "_(sem revisões ainda)_"])
    else:
        lines.extend([
            "",
            "### Top revision tags",
            "",
            "| Tag | Contagem |",
            "|---|---|",
        ])
        for tag, c in stats["revision_tags"].most_common():
            lines.append(f"| `{tag}` | {c} |")

    lines.extend(["", "---", "", "## Padrões rejeitados"])
    if stats["total_rejected"] == 0:
        lines.extend(["", "_(sem rejeições ainda)_"])
    else:
        lines.extend([
            "",
            "### Top rejection tags",
            "",
            "| Tag | Contagem |",
            "|---|---|",
        ])
        for tag, c in stats["rejected_tags"].most_common():
            lines.append(f"| `{tag}` | {c} |")

    lines.extend([
        "",
        "---",
        "",
        "## Anti-padrões ativos",
        "",
    ])
    anti = [l for l in lessons if "evitar" in l.lower()]
    if anti:
        for a in anti:
            lines.append(f"- {a}")
    else:
        lines.append("_(nenhum anti-padrão detectado ainda)_")

    return "\n".join(lines) + "\n"


def main():
    approved = parse_entries(APPROVED)
    rejected = parse_entries(REJECTED)
    revisions = parse_entries(REVISIONS) if REVISIONS.exists() else []
    stats = compute_stats(approved, rejected, revisions)
    lessons = detect_lessons(stats, rejected)
    profile_content = render_profile(stats, lessons)
    PROFILE.write_text(profile_content, encoding="utf-8")
    print(f"✅ PROFILE.md updated")
    print(f"   base: {stats['total_reviews']} reviews ({stats['total_approved']}a {stats['total_revisions']}v {stats['total_rejected']}r)")
    print(f"   approval rate: {stats['approval_rate']:.1f}% · revision rate: {stats['revision_rate']:.1f}%")
    print(f"   lessons: {len([l for l in lessons if not l.startswith('_')])}")


if __name__ == "__main__":
    main()
