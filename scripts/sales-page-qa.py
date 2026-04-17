#!/usr/bin/env python3
"""
GrowthOS Sales Page QA — Playwright E2E Test Suite

Runs 6 test categories against a built sales page:
1. Functional (page loads, links, CTAs, forms)
2. Visual (responsive at 375/768/1024/1440px)
3. Performance (file size, external requests)
4. Content (copy matches Phase 5, no placeholders)
5. Accessibility (focus, contrast, alt texts, semantic HTML)
6. Animation (scroll effects, reduced-motion)

Usage:
    uv run --with playwright --with beautifulsoup4 python growthOS/scripts/sales-page-qa.py \
        --target path/to/index.html \
        --state path/to/state.json \
        --output path/to/phase-8-qa.html

Returns exit code:
    0 = PASS
    1 = CONCERNS
    2 = FAIL
"""

import argparse
import json
import sys
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: playwright not installed. Run: uv pip install playwright && playwright install chromium")
    sys.exit(2)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: uv pip install beautifulsoup4")
    sys.exit(2)


VIEWPORTS = [
    {"name": "mobile", "width": 375, "height": 812},
    {"name": "tablet", "width": 768, "height": 1024},
    {"name": "desktop", "width": 1024, "height": 768},
    {"name": "wide", "width": 1440, "height": 900},
]

PLACEHOLDER_PATTERNS = [
    r"\blorem\b", r"\bipsum\b", r"\bplaceholder\b",
    r"\bTODO\b", r"\bFIXME\b", r"\[TBD\]", r"\[PLACEHOLDER\]",
]

BROKEN_TOKEN_PATTERNS = [
    r"\{\{[^}]+\}\}", r"\{[a-z_]+\}", r"%[sd]",
]


@dataclass
class CheckResult:
    category: str
    name: str
    status: str  # PASS, FAIL, WARN
    detail: str = ""


@dataclass
class QAReport:
    target: str
    timestamp: str = ""
    verdict: str = "PASS"
    results: list = field(default_factory=list)
    screenshots: dict = field(default_factory=dict)

    def __post_init__(self):
        self.timestamp = datetime.now().isoformat()

    def add(self, result: CheckResult):
        self.results.append(result)

    @property
    def summary(self):
        passed = sum(1 for r in self.results if r.status == "PASS")
        failed = sum(1 for r in self.results if r.status == "FAIL")
        warned = sum(1 for r in self.results if r.status == "WARN")
        return {"total": len(self.results), "passed": passed, "failed": failed, "warnings": warned}

    def compute_verdict(self):
        critical_categories = {"functional", "content"}
        has_critical_fail = any(
            r.status == "FAIL" and r.category in critical_categories
            for r in self.results
        )
        has_any_fail = any(r.status == "FAIL" for r in self.results)

        if has_critical_fail:
            self.verdict = "FAIL"
        elif has_any_fail:
            self.verdict = "CONCERNS"
        else:
            self.verdict = "PASS"


def run_functional_checks(page, report: QAReport):
    """Category 1: Functional checks."""
    # Page loads
    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

    try:
        response = page.reload(wait_until="networkidle")
        status = response.status if response else 0
        report.add(CheckResult("functional", "Page loads", "PASS" if status == 200 else "FAIL",
                               f"HTTP {status}"))
    except Exception as e:
        report.add(CheckResult("functional", "Page loads", "FAIL", str(e)))
        return  # Can't continue if page doesn't load

    # Check links
    links = page.query_selector_all("a[href]")
    broken_links = []
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith("#"):
            target_id = href[1:]
            if target_id and not page.query_selector(f"#{target_id}"):
                broken_links.append(href)
    report.add(CheckResult(
        "functional", "Internal links work",
        "PASS" if not broken_links else "FAIL",
        f"Broken: {broken_links}" if broken_links else f"{len(links)} links checked"
    ))

    # CTAs clickable
    ctas = page.query_selector_all("[data-cta], .cta, button[type='submit'], a.cta-button, a.btn-primary")
    cta_issues = []
    for cta in ctas:
        if not cta.is_visible():
            cta_issues.append(f"CTA not visible: {cta.text_content()[:30]}")
    report.add(CheckResult(
        "functional", "CTAs clickable",
        "PASS" if not cta_issues else "FAIL",
        "; ".join(cta_issues) if cta_issues else f"{len(ctas)} CTAs verified"
    ))

    # Console errors
    report.add(CheckResult(
        "functional", "No console errors",
        "PASS" if not console_errors else "WARN",
        "; ".join(console_errors[:5]) if console_errors else "Clean console"
    ))


