#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# GrowthOS installer
#
# Why this exists:
#   Claude Code does NOT discover plugins by their presence in
#   ~/.claude/plugins/<name> — that directory is Claude Code's
#   own managed state (cache/, marketplaces/, installed_plugins.json).
#   A plugin is discovered only when it is registered as a
#   marketplace and installed from it. This repo ships its own
#   local marketplace manifest (.claude-plugin/marketplace.json),
#   so the two commands below are all that is needed.
#
# Usage:
#   git clone https://github.com/melgarafael/growthOS.git
#   cd growthOS
#   ./install.sh
# ──────────────────────────────────────────────────────────────

set -euo pipefail

REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLUGIN_ID="growthOS@growthOS"

echo "→ GrowthOS installer"
echo "  repo: ${REPO_DIR}"
echo

# Sanity: must be run from inside the repo
if [[ ! -f "${REPO_DIR}/.claude-plugin/plugin.json" ]]; then
  echo "✗ .claude-plugin/plugin.json not found — run this script from the growthOS repo root." >&2
  exit 1
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "✗ the 'claude' CLI is not on PATH — install Claude Code first." >&2
  exit 1
fi

# Fail fast on a malformed manifest instead of installing something broken
echo "→ validating manifests…"
claude plugin validate "${REPO_DIR}"

# Remove the symlink left behind by older versions of this installer
LEGACY_LINK="${HOME}/.claude/plugins/growthOS"
if [[ -L "${LEGACY_LINK}" ]]; then
  rm "${LEGACY_LINK}"
  echo "✓ removed legacy symlink ${LEGACY_LINK} (no longer used)"
fi

echo "→ registering local marketplace…"
claude plugin marketplace add "${REPO_DIR}" --scope user 2>&1 | tail -1 || true
claude plugin marketplace update growthOS >/dev/null 2>&1 || true

echo "→ installing plugin…"
claude plugin install "${PLUGIN_ID}" --scope user -y

# Copy brand-voice template if user has not set one yet
if [[ ! -f "${REPO_DIR}/brand-voice.yaml" && -f "${REPO_DIR}/brand-voice.example.yaml" ]]; then
  cp "${REPO_DIR}/brand-voice.example.yaml" "${REPO_DIR}/brand-voice.yaml"
  echo "✓ created brand-voice.yaml from template"
fi

cat <<EOF

──────────────────────────────────────────────────────────────
✓ GrowthOS installed.

Next steps:
  1. Restart Claude Code (exit the session and open a new one).
  2. Run the onboarding wizard:
        /grow setup
  3. Verify what actually loaded:
        claude plugin details growthOS

If the slash commands still don't appear:
  - claude plugin list                 # must show growthOS@growthOS as enabled
  - claude plugin details growthOS     # must list the commands, agents and skills
  - claude plugin validate .           # manifest must pass
  - restart Claude Code fully.

After editing this repo, re-sync the installed copy:
  claude plugin marketplace update growthOS && claude plugin update ${PLUGIN_ID}
  (if the version did not change, reinstall: claude plugin uninstall ${PLUGIN_ID} && claude plugin install ${PLUGIN_ID} -y)

To uninstall:
  claude plugin uninstall ${PLUGIN_ID}
  claude plugin marketplace remove growthOS
──────────────────────────────────────────────────────────────
EOF
