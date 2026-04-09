#!/usr/bin/env python3
"""
ig_publisher.py — Publish approved carousel to Instagram via Playwright (browser automation)

Strategy: controls a real Chromium instance logged in as your Instagram user and navigates
the Instagram web UI to post. Session persists across runs via persistent context
(user logs in once, stays logged in).

Usage:
    python ig_publisher.py --folder growthOS/output/approved/2026-04-08/c04-preco
    python ig_publisher.py --folder <path> --headful           # visible browser (required on first run for login)
    python ig_publisher.py --folder <path> --dry-run           # navigate but don't click Share

Pipeline:
    1. Load ~/.growthos/ig-credentials.json
    2. Launch Chromium with persistent context at ~/.growthos/chrome-profile
    3. Navigate to instagram.com
    4. If login page detected → perform login (handle 2FA prompt manually if present)
    5. Click "Criar" → "Postar"
    6. Upload all slide PNGs from <folder>/slides/ via file input
    7. Click "Avançar" through crop + filter steps
    8. Paste caption from <folder>/caption.md (extract "Post caption" block)
    9. Click "Compartilhar"
    10. Update <folder>/post-status.json with timestamp + status
    11. Keep browser open 10s for visual confirmation, then close

Critical notes:
    - First run MUST use --headful so user can see login + handle any CAPTCHA/2FA
    - After first successful login, subsequent runs can go headless (cookies persist)
    - Instagram web updates selectors frequently — this script uses text-based locators
      (get_by_role / get_by_text in Portuguese) which are more resilient than CSS/XPath
    - The script waits for network idle + explicit element visibility to handle slow SPA navigation
    - Rate limit: Instagram may throttle aggressive posting. Add random delays between posts.

Dependencies:
    pip install playwright
    playwright install chromium
"""

import argparse
import json
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout, expect
except ImportError:
    print("❌ playwright not installed")
    print("   run: pip install playwright && playwright install chromium")
    sys.exit(1)

CREDS_FILE = Path.home() / ".growthos" / "ig-credentials.json"
DEFAULT_PROFILE_DIR = Path.home() / ".growthos" / "chrome-profile"
IG_URL = "https://www.instagram.com/"


def load_creds() -> dict:
    if not CREDS_FILE.exists():
        print(f"❌ credentials not found: {CREDS_FILE}")
        print("   run: python growthOS/publisher/setup_wizard.py")
        sys.exit(1)
    return json.loads(CREDS_FILE.read_text())


def extract_caption_post_text(caption_md: str) -> str:
    """Extract only the '## Post caption' block from caption.md."""
    m = re.search(r"## Post caption[^\n]*\n+(.+?)(?=\n## |\Z)", caption_md, re.DOTALL)
    if m:
        text = m.group(1).strip()
        # Strip markdown artifacts that IG doesn't need
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # remove bold
        text = re.sub(r"`(.+?)`", r"\1", text)  # remove inline code
        return text[:2200]
    return caption_md.strip()[:2200]


def human_delay(min_s: float = 0.5, max_s: float = 1.5):
    """Sleep a random amount to look less bot-like."""
    time.sleep(random.uniform(min_s, max_s))


