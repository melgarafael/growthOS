#!/usr/bin/env bash
# GrowthOS Health Check — Monitors all services, alerts on failure
# Cron: */5 * * * * /opt/growthos/deploy/scripts/health-check.sh
set -euo pipefail

WEBHOOK_URL="${GROWTHOS_WEBHOOK_URL:-}"
DOMAIN="${DOMAIN:-localhost}"
STATE_DIR="/var/run/growthos"
mkdir -p "$STATE_DIR" 2>/dev/null || true
ALERT_FILE="${STATE_DIR}/alert-state"

notify() {
    if [[ -n "$WEBHOOK_URL" ]]; then
        curl -sS -H "Content-Type: application/json" \
            -d "{\"content\":\"$1\"}" \
            "$WEBHOOK_URL" >/dev/null 2>&1 || true
    fi
}

ISSUES=()

# ─── Check Docker containers ────────────────────────────
CONTAINERS=(
    "growthos-caddy"
    "growthos-mcp-publish"
    "growthos-mcp-discover"
    "growthos-mcp-vault"
    "growthos-review"
    "growthos-ig-publisher"
    "growthos-ship-queue"
)

for container in "${CONTAINERS[@]}"; do
    STATUS=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null || echo "missing")
    if [[ "$STATUS" != "running" ]]; then
        ISSUES+=("Container $container: $STATUS")
    fi

    # Check health status if available
    HEALTH=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "none")
    if [[ "$HEALTH" == "unhealthy" ]]; then
        ISSUES+=("Container $container: unhealthy")
    fi
done

# ─── Check disk usage ───────────────────────────────────
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if (( DISK_USAGE > 85 )); then
    ISSUES+=("Disco em ${DISK_USAGE}% — limpar espaco")
fi

# ─── Check memory ────────────────────────────────────────
MEM_AVAILABLE=$(free -m | awk '/^Mem:/{print $7}')
if (( MEM_AVAILABLE < 512 )); then
    ISSUES+=("Memoria disponivel: ${MEM_AVAILABLE}MB — baixa")
fi

# ─── Check HTTPS endpoint ───────────────────────────────
if [[ "$DOMAIN" != "localhost" ]]; then
    HTTP_CODE=$(curl -sS -o /dev/null -w "%{http_code}" --max-time 10 "https://$DOMAIN/health" 2>/dev/null || echo "000")
    if [[ "$HTTP_CODE" != "200" ]]; then
        ISSUES+=("HTTPS health check falhou: HTTP $HTTP_CODE")
    fi
fi

# ─── Alert logic (avoid spam) ────────────────────────────
if [[ ${#ISSUES[@]} -gt 0 ]]; then
    ISSUE_TEXT=$(printf "- %s\n" "${ISSUES[@]}")

    # Only alert if state changed (avoid repeat alerts every 5 min)
    CURRENT_HASH=$(echo "$ISSUE_TEXT" | md5sum | cut -d' ' -f1)
    PREVIOUS_HASH=$(cat "$ALERT_FILE" 2>/dev/null || echo "")

    if [[ "$CURRENT_HASH" != "$PREVIOUS_HASH" ]]; then
        notify "🔴 **GrowthOS ALERTA** — $(date '+%H:%M %d/%m')\n${ISSUE_TEXT}"
        echo "$CURRENT_HASH" > "$ALERT_FILE"
    fi

    echo "[$(date -Iseconds)] ISSUES: ${ISSUES[*]}"
    exit 1
else
    # Clear alert state on recovery
    if [[ -f "$ALERT_FILE" ]]; then
        notify "🟢 **GrowthOS RECUPERADO** — todos os servicos healthy ($(date '+%H:%M %d/%m'))"
        rm -f "$ALERT_FILE"
    fi
    echo "[$(date -Iseconds)] OK — all services healthy"
fi