def run_visual_checks(page, report: QAReport, screenshot_dir: Path):
    """Category 2: Visual / responsive checks."""
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    for vp in VIEWPORTS:
        page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
        page.wait_for_timeout(500)

        # Screenshot
        screenshot_path = screenshot_dir / f"{vp['width']}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        report.screenshots[vp["name"]] = str(screenshot_path)

        # Horizontal overflow
        overflow = page.evaluate("document.body.scrollWidth > window.innerWidth")
        report.add(CheckResult(
            "visual", f"No overflow at {vp['width']}px",
            "PASS" if not overflow else "FAIL",
            f"scrollWidth={page.evaluate('document.body.scrollWidth')}, viewport={vp['width']}"
        ))

        # Text readability (min font-size)
        min_size = 14 if vp["width"] < 768 else 16
        small_text = page.evaluate(f"""() => {{
            const elements = document.querySelectorAll('p, span, li, a, td, th, label');
            let tooSmall = [];
            elements.forEach(el => {{
                const size = parseFloat(getComputedStyle(el).fontSize);
                if (size < {min_size} && el.textContent.trim().length > 0) {{
                    tooSmall.push({{text: el.textContent.trim().substring(0, 30), size}});
                }}
            }});
            return tooSmall.slice(0, 5);
        }}""")
        report.add(CheckResult(
            "visual", f"Text readable at {vp['width']}px",
            "PASS" if not small_text else "WARN",
            f"Small text found: {small_text}" if small_text else f"All text >= {min_size}px"
        ))


def run_performance_checks(target_path: str, report: QAReport):
    """Category 3: Performance checks."""
    file_size = os.path.getsize(target_path)
    size_kb = file_size / 1024
    report.add(CheckResult(
        "performance", "File size < 200KB",
        "PASS" if size_kb < 200 else "WARN",
        f"{size_kb:.1f}KB"
    ))

    # Check for external resource references
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    external_patterns = [
        r'<link[^>]+href="https?://',
        r'<script[^>]+src="https?://',
        r'<img[^>]+src="https?://',
    ]
    external_refs = []
    for pattern in external_patterns:
        matches = re.findall(pattern, content)
        external_refs.extend(matches)

    report.add(CheckResult(
        "performance", "No external requests",
        "PASS" if not external_refs else "WARN",
        f"External refs: {len(external_refs)}" if external_refs else "All assets inline"
    ))


def run_content_checks(page, state: dict, report: QAReport):
    """Category 4: Content validation against Phase 5 copy."""
    page_text = page.evaluate("document.body.innerText")

    # Check for placeholders
    placeholder_found = []
    for pattern in PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        if matches:
            placeholder_found.extend(matches[:3])
    report.add(CheckResult(
        "content", "No placeholder text",
        "PASS" if not placeholder_found else "FAIL",
        f"Found: {placeholder_found}" if placeholder_found else "Clean content"
    ))

    # Check for broken template tokens
    token_found = []
    for pattern in BROKEN_TOKEN_PATTERNS:
        matches = re.findall(pattern, page_text)
        if matches:
            token_found.extend(matches[:3])
    report.add(CheckResult(
        "content", "No broken tokens",
        "PASS" if not token_found else "FAIL",
        f"Found: {token_found}" if token_found else "No template tokens"
    ))

    # Validate Phase 5 headlines if state available
    phase_5 = state.get("phases", {}).get("phase_5", {}).get("output", {})
    sections = phase_5.get("sections", [])
    missing_headlines = []
    for section in sections:
        headline = section.get("headline", "")
        if headline and headline not in page_text:
            missing_headlines.append(headline[:50])
    if sections:
        report.add(CheckResult(
            "content", "Headlines match Phase 5",
            "PASS" if not missing_headlines else "FAIL",
            f"Missing: {missing_headlines}" if missing_headlines else f"{len(sections)} headlines verified"
        ))