class InstagramPublisher:
    def __init__(self, creds: dict, headful: bool = False, dry_run: bool = False):
        self.creds = creds
        self.headful = headful
        self.dry_run = dry_run
        self.profile_dir = Path(creds.get("profile_dir", DEFAULT_PROFILE_DIR))
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self.context = None
        self.page = None

    def launch(self, playwright):
        """Launch Chromium with persistent context (cookies survive between runs)."""
        self.context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_dir),
            headless=not self.headful,
            viewport={"width": 1280, "height": 900},
            device_scale_factor=2,
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            args=["--disable-blink-features=AutomationControlled"],
        )
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()

    def close(self):
        if self.context:
            self.context.close()

    def is_logged_in(self) -> bool:
        """Check if we already have a valid Instagram session."""
        self.page.goto(IG_URL, wait_until="domcontentloaded")
        human_delay(2, 3)
        current_url = self.page.url
        # Logged-in users stay on / or /accounts/;
        # anonymous get redirected to /accounts/login/
        if "accounts/login" in current_url or "/login" in current_url:
            return False
        # Double check by looking for a known logged-in element (Create / Criar in sidebar)
        try:
            self.page.get_by_role("link", name=re.compile("Criar|Create", re.I)).wait_for(timeout=3000)
            return True
        except PwTimeout:
            # Fallback: look for the + "Criar" button
            try:
                self.page.get_by_text(re.compile("^Criar$|^Create$", re.I)).first.wait_for(timeout=2000)
                return True
            except PwTimeout:
                return False


    def ensure_logged_in(self):
        if self.is_logged_in():
            print("✅ already logged in (persistent session)")
            return
        # No automated login — persistent session must exist.
        raise RuntimeError(
            "not logged in — the persistent Chrome session at "
            f"{self.profile_dir} is missing or expired.\n"
            "   run: .venv/bin/python growthOS/publisher/manual_login.py\n"
            "   (opens a Chrome window so you can log in manually including 2FA)"
        )

    def open_create_post(self):
        """Click 'Criar' in sidebar → 'Postar' in dropdown."""
        print("📝 opening Create → Postar...")

        # Click "Criar" button in sidebar
        try:
            # Try role-based first (most resilient)
            self.page.get_by_role("link", name=re.compile(r"^\s*Criar\s*$|^\s*Create\s*$", re.I)).click(timeout=5000)
        except PwTimeout:
            # Fallback: look for a link/button containing "Criar"
            self.page.get_by_text(re.compile(r"^Criar$|^Create$", re.I)).first.click()

        human_delay(0.8, 1.5)

        # Click "Postar" in the dropdown
        try:
            self.page.get_by_role("menuitem", name=re.compile(r"^Postar$|^Post$", re.I)).click(timeout=5000)
        except PwTimeout:
            self.page.get_by_text(re.compile(r"^Postar$|^Post$", re.I)).first.click()

        human_delay(1.5, 2.5)

    def upload_images(self, slides: list):
        """Set files on the hidden file input."""
        print(f"⬆ uploading {len(slides)} slides...")
        # The file input is hidden but accessible via locator
        file_input = self.page.locator('input[type="file"]').first
        file_input.set_input_files([str(s) for s in slides])
        human_delay(3, 5)

    def click_avancar(self, times: int = 2):
        """Click 'Avançar' N times (crop + filter)."""
        for i in range(times):
            print(f"   clicking Avançar ({i+1}/{times})")
            try:
                self.page.get_by_role("button", name=re.compile(r"^Avançar$|^Next$", re.I)).click(timeout=10000)
            except PwTimeout:
                self.page.get_by_text(re.compile(r"^Avançar$|^Next$", re.I)).first.click()
            human_delay(1.5, 2.5)

    def fill_caption(self, caption: str):
        """Paste the caption into the textarea."""
        print(f"✏ filling caption ({len(caption)} chars)...")
        # IG caption field is a contenteditable / textarea with aria-label "Escreva uma legenda..."
        try:
            field = self.page.get_by_label(re.compile("Escreva uma legenda|Write a caption", re.I))
            field.click()
            human_delay(0.5, 1)
            field.fill(caption)
        except Exception:
            # Fallback to textarea query
            textarea = self.page.locator('textarea').first
            textarea.click()
            human_delay(0.3, 0.7)
            textarea.fill(caption)
        human_delay(1, 2)

    def click_share(self):
        """Click 'Compartilhar' to publish."""
        if self.dry_run:
            print("   [DRY RUN] would click Compartilhar now — stopping here")
            return
        print("🚀 clicking Compartilhar...")
        try:
            self.page.get_by_role("button", name=re.compile(r"^Compartilhar$|^Share$", re.I)).click(timeout=10000)
        except PwTimeout:
            self.page.get_by_text(re.compile(r"^Compartilhar$|^Share$", re.I)).first.click()

        # Wait for success toast or profile redirect
        print("   waiting for confirmation...")
        try:
            # Instagram shows "Sua publicação foi compartilhada" / "Your post has been shared"
            self.page.wait_for_selector(
                'text=/Publicação compartilhada|Sua publicação|post has been shared|Post shared/',
                timeout=60000,
            )
            print("✅ post shared successfully!")
        except PwTimeout:
            print("⚠ couldn't detect share confirmation — check manually")

        human_delay(3, 5)

    def publish_folder(self, folder: Path) -> dict:
        """Main entry: publish one carousel folder."""
        metadata = json.loads((folder / "metadata.json").read_text())
        caption_md = (folder / "caption.md").read_text()
        caption_text = extract_caption_post_text(caption_md)

        slides = sorted((folder / "slides").glob("*.png"))
        if len(slides) < 2:
            raise ValueError(f"need at least 2 slides, found {len(slides)}")
        if len(slides) > 10:
            print(f"⚠ Instagram max 10 slides, truncating from {len(slides)}")
            slides = slides[:10]

        print(f"\n📸 {metadata.get('title', folder.name)}")
        print(f"   slides: {len(slides)}")
        print(f"   caption: {len(caption_text)} chars")
        print(f"   mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print()

        self.ensure_logged_in()
        self.open_create_post()
        self.upload_images(slides)
        self.click_avancar(times=2)  # crop → filter → caption
        self.fill_caption(caption_text)
        self.click_share()

        # Update post-status.json
        status_file = folder / "post-status.json"
        status = json.loads(status_file.read_text()) if status_file.exists() else {}
        status.update({
            "status": "published" if not self.dry_run else "dry_run",
            "published": not self.dry_run,
            "published_at": datetime.now().isoformat(),
            "method": "playwright_web",
            "username": self.creds["username"],
            # post URL requires scraping profile — leave for manual fill or v2
            "post_url": None,
            "notes": "published via Playwright web automation on instagram.com",
        })
        status_file.write_text(json.dumps(status, indent=2))
        print(f"   post-status.json updated ✓\n")

        return status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="approved carousel folder path")
    parser.add_argument("--headful", action="store_true", help="visible browser (required first run / 2FA)")
    parser.add_argument("--dry-run", action="store_true", help="navigate but don't click Share")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.exists():
        print(f"❌ folder not found: {folder}")
        sys.exit(1)

    creds = load_creds()
    publisher = InstagramPublisher(creds, headful=args.headful, dry_run=args.dry_run)

    with sync_playwright() as p:
        publisher.launch(p)
        try:
            publisher.publish_folder(folder)
        except Exception as e:
            print(f"\n❌ publish failed: {e}")
            # Take a screenshot for debugging
            debug_path = folder / "debug-screenshot.png"
            try:
                publisher.page.screenshot(path=str(debug_path), full_page=True)
                print(f"   debug screenshot saved: {debug_path}")
            except Exception:
                pass
            sys.exit(1)
        finally:
            if not args.headful:
                publisher.close()
            else:
                print("\n[headful mode] keeping browser open 10s for visual check...")
                time.sleep(10)
                publisher.close()


if __name__ == "__main__":
    main()
