#!/usr/bin/env bash
# GrowthOS UFW Firewall Setup
set -euo pipefail

echo "Configurando firewall UFW..."

ufw default deny incoming
ufw default allow outgoing

# SSH (ajustar porta se mudou)
ufw allow 22/tcp comment 'SSH'

# HTTP/HTTPS only — Caddy handles routing
ufw allow 80/tcp comment 'HTTP redirect to HTTPS'
ufw allow 443/tcp comment 'HTTPS'

# Block direct access to app ports (should never be exposed anyway)
ufw deny 8001:8003/tcp comment 'Block direct MCP access'
ufw deny 5050/tcp comment 'Block direct dashboard access'

# Enable with auto-yes
echo "y" | ufw enable

ufw status verbose
echo "Firewall configurado."
