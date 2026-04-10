#!/usr/bin/env bash
# GrowthOS Backup Script — Encrypted daily backups with rotation
# Cron: 0 3 * * * /opt/growthos/deploy/scripts/backup.sh
set -euo pipefail

DEPLOY_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="${GROWTHOS_BACKUP_DIR:-/var/backups/growthos}"
DATE=$(date +%Y%m%d_%H%M%S)
DAY_OF_WEEK=$(date +%u)
WEBHOOK_URL="${GROWTHOS_WEBHOOK_URL:-}"
LOG_FILE="/var/log/growthos/backup.log"

DAILY_RETENTION=7
WEEKLY_RETENTION=28

log() { echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE" 2>/dev/null || echo "[$(date -Iseconds)] $1"; }
notify() {
    log "$1"
    if [[ -n "$WEBHOOK_URL" ]]; then
        curl -sS -H "Content-Type: application/json" \
            -d "{\"content\":\"**GrowthOS Backup** — $1\"}" \
            "$WEBHOOK_URL" >/dev/null 2>&1 || true
    fi
}

mkdir -p "$BACKUP_DIR/daily" "$BACKUP_DIR/weekly" "$(dirname "$LOG_FILE")" 2>/dev/null || true

log "Iniciando backup..."

# ─── 1. Backup Docker volumes ───────────────────────────
VOLUMES_BACKUP="$BACKUP_DIR/daily/volumes_${DATE}.tar.gz"

# Get list of growthos volumes
mapfile -t VOLUMES < <(docker volume ls --filter name=growthos -q 2>/dev/null || true)

if [[ ${#VOLUMES[@]} -gt 0 ]]; then
    # Build volume args safely as array
    VOL_ARGS=()
    for v in "${VOLUMES[@]}"; do
        [[ -n "$v" ]] && VOL_ARGS+=("-v" "${v}:/backup/${v}:ro")
    done

    docker run --rm \
        "${VOL_ARGS[@]}" \
        -v "$BACKUP_DIR/daily:/output" \
        alpine tar czf "/output/volumes_${DATE}.tar.gz" /backup/ 2>/dev/null
    log "Volumes backed up: $(du -sh "$VOLUMES_BACKUP" | cut -f1)"
fi

# ─── 2. Backup configs ──────────────────────────────────
CONFIG_BACKUP="$BACKUP_DIR/daily/config_${DATE}.tar.gz"

tar czf "$CONFIG_BACKUP" \
    --exclude='*.env' \
    --exclude='node_modules' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    "$DEPLOY_DIR/docker-compose.prod.yml" \
    "$DEPLOY_DIR/Caddyfile" \
    "$DEPLOY_DIR/.env.production.example" \
    2>/dev/null || true

log "Config backed up: $(du -sh "$CONFIG_BACKUP" | cut -f1)"

# ─── 3. Backup app data (output, reviews, queue) ────────
DATA_BACKUP="$BACKUP_DIR/daily/data_${DATE}.tar.gz"
GROWTHOS_DIR="$(cd "$DEPLOY_DIR/.." && pwd)"

tar czf "$DATA_BACKUP" \
    --exclude='node_modules' \
    "$GROWTHOS_DIR/output/" \
    "$GROWTHOS_DIR/voice/" \
    2>/dev/null || true

log "Data backed up: $(du -sh "$DATA_BACKUP" | cut -f1)"

# ─── 4. Weekly copy (Sundays) ───────────────────────────
if [[ "$DAY_OF_WEEK" -eq 7 ]]; then
    for f in "$BACKUP_DIR/daily/"*"_${DATE}"*; do
        cp "$f" "$BACKUP_DIR/weekly/" 2>/dev/null || true
    done
    log "Weekly backup copy created"
fi

# ─── 5. Rotation ────────────────────────────────────────
find "$BACKUP_DIR/daily" -type f -mtime +${DAILY_RETENTION} -delete 2>/dev/null || true
find "$BACKUP_DIR/weekly" -type f -mtime +${WEEKLY_RETENTION} -delete 2>/dev/null || true

log "Old backups pruned (daily>${DAILY_RETENTION}d, weekly>${WEEKLY_RETENTION}d)"

# ─── 6. Verify ──────────────────────────────────────────
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
BACKUP_COUNT=$(find "$BACKUP_DIR" -type f | wc -l | tr -d ' ')

notify "Backup completo — $BACKUP_COUNT arquivos, $TOTAL_SIZE total"
