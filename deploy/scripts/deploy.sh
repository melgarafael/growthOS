#!/usr/bin/env bash
# GrowthOS Deploy Script — Rolling restart with auto-rollback
# Usage: ./deploy.sh [--rollback]
set -euo pipefail

DEPLOY_DIR="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="$DEPLOY_DIR/docker-compose.prod.yml"
LOG_FILE="/var/log/growthos/deploy.log"
WEBHOOK_URL="${GROWTHOS_WEBHOOK_URL:-}"
ROLLBACK_TAG="rollback"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE" 2>/dev/null || echo -e "[$(date -Iseconds)] $1"; }
notify() {
    log "$1"
    if [[ -n "$WEBHOOK_URL" ]]; then
        curl -sS -H "Content-Type: application/json" \
            -d "{\"content\":\"**GrowthOS Deploy** — $1\"}" \
            "$WEBHOOK_URL" >/dev/null 2>&1 || true
    fi
}

health_check() {
    local service="$1"
    local max_attempts=10
    local attempt=0

    while (( attempt < max_attempts )); do
        if docker inspect --format='{{.State.Health.Status}}' "$service" 2>/dev/null | grep -q "healthy"; then
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 3
    done
    return 1
}

# Tag all running container images with :rollback for safe rollback
save_current_images() {
    log "Salvando imagens atuais com tag :$ROLLBACK_TAG..."
    for container in $(docker compose -f "$COMPOSE_FILE" ps -q 2>/dev/null); do
        local image
        image=$(docker inspect --format='{{.Config.Image}}' "$container" 2>/dev/null || true)
        if [[ -n "$image" && "$image" != *"$ROLLBACK_TAG"* ]]; then
            local base_name="${image%%:*}"
            docker tag "$image" "${base_name}:${ROLLBACK_TAG}" 2>/dev/null || true
        fi
    done
}

rollback() {
    notify "${RED}ROLLBACK INICIADO${NC}"

    # Stop current (broken) containers
    docker compose -f "$COMPOSE_FILE" down --timeout 30 2>/dev/null || true

    # Retag rollback images as latest so compose picks them up
    local found_rollback=false
    for image in $(docker images --format '{{.Repository}}:{{.Tag}}' | grep ":${ROLLBACK_TAG}$"); do
        local base_name="${image%%:*}"
        docker tag "$image" "${base_name}:latest" 2>/dev/null || true
        found_rollback=true
    done

    if $found_rollback; then
        docker compose -f "$COMPOSE_FILE" up -d
        notify "${GREEN}Rollback completo — servicos restaurados${NC}"
    else
        notify "${RED}FALHA: Sem imagens :$ROLLBACK_TAG para rollback${NC}"
        # Try starting with whatever is available
        docker compose -f "$COMPOSE_FILE" up -d
        exit 1
    fi
}

# Handle --rollback flag
if [[ "${1:-}" == "--rollback" ]]; then
    rollback
    exit 0
fi

# ─── Pre-Deploy ──────────────────────────────────────────
log "${YELLOW}Iniciando deploy...${NC}"
mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true

# Save current images for rollback BEFORE pulling new ones
save_current_images

# ─── Pull Latest Images ─────────────────────────────────
log "Pulling latest images..."
docker compose -f "$COMPOSE_FILE" pull --quiet 2>/dev/null || true
docker compose -f "$COMPOSE_FILE" build --quiet

# ─── Rolling Restart ─────────────────────────────────────
# Order matters: infrastructure first, then services
SERVICES=(
    "caddy"
    "mcp-obsidian-vault"
    "mcp-social-discover"
    "mcp-social-publish"
    "review-server"
    "ig-publisher"
    "ship-queue"
)

FAILED=false

for service in "${SERVICES[@]}"; do
    log "Restarting $service..."
    docker compose -f "$COMPOSE_FILE" up -d --no-deps --build "$service"

    # Services with health checks get verified
    container="growthos-${service}"
    if docker inspect --format='{{.Config.Healthcheck}}' "$container" 2>/dev/null | grep -q "Test"; then
        log "  Aguardando health check de $service..."
        if ! health_check "$container"; then
            log "${RED}  FALHA: $service nao ficou healthy em 30s${NC}"
            FAILED=true
            break
        fi
        log "${GREEN}  $service healthy${NC}"
    else
        sleep 2
        if ! docker inspect --format='{{.State.Running}}' "$container" 2>/dev/null | grep -q "true"; then
            log "${RED}  FALHA: $service nao esta rodando${NC}"
            FAILED=true
            break
        fi
        log "${GREEN}  $service running${NC}"
    fi
done

# ─── Post-Deploy ─────────────────────────────────────────
if $FAILED; then
    notify "Deploy FALHOU — iniciando rollback automatico"
    rollback
    exit 1
fi

# Cleanup old images (but keep :rollback tags for safety)
docker image prune -f --filter "label!=rollback" >/dev/null 2>&1 || true

notify "${GREEN}Deploy concluido com sucesso${NC} — todos os servicos healthy"
log "Deploy finalizado em $(date -Iseconds)"
