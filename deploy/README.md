# GrowthOS Production Deploy

Production-grade VPS deployment for GrowthOS.

## Quick Start (< 5 min)

### Option 1: Automated Setup (recommended)

```bash
# On a fresh Ubuntu/Debian VPS (Hostinger, DigitalOcean, etc.)
curl -fsSL https://raw.githubusercontent.com/<your-org>/growthos/main/growthOS/deploy/scripts/setup-vps.sh | sudo bash
```

### Option 2: Manual Setup

```bash
# 1. Clone
git clone https://github.com/<your-org>/growthos /opt/growthos
cd /opt/growthos/growthOS/deploy

# 2. Configure
cp .env.production.example .env.production
# Edit .env.production with your API keys, domain, etc.

# 3. Generate dashboard password hash
docker run --rm caddy:2-alpine caddy hash-password --plaintext 'your-password'
# Copy the hash into DASHBOARD_HASH in .env.production

# 4. Start
docker compose -f docker-compose.prod.yml up -d --build

# 5. Verify
curl https://your-domain.com/health
```

## Architecture

```
Internet → Caddy (SSL) → Internal Docker Network
                ├── /dashboard  → review-server:5050
                ├── /api/publish → mcp-social-publish:8001
                ├── /api/discover → mcp-social-discover:8002
                └── /api/vault  → mcp-obsidian-vault:8003
```

- **Caddy**: Reverse proxy with automatic SSL (Let's Encrypt)
- **3 MCP Servers**: Social publish, social discover, obsidian vault
- **Review Dashboard**: Flask + Gunicorn for carousel review/approval
- **IG Publisher**: Playwright-based Instagram automation
- **Ship Queue**: Orchestrates scheduled posts

### Networks

| Network | Purpose | Internet Access |
|---------|---------|----------------|
| `proxy-net` | Caddy ↔ Dashboard | Yes |
| `mcp-internal` | Service-to-service | No (`internal: true`) |
| `social-egress` | Social API calls | Yes (outbound only) |

## Operations

### Deploy

```bash
# Automated (from CI/CD or manual)
./scripts/deploy.sh

# Rollback
./scripts/rollback.sh
```

### Monitoring

Health checks run every 5 minutes via cron. Alerts go to your Discord/Slack webhook.

```bash
# Manual check
./scripts/health-check.sh

# View logs
docker compose -f docker-compose.prod.yml logs -f
docker compose -f docker-compose.prod.yml logs -f mcp-social-publish
```

### Backup

Daily automated backups at 3 AM. 7 daily + 4 weekly retention.

```bash
# Manual backup
./scripts/backup.sh

# Backups stored at /var/backups/growthos/
```

### Security

```bash
# Run security posture check
./scripts/security-check.sh
```

## CI/CD

Push to `main` triggers: lint → test → docker build → security scan → deploy → health verify.

### GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `VPS_HOST` | VPS IP or hostname |
| `VPS_USER` | SSH username |
| `VPS_SSH_KEY` | SSH private key |
| `DOMAIN` | Production domain |

## File Structure

```
deploy/
├── docker-compose.prod.yml    # All services
├── Caddyfile                  # Reverse proxy + SSL
├── Dockerfile.review          # Dashboard container
├── Dockerfile.publisher       # IG publisher container
├── Dockerfile.queue           # Ship queue container
├── .env.production.example    # Environment template
├── README.md                  # This file
├── scripts/
│   ├── deploy.sh              # Rolling deploy + auto-rollback
│   ├── rollback.sh            # One-command rollback
│   ├── backup.sh              # Daily encrypted backups
│   ├── setup-vps.sh           # Automated VPS setup
│   ├── health-check.sh        # Cron health monitor
│   └── security-check.sh      # Security posture check
└── configs/
    ├── ufw-setup.sh           # Firewall rules
    ├── fail2ban-jail.local    # Brute-force protection
    └── sshd_config.production # SSH hardening
```

## Requirements

- Ubuntu 22.04+ or Debian 12+ (recommended)
- Docker Engine 24+
- 4+ CPU cores, 8+ GB RAM
- Domain with DNS pointing to VPS IP