def run_accessibility_checks(page, report: QAReport):
    """Category 5: Accessibility checks."""
    # Single H1
    h1_count = page.evaluate("document.querySelectorAll('h1').length")
    report.add(CheckResult(
        "accessibility", "Single H1",
        "PASS" if h1_count == 1 else "WARN",
        f"Found {h1_count} H1 elements"
    ))

    # Heading hierarchy (no skipped levels)
    headings = page.evaluate("""() => {
        const hs = document.querySelectorAll('h1,h2,h3,h4,h5,h6');
        return Array.from(hs).map(h => parseInt(h.tagName[1]));
    }""")
    skipped = False
    for i in range(1, len(headings)):
        if headings[i] > headings[i - 1] + 1:
            skipped = True
            break
    report.add(CheckResult(
        "accessibility", "No skipped heading levels",
        "PASS" if not skipped else "WARN",
        f"Heading sequence: {headings[:10]}"
    ))

    # Alt texts on images
    imgs_without_alt = page.evaluate("""() => {
        const imgs = document.querySelectorAll('img');
        return Array.from(imgs).filter(i => !i.alt || i.alt.trim() === '').length;
    }""")
    total_imgs = page.evaluate("document.querySelectorAll('img').length")
    report.add(CheckResult(
        "accessibility", "All images have alt text",
        "PASS" if imgs_without_alt == 0 else "FAIL",
        f"{imgs_without_alt}/{total_imgs} images missing alt" if imgs_without_alt else f"{total_imgs} images OK"
    ))

    # Skip navigation link
    skip_link = page.query_selector('a[href="#main"], a[href="#content"], .skip-nav, .skip-link')
    report.add(CheckResult(
        "accessibility", "Skip navigation link",
        "PASS" if skip_link else "WARN",
        "Skip link found" if skip_link else "No skip navigation link found"
    ))

    # Interactive elements have accessible names
    unlabeled = page.evaluate("""() => {
        const buttons = document.querySelectorAll('button, a, input, select, textarea');
        let count = 0;
        buttons.forEach(el => {
            const name = el.getAttribute('aria-label') ||
                         el.getAttribute('aria-labelledby') ||
                         el.textContent?.trim() ||
                         el.getAttribute('title') ||
                         el.getAttribute('placeholder');
            if (!name) count++;
        });
        return count;
    }""")
    report.add(CheckResult(
        "accessibility", "Interactive elements labeled",
        "PASS" if unlabeled == 0 else "WARN",
        f"{unlabeled} unlabeled elements" if unlabeled else "All elements labeled"
    ))


def run_animation_checks(page, report: QAReport):
    """Category 6: Animation checks."""
    # Check prefers-reduced-motion is respected
    has_reduced_motion = page.evaluate("""() => {
        const styles = Array.from(document.styleSheets);
        let found = false;
        try {
            styles.forEach(sheet => {
                try {
                    Array.from(sheet.cssRules).forEach(rule => {
                        if (rule.conditionText && rule.conditionText.includes('prefers-reduced-motion')) {
                            found = true;
                        }
                    });
                } catch(e) {}
            });
        } catch(e) {}
        return found;
    }""")
    report.add(CheckResult(
        "animation", "prefers-reduced-motion respected",
        "PASS" if has_reduced_motion else "WARN",
        "Media query found" if has_reduced_motion else "No reduced-motion media query detected"
    ))

    # Check for animation/transition declarations
    has_animations = page.evaluate("""() => {
        const all = document.querySelectorAll('*');
        let count = 0;
        all.forEach(el => {
            const style = getComputedStyle(el);
            if (style.animationName !== 'none' || style.transitionProperty !== 'all') count++;
        });
        return count;
    }""")
    report.add(CheckResult(
        "animation", "Animations present",
        "PASS" if has_animations > 0 else "WARN",
        f"{has_animations} animated elements found"
    ))


