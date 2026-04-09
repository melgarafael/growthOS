#!/bin/bash
# sync-plugin.sh — Sincroniza o repo growthOS/ com as instalações do plugin no Claude Code
#
# Uso:
#   ./scripts/sync-plugin.sh           # copy-based sync (default)
#   ./scripts/sync-plugin.sh --link    # symlink (repo vira fonte única, sync automático)
#   ./scripts/sync-plugin.sh --dry-run # mostra o que faria
#
# Por quê existe:
#   Os comandos /grow, agentes, skills e brand-voice ficam em TRÊS lugares:
#   1. /Users/rafaelmelgaco/Downloads/melgateam/growthOS/ (este repo — fonte de verdade)
#   2. ~/.claude/plugins/cache/growthOS/growthOS/1.0.0/ (versioned plugin cache)
#   3. ~/.claude/plugins/cache/temp_local_*/ (temp local install)
#
#   Sem esse sync, edits no repo não aparecem em novas sessões do Claude Code.

set -euo pipefail

REPO="/Users/rafaelmelgaco/Downloads/melgateam/growthOS"
PLUGIN_V="/Users/rafaelmelgaco/.claude/plugins/cache/growthOS/growthOS/1.0.0"
PLUGIN_T_PATTERN="/Users/rafaelmelgaco/.claude/plugins/cache/temp_local_*"

MODE="copy"
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --link) MODE="link" ;;
    --dry-run) DRY_RUN=true ;;
    --help|-h)
      head -20 "$0" | tail -18
      exit 0
      ;;
  esac
done

# Resolve temp plugin (there is usually exactly 1)
PLUGIN_T=$(ls -d $PLUGIN_T_PATTERN 2>/dev/null | head -1 || true)

DESTINATIONS=()
[ -d "$PLUGIN_V" ] && DESTINATIONS+=("$PLUGIN_V")
[ -n "$PLUGIN_T" ] && [ -d "$PLUGIN_T" ] && DESTINATIONS+=("$PLUGIN_T")

if [ ${#DESTINATIONS[@]} -eq 0 ]; then
  echo "no plugin install found in ~/.claude/plugins/cache/"
  exit 1
fi

TARGETS=(
  "commands/grow/COMMAND.md"
  "commands/grow/FREE-CONTENT.md"
  "commands/grow/README.md"
  "commands/grow/setup.md"
  "brand-voice.yaml"
  "agents/carousel-designer/AGENT.md"
  "agents/content-creator/AGENT.md"
  "agents/caption-writer/AGENT.md"
  "agents/growth-strategist/AGENT.md"
  "agents/social-publisher/AGENT.md"
  "agents/intelligence-analyst/AGENT.md"
  "agents/visual-designer/AGENT.md"
  "agents/growth-engineer/AGENT.md"
  "agents/video-producer/AGENT.md"
  "agents/cmo/AGENT.md"
  "skills/copywriting/SKILL.md"
  "skills/content-creation/SKILL.md"
  "skills/instagram-carousel/SKILL.md"
  "design-system/DESIGN-SYSTEM.md"
)

DIRS_TO_MIRROR=(
  "scripts"
  "review-server"
  "publisher"
  "voice/preferences"
  "voice/virais"
  "assets/_meta"
)

sync_file() {
  local src_rel="$1"
  local dst_base="$2"
  local src="$REPO/$src_rel"
  local dst="$dst_base/$src_rel"

  [ ! -e "$src" ] && return
  mkdir -p "$(dirname "$dst")"

  if [ "$DRY_RUN" = true ]; then
    echo "  would sync: $src_rel"
    return
  fi

  if [ "$MODE" = "link" ]; then
    rm -rf "$dst"
    ln -s "$src" "$dst"
  else
    cp "$src" "$dst"
  fi
}

sync_dir() {
  local src_rel="$1"
  local dst_base="$2"
  local src="$REPO/$src_rel"
  local dst="$dst_base/$src_rel"

  [ ! -d "$src" ] && return

  if [ "$DRY_RUN" = true ]; then
    echo "  would mirror dir: $src_rel"
    return
  fi

  if [ "$MODE" = "link" ]; then
    rm -rf "$dst"
    ln -s "$src" "$dst"
  else
    mkdir -p "$dst"
    if command -v rsync >/dev/null; then
      rsync -a --delete "$src/" "$dst/"
    else
      rm -rf "$dst"
      cp -R "$src" "$dst"
    fi
  fi
}

echo "sync mode: $MODE"
echo "source: $REPO"

for dst in "${DESTINATIONS[@]}"; do
  echo ""
  echo "syncing to: $(basename "$(dirname "$dst")")/$(basename "$dst")"
  for target in "${TARGETS[@]}"; do
    sync_file "$target" "$dst"
  done
  for d in "${DIRS_TO_MIRROR[@]}"; do
    sync_dir "$d" "$dst"
  done
  echo "  done"
done

echo ""
echo "verification:"
for dst in "${DESTINATIONS[@]}"; do
  if grep -q "Subcommand: \`review\`" "$dst/commands/grow/COMMAND.md" 2>/dev/null; then
    echo "  OK $(basename "$(dirname "$dst")") — review subcommand present"
  else
    echo "  FAIL $(basename "$(dirname "$dst")") — review NOT found"
  fi
done

echo ""
echo "tip: run '$0 --link' ONCE to convert plugin caches to symlinks."
echo "after that, your edits in the repo apply immediately to new sessions."
