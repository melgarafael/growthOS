#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# GrowthOS installer
#
# Why this exists:
#   GrowthOS is distributed as a git repo (NOT via the Claude
#   Code marketplace). Cloning alone is not enough — Claude Code
#   only discovers plugins that live inside its plugin directory
#   (~/.claude/plugins/<plugin-name>). This script symlinks the
#   cloned repo into that directory so all skills, agents,
#   commands and hooks become available as slash commands like
#   /grow and /growthOS:<skill>.
#
# Usage:
#   git clone https://github.com/melgarafael/growthOS.git
#   cd growthOS
#   ./install.sh
# ──────────────────────────────────────────────────────────────

set -euo pipefail

REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLUGIN_NAME="growthOS"
CLAUDE_PLUGINS_DIR="${HOME}/.claude/plugins"
TARGET="${CLAUDE_PLUGINS_DIR}/${PLUGIN_NAME}"

echo "→ GrowthOS installer"
echo "  repo:   ${REPO_DIR}"
echo "  target: ${TARGET}"
echo

# Sanity: must be run from inside the repo
if [[ ! -f "${REPO_DIR}/.claude-plugin/plugin.json" ]]; then
  echo "✗ .claude-plugin/plugin.json not found — run this script from the growthOS repo root." >&2
  exit 1
fi

mkdir -p "${CLAUDE_PLUGINS_DIR}"

# If target already exists, handle gracefully
if [[ -L "${TARGET}" ]]; then
  CURRENT="$(readlink "${TARGET}")"
  if [[ "${CURRENT}" == "${REPO_DIR}" ]]; then
    echo "✓ already linked to this repo — nothing to do."
    exit 0
  fi
  echo "! ${TARGET} is a symlink pointing elsewhere (${CURRENT})."
  read -r -p "  replace it? [y/N] " ans
  [[ "${ans}" =~ ^[Yy]$ ]] || { echo "aborted."; exit 1; }
  rm "${TARGET}"
elif [[ -e "${TARGET}" ]]; then
  echo "! ${TARGET} already exists and is not a symlink."
  read -r -p "  back it up to ${TARGET}.bak and replace? [y/N] " ans
  [[ "${ans}" =~ ^[Yy]$ ]] || { echo "aborted."; exit 1; }
  mv "${TARGET}" "${TARGET}.bak"
fi

ln -s "${REPO_DIR}" "${TARGET}"
echo "✓ linked ${TARGET} → ${REPO_DIR}"

# Copy brand-voice template if user has not set one yet
if [[ ! -f "${REPO_DIR}/brand-voice.yaml" && -f "${REPO_DIR}/brand-voice.example.yaml" ]]; then
  cp "${REPO_DIR}/brand-voice.example.yaml" "${REPO_DIR}/brand-voice.yaml"
  echo "✓ created brand-voice.yaml from template"
fi

cat <<EOF

──────────────────────────────────────────────────────────────
✓ GrowthOS installed.

Next steps:
  1. Restart Claude Code (or open a new session) so it picks
     up the new plugin.
  2. Run the onboarding wizard:
        /grow setup
  3. List available skills / commands to verify:
        /help

If the slash commands still don't appear:
  - confirm the symlink:  ls -la ~/.claude/plugins/growthOS
  - confirm plugin.json:  cat ~/.claude/plugins/growthOS/.claude-plugin/plugin.json
  - restart Claude Code fully.

To uninstall:
  rm ~/.claude/plugins/growthOS
──────────────────────────────────────────────────────────────
EOF
