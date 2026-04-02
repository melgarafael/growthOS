# Guia dos MCP Servers - GrowthOS

> Documentacao completa dos tres MCP Servers que compoem a infraestrutura do GrowthOS.
> Versao: 2.0 | Ultima atualizacao: 2026-04-01

---

## Sumario

1. [O que sao MCP Servers](#1-o-que-sao-mcp-servers)
2. [mcp-social-publish](#2-mcp-social-publish)
3. [mcp-social-discover](#3-mcp-social-discover)
4. [mcp-obsidian-vault](#4-mcp-obsidian-vault)
5. [Deploy com Docker](#5-deploy-com-docker)

---

## 1. O que sao MCP Servers

### O Protocolo MCP

MCP (Model Context Protocol) e um protocolo aberto que permite a modelos de linguagem (LLMs)
interagir com servicos externos por meio de **tools** bem definidas. Cada MCP Server expoe
um conjunto de ferramentas tipadas que o agente de IA pode invocar durante uma conversa,
criando uma ponte entre o raciocinio do modelo e acoes concretas no mundo real.

O protocolo funciona da seguinte forma:

1. O MCP Server registra suas tools com nomes, parametros e descricoes
2. O LLM (ex: Claude) recebe a lista de tools disponiveis no inicio da sessao
3. Durante a conversa, o LLM decide quando invocar uma tool e com quais parametros
4. O MCP Server executa a operacao e retorna o resultado ao LLM
5. O LLM interpreta o resultado e continua a conversa

### Como o GrowthOS Utiliza MCP

O GrowthOS implementa tres MCP Servers especializados que, juntos, cobrem todo o ciclo
de marketing de conteudo:

```
+-----------------------+     +------------------------+     +----------------------+
|  mcp-social-publish   |     |  mcp-social-discover   |     |  mcp-obsidian-vault  |
|                       |     |                        |     |                      |
|  Publicacao de        |     |  Analytics, trends,    |     |  Gestao de notas,    |
|  conteudo em redes    |     |  mencoes, concorrencia |     |  calendario de       |
|  sociais              |     |  e hashtags            |     |  conteudo no Obsidian |
+-----------+-----------+     +------------+-----------+     +-----------+----------+
            |                              |                             |
            +------------------------------+-----------------------------+
                                           |
                                    shared-lib (growthOS_shared)
                                    Rate Limiting, Circuit Breaker,
                                    Token Manager, Audit Logger
```

### Fluxo Tipico de Uso

1. **Descoberta** - O agente usa `mcp-social-discover` para pesquisar tendencias,
   analisar concorrentes e identificar hashtags com melhor performance.
2. **Criacao** - Com base nos insights, o conteudo e redigido e salvo no
   `mcp-obsidian-vault` como nota com frontmatter estruturado.
3. **Publicacao** - O agente usa `mcp-social-publish` para publicar o conteudo
   na(s) plataforma(s) escolhida(s), com preview e dry-run antes da publicacao real.

### Infraestrutura Compartilhada (shared-lib)

Todos os servidores utilizam o pacote `growthOS_shared` que fornece:

| Componente | Funcao |
|------------|--------|
| **TokenManager** | Gerenciamento de rate limits por plataforma com janela deslizante |
| **RateLimits** | Configuracao de limites de requisicoes (max_requests por dia) |
| **CircuitBreaker** | Protecao contra falhas em cascata (threshold: 3 falhas, recovery: 300s) |
| **AuditLogger** | Log de auditoria em JSONL de todas as acoes executadas |

### Stack Tecnico

Todos os MCP Servers sao construidos com:

- **FastMCP** - Framework Python para criar MCP Servers
- **Python 3.11+** - Tipagem moderna com `type[T]` e `X | None`
- **python-frontmatter** - Parsing de YAML frontmatter (vault server)
- **shared-lib** - Biblioteca compartilhada para rate limiting, circuit breaking e auditoria

---

## 2. mcp-social-publish

**Servidor:** `growthos-social-publish`
**Porta:** 8001
**Caminho:** `mcp-servers/mcp-social-publish/`
**Framework:** FastMCP (Python)

### Descricao

Servidor MCP responsavel pela publicacao de conteudo em multiplas redes sociais.
Suporta modo dry-run por padrao (protecao contra publicacoes acidentais), validacao
de conteudo por plataforma, e rate limiting independente por rede.

### Plataformas Suportadas

| Plataforma | Rate Limit (req/dia) | Adapter | Descricao |
|------------|---------------------|---------|-----------|
| **LinkedIn** | 100 | `LinkedInAdapter` | Posts profissionais, artigos, carousels |
| **Twitter/X** | 300 | `TwitterAdapter` | Tweets com limite de 280 caracteres |
| **Reddit** | 100 | `RedditAdapter` | Posts de texto em subreddits |
| **GitHub** | 500 | `GitHubAdapter` | Discussions e issues em Markdown |
| **Threads** | 200 | `ThreadsAdapter` | Posts na plataforma da Meta |

### Arquitetura de Adapters

Cada plataforma implementa a interface `PlatformAdapter` (classe abstrata):

```python
class PlatformAdapter(ABC):
    async def publish(self, content: str, media_urls: list[str] | None = None) -> dict
    async def preview(self, content: str) -> str
    def validate_content(self, content: str) -> list[str]
    @property
    def platform_name(self) -> str      # Ex: "linkedin"
    @property
    def max_length(self) -> int          # Ex: 3000
```

- `publish()` - Publica o conteudo na plataforma. Retorna dict com post URL/ID.
- `preview()` - Retorna preview formatado de como o post aparecera.
- `validate_content()` - Valida contra limites da plataforma. Retorna lista de erros (vazia se valido).
- `platform_name` - Identificador unico em minusculo.
- `max_length` - Limite maximo de caracteres por post.

> **Nota:** Ate que credenciais reais sejam configuradas, os adapters operam em modo
> stub -- validacao e preview funcionam, mas `publish()` levanta `NotImplementedError`.

### Tools Disponiveis

#### 2.1 `publish_post`

Publica um post em uma plataforma de rede social.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Padrao | Descricao |
|-----------|------|-------------|--------|-----------|
| `platform` | `str` | Sim | - | Plataforma: `linkedin`, `twitter`, `reddit`, `github`, `threads` |
| `content` | `str` | Sim | - | Texto do post |
| `media_urls` | `list[str]` | Nao | `None` | Lista de URLs de midia para anexar |
| `dry_run` | `bool` | Nao | `True` | Se `True`, simula a publicacao sem postar de fato |

**Retorno (dry_run=True):**
```json
{
  "status": "dry_run",
  "platform": "linkedin",
  "preview": "...",
  "message": "Dry run - content validated but NOT published. Set dry_run=False to publish."
}
```

**Retorno (dry_run=False, sucesso):**
```json
{
  "status": "success",
  "platform": "linkedin",
  "result": { "post_url": "...", "post_id": "..." }
}
```

**Retorno (erro de validacao):**
```json
{
  "status": "error",
  "platform": "linkedin",
  "errors": ["Content exceeds maximum length of 3000 characters"]
}
```

**Retorno (rate limit excedido):**
```json
{
  "status": "error",
  "platform": "linkedin",
  "errors": ["Rate limit exceeded. Resets at 2026-04-02T00:00:00"]
}
```

**Exemplo de uso:**
```json
{
  "tool": "publish_post",
  "arguments": {
    "platform": "twitter",
    "content": "Lancamos a v2.0 do GrowthOS! Automacao inteligente para marketing de conteudo. #GrowthOS #AI",
    "dry_run": true
  }
}
```

#### 2.2 `preview_post`

Gera um preview de como o post aparecera na plataforma, sem publicar.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| `platform` | `str` | Sim | Plataforma alvo |
| `content` | `str` | Sim | Texto do post |

**Retorno:**
```json
{
  "status": "ok",
  "platform": "twitter",
  "preview": "...",
  "content_length": 95,
  "max_length": 280,
  "remaining_chars": 185
}
```

**Exemplo de uso:**
```json
{
  "tool": "preview_post",
  "arguments": {
    "platform": "linkedin",
    "content": "3 licoes que aprendi escalando um produto B2B SaaS de 0 a 10k usuarios..."
  }
}
```

#### 2.3 `list_platforms`

Lista todas as plataformas configuradas com seus status atuais.

**Parametros:** Nenhum.

**Retorno:**
```json
{
  "status": "ok",
  "count": 5,
  "platforms": {
    "linkedin": {
      "max_length": 3000,
      "rate_limit": {
        "remaining": 95,
        "limit": 100,
        "reset_at": "2026-04-02T00:00:00"
      },
      "circuit_breaker": "closed"
    },
    "twitter": { "..." },
    "reddit": { "..." },
    "github": { "..." },
    "threads": { "..." }
  }
}
```

#### 2.4 `get_rate_limits`

Consulta o status de rate limit de todas as plataformas.

**Parametros:** Nenhum.

**Retorno:**
```json
{
  "status": "ok",
  "rate_limits": {
    "linkedin": {
      "remaining": 95,
      "limit": 100,
      "reset_at": "2026-04-02T00:00:00",
      "usage_percent": 5.0
    },
    "twitter": {
      "remaining": 298,
      "limit": 300,
      "reset_at": "2026-04-02T00:00:00",
      "usage_percent": 0.7
    }
  }
}
```

### Fluxo de Seguranca

O `publish_post` passa por multiplas camadas de protecao antes de executar:

```
Requisicao de publicacao
  |
  v
1. Validacao de conteudo (adapter.validate_content)
  |-- Erros encontrados? -> Retorna lista de erros, PARA
  |
  v
2. Verificacao de rate limit (TokenManager)
  |-- Limite excedido? -> Retorna erro + horario de reset, PARA
  |-- Log de auditoria: "publish_rejected" com status "rate_limited"
  |
  v
3. dry_run=True?
  |-- Sim -> Gera preview + log "publish_dry_run" -> Retorna preview, PARA
  |
  v
4. Publicacao real via Circuit Breaker
  |-- Circuit breaker OPEN? -> Bloqueia requisicao
  |-- Sucesso -> Consome token de rate limit + log "publish" -> Retorna resultado
  |-- NotImplementedError -> Log "publish_failed" com status "not_implemented"
  |-- Outro erro -> Log "publish_failed" com status "error"
```

### Rastreabilidade

Todas as acoes sao registradas no AuditLogger com um `content_hash` (SHA-256 truncado
em 16 caracteres). Isso permite rastrear operacoes sem armazenar o conteudo original:

| Acao | Status | Quando |
|------|--------|--------|
| `publish_dry_run` | `simulated` | dry_run=True, conteudo valido |
| `publish` | `success` | Publicacao real bem-sucedida |
| `publish_rejected` | `rate_limited` | Rate limit excedido |
| `publish_failed` | `not_implemented` | Adapter sem credenciais |
| `publish_failed` | `error` | Erro generico na API |

### Autenticacao por Plataforma

| Plataforma | Variaveis de Ambiente Necessarias |
|------------|----------------------------------|
| LinkedIn | `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET`, `LINKEDIN_ACCESS_TOKEN` |
| Twitter/X | `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET` |
| Reddit | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD` |
| GitHub | `GITHUB_TOKEN` |
| Threads | `THREADS_ACCESS_TOKEN` |

---

## 3. mcp-social-discover

**Servidor:** `growthos-social-discover`
**Porta:** 8002
**Caminho:** `mcp-servers/mcp-social-discover/`
**Framework:** FastMCP (Python)

### Descricao

Servidor MCP focado em analytics, descoberta de tendencias e social listening.
Permite ao agente pesquisar mencoes de marca, analisar concorrentes, descobrir
hashtags e tendencias, e obter metricas de engajamento de multiplas plataformas.

### Plataformas Suportadas

| Plataforma | Rate Limit (req/dia) | Adapter |
|------------|---------------------|---------|
| **LinkedIn** | 200 | `LinkedInDiscoveryAdapter` |
| **Twitter/X** | 500 | `TwitterDiscoveryAdapter` |
| **Reddit** | 300 | `RedditDiscoveryAdapter` |

### Arquitetura de Adapters

Cada plataforma implementa a interface `DiscoveryAdapter` (classe abstrata):

```python
class DiscoveryAdapter(ABC):
    async def get_analytics(self, date_from: str, date_to: str) -> dict
    async def discover_trends(self, topic: str) -> dict
    async def search_mentions(self, query: str, limit: int = 50) -> dict
    async def get_competitor_activity(self, competitor: str) -> dict
    async def get_hashtag_performance(self, hashtag: str) -> dict
    @property
    def platform_name(self) -> str
```

**Metodos e seus retornos esperados:**

| Metodo | Retorna |
|--------|---------|
| `get_analytics` | `impressions`, `clicks`, `shares`, `comments`, `engagement_rate`, `top_posts` |
| `discover_trends` | `trending_hashtags`, `trending_topics`, `popular_formats`, `insights` |
| `search_mentions` | `mentions` (lista), `total_count`, `sentiment_breakdown` |
| `get_competitor_activity` | `recent_posts`, `avg_engagement`, `posting_frequency`, `top_content` |
| `get_hashtag_performance` | `reach`, `posts_count`, `engagement_rate`, `peak_hours`, `related_hashtags` |

> **Nota:** Atualmente os adapters retornam dados mock deterministicos para testes de agentes.
> Os dados mock sao identificados pelo campo `_mock: true` no retorno.

### Tools Disponiveis

#### 3.1 `get_analytics`

Obtem metricas de engajamento de uma plataforma em um periodo especifico.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| `platform` | `str` | Sim | Plataforma: `linkedin`, `twitter`, `reddit` |
| `date_from` | `str` | Sim | Data inicial no formato `YYYY-MM-DD` |
| `date_to` | `str` | Sim | Data final no formato `YYYY-MM-DD` |

**Retorno:**
```json
{
  "status": "ok",
  "data": {
    "impressions": 45200,
    "clicks": 1830,
    "shares": 420,
    "comments": 156,
    "engagement_rate": 5.3,
    "top_posts": [
      {
        "id": "post_001",
        "content_preview": "...",
        "engagement": 8.2
      }
    ]
  }
}
```

**Exemplo de uso:**
```json
{
  "tool": "get_analytics",
  "arguments": {
    "platform": "linkedin",
    "date_from": "2026-03-01",
    "date_to": "2026-03-31"
  }
}
```

#### 3.2 `discover_trends`

Descobre tendencias, hashtags em alta e formatos de conteudo populares para um topico.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Padrao | Descricao |
|-----------|------|-------------|--------|-----------|
| `topic` | `str` | Sim | - | Topico a pesquisar (ex: "AI marketing") |
| `platforms` | `list[str]` | Nao | `None` (todas) | Plataformas onde pesquisar |

**Retorno:**
```json
{
  "status": "ok",
  "topic": "AI marketing",
  "platforms": {
    "linkedin": {
      "trending_hashtags": ["#AIMarketing", "#GenAI", "#ContentAutomation"],
      "trending_topics": [
        { "topic": "AI-powered content", "volume": 12500, "growth": "+45%" }
      ],
      "popular_formats": [
        { "format": "carousel", "engagement_multiplier": 2.1 },
        { "format": "long-form article", "engagement_multiplier": 1.8 }
      ],
      "insights": [
        "Carousels com dados geram 2.1x mais engajamento",
        "Posts entre 12h-14h tem melhor alcance",
        "Hashtags especificas performam melhor que genericas"
      ]
    },
    "twitter": { "..." },
    "reddit": { "..." }
  }
}
```

**Exemplo - Pesquisar em plataformas especificas:**
```json
{
  "tool": "discover_trends",
  "arguments": {
    "topic": "automacao de marketing com IA",
    "platforms": ["linkedin", "twitter"]
  }
}
```

#### 3.3 `search_mentions`

Pesquisa mencoes de marca ou palavras-chave com analise de sentimento.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Padrao | Descricao |
|-----------|------|-------------|--------|-----------|
| `query` | `str` | Sim | - | Termo de busca (marca, palavra-chave) |
| `platforms` | `list[str]` | Nao | `None` (todas) | Plataformas onde pesquisar |
| `limit` | `int` | Nao | `50` | Maximo de mencoes por plataforma |

**Retorno:**
```json
{
  "status": "ok",
  "query": "GrowthOS",
  "total_mentions": 127,
  "platforms": {
    "linkedin": {
      "mentions": [
        {
          "id": "mention_001",
          "author": "Maria Silva",
          "content": "Estou usando o GrowthOS e os resultados sao incriveis...",
          "sentiment": "positive",
          "engagement": { "likes": 45, "comments": 12 },
          "date": "2026-03-28"
        }
      ],
      "total_count": 45,
      "sentiment_breakdown": {
        "positive": 28,
        "neutral": 13,
        "negative": 4
      }
    },
    "twitter": { "..." },
    "reddit": { "..." }
  }
}
```

**Exemplo de uso:**
```json
{
  "tool": "search_mentions",
  "arguments": {
    "query": "GrowthOS",
    "platforms": ["twitter", "reddit"],
    "limit": 25
  }
}
```

#### 3.4 `get_competitor_activity`

Analisa a atividade recente e engajamento de um concorrente nas plataformas.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Padrao | Descricao |
|-----------|------|-------------|--------|-----------|
| `competitor` | `str` | Sim | - | Nome ou handle do concorrente |
| `platforms` | `list[str]` | Nao | `None` (todas) | Plataformas onde analisar |

**Retorno:**
```json
{
  "status": "ok",
  "competitor": "CompetitorX",
  "platforms": {
    "linkedin": {
      "recent_posts": [
        {
          "date": "2026-03-30",
          "content_preview": "Announcing our new AI feature...",
          "engagement_rate": 4.5
        }
      ],
      "avg_engagement": 4.2,
      "posting_frequency": "3x/semana",
      "top_content": {
        "best_format": "carousel",
        "best_time": "10:00 AM",
        "top_hashtags": ["#AI", "#Marketing"]
      }
    },
    "twitter": { "..." },
    "reddit": { "..." }
  }
}
```

**Exemplo de uso:**
```json
{
  "tool": "get_competitor_activity",
  "arguments": {
    "competitor": "@concorrente_direto",
    "platforms": ["linkedin"]
  }
}
```

#### 3.5 `get_hashtag_performance`

Obtem metricas de alcance e engajamento de uma hashtag especifica em uma plataforma.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| `hashtag` | `str` | Sim | Hashtag a analisar (com ou sem `#`) |
| `platform` | `str` | Sim | Plataforma: `linkedin`, `twitter`, `reddit` |

**Retorno:**
```json
{
  "status": "ok",
  "data": {
    "platform": "twitter",
    "hashtag": "#AIMarketing",
    "reach": 250000,
    "posts_count": 5400,
    "engagement_rate": 3.5,
    "peak_hours": ["10:00 AM", "1:00 PM", "7:00 PM"],
    "related_hashtags": ["#ContentMarketing", "#DigitalStrategy", "#AI"],
    "trend": "rising"
  }
}
```

**Exemplo de uso:**
```json
{
  "tool": "get_hashtag_performance",
  "arguments": {
    "hashtag": "#AIMarketing",
    "platform": "twitter"
  }
}
```

### Comportamento Multi-Plataforma

As tools `discover_trends`, `search_mentions` e `get_competitor_activity` aceitam
o parametro `platforms` como lista opcional. Quando omitido (`None`), a consulta e
executada em **todas as plataformas disponiveis** automaticamente:

```
platforms=None
  |
  v
_resolve_platforms() -> ["linkedin", "reddit", "twitter"]
  |
  v
Para cada plataforma:
  1. Obter adapter via get_adapter()
  2. Verificar circuit breaker
  3. Consumir token de rate limit
  4. Executar consulta via adapter
  5. Agregar resultado no dict final
  |
  v
Registrar acao no audit log
  |
  v
Retornar resultado consolidado com dados por plataforma
```

Se uma plataforma invalida for fornecida na lista, o servidor retorna um `ValueError`
com a lista de plataformas disponiveis.

---

## 4. mcp-obsidian-vault

**Servidor:** `growthos-obsidian-vault`
**Porta:** 8003
**Caminho:** `mcp-servers/mcp-obsidian-vault/`
**Framework:** FastMCP (Python)

### Descricao

Servidor MCP que fornece operacoes CRUD completas sobre um vault Obsidian-compativel.
Permite ao agente criar, ler, atualizar, deletar, listar e pesquisar notas markdown
com suporte completo a frontmatter YAML. E o componente central para gerenciar o
calendario de conteudo, organizar ideias, rascunhos e publicacoes.

### Configuracao do Vault

O caminho do vault e definido pela variavel de ambiente `GROWTHOS_VAULT_PATH`.
Se nao definida, o padrao e `./vault/`.

```bash
# No arquivo .env
GROWTHOS_VAULT_PATH=/caminho/para/seu/obsidian-vault
```

### Estrutura de Frontmatter

Toda nota criada pelo servidor segue um schema padrao de frontmatter YAML:

```yaml
---
title: "Titulo da Nota"
date: "2026-04-01"
tags: ["marketing", "ai"]
type: "idea"
status: "draft"
platform: "linkedin"
---
Corpo da nota em Markdown aqui...
```

**Campos padrao:**

| Campo | Tipo | Padrao | Descricao |
|-------|------|--------|-----------|
| `title` | `str` | `""` | Titulo da nota |
| `date` | `str` | Data atual (UTC, `YYYY-MM-DD`) | Data de criacao |
| `tags` | `list[str]` | `[]` | Tags para organizacao e busca |
| `type` | `str` | `""` | Tipo: `idea`, `article`, `reference`, `social` |
| `status` | `str` | `""` | Status: `draft`, `review`, `scheduled`, `published` |

**Campo opcional:**

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `platform` | `str` | Plataforma alvo (incluido apenas quando fornecido) |

> O vault aceita campos adicionais arbitrarios no frontmatter --
> o Obsidian e flexivel com metadados customizados.

### Tools Disponiveis

#### 4.1 `create_note`

Cria uma nova nota markdown no vault.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Padrao | Descricao |
|-----------|------|-------------|--------|-----------|
| `path` | `str` | Sim | - | Caminho relativo no vault (ex: `ideias/ai-marketing`) |
| `title` | `str` | Sim | - | Titulo da nota (salvo no frontmatter) |
| `content` | `str` | Sim | - | Corpo da nota em Markdown |
| `tags` | `list[str]` | Nao | `None` | Tags da nota |
| `note_type` | `str` | Nao | `""` | Tipo da nota |
| `status` | `str` | Nao | `""` | Status da nota |
| `platform` | `str` | Nao | `None` | Plataforma alvo |

**Retorno (sucesso):**
```json
{
  "status": "success",
  "path": "/vault/ideias/ai-marketing.md",
  "message": "Note created: ideias/ai-marketing"
}
```

**Retorno (nota ja existe):**
```json
{
  "status": "error",
  "error": "Note already exists: ideias/ai-marketing"
}
```

> A extensao `.md` e adicionada automaticamente se nao fornecida.
> Diretorios intermediarios sao criados automaticamente.

**Exemplo - Criando uma ideia de conteudo:**
```json
{
  "tool": "create_note",
  "arguments": {
    "path": "ideias/ai-marketing-tendencias",
    "title": "Tendencias de AI Marketing para Q2 2026",
    "content": "## Principais Tendencias\n\n1. Automacao de conteudo com LLMs\n2. Personalizacao em escala\n3. Analytics preditivo",
    "tags": ["marketing", "ai", "tendencias"],
    "note_type": "idea",
    "status": "draft",
    "platform": "linkedin"
  }
}
```

#### 4.2 `read_note`

Le uma nota do vault, retornando frontmatter e conteudo separados.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| `path` | `str` | Sim | Caminho relativo (com ou sem `.md`) |

**Retorno:**
```json
{
  "status": "success",
  "frontmatter": {
    "title": "Tendencias de AI Marketing para Q2 2026",
    "date": "2026-04-01",
    "tags": ["marketing", "ai", "tendencias"],
    "type": "idea",
    "status": "draft",
    "platform": "linkedin"
  },
  "content": "## Principais Tendencias\n\n1. Automacao de conteudo com LLMs..."
}
```

#### 4.3 `update_note`

Atualiza o conteudo e/ou frontmatter de uma nota existente.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Padrao | Descricao |
|-----------|------|-------------|--------|-----------|
| `path` | `str` | Sim | - | Caminho relativo da nota |
| `content` | `str` | Nao | `None` | Novo corpo Markdown (substitui o existente) |
| `frontmatter_updates` | `dict` | Nao | `None` | Campos de frontmatter para atualizar |

**Comportamento de merge:** O `frontmatter_updates` faz **merge** com o frontmatter
existente. Apenas os campos fornecidos sao alterados; campos nao mencionados
sao preservados intactos.

**Retorno:**
```json
{
  "status": "success",
  "path": "/vault/ideias/ai-marketing-tendencias.md",
  "message": "Note updated: ideias/ai-marketing-tendencias"
}
```

**Exemplo - Atualizando status para publicado:**
```json
{
  "tool": "update_note",
  "arguments": {
    "path": "ideias/ai-marketing-tendencias",
    "frontmatter_updates": {
      "status": "published",
      "published_date": "2026-04-01",
      "post_url": "https://linkedin.com/post/12345"
    }
  }
}
```

**Exemplo - Atualizando apenas o conteudo:**
```json
{
  "tool": "update_note",
  "arguments": {
    "path": "ideias/ai-marketing-tendencias",
    "content": "## Tendencias Atualizadas\n\n1. LLMs para criacao de conteudo\n2. Agentes autonomos de marketing"
  }
}
```

#### 4.4 `delete_note`

Remove uma nota do vault permanentemente.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| `path` | `str` | Sim | Caminho relativo da nota |

**Retorno:**
```json
{
  "status": "success",
  "message": "Note deleted: ideias/nota-obsoleta"
}
```

#### 4.5 `search_notes`

Pesquisa notas por conteudo, titulo e filtros opcionais.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Padrao | Descricao |
|-----------|------|-------------|--------|-----------|
| `query` | `str` | Sim | - | Texto para buscar (substring, case-insensitive) |
| `tags` | `list[str]` | Nao | `None` | Tags para filtrar (logica OR -- match se qualquer tag presente) |
| `folder` | `str` | Nao | `None` | Pasta para restringir a busca |

**Retorno:**
```json
{
  "status": "success",
  "count": 3,
  "results": [
    {
      "path": "ideias/ai-marketing-tendencias.md",
      "frontmatter": {
        "title": "Tendencias de AI Marketing para Q2 2026",
        "tags": ["marketing", "ai", "tendencias"],
        "status": "draft"
      },
      "content_preview": "## Principais Tendencias\n\n1. Automacao de conteudo com LLMs..."
    }
  ]
}
```

**Detalhes da busca:**
- A busca e feita no titulo (frontmatter) e no corpo da nota
- O match e por substring case-insensitive (regex escapado)
- O filtro de tags usa logica OR: a nota aparece se tiver **qualquer** das tags fornecidas
- O `content_preview` retorna os primeiros 200 caracteres do conteudo
- A busca percorre recursivamente todas as subpastas da `folder` (ou vault root)

**Exemplo - Buscar rascunhos sobre marketing:**
```json
{
  "tool": "search_notes",
  "arguments": {
    "query": "marketing",
    "tags": ["draft"],
    "folder": "ideias"
  }
}
```

#### 4.6 `list_notes`

Lista todas as notas do vault ou de uma pasta especifica.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Padrao | Descricao |
|-----------|------|-------------|--------|-----------|
| `folder` | `str` | Nao | `None` | Pasta para listar (relativa ao vault root) |
| `recursive` | `bool` | Nao | `True` | Incluir notas de subpastas |

**Retorno:**
```json
{
  "status": "success",
  "count": 42,
  "notes": [
    {
      "path": "ideias/ai-marketing-tendencias.md",
      "frontmatter": { "title": "...", "date": "...", "tags": ["..."] },
      "content_preview": "Primeiros 200 caracteres..."
    }
  ]
}
```

> As notas sao retornadas em ordem alfabetica pelo caminho.

#### 4.7 `get_frontmatter`

Retorna apenas os metadados (frontmatter) de uma nota, sem o conteudo.
Util para consultas rapidas de status, tags ou tipo sem carregar o corpo completo.

**Parametros:**

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| `path` | `str` | Sim | Caminho relativo da nota |

**Retorno:**
```json
{
  "status": "success",
  "frontmatter": {
    "title": "Tendencias de AI Marketing para Q2 2026",
    "date": "2026-04-01",
    "tags": ["marketing", "ai", "tendencias"],
    "type": "idea",
    "status": "draft",
    "platform": "linkedin"
  }
}
```

### Estrutura Sugerida do Vault para Calendario de Conteudo

```
vault/
  ideias/                   # Ideias brutas e brainstorming
  rascunhos/                # Conteudo em elaboracao
    linkedin/
    twitter/
    reddit/
  agendado/                 # Conteudo aprovado e agendado para publicacao
  publicado/                # Conteudo ja publicado (com post_url no frontmatter)
    linkedin/
    twitter/
    reddit/
    github/
    threads/
  analytics/                # Relatorios e insights salvos
  concorrencia/             # Analises de concorrentes
  templates/                # Templates de conteudo por plataforma
```

**Fluxo do conteudo pelas pastas:**

```
ideias/ -> rascunhos/ -> agendado/ -> publicado/
  (draft)   (review)    (scheduled)   (published)
```

### Integracao com Obsidian Dataview

O frontmatter e compativel com o plugin Dataview do Obsidian, permitindo
criar dashboards e consultas dinamicas:

```dataview
TABLE title, platform, status, date
FROM "agendado"
WHERE status = "scheduled"
SORT date ASC
```

### Seguranca: Protecao contra Path Traversal

O servidor implementa validacao de seguranca em todos os acessos ao filesystem.
Todos os caminhos sao resolvidos dentro do vault root, e qualquer tentativa de
acessar arquivos fora do vault e bloqueada:

```
create_note(path="../../etc/passwd", ...)
-> ValueError: Path traversal detected: ../../etc/passwd
```

A validacao ocorre no metodo `_resolve()`:
1. Adiciona `.md` se a extensao estiver ausente
2. Resolve o caminho absoluto
3. Verifica se o caminho resolvido comeca com o vault root
4. Bloqueia com `ValueError` se o caminho escapar do vault

---

## 5. Deploy com Docker

### Visao Geral da Arquitetura

Os tres MCP Servers sao implantados via Docker Compose em uma rede interna
compartilhada (`growthos-network`):

```
+--------------------------------------------+
|            docker-compose                   |
|                                             |
|  +------------------+  porta 8001           |
|  | mcp-social-      | <--- Claude Code      |
|  | publish           |                      |
|  +------------------+                       |
|                                             |
|  +------------------+  porta 8002           |
|  | mcp-social-      | <--- Claude Code      |
|  | discover          |                      |
|  +------------------+                       |
|                                             |
|  +------------------+  porta 8003           |
|  | mcp-obsidian-    | <--- Claude Code      |
|  | vault             |                      |
|  +------------------+                       |
|                                             |
|  Volume: host vault <---> /vault (rw)       |
|  Network: growthos-network (bridge)         |
+--------------------------------------------+
```

### docker-compose.yml

```yaml
version: "3.9"

services:
  mcp-social-publish:
    build:
      context: .
      target: mcp-social-publish
    container_name: growthos-social-publish
    env_file: .env
    ports:
      - "8001:8001"
    networks:
      - growthos
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

  mcp-social-discover:
    build:
      context: .
      target: mcp-social-discover
    container_name: growthos-social-discover
    env_file: .env
    ports:
      - "8002:8002"
    networks:
      - growthos
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

  mcp-obsidian-vault:
    build:
      context: .
      target: mcp-obsidian-vault
    container_name: growthos-obsidian-vault
    env_file: .env
    ports:
      - "8003:8003"
    volumes:
      - ${GROWTHOS_VAULT_PATH:-./vault}:/vault:rw
    networks:
      - growthos
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

networks:
  growthos:
    driver: bridge
    name: growthos-network
```

### Mapeamento de Portas

| Servico | Container Name | Porta Host | Porta Container |
|---------|---------------|-----------|-----------------|
| mcp-social-publish | growthos-social-publish | 8001 | 8001 |
| mcp-social-discover | growthos-social-discover | 8002 | 8002 |
| mcp-obsidian-vault | growthos-obsidian-vault | 8003 | 8003 |

### Variaveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto:

```bash
# === Social Publish - Credenciais por Plataforma ===
LINKEDIN_CLIENT_ID=seu_client_id
LINKEDIN_CLIENT_SECRET=seu_client_secret
LINKEDIN_ACCESS_TOKEN=seu_access_token

TWITTER_API_KEY=sua_api_key
TWITTER_API_SECRET=seu_api_secret
TWITTER_ACCESS_TOKEN=seu_access_token
TWITTER_ACCESS_SECRET=seu_access_secret

REDDIT_CLIENT_ID=seu_client_id
REDDIT_CLIENT_SECRET=seu_client_secret
REDDIT_USERNAME=seu_username
REDDIT_PASSWORD=sua_senha

GITHUB_TOKEN=ghp_seu_token

THREADS_ACCESS_TOKEN=seu_access_token

# === Obsidian Vault ===
GROWTHOS_VAULT_PATH=/caminho/absoluto/para/obsidian-vault
```

### Comandos de Operacao

```bash
# --- Ciclo de vida ---

# Subir todos os servicos
docker compose up -d

# Subir um servico especifico
docker compose up -d mcp-social-publish

# Parar todos os servicos
docker compose down

# Reiniciar um servico
docker compose restart mcp-obsidian-vault

# --- Build ---

# Rebuild apos mudancas no codigo
docker compose build --no-cache
docker compose up -d

# Rebuild de um servico especifico
docker compose build --no-cache mcp-social-discover
docker compose up -d mcp-social-discover

# --- Logs ---

# Ver logs em tempo real (todos)
docker compose logs -f

# Ver logs de um servico especifico
docker compose logs -f mcp-social-discover

# Ver ultimas 100 linhas
docker compose logs --tail=100 mcp-social-publish
```

### Health Checks

Todos os servicos possuem health checks configurados:

| Parametro | Valor |
|-----------|-------|
| **Endpoint** | `GET /health` |
| **Intervalo** | 30 segundos |
| **Timeout** | 5 segundos |
| **Retries** | 3 tentativas antes de marcar como unhealthy |
| **Start Period** | 10 segundos (tempo para inicializacao) |

**Comandos de verificacao:**

```bash
# Status geral de todos os containers
docker compose ps

# Saude de um container especifico
docker inspect --format='{{.State.Health.Status}}' growthos-social-publish

# Historico de health checks
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' growthos-social-publish

# Testar endpoint de health manualmente
curl -f http://localhost:8001/health
curl -f http://localhost:8002/health
curl -f http://localhost:8003/health
```

### Volume do Vault

O servico `mcp-obsidian-vault` monta o diretorio do vault Obsidian como volume
com permissao de leitura e escrita (`rw`):

```yaml
volumes:
  - ${GROWTHOS_VAULT_PATH:-./vault}:/vault:rw
```

- Se `GROWTHOS_VAULT_PATH` estiver definida no `.env`, usa esse caminho
- Se nao estiver definida, usa `./vault` relativo ao docker-compose.yml
- O container ve o vault em `/vault`

### Rede Interna

Os tres servicos compartilham a rede `growthos-network` (bridge), permitindo
comunicacao interna entre containers usando os nomes dos servicos como hostname:

```
# De dentro de qualquer container:
curl http://mcp-social-publish:8001/health
curl http://mcp-social-discover:8002/health
curl http://mcp-obsidian-vault:8003/health
```

### Execucao Local (Sem Docker)

Para desenvolvimento ou debug, cada servidor pode ser executado diretamente:

```bash
# Terminal 1: Social Publish
cd mcp-servers/mcp-social-publish
python server.py

# Terminal 2: Social Discover
cd mcp-servers/mcp-social-discover
python server.py

# Terminal 3: Obsidian Vault
GROWTHOS_VAULT_PATH=/path/to/vault python mcp-servers/mcp-obsidian-vault/server.py
```

### Configuracao no Claude Code (.mcp.json)

Para usar os MCP Servers diretamente no Claude Code sem Docker:

```json
{
  "mcpServers": {
    "growthos-social-publish": {
      "command": "python",
      "args": ["mcp-servers/mcp-social-publish/server.py"],
      "env": {
        "LINKEDIN_ACCESS_TOKEN": "...",
        "TWITTER_API_KEY": "..."
      }
    },
    "growthos-social-discover": {
      "command": "python",
      "args": ["mcp-servers/mcp-social-discover/server.py"]
    },
    "growthos-obsidian-vault": {
      "command": "python",
      "args": ["mcp-servers/mcp-obsidian-vault/server.py"],
      "env": {
        "GROWTHOS_VAULT_PATH": "/path/to/vault"
      }
    }
  }
}
```

### Troubleshooting

#### Container nao inicia

```bash
# Verificar logs de erro
docker compose logs mcp-social-publish

# Verificar se a porta esta em uso
lsof -i :8001

# Verificar se o .env existe e tem conteudo
cat .env | grep -v "^#" | grep -v "^$"
```

#### Health check falhando (container unhealthy)

```bash
# Testar endpoint manualmente de fora do container
curl -f http://localhost:8001/health

# Testar de dentro do container
docker compose exec mcp-social-publish curl -f http://localhost:8001/health

# Ver historico completo de health checks
docker inspect growthos-social-publish | python3 -m json.tool | grep -A 20 "Health"
```

#### Vault nao acessivel no container

```bash
# Verificar se o volume foi montado corretamente
docker compose exec mcp-obsidian-vault ls -la /vault

# Verificar permissoes do diretorio
docker compose exec mcp-obsidian-vault stat /vault

# Verificar variavel de ambiente no container
docker compose exec mcp-obsidian-vault env | grep VAULT

# Verificar se o diretorio existe no host
ls -la ${GROWTHOS_VAULT_PATH:-./vault}
```

#### Circuit breaker aberto (erros repetidos)

Quando uma plataforma acumula 3 falhas consecutivas, o circuit breaker entra
em estado `OPEN` e bloqueia novas requisicoes por 300 segundos (5 minutos).

**Diagnostico:**
1. Verifique os logs para identificar a causa: `docker compose logs -f mcp-social-publish`
2. Causas comuns: credenciais expiradas, API fora do ar, rate limit da API externa
3. O circuit breaker transiciona automaticamente para `HALF_OPEN` apos 300s
4. Para resetar imediatamente: `docker compose restart mcp-social-publish`

#### Rate limit excedido

Os rate limits sao gerenciados pelo `TokenManager` com reset diario.

```bash
# Verificar status via tool MCP
# -> get_rate_limits() no mcp-social-publish

# Para resetar, reinicie o servico (os contadores sao em memoria)
docker compose restart mcp-social-publish
```

#### Erro "Unknown platform"

```bash
# Verificar plataformas disponiveis
# -> list_platforms() no mcp-social-publish
# Plataformas validas (publish): linkedin, twitter, reddit, github, threads
# Plataformas validas (discover): linkedin, twitter, reddit
```

---

## Referencia Rapida

### Todas as Tools por Servidor

| Servidor | Tool | Descricao |
|----------|------|-----------|
| **publish** | `publish_post` | Publica ou simula publicacao em rede social |
| **publish** | `preview_post` | Preview do post sem publicar |
| **publish** | `list_platforms` | Lista plataformas e seus status |
| **publish** | `get_rate_limits` | Status de rate limits por plataforma |
| **discover** | `get_analytics` | Metricas de engajamento por periodo |
| **discover** | `discover_trends` | Tendencias, hashtags em alta e formatos populares |
| **discover** | `search_mentions` | Mencoes de marca com analise de sentimento |
| **discover** | `get_competitor_activity` | Atividade recente de concorrentes |
| **discover** | `get_hashtag_performance` | Performance de hashtags especificas |
| **vault** | `create_note` | Criar nova nota no vault |
| **vault** | `read_note` | Ler nota (frontmatter + conteudo) |
| **vault** | `update_note` | Atualizar conteudo e/ou frontmatter |
| **vault** | `delete_note` | Deletar nota do vault |
| **vault** | `search_notes` | Buscar notas por texto, tags e pasta |
| **vault** | `list_notes` | Listar notas do vault ou pasta |
| **vault** | `get_frontmatter` | Obter apenas metadados de uma nota |

### Portas e Endpoints

| Servidor | Porta | Health Check | Container Name |
|----------|-------|-------------|----------------|
| mcp-social-publish | 8001 | `http://localhost:8001/health` | growthos-social-publish |
| mcp-social-discover | 8002 | `http://localhost:8002/health` | growthos-social-discover |
| mcp-obsidian-vault | 8003 | `http://localhost:8003/health` | growthos-obsidian-vault |

---

*Guia de MCP Servers -- GrowthOS v2.0*
