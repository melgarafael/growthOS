# GrowthOS Production VPS Infrastructure Spec

> Status: **Draft** | Author: @architect | Date: 2026-04-09

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Reverse Proxy: Caddy](#2-reverse-proxy-caddy)
3. [Unified Docker Compose](#3-unified-docker-compose)
4. [Network Architecture](#4-network-architecture)
5. [SSL/TLS Strategy](#5-ssltls-strategy)
6. [Zero-Downtime Deploy](#6-zero-downtime-deploy)
7. [Resource Limits](#7-resource-limits)
8. [Health Checks & Restart Policies](#8-health-checks--restart-policies)
9. [Logging Strategy](#9-logging-strategy)
10. [Environment Management](#10-environment-management)
11. [Scaling Strategy](#11-scaling-strategy)
12. [Backup Strategy](#12-backup-strategy)
13. [Deploy Script](#13-deploy-script)
14. [Monitoring & Alerting](#14-monitoring--alerting)
15. [Self-Hosting Guide (Community)](#15-self-hosting-guide)

---

## 1. System Overview

### Service Inventory

| Service | Runtime | Internal Port | Public? | Resource Profile |
|---------|---------|---------------|---------|-----------------|
| `mcp-social-publish` | Python 3.11 (FastMCP) | 8001 | Via API subdomain | Low CPU, low RAM |
| `mcp-social-discover` | Python 3.11 (FastMCP) | 8002 | Via API subdomain | Low CPU, low RAM |
| `mcp-obsidian-vault` | Python 3.11 (FastMCP) | 8003 | Via API subdomain | Low CPU, medium RAM (file I/O) |
| `mcp-remotion-render` | Python 3.11 (FastMCP) | 8004 | Via API subdomain | Low CPU (delegates to Node) |
| `review-dashboard` | Python 3.11 (Flask) | 5050 | Via app subdomain | Low CPU, low RAM |
| `remotion-renderer` | Node.js 20 (Remotion CLI) | -- | Not exposed | **HIGH CPU, HIGH RAM** (video render) |
| `ig-publisher` | Python 3.11 (Playwright) | -- | Not exposed | Medium CPU, high RAM (headless Chrome) |
| `ship-queue` | Python 3.11 (orchestrator) | -- | Not exposed | Negligible (coordinator) |
| `caddy` | Go binary | 80, 443 | Yes | Negligible |

### Architecture Diagram

```
                    Internet
                       |
                   [Hostinger VPS]
                       |
              +--------+--------+
              |     Caddy       |
              | :80 :443 (auto) |
              +--------+--------+
                       |
         +-------------+-------------+
         |             |             |
    api.growth.    app.growth.    (future)
         |             |
   +-----------+  +----------+
   | growthos  |  | review   |
   | -internal |  | -dash    |
   | network   |  | :5050    |
   +-----------+  +----------+
   | mcp-pub   |
   | :8001     |
   | mcp-disc  |
   | :8002     |
   | mcp-vault |
   | :8003     |
   | mcp-remo  |
   | :8004     |
   +-----------+
         |
   +-----+------+------+
   |             |      |
remotion   ig-pub   ship-queue
(worker)  (worker)  (cron/worker)
```

---

## 2. Reverse Proxy: Caddy

### Decision: Caddy over Nginx

**Why Caddy for this project:**

| Factor | Caddy | Nginx |
|--------|-------|-------|
| Auto SSL (Let's Encrypt + ZeroSSL) | Built-in, zero config | Requires certbot, cron, reload hooks |
| Config complexity | 25 lines Caddyfile | 100+ lines nginx.conf + sites-enabled |
| Auto HTTPS redirect | Default behavior | Manual `return 301` block |
| OCSP stapling | Automatic | Manual config |
| Hot reload | `caddy reload` (no downtime) | `nginx -s reload` (brief interruption possible) |
| HTTP/3 (QUIC) | Built-in | Requires recompile with quic patch |
| Memory footprint | ~15MB | ~5MB |
| Community self-hosting | One binary, one file | Familiar but more error-prone for beginners |

The 10MB extra RAM cost is trivially worth eliminating an entire cert management subsystem. For an open-source project where community members self-host, "it just works" SSL is a critical DX win.

**The one Nginx advantage (raw throughput at 50k+ concurrent) does not apply here.** A Hostinger 4-8 core VPS will not see that traffic shape. The bottleneck will be Python/Node services long before the reverse proxy.

### Caddyfile

```caddyfile
# /opt/growthos/Caddyfile

{
    email admin@growthos.dev
    acme_ca https://acme-v02.api.letsencrypt.org/directory
    # Fallback to ZeroSSL if LE fails
    acme_ca https://acme.zerossl.com/v2/DV90

    servers {
        protocols h1 h2 h3
    }
}

# --- API Gateway ---
api.growthos.dev {
    # Rate limiting: 100 req/s per IP
    rate_limit {remote.ip} 100r/s

    # MCP Social Publish
    handle /publish/* {
        reverse_proxy mcp-social-publish:8001 {
            health_uri /health
            health_interval 15s
            health_timeout 3s
            lb_policy first
        }
    }

    # MCP Social Discover
    handle /discover/* {
        reverse_proxy mcp-social-discover:8002 {
            health_uri /health
            health_interval 15s
            health_timeout 3s
        }
    }

    # MCP Obsidian Vault
    handle /vault/* {
        reverse_proxy mcp-obsidian-vault:8003 {
            health_uri /health
            health_interval 15s
            health_timeout 3s
        }
    }

    # MCP Remotion Render
    handle /render/* {
        reverse_proxy mcp-remotion-render:8004 {
            health_uri /health
            health_interval 15s
            health_timeout 3s
        }
    }

    # Default: 404
    handle {
        respond "Not Found" 404
    }

    # Security headers
    header {
        X-Content-Type-Options nosniff
        X-Frame-Options DENY
        Referrer-Policy strict-origin-when-cross-origin
        -Server
    }

    log {
        output file /var/log/caddy/api-access.log {
            roll_size 50MiB
            roll_keep 5
            roll_keep_for 168h
        }
        format json
    }
}

# --- Review Dashboard ---
app.growthos.dev {
    reverse_proxy review-dashboard:5050 {
        health_uri /health
        health_interval 30s
    }

    header {
        X-Content-Type-Options nosniff
        X-Frame-Options SAMEORIGIN
        -Server
    }

    log {
        output file /var/log/caddy/app-access.log {
            roll_size 50MiB
            roll_keep 5
            roll_keep_for 168h
        }
        format json
    }
}
```

**For self-hosters who want `localhost` only (no domain):**

```caddyfile
# Caddyfile.local — no TLS, localhost only
:80 {
    handle /api/publish/* {
        reverse_proxy mcp-social-publish:8001
    }
    handle /api/discover/* {
        reverse_proxy mcp-social-discover:8002
    }
    handle /api/vault/* {
        reverse_proxy mcp-obsidian-vault:8003
    }
    handle /api/render/* {
        reverse_proxy mcp-remotion-render:8004
    }
    handle /* {
        reverse_proxy review-dashboard:5050
    }
}
```

---

## 3. Unified Docker Compose

### File: `docker-compose.prod.yml`

```yaml
# docker-compose.prod.yml — GrowthOS Production Stack
#
# Usage:
#   docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
#   docker compose -f docker-compose.prod.yml --env-file .env.prod logs -f

x-python-base: &python-base
  restart: unless-stopped
  logging: &json-logging
    driver: json-file
    options:
      max-size: "10m"
      max-file: "3"
      tag: "{{.Name}}"
  networks:
    - internal

x-healthcheck-http: &healthcheck-http
  interval: 30s
  timeout: 5s
  retries: 3
  start_period: 15s

services:
  # ═══════════════════════════════════════════
  # REVERSE PROXY
  # ═══════════════════════════════════════════
  caddy:
    image: caddy:2-alpine
    container_name: growthos-caddy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "443:443/udp"  # HTTP/3 QUIC
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy-data:/data          # certs persisted here
      - caddy-config:/config
      - caddy-logs:/var/log/caddy
    networks:
      - public
      - internal
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 64M
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:80"]
      <<: *healthcheck-http
    logging:
      <<: *json-logging

  # ═══════════════════════════════════════════
  # MCP SERVERS (Python / FastMCP)
  # ═══════════════════════════════════════════
  mcp-social-publish:
    build:
      context: .
      dockerfile: Dockerfile
      target: mcp-social-publish
    image: growthos/mcp-social-publish:${IMAGE_TAG:-latest}
    container_name: growthos-mcp-publish
    env_file: .env.prod
    expose:
      - "8001"
    <<: *python-base
    deploy:
      resources:
        limits:
          cpus: "0.50"
          memory: 256M
        reservations:
          memory: 64M
    healthcheck:
      test: ["CMD", "curl", "-sf", "http://localhost:8001/health"]
      <<: *healthcheck-http

  mcp-social-discover:
    build:
      context: .
      dockerfile: Dockerfile
      target: mcp-social-discover
    image: growthos/mcp-social-discover:${IMAGE_TAG:-latest}
    container_name: growthos-mcp-discover
    env_file: .env.prod
    expose:
      - "8002"
    <<: *python-base
    deploy:
      resources:
        limits:
          cpus: "0.50"
          memory: 256M
        reservations:
          memory: 64M
    healthcheck:
      test: ["CMD", "curl", "-sf", "http://localhost:8002/health"]
      <<: *healthcheck-http

  mcp-obsidian-vault:
    build:
      context: .
      dockerfile: Dockerfile
      target: mcp-obsidian-vault
    image: growthos/mcp-obsidian-vault:${IMAGE_TAG:-latest}
    container_name: growthos-mcp-vault
    env_file: .env.prod
    expose:
      - "8003"
    volumes:
      - vault-data:/vault:rw
    <<: *python-base
    deploy:
      resources:
        limits:
          cpus: "0.50"
          memory: 512M
        reservations:
          memory: 128M
    healthcheck:
      test: ["CMD", "curl", "-sf", "http://localhost:8003/health"]
      <<: *healthcheck-http

  mcp-remotion-render:
    build:
      context: .
      dockerfile: Dockerfile.remotion-mcp
    image: growthos/mcp-remotion-render:${IMAGE_TAG:-latest}
    container_name: growthos-mcp-remotion
    env_file: .env.prod
    expose:
      - "8004"
    volumes:
      - render-output:/app/output:rw
      - remotion-cache:/app/remotion/.remotion:rw
    <<: *python-base
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2048M
        reservations:
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-sf", "http://localhost:8004/health"]
      interval: 60s
      timeout: 10s
      retries: 3
      start_period: 30s

  # ═══════════════════════════════════════════
  # REVIEW DASHBOARD (Flask)
  # ═══════════════════════════════════════════
  review-dashboard:
    build:
      context: .
      dockerfile: Dockerfile.review
    image: growthos/review-dashboard:${IMAGE_TAG:-latest}
    container_name: growthos-review
    env_file: .env.prod
    environment:
      - FLASK_ENV=production
      - GUNICORN_WORKERS=2
      - GUNICORN_BIND=0.0.0.0:5050
    expose:
      - "5050"
    volumes:
      - design-system:/app/growthOS/design-system:rw
      - output-data:/app/growthOS/output:rw
    <<: *python-base
    deploy:
      resources:
        limits:
          cpus: "0.50"
          memory: 256M
        reservations:
          memory: 64M
    healthcheck:
      test: ["CMD", "curl", "-sf", "http://localhost:5050/health"]
      <<: *healthcheck-http

  # ═══════════════════════════════════════════
  # WORKERS (not exposed to network)
  # ═══════════════════════════════════════════
  ig-publisher:
    build:
      context: .
      dockerfile: Dockerfile.publisher
    image: growthos/ig-publisher:${IMAGE_TAG:-latest}
    container_name: growthos-ig-publisher
    env_file: .env.prod
    volumes:
      - output-data:/app/growthOS/output:rw
      - chrome-profile:/home/appuser/.growthos/chrome-profile:rw
      - ig-credentials:/home/appuser/.growthos:ro
    networks:
      - internal
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1024M
        reservations:
          memory: 256M
    # No healthcheck: this is a run-on-demand worker, not a daemon
    # Started by ship-queue via `docker compose exec`
    command: ["sleep", "infinity"]
    logging:
      <<: *json-logging

  ship-queue:
    build:
      context: .
      dockerfile: Dockerfile.ship-queue
    image: growthos/ship-queue:${IMAGE_TAG:-latest}
    container_name: growthos-ship-queue
    env_file: .env.prod
    volumes:
      - output-data:/app/growthOS/output:rw
      - /var/run/docker.sock:/var/run/docker.sock:ro  # to exec into ig-publisher
    networks:
      - internal
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 128M
    # Runs on cron schedule via container-internal cron or external systemd timer
    command: ["python", "-m", "scripts.ship_queue_daemon"]
    logging:
      <<: *json-logging

# ═══════════════════════════════════════════
# NETWORKS
# ═══════════════════════════════════════════
networks:
  public:
    driver: bridge
    name: growthos-public
  internal:
    driver: bridge
    name: growthos-internal
    internal: true  # No outbound internet access for internal services

# ═══════════════════════════════════════════
# VOLUMES
# ═══════════════════════════════════════════
volumes:
  caddy-data:
    name: growthos-caddy-data
  caddy-config:
    name: growthos-caddy-config
  caddy-logs:
    name: growthos-caddy-logs
  vault-data:
    name: growthos-vault
  render-output:
    name: growthos-render-output
  remotion-cache:
    name: growthos-remotion-cache
  design-system:
    name: growthos-design-system
  output-data:
    name: growthos-output
  chrome-profile:
    name: growthos-chrome-profile
  ig-credentials:
    name: growthos-ig-credentials
```

### Why `internal: true` on the internal network

Services that do not need outbound internet access (MCP servers processing internal data, ship-queue, etc.) are placed on a network with `internal: true`. This means:
- They can talk to each other via Docker DNS
- They **cannot** reach the internet
- If compromised, lateral movement to the internet is blocked

Services that DO need internet (ig-publisher needs Instagram, mcp-social-publish may need external APIs) must be placed on both `internal` and `public`, or the `internal: true` flag must be removed. **Adjust per actual service requirements.**

**Important correction:** In practice, several MCP servers call external APIs (httpx calls to Instagram Graph API, etc.). The recommended approach is:

```yaml
networks:
  internal:
    driver: bridge
    name: growthos-internal
    # Remove `internal: true` if MCP servers need outbound HTTP
```

Keep `internal: true` only if you deploy an HTTP proxy sidecar that whitelists specific external domains. For v1, remove the `internal: true` flag and use firewall rules (ufw) instead.

---

## 4. Network Architecture

### Port Exposure Strategy

| Port | Bound to Host? | Purpose |
|------|----------------|---------|
| 80 | Yes (Caddy) | HTTP -> HTTPS redirect |
| 443 | Yes (Caddy) | HTTPS termination |
| 443/udp | Yes (Caddy) | HTTP/3 QUIC |
| 8001-8004 | **No** (`expose` only) | MCP servers, internal only |
| 5050 | **No** (`expose` only) | Review dashboard, internal only |

**Zero ports exposed to host except 80/443.** All service-to-service communication happens over Docker's internal DNS resolution (`mcp-social-publish:8001`).

### Service Discovery

Docker Compose provides DNS-based service discovery automatically. Service name = hostname. No Consul/etcd needed at this scale.

```
caddy           -> mcp-social-publish:8001   (via Docker DNS)
caddy           -> review-dashboard:5050     (via Docker DNS)
ship-queue      -> ig-publisher              (via docker exec)
mcp-remotion    -> remotion CLI              (local subprocess)
```

### Firewall (UFW)

```bash
# /opt/growthos/setup-firewall.sh
#!/bin/bash
set -euo pipefail

ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    comment "SSH"
ufw allow 80/tcp    comment "HTTP"
ufw allow 443/tcp   comment "HTTPS"
ufw allow 443/udp   comment "HTTP/3 QUIC"
ufw --force enable

echo "Firewall configured. Only SSH + HTTP(S) exposed."
```

---

## 5. SSL/TLS Strategy

### How It Works (Caddy Auto-TLS)

1. Caddy reads the domain names from the Caddyfile (`api.growthos.dev`, `app.growthos.dev`)
2. On first start, Caddy performs ACME challenge (HTTP-01 via port 80) with Let's Encrypt
3. Certs are stored in the `caddy-data` Docker volume (persists across deploys)
4. Caddy auto-renews 30 days before expiry (checks every 12 hours)
5. If Let's Encrypt fails, Caddy falls back to ZeroSSL (configured in Caddyfile global block)
6. OCSP stapling is automatic

### What About Wildcards?

**Not needed for v1.** You have two subdomains (`api.*`, `app.*`). Caddy handles individual certs efficiently. Wildcard certs require DNS-01 challenge (API access to DNS provider), which adds complexity for community self-hosters.

If you later need `*.growthos.dev` (e.g., per-tenant subdomains), add:

```caddyfile
{
    acme_dns cloudflare {env.CLOUDFLARE_API_TOKEN}
}
*.growthos.dev {
    tls {
        dns cloudflare {env.CLOUDFLARE_API_TOKEN}
    }
}
```

### What Breaks at 2AM

**Scenario:** Let's Encrypt rate limit hit (50 certs/week/domain).
**Mitigation:** Caddy caches certs in `caddy-data` volume. As long as the volume is not deleted, renewals are infrequent. The ZeroSSL fallback provides a second CA.

**Scenario:** Port 80 blocked by Hostinger firewall.
**Mitigation:** Verify port 80 is open during initial setup. HTTP-01 challenge requires it. Document this in self-hosting guide.

---

## 6. Zero-Downtime Deploy

### Strategy: Rolling Update with Health Check Gate

Docker Compose (without Swarm) does not natively support rolling updates. The strategy uses a deploy script that:

1. Pulls new images
2. Recreates one service at a time
3. Waits for health check to pass before moving to the next
4. Rolls back on failure

### Deploy Script: `/opt/growthos/deploy.sh`

```bash
#!/bin/bash
# deploy.sh — Zero-downtime deploy for GrowthOS
# Usage: ./deploy.sh [image_tag]
#
# Requirements: docker compose v2, curl, jq

set -euo pipefail

DEPLOY_DIR="/opt/growthos"
COMPOSE_FILE="$DEPLOY_DIR/docker-compose.prod.yml"
ENV_FILE="$DEPLOY_DIR/.env.prod"
IMAGE_TAG="${1:-latest}"
LOG_FILE="/var/log/growthos/deploy-$(date +%Y%m%d-%H%M%S).log"

mkdir -p /var/log/growthos

log() { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*" | tee -a "$LOG_FILE"; }
die() { log "FATAL: $*"; exit 1; }

export IMAGE_TAG

cd "$DEPLOY_DIR"

log "=== Deploy started: tag=$IMAGE_TAG ==="

# 1. Pull new images (does not stop running containers)
log "Pulling images..."
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" pull 2>&1 | tee -a "$LOG_FILE"

# 2. Snapshot current state for rollback
PREVIOUS_TAG=$(docker inspect growthos-mcp-publish --format '{{.Config.Image}}' 2>/dev/null | cut -d: -f2 || echo "unknown")
log "Previous tag: $PREVIOUS_TAG"

# 3. Rolling update: one service at a time
# Order matters: infrastructure first, then API services, then workers
SERVICES_ORDERED=(
    "caddy"
    "mcp-social-publish"
    "mcp-social-discover"
    "mcp-obsidian-vault"
    "mcp-remotion-render"
    "review-dashboard"
    "ship-queue"
    "ig-publisher"
)

rollback() {
    local failed_service="$1"
    log "ROLLBACK: $failed_service failed health check. Rolling back all services."
    export IMAGE_TAG="$PREVIOUS_TAG"
    docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d 2>&1 | tee -a "$LOG_FILE"
    die "Deploy rolled back to $PREVIOUS_TAG due to $failed_service failure"
}

wait_healthy() {
    local service="$1"
    local container="growthos-${service//mcp-/mcp-}"
    local max_wait=120
    local elapsed=0

    # Workers without healthchecks
    if [[ "$service" == "ig-publisher" || "$service" == "ship-queue" ]]; then
        log "  $service: worker service, checking container is running..."
        sleep 5
        if docker inspect "$container" --format '{{.State.Running}}' 2>/dev/null | grep -q true; then
            log "  $service: running"
            return 0
        fi
        return 1
    fi

    log "  $service: waiting for healthy (max ${max_wait}s)..."
    while [ $elapsed -lt $max_wait ]; do
        local health
        health=$(docker inspect "$container" --format '{{.State.Health.Status}}' 2>/dev/null || echo "missing")
        if [ "$health" = "healthy" ]; then
            log "  $service: healthy (${elapsed}s)"
            return 0
        fi
        sleep 5
        elapsed=$((elapsed + 5))
    done
    log "  $service: UNHEALTHY after ${max_wait}s"
    return 1
}

for svc in "${SERVICES_ORDERED[@]}"; do
    log "Updating: $svc"
    docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d --no-deps --build "$svc" 2>&1 | tee -a "$LOG_FILE"

    if ! wait_healthy "$svc"; then
        rollback "$svc"
    fi
done

# 4. Prune old images
log "Pruning dangling images..."
docker image prune -f 2>&1 | tee -a "$LOG_FILE"

log "=== Deploy complete: tag=$IMAGE_TAG ==="
```

### GitHub Actions CD Pipeline Addition

```yaml
# .github/workflows/cd.yml
name: GrowthOS CD

on:
  push:
    branches: [main]
    paths: ["growthOS/**"]

jobs:
  deploy:
    name: Deploy to VPS
    runs-on: ubuntu-latest
    needs: [lint, test, docker, security]  # from existing ci.yml
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Set image tag
        run: echo "IMAGE_TAG=$(git rev-parse --short HEAD)" >> $GITHUB_ENV

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /opt/growthos
            git pull origin main
            ./deploy.sh ${{ env.IMAGE_TAG }}
```

---

## 7. Resource Limits

### Budget: Hostinger VPS 4-core / 8GB RAM

| Service | CPU Limit | RAM Limit | RAM Reserved | Justification |
|---------|-----------|-----------|--------------|---------------|
| caddy | 0.25 | 64 MB | -- | Reverse proxy is I/O bound, not compute |
| mcp-social-publish | 0.50 | 256 MB | 64 MB | Python ASGI, small payloads |
| mcp-social-discover | 0.50 | 256 MB | 64 MB | Python ASGI, small payloads |
| mcp-obsidian-vault | 0.50 | 512 MB | 128 MB | File I/O, could load large vault index |
| mcp-remotion-render | 2.00 | 2048 MB | 512 MB | Spawns Node subprocess for video render |
| review-dashboard | 0.50 | 256 MB | 64 MB | Flask + Gunicorn, serves HTML |
| ig-publisher | 1.00 | 1024 MB | 256 MB | Headless Chromium is RAM-hungry |
| ship-queue | 0.25 | 128 MB | -- | Orchestrator, minimal work |
| **TOTAL** | **5.50** | **4544 MB** | -- | Fits in 8GB with OS overhead |

### Why the Totals Exceed 4 Cores

CPU limits are **not reservations**. They are ceilings. The remotion renderer needs burst CPU for renders but is idle most of the time. Docker CFS scheduler handles the time-slicing. In practice, at most 2-3 services are CPU-active simultaneously.

### For 16GB RAM VPS (Recommended for Production)

Double the limits for `mcp-remotion-render` (4096 MB) and `ig-publisher` (2048 MB). These are the two services that will OOM-kill under load on 8GB.

### OOM Protection

```bash
# /etc/docker/daemon.json — add to VPS
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 65536,
      "Soft": 65536
    }
  },
  "oom-score-adjust": -500
}
```

---

## 8. Health Checks & Restart Policies

### Health Check Design

Every HTTP service must expose a `/health` endpoint that returns:

```json
{
  "status": "ok",
  "service": "mcp-social-publish",
  "uptime_seconds": 3600,
  "version": "1.2.3"
}
```

**Response codes:**
- `200` = healthy
- `503` = degraded (e.g., external API unreachable but service itself is running)
- No response / timeout = unhealthy

### Health Check Parameters by Service Type

| Service Type | Interval | Timeout | Start Period | Retries | Rationale |
|-------------|----------|---------|-------------|---------|-----------|
| API servers (MCP) | 30s | 5s | 15s | 3 | Fast startup, fast health response |
| Review dashboard | 30s | 5s | 15s | 3 | Same profile as MCP |
| Remotion MCP | 60s | 10s | 30s | 3 | Longer startup (Node deps), render may block |
| Caddy | 30s | 5s | 10s | 3 | Very fast startup |

### Restart Policy

All services use `restart: unless-stopped`:
- Automatically restarts on crash
- Survives VPS reboot (Docker starts on boot)
- Does NOT restart if manually stopped (`docker compose stop`)

**Backoff:** Docker's built-in exponential backoff (100ms, 200ms, 400ms... up to 1min) prevents crash-loops from consuming resources.

### What Breaks at 2AM: Cascade Failure

**Scenario:** `mcp-obsidian-vault` crashes in a loop (e.g., corrupt vault file). Docker restarts it every minute. Each restart reads the corrupt file, crashes again.

**Mitigation:** After 3 consecutive failures within 5 minutes, Docker stops restarting (due to the backoff ceiling). The other services continue operating. Caddy's health check marks the vault backend as down and returns 502 for vault requests only. The monitoring system (Section 14) fires an alert.

---

## 9. Logging Strategy

### Approach: Docker JSON + Logrotate + Loki (Optional)

For a single VPS, heavy log infrastructure (ELK, Splunk) is overkill. The strategy is:

1. **Docker json-file driver** with size rotation (already configured per service)
2. **Structured JSON logging** inside applications
3. **Caddy access logs** in JSON format to a mounted volume
4. **Logrotate** for Caddy logs
5. **Optional Loki + Promtail** for searchable logs (adds ~200MB RAM)

### Application Log Format

All Python services must use structured JSON logging:

```python
# shared-lib/growthOS_shared/logging_config.py
import json
import logging
import sys
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": getattr(record, "service", "unknown"),
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        # Correlation ID for request tracing
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging(service_name: str, level: str = "INFO"):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper()))
    root.handlers = [handler]
    # Inject service name into all records
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.service = service_name
        return record
    logging.setLogRecordFactory(record_factory)
```

### Docker Log Limits (Already in Compose)

```yaml
logging:
  driver: json-file
  options:
    max-size: "10m"   # rotates at 10MB
    max-file: "3"     # keeps 3 files = 30MB max per service
```

Total log disk: 8 services x 30MB = 240MB max. Safe for any VPS disk.

### Viewing Logs

```bash
# All services
docker compose -f docker-compose.prod.yml logs -f --tail 100

# Single service
docker compose -f docker-compose.prod.yml logs -f mcp-social-publish

# Search across all containers (via docker CLI)
docker logs growthos-mcp-publish 2>&1 | jq 'select(.level == "ERROR")'
```

### Caddy Log Rotation

```bash
# /etc/logrotate.d/growthos-caddy
/var/lib/docker/volumes/growthos-caddy-logs/_data/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    postrotate
        docker exec growthos-caddy caddy reload --config /etc/caddy/Caddyfile 2>/dev/null || true
    endscript
}
```

---

## 10. Environment Management

### File Layout on VPS

```
/opt/growthos/
├── docker-compose.prod.yml
├── Caddyfile
├── .env.prod                    # secrets — NOT in git
├── Dockerfile
├── Dockerfile.review
├── Dockerfile.publisher
├── Dockerfile.ship-queue
├── Dockerfile.remotion-mcp
├── deploy.sh
├── backup.sh
└── growthOS/                    # git checkout (code only)
```

### `.env.prod` Template

```bash
# .env.prod — Production secrets
# NEVER commit this file. Add to .gitignore.

# === Image versioning ===
IMAGE_TAG=latest

# === Instagram Credentials ===
IG_USERNAME=
IG_PASSWORD=

# === API Keys (for MCP servers) ===
INSTAGRAM_ACCESS_TOKEN=
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=

# === Obsidian Vault ===
GROWTHOS_VAULT_PATH=/vault

# === Flask ===
FLASK_SECRET_KEY=  # generate: python3 -c "import secrets; print(secrets.token_hex(32))"
FLASK_ENV=production

# === Logging ===
LOG_LEVEL=INFO

# === Ship Queue ===
SHIP_QUEUE_DELAY=900
SHIP_QUEUE_MAX_PER_RUN=5
```

### Secrets Handling Rules

1. **`.env.prod` is created manually on the VPS**, never pushed via git or CI
2. **GitHub Secrets** store the SSH key for deployment, not app secrets
3. **Rotation:** When a secret changes, update `.env.prod` and run `docker compose up -d` (containers re-read env on restart)
4. **For community self-hosters:** Provide `.env.example` with all keys listed (values blank) and documentation per key

### `.env.example` (committed to repo)

```bash
# .env.example — Copy to .env.prod and fill in values
# See docs/architecture/vps-production-infra.md for details

IMAGE_TAG=latest
IG_USERNAME=
IG_PASSWORD=
INSTAGRAM_ACCESS_TOKEN=
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=
GROWTHOS_VAULT_PATH=/vault
FLASK_SECRET_KEY=
FLASK_ENV=production
LOG_LEVEL=INFO
SHIP_QUEUE_DELAY=900
SHIP_QUEUE_MAX_PER_RUN=5
```

---

## 11. Scaling Strategy

### Phase 1: Single VPS (Current — handles hundreds of users)

Everything on one VPS. Caddy + all services. Simple, observable, cheap.

### Phase 2: Offload Heavy Workers (thousands of users)

**Problem:** Video rendering and Playwright publishing are CPU/RAM hogs that compete with API services.

**Solution:** Dedicated worker VPS.

```
VPS-1 (API):                    VPS-2 (Workers):
  caddy                           remotion-renderer
  mcp-social-publish              ig-publisher
  mcp-social-discover             ship-queue
  mcp-obsidian-vault
  mcp-remotion-render (proxy)
  review-dashboard
```

Communication between VPS-1 and VPS-2 via:
- **Redis** as a job queue (add `redis` service to VPS-1)
- `mcp-remotion-render` on VPS-1 enqueues render jobs
- Worker on VPS-2 picks them up, renders, pushes result to shared storage (S3/Minio)

### Phase 3: Docker Swarm (tens of thousands of users)

Convert `docker-compose.prod.yml` to Swarm mode:

```bash
docker swarm init
docker stack deploy -c docker-compose.prod.yml growthos
```

Changes needed:
- Replace `container_name` with `deploy.replicas`
- Add `deploy.update_config` for native rolling updates
- Caddy becomes a Swarm-aware load balancer

```yaml
# Swarm additions per service
deploy:
  replicas: 2
  update_config:
    parallelism: 1
    delay: 30s
    failure_action: rollback
    monitor: 60s
    order: start-first  # new container starts before old stops
  rollback_config:
    parallelism: 0
    order: stop-first
```

### Phase 4: Kubernetes (if Swarm is not enough)

Only if you outgrow Swarm. At this point you need a dedicated ops team.

### What NOT to Do

- Do not jump to Kubernetes on day 1. A 4-core VPS with Docker Compose handles more traffic than most open-source projects will ever see.
- Do not add a load balancer between a single VPS and the internet. Caddy handles this fine.
- Do not split MCP servers across VPS unless a specific one is a bottleneck (unlikely — they are thin API layers).

---

## 12. Backup Strategy

### What to Back Up

| Data | Volume | Frequency | Retention |
|------|--------|-----------|-----------|
| SSL certs | `caddy-data` | Daily | 7 days |
| Vault content | `vault-data` | Daily | 30 days |
| Approved output | `output-data` | Daily | 30 days |
| Design system assets | `design-system` | Daily | 14 days |
| Chrome profile | `chrome-profile` | Weekly | 2 copies |
| Instagram credentials | `ig-credentials` | Weekly | 2 copies |
| `.env.prod` | File | On change | 5 copies |

### Backup Script

```bash
#!/bin/bash
# /opt/growthos/backup.sh — Daily backup of GrowthOS data volumes
# Add to crontab: 0 3 * * * /opt/growthos/backup.sh

set -euo pipefail

BACKUP_DIR="/opt/growthos/backups"
DATE=$(date +%Y%m%d)
RETENTION_DAYS=30

mkdir -p "$BACKUP_DIR"

log() { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*"; }

# Backup Docker volumes
VOLUMES=(
    "growthos-vault"
    "growthos-output"
    "growthos-design-system"
    "growthos-caddy-data"
)

for vol in "${VOLUMES[@]}"; do
    ARCHIVE="$BACKUP_DIR/${vol}-${DATE}.tar.gz"
    log "Backing up $vol -> $ARCHIVE"
    docker run --rm \
        -v "${vol}:/source:ro" \
        -v "$BACKUP_DIR:/backup" \
        alpine tar czf "/backup/${vol}-${DATE}.tar.gz" -C /source .
done

# Backup .env.prod
cp /opt/growthos/.env.prod "$BACKUP_DIR/env-prod-${DATE}.enc"

# Prune old backups
log "Pruning backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +"$RETENTION_DAYS" -delete
find "$BACKUP_DIR" -name "*.enc" -mtime +90 -delete

log "Backup complete."
```

### Offsite Backup (Recommended)

```bash
# Add to backup.sh after local backup
# Sync to Backblaze B2 (cheap, S3-compatible)
if command -v rclone &>/dev/null; then
    rclone sync "$BACKUP_DIR" b2:growthos-backups/ --max-age 7d
    log "Offsite sync complete."
fi
```

---

## 13. Deploy Script

See Section 6 for the full deploy script. Summary of the deploy flow:

```
git push main
  -> GitHub Actions CI (lint, test, docker build, trivy)
  -> GitHub Actions CD (SSH into VPS)
    -> git pull
    -> deploy.sh (rolling update per service)
      -> pull images
      -> recreate service
      -> wait for healthcheck
      -> next service (or rollback)
    -> prune old images
```

### Manual Deploy (Escape Hatch)

```bash
ssh growthos@vps.example.com
cd /opt/growthos
git pull origin main
IMAGE_TAG=$(git rev-parse --short HEAD) ./deploy.sh
```

---

## 14. Monitoring & Alerting

### Lightweight Stack: Node Exporter + Prometheus + Grafana (Optional)

For v1, use Docker's built-in monitoring + a simple cron health checker.

### Health Check Cron (Mandatory — Zero Dependencies)

```bash
#!/bin/bash
# /opt/growthos/healthcheck-cron.sh
# Crontab: */5 * * * * /opt/growthos/healthcheck-cron.sh

set -euo pipefail

WEBHOOK_URL="${ALERT_WEBHOOK_URL:-}"  # Discord/Slack webhook
SERVICES=(
    "mcp-social-publish:8001"
    "mcp-social-discover:8002"
    "mcp-obsidian-vault:8003"
    "mcp-remotion-render:8004"
    "review-dashboard:5050"
)

alert() {
    local msg="$1"
    echo "[ALERT] $msg"
    if [ -n "$WEBHOOK_URL" ]; then
        curl -s -X POST "$WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{\"content\": \"[GrowthOS ALERT] $msg\"}" \
            >/dev/null 2>&1 || true
    fi
}

for svc_port in "${SERVICES[@]}"; do
    svc="${svc_port%%:*}"
    port="${svc_port##*:}"
    container="growthos-${svc//mcp-/mcp-}"

    # Check container is running
    if ! docker inspect "$container" --format '{{.State.Running}}' 2>/dev/null | grep -q true; then
        alert "$svc container is NOT running"
        continue
    fi

    # Check health endpoint
    if ! docker exec "$container" curl -sf "http://localhost:$port/health" >/dev/null 2>&1; then
        alert "$svc health check FAILED (port $port)"
    fi
done

# Disk usage alert (>85%)
DISK_USAGE=$(df /opt/growthos --output=pcent | tail -1 | tr -d ' %')
if [ "$DISK_USAGE" -gt 85 ]; then
    alert "Disk usage at ${DISK_USAGE}% on /opt/growthos"
fi

# Memory alert (>90%)
MEM_USAGE=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 90 ]; then
    alert "Memory usage at ${MEM_USAGE}%"
fi
```

### Prometheus + Grafana (Phase 2)

When you need dashboards, add to compose:

```yaml
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    expose:
      - "9090"
    networks:
      - internal
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 256M

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana-data:/var/lib/grafana
    expose:
      - "3000"
    networks:
      - internal
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 128M
```

And expose Grafana through Caddy:

```caddyfile
monitor.growthos.dev {
    basicauth {
        admin $2a$14$... # caddy hash-password
    }
    reverse_proxy grafana:3000
}
```

---

## 15. Self-Hosting Guide

### Quick Start (Community)

```bash
# 1. Clone
git clone https://github.com/your-org/growthos.git
cd growthos/growthOS

# 2. Configure
cp .env.example .env.prod
nano .env.prod  # fill in your credentials

# 3. Choose your Caddyfile
# For domain with auto-SSL:
cp Caddyfile.domain Caddyfile
# Edit domain names in Caddyfile

# For localhost only (no SSL):
cp Caddyfile.local Caddyfile

# 4. Launch
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d

# 5. Verify
docker compose -f docker-compose.prod.yml ps
curl http://localhost/api/publish/health  # or https://api.yourdomain.com/publish/health
```

### Minimum VPS Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 4 GB | 8-16 GB |
| Disk | 20 GB | 50 GB |
| OS | Ubuntu 22.04+ | Ubuntu 24.04 LTS |
| Docker | 24.0+ | Latest stable |
| Docker Compose | v2.20+ | Latest stable |

### Hostinger-Specific Notes

1. Hostinger VPS comes with Ubuntu pre-installed. SSH in and install Docker:
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   ```
2. Hostinger's firewall panel may override UFW. Configure both: Hostinger panel (allow 80, 443, 22) AND UFW on the VPS.
3. Hostinger VPS IPs are sometimes on spam blocklists. If Let's Encrypt challenges fail, check if your IP can reach `acme-v02.api.letsencrypt.org`.

---

## Appendix A: Additional Dockerfiles Needed

### `Dockerfile.review` (Review Dashboard)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask gunicorn

COPY shared-lib/ shared-lib/
COPY pyproject.toml .
RUN pip install --no-cache-dir -e shared-lib/

COPY review-server/ review-server/
COPY scripts/ scripts/

EXPOSE 5050

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5050/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5050", "--workers", "2", "--timeout", "120", "review-server.server:app"]
```

### `Dockerfile.publisher` (Instagram Publisher)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libnss3 libatk-bridge2.0-0 libdrm2 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser
USER appuser

RUN pip install --user --no-cache-dir playwright
RUN python -m playwright install chromium

COPY --chown=appuser:appuser publisher/ publisher/

CMD ["sleep", "infinity"]
```

### `Dockerfile.ship-queue` (Ship Queue Orchestrator)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl docker.io \
    && rm -rf /var/lib/apt/lists/*

COPY shared-lib/ shared-lib/
COPY pyproject.toml .
RUN pip install --no-cache-dir -e shared-lib/

COPY scripts/ scripts/
COPY publisher/ publisher/

CMD ["python", "-m", "scripts.ship_queue_daemon"]
```

### `Dockerfile.remotion-mcp` (Remotion MCP + Node.js)

```dockerfile
# Stage 1: Node.js for Remotion
FROM node:20-slim AS remotion-deps

WORKDIR /app/remotion
COPY remotion/package.json remotion/package-lock.json* ./
RUN npm ci --production

# Stage 2: Python + Node.js
FROM python:3.11-slim

WORKDIR /app

# Install Node.js (needed to run Remotion CLI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY shared-lib/ shared-lib/
COPY pyproject.toml .
RUN pip install --no-cache-dir -e shared-lib/

COPY mcp-servers/mcp-remotion-render/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY mcp-servers/mcp-remotion-render/ mcp-servers/mcp-remotion-render/
COPY --from=remotion-deps /app/remotion/node_modules remotion/node_modules
COPY remotion/ remotion/

EXPOSE 8004

HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8004/health || exit 1

CMD ["python", "-m", "mcp-servers.mcp-remotion-render.server"]
```

---

## Appendix B: VPS Initial Setup Checklist

```bash
#!/bin/bash
# /opt/growthos/initial-setup.sh — Run once on fresh VPS

set -euo pipefail

echo "=== GrowthOS VPS Initial Setup ==="

# 1. System updates
apt-get update && apt-get upgrade -y

# 2. Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker

# 3. Create deploy user
useradd -m -s /bin/bash growthos
usermod -aG docker growthos

# 4. Firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 443/udp
ufw --force enable

# 5. Swap (important for 8GB VPS under memory pressure)
if ! swapon --show | grep -q partition; then
    fallocate -l 4G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo "/swapfile none swap sw 0 0" >> /etc/fstab
    # Tune: prefer RAM, use swap only under pressure
    sysctl vm.swappiness=10
    echo "vm.swappiness=10" >> /etc/sysctl.conf
fi

# 6. Create directories
mkdir -p /opt/growthos
mkdir -p /var/log/growthos
chown -R growthos:growthos /opt/growthos /var/log/growthos

# 7. Setup crontabs
cat > /etc/cron.d/growthos <<'EOF'
# Backups at 3 AM
0 3 * * * growthos /opt/growthos/backup.sh >> /var/log/growthos/backup.log 2>&1
# Health checks every 5 minutes
*/5 * * * * growthos /opt/growthos/healthcheck-cron.sh >> /var/log/growthos/healthcheck.log 2>&1
# Docker prune weekly (Sunday 4 AM)
0 4 * * 0 root docker system prune -af --volumes --filter "until=168h" >> /var/log/growthos/prune.log 2>&1
EOF

echo "=== Setup complete. Now:"
echo "  1. su - growthos"
echo "  2. cd /opt/growthos"
echo "  3. git clone <repo> ."
echo "  4. cp .env.example .env.prod && nano .env.prod"
echo "  5. docker compose -f docker-compose.prod.yml --env-file .env.prod up -d"
```

---

## Appendix C: What Breaks at 2AM — Failure Scenarios

| Scenario | Detection | Auto-Recovery | Manual Action |
|----------|-----------|---------------|---------------|
| MCP server crash | Docker healthcheck (30s) | `restart: unless-stopped` restarts in <1min | None needed |
| OOM kill (remotion render) | Docker logs `OOMKilled: true` | Container restarts, current render lost | Increase memory limit or move to worker VPS |
| Disk full | Healthcheck cron (5min) alerts at 85% | None | `docker system prune -af`, expand disk |
| SSL cert expiry | Caddy auto-renews 30 days early | Caddy retries renewal every 12h | Check port 80 is accessible, check Caddy logs |
| Caddy crash | Docker healthcheck restarts it | ~10s downtime while container restarts | Check Caddyfile syntax if crash-looping |
| VPS reboot | Docker `restart: unless-stopped` | All containers auto-start | None |
| Deploy failure | `deploy.sh` rollback logic | Auto-rollback to previous tag | Check deploy log, fix code, re-deploy |
| Instagram rate limit | ig-publisher logs the error | ship-queue retries with backoff | Reduce `SHIP_QUEUE_MAX_PER_RUN` |
| Chrome profile corrupt | ig-publisher fails login | None | Delete `chrome-profile` volume, re-login with `--headful` |
| Database/vault corruption | Health check 503 | None | Restore from backup |

---

## Appendix D: Decision Log

| Decision | Chosen | Rejected | Rationale |
|----------|--------|----------|-----------|
| Reverse proxy | Caddy | Nginx, Traefik | Auto-SSL is the killer feature for self-hosters. Traefik's Docker provider adds complexity without benefit for static compose. |
| Orchestration | Docker Compose | Swarm, K8s | Single VPS. Compose is the simplest thing that works. Upgrade path to Swarm is well-defined. |
| Logging | json-file + structured JSON | ELK, Loki | No budget for 2GB+ RAM log infrastructure on same VPS. json-file with rotation is zero-overhead. |
| Secrets | .env.prod file on VPS | Vault, SOPS | Team of 1-2. Vault's operational overhead is not justified. .env.prod with proper permissions (600) is sufficient. |
| Backup | Volume tar + rclone offsite | Velero, restic | Volume tarballs are simple, scriptable, and community-friendly. No k8s = no Velero. |
| Workers | Sleep + exec pattern | Celery, Bull | No persistent job queue needed. ship-queue is a simple sequential orchestrator. Adding Redis/Celery for 5 posts/day is over-engineering. |
| Network | Bridge + expose-only | Host networking, overlay | Bridge gives DNS resolution + port isolation. Overlay is for multi-host (not yet needed). |
