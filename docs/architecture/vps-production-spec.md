# GrowthOS VPS Production Architecture

> Design spec para deploy production-grade em Hostinger VPS.
> Escala: milhares de usuarios. Open-source community-driven.

## Decisoes Arquiteturais

| Decisao | Escolha | Motivo |
|---------|---------|--------|
| Reverse proxy | **Caddy 2** | SSL automatico, zero config certbot, ideal para self-hosting comunitario |
| Orquestracao | **Docker Compose v2** | Suficiente para VPS unico, sem overhead de Swarm/K8s |
| Secrets | **SOPS + age** | Criptografa .env no repo, descriptografa no deploy, sem infra extra |
| Monitoring | **Cron + webhook** | Zero dependencias, alerta via Discord/Slack |
| Backup | **age-encrypted + rotation** | Volumes + configs, 7 daily + 4 weekly |
| CI/CD | **GitHub Actions → SSH deploy** | Build no GH, deploy via SSH no VPS |
| Auth (dashboard) | **Basic auth no Caddy** | Fase 1 simples, upgrade para Authelia na fase 2 |
| IDS | **CrowdSec** | Community-driven, lightweight, perfeito para VPS unico |

## Servicos

```
                    Internet
                       |
                   [Caddy:443]
                    /    |    \
           /dashboard  /api   /mcp
              |         |       |
        [review:5050] [pub:8001] [discover:8002]
                                  |
                            [vault:8003]
                                  |
                           [obsidian volume]

Rede interna (sem internet):
  mcp-social-publish  → precisa egress (APIs sociais)
  mcp-social-discover → precisa egress (busca web)
  mcp-obsidian-vault  → sem egress (local only)
  review-server       → sem egress (local only)
  ig-publisher        → precisa egress (Instagram)
  ship-queue          → acesso ao Docker socket
```

## Containers

| Servico | Base Image | Porta | RAM Limit | CPU Limit |
|---------|-----------|-------|-----------|-----------|
| caddy | caddy:2-alpine | 80, 443 | 128M | 0.25 |
| mcp-social-publish | python:3.11-slim | 8001 | 256M | 0.50 |
| mcp-social-discover | python:3.11-slim | 8002 | 256M | 0.50 |
| mcp-obsidian-vault | python:3.11-slim | 8003 | 256M | 0.50 |
| review-server | python:3.11-slim | 5050 | 256M | 0.50 |
| ig-publisher | python:3.11-slim + playwright | - | 1024M | 1.00 |
| ship-queue | python:3.11-slim | - | 128M | 0.25 |

**Total**: ~2.3GB RAM, 3.5 CPU cores → cabe em VPS 4-core 8GB com folga.

## Redes Docker

| Rede | Tipo | Servicos |
|------|------|----------|
| proxy-net | bridge | caddy, review-server |
| mcp-internal | bridge, internal:true | todos os MCP servers, review-server |
| social-egress | bridge | mcp-social-publish, mcp-social-discover, ig-publisher |

## Estrutura de Arquivos

```
growthOS/deploy/
  docker-compose.prod.yml    # Compose unificado
  Caddyfile                  # Reverse proxy config
  Dockerfile.review          # Flask review dashboard
  Dockerfile.publisher       # IG publisher + Playwright
  Dockerfile.queue           # Ship queue orchestrator
  .env.production.example    # Template de envs
  scripts/
    deploy.sh                # Deploy com rolling restart
    rollback.sh              # Rollback one-command
    backup.sh                # Backup diario encriptado
    setup-vps.sh             # Setup inicial do VPS
    security-check.sh        # Posture check
  configs/
    fail2ban-jail.local      # fail2ban config
    sshd_config.production   # SSH hardened
    ufw-setup.sh             # Firewall rules
  monitoring/
    health-check.sh          # Cron health checker + alertas
```

## Deploy Flow

```
git push main
  → GitHub Actions CI (lint + test + docker build + trivy)
  → Push images para GHCR
  → SSH no VPS
  → docker compose pull
  → Rolling restart (1 servico por vez)
  → Health check cada servico
  → Falhou? Rollback automatico
  → Sucesso? Webhook de notificacao
```

## Self-Hosting (Community)

```bash
curl -fsSL https://raw.githubusercontent.com/.../deploy/scripts/setup-vps.sh | bash
# Wizard interativo: dominio, API keys, email para SSL
# Resultado: tudo rodando em < 5 minutos
```
