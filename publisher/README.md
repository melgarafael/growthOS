# GrowthOS Instagram Publisher (Playwright Web)

Publica carrosséis aprovados no Instagram via **Playwright controlando o Chrome no site instagram.com**. Sem Meta Graph API, sem Facebook Page, sem business account. Zero burocracia.

## Como funciona

1. Launcha Chromium com **persistent context** (cookies/sessão ficam salvos em `~/.growthos/chrome-profile/`)
2. **Login é sempre manual** — automatizar o login do IG é frágil demais (a página muda muito + CAPTCHA + 2FA). Você loga uma vez no Chrome visível, a sessão persiste 60-90 dias
3. Próximas execuções: reusa a sessão logada, roda headless sem interação
4. Navega: **Criar → Postar → upload dos PNGs → Avançar → Avançar → caption → Compartilhar**
5. Atualiza `post-status.json` com timestamp + status

## Auth flow (2 scripts separados)

| Script | Quando usar | O que faz |
|---|---|---|
| `manual_login.py` | 1× a cada 60-90 dias | Abre Chrome visível, você loga (username + password + 2FA), script detecta e salva sessão |
| `ig_publisher.py` | toda publicação | Reusa sessão persistida, **nunca tenta logar**. Se detectar que não tá logado, aborta e avisa pra rodar o manual_login |

## Quick start

### Setup one-time (~2 min + primeiro login manual)

```bash
.venv/bin/python growthOS/publisher/setup_wizard.py
```

O wizard:
1. Instala Playwright + Chromium (no venv do growthOS, não system-wide)
2. Salva username/password em `~/.growthos/ig-credentials.json` (só pra referência)
3. Chama `manual_login.py` que abre Chrome visível
4. **Você faz o login manualmente** (username + senha + 2FA)
5. Script detecta quando o feed carregar (procurando botão "Criar" no sidebar)
6. Fecha o Chrome automaticamente salvando cookies em `~/.growthos/chrome-profile/`

Quer rodar só o manual login sem o wizard todo?

```bash
.venv/bin/python growthOS/publisher/manual_login.py
```

### Publicar um carrossel

```bash
# Headless (default) — após primeiro login
python growthOS/publisher/ig_publisher.py \
    --folder growthOS/output/approved/2026-04-08/c04-preco

# Headful (visível) — recomendado em produção pra monitorar
python growthOS/publisher/ig_publisher.py \
    --folder growthOS/output/approved/2026-04-08/c04-preco \
    --headful

# Dry-run — navega todo o fluxo mas NÃO clica "Compartilhar"
python growthOS/publisher/ig_publisher.py \
    --folder growthOS/output/approved/2026-04-08/c04-preco \
    --dry-run --headful
```

### Batch via /grow ship

```bash
/grow ship                      # publica todos os aprovados de hoje
/grow ship --dry-run            # testa tudo sem postar
/grow ship --date 2026-04-09    # publica aprovados de uma data específica
```

## Credenciais

Arquivo: `~/.growthos/ig-credentials.json` (chmod 600, só você lê)

```json
{
  "method": "playwright_web",
  "username": "<your-instagram-handle>",
  "password": "...",
  "profile_dir": "<your-home>/.growthos/chrome-profile",
  "saved_at": "2026-04-08",
  "note": "Playwright browser automation on instagram.com"
}
```

**NUNCA comita esse arquivo no git.** Ele fica fora do repo por design.

## Chrome profile persistente

Diretório: `~/.growthos/chrome-profile/`

Contém cookies, localStorage, cache — tudo que mantém você logado. Primeira execução loga uma vez, as próximas 30+ dias rodam sem reautenticação.

Se o Instagram deslogar (trocou senha, expirou, nova detecção de device), roda o setup wizard de novo:

```bash
python growthOS/publisher/setup_wizard.py
```

## Fluxo navegado no IG web

Baseado no screenshot que você mandou:

```
Sidebar esquerda:
├── Página inicial
├── Reels
├── Mensagens
├── Pesquisa
├── Explorar
├── Notificações
└── Criar  ← clica aqui
    ├── Postar     ← depois aqui
    ├── Vídeo ao vivo
    ├── Anúncio
    └── IA
```

Depois de clicar **Postar**:
1. Modal abre com "Selecione fotos e vídeos"
2. Script chama `set_input_files()` no `<input type="file">` (não precisa clicar no botão visível)
3. Modal muda pra tela de **crop**
4. Script clica **Avançar**
5. Modal muda pra tela de **filtros**
6. Script clica **Avançar**
7. Modal muda pra tela de **caption**
8. Script preenche a textarea com o caption extraído de `caption.md`
9. Script clica **Compartilhar**
10. Espera confirmação "Sua publicação foi compartilhada"
11. Atualiza `post-status.json`

## Seletores resilientes

O Instagram atualiza classes CSS constantemente. O script usa:
- **`get_by_role("button", name=...)`** — baseado em ARIA (mais estável)
- **`get_by_text(regex)`** — baseado em texto visível em português (PT-BR) + inglês fallback
- **`get_by_label(...)`** — pros campos de input (nome + senha + caption)
- **`input[type="file"]`** — único elemento que usa CSS (é estável)

Se Instagram quebrar os seletores, só mexer em `ig_publisher.py` nas funções `open_create_post`, `click_avancar`, `fill_caption`, `click_share`.

## Tratamento de 2FA

Se você tiver 2FA ativado:

- **Primeiro login:** rode com `--headful`, digite o código manualmente quando aparecer
- **Execuções seguintes:** rodam normal (2FA só pede em logins novos)
- **Se a sessão expirar:** rerun `setup_wizard.py` em headful pra revalidar

## Rate limiting

Instagram não gosta de spam. Recomendações:

- **Máximo 3-5 posts por dia** por conta
- **Delay de ~30 min entre posts** (use `/grow ship` com schedule)
- **Varie horários** (não poste sempre 09:00 em ponto)
- **Evite auto-post 100% consecutivo** — deixa espaço pra interação manual

## Debugging

Se algo quebrar, o script:
1. Tira screenshot em `<folder>/debug-screenshot.png`
2. Printa o erro no terminal
3. Mantém browser aberto 10s pra inspeção visual (em modo headful)

Pra rodar com logs detalhados:

```bash
DEBUG=pw:api python growthOS/publisher/ig_publisher.py --folder ... --headful
```

## Comparação com Meta Graph API

| Aspecto | Playwright Web | Meta Graph API |
|---|---|---|
| Setup | username + password (2 min) | Business account + FB Page + Dev App (~15 min) |
| Custo | Grátis | Grátis (mas exige Supabase pra hospedar imagens) |
| Risco de ban | Moderado (se rodar demais) | Baixo (API oficial) |
| Schedule nativo | Manual via cron | Suportado na API |
| Dependências | Playwright + Chromium | Só `requests` + Supabase |
| Atualizações | Frágil a mudanças do site | Estável (API versionada) |

**Escolha:** Playwright ganha em simplicidade de setup, perde em robustez a mudanças do site IG.
