#!/usr/bin/env bash
# GrowthOS VPS Setup — One-command production setup
# Usage: curl -fsSL https://raw.githubusercontent.com/.../setup-vps.sh | bash
# Or: ./setup-vps.sh
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

INSTALL_DIR="/opt/growthos"

echo -e "${BLUE}"
echo "  ╔══════════════════════════════════════════╗"
echo "  ║         GrowthOS VPS Setup               ║"
echo "  ║   Production-ready in under 5 minutes    ║"
echo "  ╚══════════════════════════════════════════╝"
echo -e "${NC}"

# ─── Pre-flight checks ──────────────────────────────────
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}Este script precisa rodar como root (sudo)${NC}"
        exit 1
    fi
}

check_os() {
    if ! grep -qi "ubuntu\|debian" /etc/os-release 2>/dev/null; then
        echo -e "${YELLOW}Aviso: Este script foi testado em Ubuntu/Debian. Outros OS podem funcionar mas nao sao garantidos.${NC}"
        read -p "Continuar? [y/N] " -n 1 -r
        echo
        [[ $REPLY =~ ^[Yy]$ ]] || exit 1
    fi
}

# ─── 1. System updates ──────────────────────────────────
install_deps() {
    echo -e "${BLUE}[1/7] Atualizando sistema e instalando dependencias...${NC}"
    apt-get update -qq
    apt-get install -y -qq \
        curl \
        git \
        ufw \
        fail2ban \
        unattended-upgrades \
        apt-listchanges \
        > /dev/null 2>&1
    echo -e "${GREEN}  Dependencias instaladas${NC}"
}

# ─── 2. Docker ───────────────────────────────────────────
install_docker() {
    echo -e "${BLUE}[2/7] Instalando Docker...${NC}"
    if command -v docker &>/dev/null; then
        echo -e "${GREEN}  Docker ja instalado ($(docker --version))${NC}"
        return
    fi
    curl -fsSL https://get.docker.com | sh -s -- --quiet
    systemctl enable docker
    systemctl start docker
    echo -e "${GREEN}  Docker instalado${NC}"
}

# ─── 3. Firewall ─────────────────────────────────────────
setup_firewall() {
    echo -e "${BLUE}[3/7] Configurando firewall...${NC}"
    ufw default deny incoming > /dev/null
    ufw default allow outgoing > /dev/null
    ufw allow 22/tcp comment 'SSH' > /dev/null
    ufw allow 80/tcp comment 'HTTP' > /dev/null
    ufw allow 443/tcp comment 'HTTPS' > /dev/null
    echo "y" | ufw enable > /dev/null 2>&1
    echo -e "${GREEN}  Firewall ativo (SSH + HTTP + HTTPS)${NC}"
}

# ─── 4. fail2ban ─────────────────────────────────────────
setup_fail2ban() {
    echo -e "${BLUE}[4/7] Configurando fail2ban...${NC}"
    cat > /etc/fail2ban/jail.local << 'JAIL'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 86400
JAIL
    systemctl restart fail2ban
    echo -e "${GREEN}  fail2ban configurado${NC}"
}

# ─── 5. Clone & setup GrowthOS ───────────────────────────
setup_growthos() {
    echo -e "${BLUE}[5/7] Configurando GrowthOS...${NC}"

    if [[ -d "$INSTALL_DIR" ]]; then
        echo -e "${YELLOW}  $INSTALL_DIR ja existe, pulando clone${NC}"
    else
        read -p "  URL do repositorio Git (ex: https://github.com/user/growthos): " REPO_URL
        git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
    fi

    # Create directories
    mkdir -p /var/log/growthos /var/backups/growthos

    echo -e "${GREEN}  GrowthOS configurado em $INSTALL_DIR${NC}"
}

# ─── 6. Environment setup ────────────────────────────────
setup_env() {
    echo -e "${BLUE}[6/7] Configurando variaveis de ambiente...${NC}"

    ENV_FILE="$INSTALL_DIR/growthOS/deploy/.env.production"

    if [[ -f "$ENV_FILE" ]]; then
        echo -e "${YELLOW}  .env.production ja existe, pulando${NC}"
        return
    fi

    cp "$INSTALL_DIR/growthOS/deploy/.env.production.example" "$ENV_FILE"

    echo ""
    echo -e "${YELLOW}  Configuracao interativa:${NC}"
    echo ""

    read -p "  Dominio (ex: app.growthOS.dev): " DOMAIN
    read -p "  Email admin (para SSL): " ADMIN_EMAIL
    read -p "  Usuario do dashboard: " DASH_USER
    read -sp "  Senha do dashboard: " DASH_PASS
    echo ""

    # Generate Caddy bcrypt hash
    DASH_HASH=$(docker run --rm caddy:2-alpine caddy hash-password --plaintext "$DASH_PASS" 2>/dev/null)

    sed -i "s|DOMAIN=.*|DOMAIN=$DOMAIN|" "$ENV_FILE"
    sed -i "s|ADMIN_EMAIL=.*|ADMIN_EMAIL=$ADMIN_EMAIL|" "$ENV_FILE"
    sed -i "s|DASHBOARD_USER=.*|DASHBOARD_USER=$DASH_USER|" "$ENV_FILE"
    sed -i "s|DASHBOARD_HASH=.*|DASHBOARD_HASH=$DASH_HASH|" "$ENV_FILE"

    echo -e "${GREEN}  Ambiente configurado${NC}"
}

# ─── 7. Start services ───────────────────────────────────
start_services() {
    echo -e "${BLUE}[7/7] Iniciando servicos...${NC}"

    cd "$INSTALL_DIR/growthOS"
    docker compose -f deploy/docker-compose.prod.yml up -d --build

    echo ""
    echo -e "${GREEN}  Todos os servicos iniciados!${NC}"

    # Setup cron jobs
    CRON_BACKUP="0 3 * * * $INSTALL_DIR/growthOS/deploy/scripts/backup.sh >> /var/log/growthos/backup.log 2>&1"
    CRON_HEALTH="*/5 * * * * $INSTALL_DIR/growthOS/deploy/scripts/health-check.sh >> /var/log/growthos/health.log 2>&1"

    (crontab -l 2>/dev/null | grep -v growthos; echo "$CRON_BACKUP"; echo "$CRON_HEALTH") | crontab -
    echo -e "${GREEN}  Cron jobs configurados (backup 3AM, health check 5min)${NC}"
}

# ─── Summary ─────────────────────────────────────────────
summary() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║       GrowthOS instalado com sucesso!    ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  Dashboard:  ${BLUE}https://${DOMAIN:-localhost}/dashboard${NC}"
    echo -e "  Health:     ${BLUE}https://${DOMAIN:-localhost}/health${NC}"
    echo -e "  Logs:       ${YELLOW}docker compose -f $INSTALL_DIR/growthOS/deploy/docker-compose.prod.yml logs -f${NC}"
    echo -e "  Deploy:     ${YELLOW}$INSTALL_DIR/growthOS/deploy/scripts/deploy.sh${NC}"
    echo -e "  Backup:     ${YELLOW}$INSTALL_DIR/growthOS/deploy/scripts/backup.sh${NC}"
    echo ""
}

# ─── Main ─────────────────────────────────────────────────
check_root
check_os
install_deps
install_docker
setup_firewall
setup_fail2ban
setup_growthos
setup_env
start_services
summary
