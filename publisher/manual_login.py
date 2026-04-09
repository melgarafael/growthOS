#!/usr/bin/env python3
"""
manual_login.py — Opens Chrome with persistent context, waits for user to log in manually.

Zero automation of credentials. Just opens the browser, navigates to instagram.com,
and polls every 5s to detect when you're logged in. Waits up to 15 min.

Run:
    .venv/bin/python growthOS/publisher/manual_login.py
"""

import re
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout
except ImportError:
    print("❌ playwright missing. run: .venv/bin/pip install playwright")
    sys.exit(1)

PROFILE_DIR = Path.home() / ".growthos" / "chrome-profile"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

IG_URL = "https://www.instagram.com/"
MAX_WAIT_SECONDS = 900  # 15 minutos
POLL_INTERVAL = 5


def is_logged_in(page) -> bool:
    """Heuristic: logged in if we're on / (not /accounts/login) AND Criar link is visible."""
    url = page.url.lower()
    if "accounts/login" in url or "/login" in url or "challenge" in url or "two_factor" in url:
        return False
    # Try to find Criar button in sidebar
    try:
        page.get_by_text(re.compile(r"^Criar$|^Create$", re.I)).first.wait_for(timeout=2000)
        return True
    except PwTimeout:
        pass
    # Fallback: look for profile picture or home feed
    try:
        page.locator('svg[aria-label*="Página inicial" i], svg[aria-label*="Home" i]').first.wait_for(timeout=2000)
        return True
    except PwTimeout:
        return False


def main():
    print("\n" + "=" * 70)
    print("   GrowthOS · Instagram · Manual Login Mode")
    print("=" * 70)
    print(f"""
  Vou abrir o Chrome visível. Faça login NA JANELA manualmente.
  Inclua o 2FA se ele pedir.

  Sem pressa — você tem até {MAX_WAIT_SECONDS // 60} minutos.

  Assim que o Instagram mostrar a tela inicial (com sidebar tendo "Criar"),
  o script detecta automaticamente e salva a sessão.

  Profile dir: {PROFILE_DIR}
    """)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            viewport={"width": 1280, "height": 900},
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        print(f"  → navegando pra {IG_URL}\n")
        page.goto(IG_URL, wait_until="domcontentloaded")
        time.sleep(3)

        # Initial check — maybe already logged in
        if is_logged_in(page):
            print("  ✅ já está logado! sessão detectada. saindo...\n")
            time.sleep(2)
            ctx.close()
            return

        print("  ⏳ aguardando você logar...")
        print(f"     (checando a cada {POLL_INTERVAL}s)\n")

        start = time.time()
        last_print = 0
        while time.time() - start < MAX_WAIT_SECONDS:
            elapsed = int(time.time() - start)
            remaining = MAX_WAIT_SECONDS - elapsed

            # Print progress every 30s
            if elapsed - last_print >= 30:
                mins_left = remaining // 60
                secs_left = remaining % 60
                print(f"     ⏱  {elapsed // 60}min{elapsed % 60:02d}s elapsed — {mins_left}min{secs_left:02d}s restante")
                last_print = elapsed

            try:
                if is_logged_in(page):
                    print(f"\n  ✅ LOGADO! detectei o feed / sidebar Criar")
                    print(f"     tempo total: {elapsed}s")
                    print(f"     sessão persistida em: {PROFILE_DIR}")
                    print(f"\n  ⏳ aguardando 8s pra salvar cookies completamente...")
                    time.sleep(8)
                    ctx.close()
                    print("  ✅ browser fechado. próximas execuções podem rodar headless.\n")
                    return
            except Exception as e:
                print(f"     check error: {e}")

            time.sleep(POLL_INTERVAL)

        print(f"\n  ❌ timeout — não detectei login em {MAX_WAIT_SECONDS}s")
        print("     você pode rodar de novo quando quiser: .venv/bin/python publisher/manual_login.py")
        ctx.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