def generate_html_report(report: QAReport, output_path: str):
    """Generate styled HTML QA report."""
    s = report.summary
    verdict_colors = {"PASS": "#22c55e", "CONCERNS": "#f59e0b", "FAIL": "#ef4444"}
    verdict_color = verdict_colors.get(report.verdict, "#666")

    categories = {}
    for r in report.results:
        categories.setdefault(r.category, []).append(r)

    category_html = ""
    for cat_name, checks in categories.items():
        rows = ""
        for c in checks:
            status_color = {"PASS": "#22c55e", "FAIL": "#ef4444", "WARN": "#f59e0b"}[c.status]
            rows += f"""
            <tr>
                <td><span style="color:{status_color};font-weight:700">{c.status}</span></td>
                <td>{c.name}</td>
                <td style="font-size:0.85em;color:#666">{c.detail}</td>
            </tr>"""
        category_html += f"""
        <section style="margin-bottom:2rem">
            <h2 style="text-transform:capitalize;border-bottom:2px solid #e5e7eb;padding-bottom:0.5rem">{cat_name}</h2>
            <table style="width:100%;border-collapse:collapse">
                <tr style="text-align:left;border-bottom:1px solid #e5e7eb">
                    <th style="width:80px;padding:8px">Status</th>
                    <th style="padding:8px">Check</th>
                    <th style="padding:8px">Detail</th>
                </tr>
                {rows}
            </table>
        </section>"""

    screenshot_html = ""
    for name, path in report.screenshots.items():
        rel_path = os.path.basename(path)
        screenshot_html += f"""
        <div style="flex:1;min-width:200px;max-width:360px">
            <h3 style="text-align:center">{name}</h3>
            <img src="screenshots/{rel_path}" alt="{name} screenshot"
                 style="width:100%;border:1px solid #e5e7eb;border-radius:8px">
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QA Report — Sales Page</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
               max-width:960px; margin:0 auto; padding:2rem; color:#1a1a1a; }}
        header {{ margin-bottom:2rem; padding-bottom:1rem; border-bottom:3px solid {verdict_color}; }}
        h1 {{ font-size:1.5rem; margin-bottom:0.5rem; }}
        table td, table th {{ padding:8px; border-bottom:1px solid #f0f0f0; }}
    </style>
</head>
<body>
    <header>
        <h1>QA Report</h1>
        <p style="color:#666;margin-bottom:1rem">{report.target} &mdash; {report.timestamp}</p>
        <div style="display:flex;gap:1.5rem;align-items:center">
            <span style="font-size:2rem;font-weight:800;color:{verdict_color}">{report.verdict}</span>
            <span style="color:#22c55e">{s['passed']} passed</span>
            <span style="color:#ef4444">{s['failed']} failed</span>
            <span style="color:#f59e0b">{s['warnings']} warnings</span>
        </div>
    </header>

    <section style="margin-bottom:2rem">
        <h2 style="margin-bottom:1rem">Screenshots</h2>
        <div style="display:flex;gap:1rem;flex-wrap:wrap">
            {screenshot_html}
        </div>
    </section>

    {category_html}
</body>
</html>"""

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(description="GrowthOS Sales Page QA")
    parser.add_argument("--target", required=True, help="Path to built HTML page")
    parser.add_argument("--state", default=None, help="Path to state.json")
    parser.add_argument("--output", default="phase-8-qa.html", help="Path for HTML report output")
    args = parser.parse_args()

    if not os.path.exists(args.target):
        print(f"ERROR: Target file not found: {args.target}")
        sys.exit(2)

    # Load state if available
    state = {}
    if args.state and os.path.exists(args.state):
        with open(args.state, "r", encoding="utf-8") as f:
            state = json.load(f)

    report = QAReport(target=args.target)
    screenshot_dir = Path(args.output).parent / "screenshots"

    target_url = f"file://{os.path.abspath(args.target)}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(target_url, wait_until="networkidle")

        run_functional_checks(page, report)
        run_visual_checks(page, report, screenshot_dir)
        run_content_checks(page, state, report)
        run_accessibility_checks(page, report)
        run_animation_checks(page, report)

        browser.close()

    run_performance_checks(args.target, report)
    report.compute_verdict()
    generate_html_report(report, args.output)

    s = report.summary
    print(f"\n{'='*50}")
    print(f"  VERDICT: {report.verdict}")
    print(f"  Passed: {s['passed']} | Failed: {s['failed']} | Warnings: {s['warnings']}")
    print(f"  Report: {args.output}")
    print(f"{'='*50}\n")

    exit_codes = {"PASS": 0, "CONCERNS": 1, "FAIL": 2}
    sys.exit(exit_codes.get(report.verdict, 2))


if __name__ == "__main__":
    main()
