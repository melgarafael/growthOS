#!/usr/bin/env bash
# run-boletim.sh — entry point do cron diário do Boletim dos Magos.
#
# O que faz:
#   1. Ativa PATH do Homebrew (cron roda com PATH mínimo)
#   2. Invoca Claude Code em modo headless (-p) com permissões auto-aceitas
#   3. Dispara o orchestrator em modo autônomo (BOLETIM_AUTONOMOUS=1)
#   4. Registra stdout/stderr num log rotativo por data
#
# Instalado via launchd em ~/Library/LaunchAgents/com.automatiklabs.boletim-dos-magos.plist
# Schedule: diário às 08:00 (horário local)

set -euo pipefail

# --- PATHS ---
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin"
PROJECT_DIR="/Users/rafaelmelgaco/Downloads/melgateam"
LOG_DIR="$PROJECT_DIR/growthOS/boletim/logs"
mkdir -p "$LOG_DIR"

DATE_TAG="$(date +%Y-%m-%d)"
LOG_FILE="$LOG_DIR/run-$DATE_TAG.log"

echo "=== Boletim dos Magos — run $DATE_TAG $(date +%H:%M:%S) ===" >> "$LOG_FILE"

# --- ENV pro orchestrator ---
export BOLETIM_AUTONOMOUS=1
export GROWTHOS_DRY_RUN=false

cd "$PROJECT_DIR"

# --- Invocar Claude Code headless ---
# --dangerously-skip-permissions: necessário porque cron não tem TTY pra aprovar tools
# --permission-mode bypassPermissions: dobra a cobertura pra ambientes onde a flag mudou de nome
# -p "...": modo print (não-interativo), sai após resposta
/Users/rafaelmelgaco/.local/bin/claude \
  -p \
  --dangerously-skip-permissions \
  --permission-mode bypassPermissions \
  "Rode o boletim dos magos em modo autônomo (BOLETIM_AUTONOMOUS=1). Pule todos os checkpoints humanos. Gere a capa com o script generate-cover.mjs antes de abrir o editor. Publique no Circle e dispare o e-mail pros membros. Ao final, reporte edição número, URL do post, status do e-mail, e caminho da capa." \
  >> "$LOG_FILE" 2>&1

echo "=== run finished $(date +%H:%M:%S) exit=$? ===" >> "$LOG_FILE"
