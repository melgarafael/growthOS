#!/usr/bin/env bash
# GrowthOS Security Posture Check
# Usage: ./security-check.sh
set -euo pipefail

PASS=0
FAIL=0
WARN=0

check() {
    local desc="$1"
    local cmd="$2"
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "  [PASS] $desc"
        ((PASS++))
    else
        echo -e "  [FAIL] $desc"
        ((FAIL++))
    fi
}

warn() {
    local desc="$1"
    local cmd="$2"
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "  [PASS] $desc"
        ((PASS++))
    else
        echo -e "  [WARN] $desc"
        ((WARN++))
    fi
}

echo "═══════════════════════════════════════════"
echo "  GrowthOS Security Posture Check"
echo "═══════════════════════════════════════════"
echo ""

echo "── Firewall ─────────────────────────────"
check "UFW ativo" "ufw status | grep -q 'Status: active'"
check "Porta 8001 nao exposta" "! ss -tlnp | grep -q ':8001'"
check "Porta 8002 nao exposta" "! ss -tlnp | grep -q ':8002'"
check "Porta 8003 nao exposta" "! ss -tlnp | grep -q ':8003'"
check "Porta 5050 nao exposta" "! ss -tlnp | grep -q '0.0.0.0:5050'"
echo ""

echo "── SSH ──────────────────────────────────"
warn "Root login desabilitado" "grep -q 'PermitRootLogin no' /etc/ssh/sshd_config"
warn "Senha auth desabilitada" "grep -q 'PasswordAuthentication no' /etc/ssh/sshd_config"
echo ""

echo "── Docker ───────────────────────────────"
check "Containers rodando como non-root" "! docker ps -q | xargs -r docker inspect --format '{{.Config.User}}' | grep -qE '^$|^root$|^0$'"
check "Sem containers privilegiados" "! docker ps -q | xargs -r docker inspect --format '{{.HostConfig.Privileged}}' | grep -q 'true'"
echo ""

echo "── Servicos ─────────────────────────────"
check "fail2ban ativo" "systemctl is-active --quiet fail2ban"
warn "Unattended upgrades ativo" "systemctl is-active --quiet unattended-upgrades"
echo ""

echo "── Backups ────────────────────────────────"
warn "Backup recente (<48h)" "find /var/backups/growthos -type f -mtime -2 2>/dev/null | grep -q '.'"
echo ""

echo ""
echo "═══════════════════════════════════════════"
echo "  Resultado: $PASS passed, $FAIL failed, $WARN warnings"
echo "═══════════════════════════════════════════"

[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
