#!/usr/bin/env python3
"""
export_carousel.py — HTML → PNG batch exporter (Python Playwright version)

Usage:
    .venv/bin/python scripts/export_carousel.py <path-to-carousels-vN.html> [--carousel cXX] [--out DIR]

Replaces the older export-carousel.mjs (Node) — uses the Python playwright
that's already in the venv, no extra npm install needed.

For each <section> in the HTML (filtered by cid if given), screenshots each
.slide element at native 1080x1350 (ignores any CSS transform scale applied).
"""

import argparse
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ playwright not installed — run: .venv/bin/pip install playwright && .venv/bin/python -m playwright install chromium")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]
GROWTHOS = REPO_ROOT / "growthOS"
DEFAULT_OUT = GROWTHOS / "output" / "carousels"


def export(html_path: Path, out_dir: Path, carousel_filter: str | None = None, parallel: int = 4):
    if not html_path.exists():
        print(f"❌ not found: {html_path}")
        sys.exit(1)

    stem = html_path.stem
    out_dir = out_dir / stem
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎬 exporting {html_path.name} → {out_dir.relative_to(GROWTHOS)}")
    if carousel_filter:
        print(f"   filter: only {carousel_filter}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1600, "height": 1500},
            device_scale_factor=2,  # retina PNGs
        )
        page = ctx.new_page()
        page.goto(f"file://{html_path.absolute()}", wait_until="networkidle")

        # Find all section elements (each = 1 carousel)
        sections = page.query_selector_all("section[id^='c'], section[data-carousel]")
        print(f"   found {len(sections)} carousel section(s)")

        total_exported = 0
        for section in sections:
            cid = section.get_attribute("data-carousel") or section.get_attribute("id") or f"c{total_exported:02d}"
            if carousel_filter and carousel_filter not in cid:
                continue

            slides_dir = out_dir / cid / "slides"
            slides_dir.mkdir(parents=True, exist_ok=True)

            slides = section.query_selector_all(".slide, [data-slide]")
            if not slides:
                print(f"   ⚠ no .slide inside {cid}, skipping")
                continue

            print(f"   📸 {cid}: exporting {len(slides)} slides")

            for i, slide in enumerate(slides, 1):
                slide_num = f"{i:02d}"
                fname = f"{cid}-s{slide_num}.png"
                fpath = slides_dir / fname

                # Temporarily neutralize transform:scale() for native-size capture
                slide.evaluate("""
                    (el) => {
                        el.dataset._originalTransform = el.style.transform;
                        el.style.transform = 'none';
                    }
                """)

                slide.screenshot(path=str(fpath), omit_background=False)

                # Restore original transform
                slide.evaluate("""
                    (el) => {
                        el.style.transform = el.dataset._originalTransform || '';
                    }
                """)

                total_exported += 1

        browser.close()

    print(f"\n✅ exported {total_exported} slides total")
    print(f"📂 output: {out_dir}")
    return total_exported


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("html", help="path to carousels-vN.html")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    parser.add_argument("--carousel", default=None, help="only export this cid (e.g., c04)")
    parser.add_argument("--parallel", type=int, default=4, help="parallel workers (unused in sync mode)")
    args = parser.parse_args()

    html_path = Path(args.html).resolve()
    out_dir = Path(args.out).resolve()
    export(html_path, out_dir, carousel_filter=args.carousel, parallel=args.parallel)


if __name__ == "__main__":
    main()
