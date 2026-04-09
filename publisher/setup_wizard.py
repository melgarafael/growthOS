#!/usr/bin/env python3
"""
setup_wizard.py — One-time Instagram publisher setup

Simple 3-step flow:
    1. Install Playwright + Chromium (if missing)
    2. Save username/password to ~/.growthos/ig-credentials.json (chmod 600)
       (credentials are kept for reference but NOT used for automated login —
        Instagram's login page is too fragile. Manual login is the way.)
    3. Launch manual_login.py — opens Chrome, you log in, session persists

After this runs once, ig_publisher.py runs headless reusing the persistent session.
When the session eventually expires (60-90 days, or if you log out), rerun:
    .venv/bin/python growthOS/publisher/manual_login.py
"""

import getpass
import json
import os
import stat
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CREDS_DIR = Path.home() / ".growthos"
CREDS_FILE = CREDS_DIR / "ig-credentials.json"
PROFILE_DIR = CREDS_DIR / "chrome-profile"
MANUAL_LOGIN = Path(__file__).parent / "manual_login.py"


def box(title: str):
    print("\n" + "─" * 70)
    print(f"  {title}")
    print("─" * 70)


def ensure_playwright():
    box("STEP 1/3 — Playwright + Chromium")
    try:
        import playwright  # noqa
        print("  ✅ playwright already installed")
    except ImportError:
        print("  📦 installing playwright in growthOS venv...")
        venv_pip = Path(__file__).resolve().parents[1] / ".venv" / "bin" / "pip"
        if venv_pip.exists():
            subprocess.run([str(venv_pip), "install", "-q", "playwright"], check=True)
        else:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", "playwright"],
                check=True,
            )
    # Install Chromium browser
    print("  🎭 ensuring Chromium is installed...")
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)
    print("  ✅ ready")


def collect_credentials() -> dict:
    box("STEP 2/3 — Credentials stash (reference only)")
    print("""
  ℹ  As credenciais ficam salvas pra referência, mas o login é MANUAL.
     (a página de login do IG muda muito, automatizar é frágil)
  """)
    if CREDS_FILE.exists():
        existing = json.loads(CREDS_FILE.read_text())
        print(f"  ℹ existing credentials for @{existing.get('username')}")
        reuse = input("  reusar? (y/n) [y]: ").strip().lower() or "y"
        if reuse == "y":
            return existing

    username = input("  username (sem o @): ").strip()
    password = getpass.getpass("  password (opcional, só pra sua referência): ")

    return {
        "method": "playwright_web",
        "username": username,
        "password": password,
        "profile_dir": str(PROFILE_DIR),
        "saved_at": datetime.now().isoformat(),
        "note": "Login é manual via manual_login.py — senha aqui é só referência",
    }


def save_credentials(creds: dict):
    CREDS_DIR.mkdir(parents=True, exist_ok=True)
    CREDS_FILE.write_text(json.dumps(creds, indent=2))
    os.chmod(CREDS_FILE, stat.S_IRUSR | stat.S_IWUSR)
    print(f"\n  ✅ saved: {CREDS_FILE} (chmod 600)")


def run_manual_login():
    box("STEP 3/3 — Manual login (headful Chrome)")
    print(f"""
  Vou abrir o Chrome visível agora.
  Faz o login com 2FA tranquilo — sem pressa, você tem 15 minutos.

  O script detecta automaticamente quando você estiver logado
  e fecha o browser sozinho salvando a sessão.
    """)
    input("  pressione ENTER pra abrir o Chrome ")
    subprocess.run([sys.executable, str(MANUAL_LOGIN)], check=False)


def print_summary():
    box("✅ SETUP COMPLETO")
    print(f"""
  Credentials: {CREDS_FILE}
  Profile:     {PROFILE_DIR}
  Login flow:  manual (via manual_login.py)

  Próximos passos:

  1. Dry-run (testa fluxo sem publicar):

     .venv/bin/python publisher/ig_publisher.py \\
         --folder output/approved/2026-04-08/FOLDER \\
         --dry-run --headful

  2. Publicar de verdade:

     .venv/bin/python publisher/ig_publisher.py \\
         --folder output/approved/2026-04-08/FOLDER

  3. Via /grow:

     /grow ship

  Quando a sessão do IG expirar (normalmente 60-90 dias), rode:

     .venv/bin/python publisher/manual_login.py
    """)


def main():
    print("\n" + "=" * 70)
    print("   GrowthOS · Instagram Publisher · Setup")
    print("=" * 70)

    ensure_playwright()
    creds = collect_credentials()
    save_credentials(creds)
    run_manual_login()
    print_summary()


if __name__ == "__main__":
    main()
