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
        """Check if we already have a valid Instagram session.

        Strategy: navigate to instagram.com and let IG redirect. If we end up on
        /accounts/login/*, we're logged out. Otherwise we're in. This is more
        resilient than DOM probing because Instagram's sidebar text varies
        (compact vs expanded view, PT vs EN) but the login redirect is stable.
        """
        self.page.goto(IG_URL, wait_until="domcontentloaded")
        try:
            self.page.wait_for_load_state("networkidle", timeout=20000)
        except PwTimeout:
            pass
        human_delay(2, 4)

        current_url = self.page.url.lower()
        # Definitive logged-out signals
        if "accounts/login" in current_url or "/login/" in current_url or current_url.endswith("/login"):
            return False
        # Definitive logged-in signals via URL alone
        if any(k in current_url for k in ["instagram.com/?", "instagram.com/#", "instagram.com/"]):
            # Double check by looking for the login form — if present, we're NOT logged in
            try:
                login_input = self.page.locator('input[name="username"]').first
                if login_input.is_visible(timeout=1000):
                    return False
            except Exception:
                pass
            return True
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
        """Click 'Criar' in sidebar → 'Postar' in dropdown.

        Uses multiple strategies because Instagram sidebar has different layouts:
        - Expanded (≥1264px viewport): shows text "Criar" next to + icon
        - Compact (<1264px): only shows + icon with aria-label
        - In headless the compact mode often kicks in even at 1280px
        """
        print("📝 opening Create → Postar...")

        # Ensure viewport is wide enough for expanded sidebar
        try:
            self.page.set_viewport_size({"width": 1440, "height": 900})
            human_delay(0.5, 1)
        except Exception:
            pass

        clicked = False
        # Strategy 1: click via SVG aria-label (most reliable, works in compact + expanded)
        svg_selectors = [
            'svg[aria-label="Novo post"]',
            'svg[aria-label="New post"]',
            'svg[aria-label*="Criar" i]',
            'svg[aria-label*="Create" i]',
        ]
        for sel in svg_selectors:
            try:
                # Click the ancestor that handles the click
                loc = self.page.locator(sel).first
                if loc.count() > 0:
                    # Click its interactive parent (usually div[role=link] or a)
                    loc.locator("xpath=ancestor::*[self::a or @role='link' or @role='button'][1]").first.click(timeout=5000)
                    clicked = True
                    print(f"   clicked via {sel}")
                    break
            except (PwTimeout, Exception):
                continue

        # Strategy 2: role-based lookup with longer timeout + force
        if not clicked:
            for role in ["link", "button"]:
                try:
                    self.page.get_by_role(role, name=re.compile(r"Criar|Create", re.I)).first.click(timeout=5000, force=True)
                    clicked = True
                    print(f"   clicked via role={role}")
                    break
                except (PwTimeout, Exception):
                    continue

        # Strategy 3: force-click the text span
        if not clicked:
            try:
                self.page.get_by_text(re.compile(r"^Criar$|^Create$", re.I)).first.click(timeout=5000, force=True)
                clicked = True
                print("   clicked via text (force)")
            except Exception:
                pass

        if not clicked:
            raise RuntimeError("couldn't click Criar button in sidebar")

        human_delay(1.5, 2.5)

        # Depending on IG version the click opens:
        #   (a) a dropdown with Postar/Vídeo ao vivo/Anúncio/IA → need to click Postar
        #   (b) directly the upload modal "Selecione fotos e vídeos"
        # Detect which path we're in by checking for the file input OR the Postar menu item.

        file_input = self.page.locator('input[type="file"]').first
        try:
            # If the file input is already present, we're at the upload modal — done
            file_input.wait_for(state="attached", timeout=4000)
            print("   upload modal ready (skipped dropdown)")
            return
        except PwTimeout:
            pass

        # Otherwise we need to click Postar in the dropdown
        print("   dropdown detected, clicking Postar...")
        post_clicked = False
        for strategy_name, strategy in [
            ("menuitem-role", lambda: self.page.get_by_role("menuitem", name=re.compile(r"^\s*Postar\s*$|^\s*Post\s*$", re.I)).click(timeout=5000)),
            ("button-role", lambda: self.page.get_by_role("button", name=re.compile(r"^\s*Postar\s*$|^\s*Post\s*$", re.I)).click(timeout=5000)),
            ("text-force", lambda: self.page.get_by_text(re.compile(r"^\s*Postar\s*$|^\s*Post\s*$", re.I)).first.click(timeout=5000, force=True)),
            ("svg-parent", lambda: self.page.locator('svg[aria-label*="Postar" i], svg[aria-label*="Post" i]').first.locator("xpath=ancestor::*[@role='menuitem' or @role='button' or self::a][1]").click(timeout=5000)),
        ]:
            try:
                strategy()
                post_clicked = True
                print(f"   clicked Postar via {strategy_name}")
                break
            except (PwTimeout, Exception):
                continue

        if not post_clicked:
            # One more try: maybe the file input appeared by now
            try:
                file_input.wait_for(state="attached", timeout=3000)
                print("   upload modal ready (late detection)")
                return
            except PwTimeout:
                raise RuntimeError("couldn't click Postar in dropdown and no upload modal appeared")

        human_delay(2, 3)
        # Wait for the upload modal after clicking Postar
        try:
            file_input.wait_for(state="attached", timeout=10000)
        except PwTimeout:
            raise RuntimeError("clicked Postar but upload modal did not appear")

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

    def set_schedule(self, schedule_iso: str):
        """Use Instagram's native scheduling: Configurações avançadas → Agendar.

        Args:
            schedule_iso: ISO datetime string (e.g., "2026-04-10T14:00:00")
        """
        from datetime import datetime as dt
        target = dt.fromisoformat(schedule_iso.replace("Z", "+00:00"))
        print(f"🕐 setting schedule: {target.strftime('%d/%m/%Y %H:%M')}...")

        # Click "Configurações avançadas" / "Advanced settings"
        try:
            self.page.get_by_text(re.compile(r"Configurações avançadas|Advanced settings", re.I)).first.click(timeout=5000)
        except (PwTimeout, Exception):
            # Try the collapsed toggle
            try:
                self.page.locator('text=/Configurações avançadas|Advanced settings/i').first.click(timeout=5000)
            except Exception:
                print("   ⚠ couldn't find Configurações avançadas — skipping schedule")
                return False
        human_delay(1, 2)

        # Toggle "Agendar" / "Schedule" switch
        try:
            sched_toggle = self.page.get_by_text(re.compile(r"^Agendar$|^Schedule this post$|^Schedule$", re.I)).first
            sched_toggle.click(timeout=5000)
        except (PwTimeout, Exception):
            # Try role-based
            try:
                self.page.get_by_role("switch", name=re.compile(r"Agendar|Schedule", re.I)).click(timeout=5000)
            except Exception:
                print("   ⚠ couldn't toggle schedule switch — skipping")
                return False
        human_delay(1, 2)

        # Fill date and time fields
        # Instagram shows date picker and time picker — use keyboard input
        try:
            # Look for date/time inputs
            date_input = self.page.locator('input[type="date"], input[placeholder*="data" i], input[placeholder*="date" i]').first
            time_input = self.page.locator('input[type="time"], input[placeholder*="hora" i], input[placeholder*="time" i]').first

            if date_input.count() > 0:
                date_input.fill(target.strftime("%Y-%m-%d"))
                human_delay(0.5, 1)

            if time_input.count() > 0:
                time_input.fill(target.strftime("%H:%M"))
                human_delay(0.5, 1)

            print(f"   ✓ schedule set to {target.strftime('%d/%m/%Y %H:%M')}")
            return True
        except Exception as e:
            print(f"   ⚠ couldn't fill schedule fields: {e}")
            # Instagram may use dropdowns instead — try selects
            try:
                selects = self.page.locator("select")
                if selects.count() >= 2:
                    # Typically: day, hour, minute selects
                    print("   trying select dropdowns...")
                    # Fill based on visible selects
                    for sel_idx in range(selects.count()):
                        sel = selects.nth(sel_idx)
                        opts = [o.text_content() for o in sel.locator("option").all()]
                        # Try to match day/hour/minute
                        day_str = str(target.day)
                        hour_str = target.strftime("%H")
                        min_str = target.strftime("%M")
                        for candidate in [day_str, hour_str, min_str]:
                            if candidate in opts:
                                sel.select_option(candidate)
                                human_delay(0.3, 0.5)
                                break
                    print("   ✓ schedule set via dropdowns")
                    return True
            except Exception:
                pass
            return False

    def click_share(self):
        """Click 'Compartilhar' to publish (or 'Agendar' if scheduled)."""
        if self.dry_run:
            print("   [DRY RUN] would click Compartilhar now — stopping here")
            return
        print("🚀 clicking Compartilhar...")
        # If scheduled, button text changes to "Agendar" / "Schedule"
        try:
            btn = self.page.get_by_role("button", name=re.compile(r"^Compartilhar$|^Share$|^Agendar$|^Schedule$", re.I))
            btn.click(timeout=10000)
        except PwTimeout:
            self.page.get_by_text(re.compile(r"^Compartilhar$|^Share$|^Agendar$|^Schedule$", re.I)).first.click()

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

    def publish_folder(self, folder: Path, schedule_for: str = None) -> dict:
        """Main entry: publish one carousel folder.

        Args:
            folder: Path to the approved carousel folder
            schedule_for: Optional ISO datetime string to schedule instead of posting immediately
        """
        metadata = json.loads((folder / "metadata.json").read_text())
        caption_md = (folder / "caption.md").read_text()
        caption_text = extract_caption_post_text(caption_md)

        slides = sorted((folder / "slides").glob("*.png"))
        if len(slides) < 2:
            raise ValueError(f"need at least 2 slides, found {len(slides)}")
        if len(slides) > 10:
            print(f"⚠ Instagram max 10 slides, truncating from {len(slides)}")
            slides = slides[:10]

        mode_label = "DRY RUN" if self.dry_run else ("SCHEDULE " + schedule_for[:16] if schedule_for else "LIVE")
        print(f"\n📸 {metadata.get('title', folder.name)}")
        print(f"   slides: {len(slides)}")
        print(f"   caption: {len(caption_text)} chars")
        print(f"   mode: {mode_label}")
        print()

        self.ensure_logged_in()
        self.open_create_post()
        self.upload_images(slides)
        self.click_avancar(times=2)  # crop → filter → caption
        self.fill_caption(caption_text)

        # If scheduling, set the schedule before clicking share
        if schedule_for and not self.dry_run:
            self.set_schedule(schedule_for)

        self.click_share()

        # Update post-status.json
        pub_status = "scheduled" if schedule_for and not self.dry_run else ("published" if not self.dry_run else "dry_run")
        status_file = folder / "post-status.json"
        status = json.loads(status_file.read_text()) if status_file.exists() else {}
        status.update({
            "status": pub_status,
            "published": not self.dry_run and not schedule_for,
            "published_at": datetime.now().isoformat(),
            "scheduled_for": schedule_for,
            "method": "playwright_web",
            "username": self.creds["username"],
            "post_url": None,
            "notes": f"{'scheduled' if schedule_for else 'published'} via Playwright web automation on instagram.com",
        })
        status_file.write_text(json.dumps(status, indent=2))
        print(f"   post-status.json updated ✓\n")

        return status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="approved carousel folder path")
    parser.add_argument("--headful", action="store_true", help="visible browser (required first run / 2FA)")
    parser.add_argument("--dry-run", action="store_true", help="navigate but don't click Share")
    parser.add_argument("--schedule", type=str, default=None, help="ISO datetime to schedule post (e.g., 2026-04-10T14:00:00)")
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
            publisher.publish_folder(folder, schedule_for=args.schedule)
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
