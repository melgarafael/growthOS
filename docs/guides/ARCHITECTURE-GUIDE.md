# GrowthOS -- Guia de Arquitetura

Referencia tecnica completa da arquitetura do GrowthOS, o plugin de marketing autonomo para Claude Code.

**Versao:** 1.0.0
**Ultima atualizacao:** 2026-04-01

---

## Sumario

1. [Visao Geral do Sistema](#1-visao-geral-do-sistema)
2. [Diagrama de Arquitetura](#2-diagrama-de-arquitetura)
3. [Camadas do Sistema](#3-camadas-do-sistema)
4. [Fluxo de Dados](#4-fluxo-de-dados)
5. [Arquitetura da Shared Library](#5-arquitetura-da-shared-library)
6. [Sistema de Templates](#6-sistema-de-templates)
7. [Decisoes de Design](#7-decisoes-de-design)

---

## 1. Visao Geral do Sistema

### O que e o GrowthOS

GrowthOS e um plugin para Claude Code que implementa uma equipe de marketing autonoma
composta por 7 agentes de IA, 9 skills especializadas, 3 servidores MCP e um unico
ponto de entrada: o comando `/grow`.

O sistema transforma o Claude Code em um departamento de marketing completo, capaz de
criar conteudo, publicar em redes sociais, analisar concorrentes, gerar landing pages,
produzir scripts de video e orquestrar campanhas -- tudo a partir de linguagem natural.

### Numeros do Sistema

| Componente         | Quantidade | Descricao                                   |
|--------------------|------------|---------------------------------------------|
| Agentes            | 7          | CMO + 6 especialistas de dominio            |
| Skills             | 9          | Capacidades especializadas de marketing     |
| Servidores MCP     | 3          | social-publish, social-discover, obsidian-vault |
| Hooks              | 4          | audit-logger, circuit-breaker, preview-before-publish, dry-run-guard |
| Comandos           | 1          | `/grow` (com subcomandos e linguagem natural) |
| Templates          | 3 categorias | landing-pages, reports, content             |

### Principios de Design

1. **Comando unico como ponto de entrada** -- O usuario interage apenas com `/grow`.
   O CMO classifica a intencao e roteia para o agente correto. Nao ha necessidade de
   memorizar multiplos comandos.

2. **Seguranca por padrao (Safety-first)** -- O sistema opera em modo dry-run por
   padrao. Toda publicacao real exige preview e confirmacao. Um kill switch global
   pode interromper qualquer operacao a qualquer momento.

3. **Brand voice como lei** -- O arquivo `brand-voice.yaml` e a configuracao central.
   Tom, frases proibidas (anti-slop), plataformas habilitadas e nivel de autonomia sao
   todos derivados deste unico arquivo.

4. **Pipelines composiveis** -- Agentes podem ser encadeados automaticamente.
   "Escreva um post e publique no LinkedIn" aciona content-creator seguido de
   social-publisher, com passagem de artefatos entre estagios.

5. **Contratos de saida explicitos** -- Cada skill tem um output contract definido
   em `docs/output-contracts.md`. Isso garante que a saida de um agente seja
   consumivel pelo proximo agente no pipeline.

6. **Resiliencia via hooks** -- Circuit breaker, audit trail e dry-run guard operam
   como interceptadores transparentes, sem que os agentes precisem implementar
   logica de protecao.

---

## 2. Diagrama de Arquitetura

### Visao Macro

```
                          +------------------+
                          |    USUARIO        |
                          +--------+---------+
                                   |
                                   | /grow <intencao>
                                   v
                    +------------------------------+
                    |   COMMAND INTERFACE           |
                    |   commands/grow/COMMAND.md    |
                    |                              |
                    |  1. First-run detection       |
                    |  2. Parse argumentos           |
                    |  3. Load brand-voice.yaml     |
                    +-------------+----------------+
                                  |
                                  v
                    +------------------------------+
                    |   CMO (ROUTER)               |
                    |   agents/cmo/router.md       |
                    |                              |
                    |  - Classifica intencao        |
                    |  - Detecta pipelines          |
                    |  - Desambigua contexto        |
                    +------+----------+------------+
                           |          |
              single agent |          | pipeline (multi-agent)
                           v          v
        +------------------------------------------+
        |        AGENT ORCHESTRATION LAYER          |
        |                                           |
        |  +------------------+  +----------------+ |
        |  | growth-strategist|  | content-creator| |
        |  +------------------+  +----------------+ |
        |  +------------------+  +----------------+ |
        |  | intelligence-    |  | visual-designer| |
        |  | analyst          |  +----------------+ |
        |  +------------------+  +----------------+ |
        |  +------------------+  | growth-engineer| |
        |  | social-publisher |  +----------------+ |
        |  +------------------+                     |
        +-----+------------------+-----------------+
              |                  |
              v                  v
    +-------------------+  +-------------------+
    |  DOMAIN SKILLS    |  |  SHARED LIBRARY   |
    |  (9 skills)       |  |  growthOS_shared/  |
    |                   |  |                   |
    | marketing-strategy|  | - config          |
    | copywriting       |  | - intent_router   |
    | seo-growth        |  | - autonomy        |
    | content-creation  |  | - token_manager   |
    | social-media-mgmt |  | - circuit_breaker |
    | competitive-intel |  | - audit_logger    |
    | video-production  |  | - html_generator  |
    | landing-page-design| | - scheduler       |
    | platform-mastery  |  +-------------------+
    +--------+----------+
             |
             v
    +------------------------------------------+
    |   HOOKS (INTERCEPTACAO)                   |
    |                                           |
    |  PreToolUse:                              |
    |    - dry-run-guard (simula se dry_run)    |
    |    - preview-before-publish (confirma)    |
    |                                           |
    |  PostToolUse:                             |
    |    - audit-logger (JSONL trail)           |
    |    - circuit-breaker (protecao falhas)    |
    +---------------------+--------------------+
                          |
                          v
    +------------------------------------------+
    |   MCP SERVERS (INTEGRACAO EXTERNA)        |
    |                                           |
    |  +----------------+  +-----------------+  |
    |  | social-publish |  | social-discover |  |
    |  | (Twitter, LI,  |  | (analytics,     |  |
    |  |  Reddit, etc.) |  |  trends, dados) |  |
    |  +----------------+  +-----------------+  |
    |  +------------------+                     |
    |  | obsidian-vault   |                     |
    |  | (knowledge base) |                     |
    |  +------------------+                     |
    +---------------------+--------------------+
                          |
                          v
    +------------------------------------------+
    |   APIs EXTERNAS                           |
    |                                           |
    |  Twitter/X API  |  LinkedIn API           |
    |  Reddit API     |  YouTube API            |
    |  Instagram API  |  Threads API            |
    |  GitHub API     |  Obsidian Vault (local) |
    +------------------------------------------+
```

### Fluxo de Interceptacao dos Hooks

```
  Agente chama MCP tool
        |
        v
  +-- PreToolUse hooks --+
  |                      |
  | dry-run-guard:       |
  |   dry_run ativo?     |
  |   SIM -> simula,     |
  |          retorna fake |
  |   NAO -> passa        |
  |                      |
  | preview-before-       |
  | publish:             |
  |   e publish_post?    |
  |   SIM -> mostra       |
  |     preview, pede    |
  |     confirmacao       |
  |   NAO -> passa        |
  +----------+-----------+
             |
             v
     MCP Tool executa
             |
             v
  +-- PostToolUse hooks -+
  |                      |
  | audit-logger:        |
  |   loga em JSONL      |
  |   redacta secrets    |
  |                      |
  | circuit-breaker:     |
  |   sucesso? reset     |
  |   falha? incrementa  |
  |   3 falhas? abre     |
  |     circuito         |
  +----------------------+
```

---

## 3. Camadas do Sistema

### Camada 1: Command Interface

**Localizacao:** `commands/grow/COMMAND.md`

A camada de entrada do sistema. O comando `/grow` e o unico ponto de interacao
do usuario com o GrowthOS.

**Responsabilidades:**

- **First-run detection** -- Verifica se `brand-voice.yaml` existe. Se nao existir,
  exibe mensagem de boas-vindas e direciona para `/grow setup`.
- **Parse de argumentos** -- Aceita linguagem natural ou subcomandos explicitos
  (strategy, create, publish, analyze, research, report, setup).
- **Carga de configuracao** -- Le `brand-voice.yaml` do diretorio do projeto ou
  do caminho definido em `GROWTHOS_CONFIG_DIR`.
- **Exibicao de ajuda** -- Quando invocado sem argumentos, mostra o menu de
  capacidades disponiveis.

**Subcomandos suportados:**

| Subcomando | Descricao                                      |
|------------|-------------------------------------------------|
| `strategy` | Planejamento estrategico, OKRs, calendarios     |
| `create`   | Criacao de conteudo (blog, newsletter, posts)   |
| `publish`  | Publicacao e agendamento em plataformas          |
| `analyze`  | Analise competitiva, SWOT, benchmarks           |
| `research` | Pesquisa profunda, exploracao de topicos         |
| `report`   | Relatorios de performance, metricas, KPIs       |
| `setup`    | Configuracao inicial do brand voice             |

### Camada 2: Agent Orchestration

**Localizacao:** `agents/`

O CMO (Chief Marketing Officer) e o orquestrador central. Ele nao cria conteudo,
nao publica posts e nao analisa dados. Sua unica funcao e classificar a intencao
do usuario e delegar para o agente especialista correto.

**Registro de Agentes:**

| Agente              | Dominio                        | Skills Primarias                              |
|---------------------|--------------------------------|-----------------------------------------------|
| `cmo`               | Orquestracao, roteamento       | Todas (via delegacao)                         |
| `growth-strategist` | Estrategia, OKRs, planejamento | marketing-strategy                            |
| `content-creator`   | Escrita, geracao de conteudo   | copywriting, content-creation, seo-growth     |
| `intelligence-analyst` | Pesquisa, analise, relatorios | competitive-intelligence                     |
| `visual-designer`   | Graficos, assets visuais       | video-production                              |
| `social-publisher`  | Publicacao, distribuicao       | social-media-management, platform-mastery     |
| `growth-engineer`   | Landing pages, CRO, analytics  | landing-page-design                           |

**Classificacao de intencao:**

O CMO usa um mapa de triggers (palavras-chave) para classificar a intencao:

- Verbos como "write", "create", "draft" -> `content-creator`
- Verbos como "publish", "post", "share" -> `social-publisher`
- Verbos como "analyze", "compare" -> `intelligence-analyst`
- Verbos como "plan", "strategy" -> `growth-strategist`
- Mencoes a "design", "visual", "image" -> `visual-designer`
- Mencoes a "landing page", "conversion" -> `growth-engineer`

**Pipelines compostos:**

O CMO detecta intencoes compostas e orquestra pipelines multi-agente:

| Pipeline                | Sequencia                                         |
|-------------------------|---------------------------------------------------|
| `create-and-publish`    | content-creator -> social-publisher               |
| `create-and-design`     | content-creator -> visual-designer                |
| `research-and-create`   | intelligence-analyst -> content-creator            |
| `strategy-to-content`   | growth-strategist -> content-creator              |
| `full-publish-pipeline` | content-creator -> visual-designer -> social-publisher |

**Regras de execucao de pipelines:**

1. Execucao sequencial -- cada agente completa antes do proximo iniciar
2. Forwarding de output -- a saida do agente anterior e a entrada do proximo
3. Checkpoints de usuario -- o usuario pode revisar/editar entre estagios
4. Fail-fast -- se qualquer estagio falha, o pipeline para e reporta
5. Completude parcial -- estagios completados sao preservados mesmo se os seguintes falharem

### Camada 3: Domain Skills

**Localizacao:** `skills/`

As 9 skills representam capacidades especializadas de marketing. Cada skill define
conhecimento de dominio, padroes de execucao e contratos de saida.

| Skill                      | Outputs Principais                           |
|----------------------------|----------------------------------------------|
| `marketing-strategy`       | Plano de marketing, campaign brief           |
| `copywriting`              | Headlines, email sequences, ad copy          |
| `seo-growth`               | Keyword research, SEO audit                  |
| `content-creation`         | Blog posts, newsletters, content calendars   |
| `social-media-management`  | Social posts, posting schedules              |
| `competitive-intelligence` | Competitor reports, SWOT analysis            |
| `video-production`         | Scripts, thumbnails, storyboards, descricoes |
| `landing-page-design`      | Landing pages HTML, A/B tests, tracking, CRO |
| `platform-mastery`         | Platform briefs, cross-platform plans        |

Cada output segue um contrato definido em `docs/output-contracts.md`. Isso garante
consistencia e interoperabilidade entre agentes no pipeline.

### Camada 4: External Integration

**Localizacao:** `mcp-servers/`

Tres servidores MCP fornecem a ponte entre o GrowthOS e o mundo externo:

| Servidor MCP        | Funcao                                        | APIs que abstrai                    |
|---------------------|-----------------------------------------------|-------------------------------------|
| `mcp-social-publish`| Publicacao real em plataformas sociais         | Twitter, LinkedIn, Reddit, Threads, Instagram, YouTube, GitHub |
| `mcp-social-discover`| Coleta de dados, analytics, tendencias        | APIs de descoberta e metricas       |
| `mcp-obsidian-vault`| Leitura/escrita no knowledge base local       | Obsidian vault (filesystem)         |

Os servidores MCP sao os unicos componentes que fazem chamadas reais a APIs externas.
Toda outra camada opera com dados em memoria ou artefatos locais.

### Camada 5: Safety & Compliance

**Localizacao:** `hooks/`

Quatro hooks implementam a camada de seguranca como interceptadores transparentes:

**PreToolUse (executam ANTES da chamada MCP):**

| Hook                    | Tipo       | Funcao                                          |
|-------------------------|------------|--------------------------------------------------|
| `dry-run-guard`         | PreToolUse | Intercepta TODAS as chamadas MCP quando dry-run esta ativo. Simula a execucao e retorna resultado sintetico sem fazer chamadas reais. |
| `preview-before-publish`| PreToolUse | Intercepta chamadas `publish_post`. Mostra preview formatado do conteudo e exige confirmacao do usuario conforme o nivel de autonomia. |

**PostToolUse (executam DEPOIS da chamada MCP):**

| Hook                | Tipo        | Funcao                                            |
|---------------------|-------------|---------------------------------------------------|
| `audit-logger`      | PostToolUse | Loga toda chamada MCP em trail JSONL append-only. Redacta campos sensiveis (*_token, *_secret, *_key, authorization, cookie). |
| `circuit-breaker`   | PostToolUse | Rastreia falhas por servidor MCP. Abre o circuito apos 3 falhas consecutivas. Reabre apos 60s em modo half-open. |

**Maquina de estados do Circuit Breaker:**

```
CLOSED ----(3 falhas consecutivas)----> OPEN
OPEN   ----(apos 60s timeout)---------> HALF_OPEN
HALF_OPEN -(1 sucesso)----------------> CLOSED
HALF_OPEN -(1 falha)------------------> OPEN
```

### Camada 6: Infrastructure

**Localizacao:** `shared-lib/`, `templates/`, `brand-voice.yaml`, `docker-compose.yml`

Componentes de infraestrutura que suportam todas as camadas superiores:

| Componente           | Descricao                                         |
|----------------------|---------------------------------------------------|
| `shared-lib/`        | Biblioteca Python compartilhada (8 modulos)       |
| `templates/`         | Templates HTML, Markdown e YAML                   |
| `brand-voice.yaml`   | Configuracao central de marca e autonomia         |
| `vault/`             | Diretorio do knowledge base Obsidian              |
| `docker-compose.yml` | Orquestracao de containers para MCP servers       |
| `Dockerfile`         | Build do ambiente de execucao                     |

---

## 4. Fluxo de Dados

### Cenario: `/grow create um blog post sobre IA em saude`

Este cenario demonstra o fluxo completo de uma requisicao de criacao de conteudo.

```
Passo 1: COMMAND INTERFACE
+----------------------------------------------------------+
| /grow create um blog post sobre IA em saude               |
|                                                           |
| 1. First-run: brand-voice.yaml existe? SIM -> continua   |
| 2. Parse: argumento = "create um blog post sobre IA..."  |
| 3. Load config: carrega brand-voice.yaml                 |
| 4. Delega para CMO                                        |
+----------------------------------------------------------+
          |
          v
Passo 2: CMO ROUTER
+----------------------------------------------------------+
| Intent classification:                                    |
|   - Verbo "create" detectado                              |
|   - Matches: create intent (triggers: write, create,      |
|     draft, blog, article...)                              |
|   - Nao e pipeline composto (sem "and publish")           |
|   - Confianca > 60% -> roteamento direto                 |
|                                                           |
| Resultado: delega para content-creator                    |
+----------------------------------------------------------+
          |
          v
Passo 3: CONTENT-CREATOR AGENT
+----------------------------------------------------------+
| Ativacao com skills: copywriting, content-creation,       |
|                      seo-growth                           |
|                                                           |
| 1. Le brand-voice.yaml para tom e restricoes              |
| 2. Aplica anti-slop (filtra frases banidas)               |
| 3. Gera blog post seguindo output contract:               |
|    - Frontmatter (title, slug, meta_description, etc.)    |
|    - Introducao (hook + tese)                             |
|    - Corpo (H2/H3 sections)                               |
|    - Conclusao (resumo + CTA)                             |
|    - 800-2500 palavras                                    |
|                                                           |
| 4. Salva artefato em content/                             |
+----------------------------------------------------------+
          |
          v
Passo 4: OUTPUT
+----------------------------------------------------------+
| Artefato: blog-post-ia-saude.md                           |
| Formato: Markdown com frontmatter YAML                    |
| Contrato: content-creation/blog-post                      |
| Localizacao: content/                                     |
+----------------------------------------------------------+
```

### Cenario: `/grow create um post sobre nosso lancamento e publique no LinkedIn`

Este cenario demonstra um pipeline composto (create-and-publish) com interceptacao
de hooks.

```
Passo 1: COMMAND INTERFACE
+----------------------------------------------------------+
| /grow create um post sobre nosso lancamento e publique    |
|      no LinkedIn                                          |
|                                                           |
| Parse e delega para CMO                                   |
+----------------------------------------------------------+
          |
          v
Passo 2: CMO ROUTER
+----------------------------------------------------------+
| Intent classification:                                    |
|   - Verbo "create" + "publique" detectados                |
|   - Pattern match: "create .* (for|on) LinkedIn"          |
|   - Pipeline identificado: create-and-publish             |
|                                                           |
| Resultado: pipeline sequencial de 2 estagios              |
+----------------------------------------------------------+
          |
          v
Passo 3: PIPELINE ESTAGIO 1 -- CONTENT-CREATOR
+----------------------------------------------------------+
| [1/2] Content Creator                                     |
|                                                           |
| 1. Le brand-voice.yaml                                    |
| 2. Gera post otimizado para LinkedIn                      |
|    (consulta platform-mastery para best practices)        |
| 3. Aplica anti-slop e tom da marca                        |
| 4. Gera artefato: social-post-lancamento.md               |
|                                                           |
| Output: content_artifact (texto do post + metadata)       |
+----------------------------------------------------------+
          |
          | content_artifact passado como input
          v
Passo 3.5: CHECKPOINT DE USUARIO
+----------------------------------------------------------+
| "Aqui esta o post gerado. Deseja revisar antes de         |
|  publicar?"                                               |
|                                                           |
| [Usuario revisa e aprova ou edita]                        |
+----------------------------------------------------------+
          |
          v
Passo 4: PIPELINE ESTAGIO 2 -- SOCIAL-PUBLISHER
+----------------------------------------------------------+
| [2/2] Social Publisher                                    |
|                                                           |
| 1. Recebe content_artifact                                |
| 2. Adapta para LinkedIn (max 3000 chars, hashtags)        |
| 3. Chama MCP: social-publish -> publish_post              |
+----------------------------------------------------------+
          |
          v
Passo 5: HOOK -- DRY-RUN-GUARD (PreToolUse)
+----------------------------------------------------------+
| Intercepta: mcp__growthOS-social-publish__publish_post    |
|                                                           |
| dry_run_default = true em brand-voice.yaml?               |
|   SIM -> Simula publicacao, retorna resultado sintetico   |
|          "[DRY RUN] Post seria publicado no LinkedIn"     |
|          Nenhuma chamada real feita.                       |
|   NAO -> Passa para proximo hook                          |
+----------------------------------------------------------+
          |
          v (se dry_run = false)
Passo 6: HOOK -- PREVIEW-BEFORE-PUBLISH (PreToolUse)
+----------------------------------------------------------+
| Intercepta: publish_post                                  |
|                                                           |
| Autonomy level = "semi"?                                  |
|   - Mostra preview formatado do post                      |
|   - Solicita confirmacao: "Publicar no LinkedIn? [S/N]"   |
|                                                           |
| Autonomy level = "manual"?                                |
|   - Sempre pede confirmacao                               |
|                                                           |
| Autonomy level = "auto"?                                  |
|   - Publica sem pedir confirmacao                         |
+----------------------------------------------------------+
          |
          v (se confirmado)
Passo 7: MCP SERVER -- SOCIAL-PUBLISH
+----------------------------------------------------------+
| Executa chamada real a LinkedIn API                       |
| Publica o post na conta configurada                       |
| Retorna: post_id, url, status                             |
+----------------------------------------------------------+
          |
          v
Passo 8: HOOK -- AUDIT-LOGGER (PostToolUse)
+----------------------------------------------------------+
| Loga em JSONL:                                            |
|   {                                                       |
|     "action": "social_publish__publish_post",             |
|     "platform": "social_publish",                         |
|     "content_hash": "sha256:a1b2c3...",                   |
|     "status": "success",                                  |
|     "duration_ms": 1247,                                  |
|     "timestamp": "2026-04-01T10:30:00Z"                   |
|   }                                                       |
|                                                           |
| Campos sensiveis redactados: [REDACTED]                   |
+----------------------------------------------------------+
          |
          v
Passo 9: HOOK -- CIRCUIT-BREAKER (PostToolUse)
+----------------------------------------------------------+
| Resultado: sucesso                                        |
| Breaker key: "social_publish"                             |
| Estado: CLOSED (reseta contador de falhas)                |
+----------------------------------------------------------+
          |
          v
Passo 10: RESPOSTA AO USUARIO
+----------------------------------------------------------+
| Pipeline: Create and Publish                              |
|                                                           |
| [1/2] Content Creator -- Post gerado (312 palavras)      |
| [2/2] Social Publisher -- Publicado no LinkedIn           |
|                                                           |
| URL: https://linkedin.com/posts/...                       |
+----------------------------------------------------------+
```

---

## 5. Arquitetura da Shared Library

**Localizacao:** `shared-lib/growthOS_shared/`
**Versao:** 1.0.0

A shared library e uma biblioteca Python que encapsula toda a logica reutilizavel
do GrowthOS. Os 8 modulos sao consumidos por hooks, agentes e servidores MCP.

### 5.1 config

**Arquivo:** `config.py`
**Proposito:** Carga e validacao da configuracao central do GrowthOS.

**Classes e funcoes principais:**

| Simbolo            | Tipo     | Descricao                                    |
|--------------------|----------|----------------------------------------------|
| `BrandVoiceConfig` | Classe   | Modelo Pydantic que valida brand-voice.yaml. Contem brand, platforms, anti_slop e autonomy. |
| `load_brand_voice` | Funcao   | Carrega e parseia brand-voice.yaml do diretorio do projeto ou de GROWTHOS_CONFIG_DIR. |

**Integracao:** Consumido por todos os agentes e hooks para obter configuracao de
marca, tom, plataformas habilitadas e nivel de autonomia.

### 5.2 intent_router

**Arquivo:** `intent_router.py`
**Proposito:** Classificacao de intencao e roteamento para agentes.

| Simbolo             | Tipo     | Descricao                                   |
|---------------------|----------|---------------------------------------------|
| `Intent`            | Enum     | Intencoes possiveis: strategy, create, publish, analyze, research, report, visual, landing |
| `RouteResult`       | Classe   | Resultado do roteamento: agente alvo, intencao classificada, confianca |
| `SubcommandResult`  | Classe   | Resultado de parse de subcomando explicito   |
| `check_first_run`   | Funcao   | Verifica se brand-voice.yaml existe (first-run detection) |
| `classify_intent`   | Funcao   | Classifica intencao a partir de texto em linguagem natural |
| `parse_subcommand`  | Funcao   | Parseia subcomandos explicitos (strategy, create, etc.) |
| `route`             | Funcao   | Funcao principal: combina parse + classificacao + roteamento |

**Integracao:** Consumido pelo COMMAND.md e pelo CMO router para determinar qual
agente deve atender a requisicao.

### 5.3 autonomy

**Arquivo:** `autonomy.py`
**Proposito:** Gerenciamento de niveis de autonomia e kill switch.

| Simbolo                | Tipo      | Descricao                                  |
|------------------------|-----------|--------------------------------------------|
| `AutonomyLevel`        | Enum      | Niveis: `manual`, `semi`, `auto`           |
| `ActionType`           | Enum      | Tipos de acao que requerem aprovacao        |
| `AutonomyManager`      | Classe    | Gerenciador que decide se uma acao requer confirmacao baseado no nivel de autonomia |
| `KillSwitchActiveError`| Excecao   | Lancada quando o kill switch esta ativo e uma operacao e tentada |

**Integracao:** Consumido pelo hook `preview-before-publish` e pelos agentes para
verificar se uma acao pode ser executada automaticamente ou requer confirmacao.

### 5.4 token_manager

**Arquivo:** `token_manager.py`
**Proposito:** Gerenciamento de rate limits por plataforma.

| Simbolo             | Tipo      | Descricao                                    |
|---------------------|-----------|----------------------------------------------|
| `TokenManager`      | Classe    | Rastreia uso de API por plataforma, gerencia janelas de rate limit |
| `RateLimits`        | Classe    | Definicao de limites por plataforma (requests/minuto, requests/dia) |
| `RateLimitExceeded` | Excecao   | Lancada quando o limite de uma plataforma e atingido |
| `PlatformStatus`    | Classe    | Estado atual de uso de uma plataforma (calls restantes, reset time) |

**Integracao:** Consumido pelos servidores MCP antes de fazer chamadas a APIs externas
para garantir que rate limits nao sejam excedidos.

### 5.5 circuit_breaker

**Arquivo:** `circuit_breaker.py`
**Proposito:** Implementacao do padrao Circuit Breaker para protecao contra falhas cascata.

| Simbolo            | Tipo      | Descricao                                     |
|--------------------|-----------|-----------------------------------------------|
| `CircuitBreaker`   | Classe    | Maquina de estados (CLOSED/OPEN/HALF_OPEN) por servico MCP |
| `CircuitState`     | Enum      | Estados possiveis do circuito                 |
| `CircuitOpenError` | Excecao   | Lancada quando uma chamada e feita com circuito aberto |

**Integracao:** Consumido pelo hook `circuit-breaker` que intercepta todas as chamadas
MCP e rastreia falhas por servidor.

### 5.6 audit_logger

**Arquivo:** `audit_logger.py`
**Proposito:** Logging de auditoria append-only em formato JSONL.

| Simbolo       | Tipo    | Descricao                                         |
|---------------|---------|---------------------------------------------------|
| `AuditLogger` | Classe  | Gerenciador do trail de auditoria. Escreve entradas em arquivo JSONL. Redacta campos sensiveis automaticamente. |
| `AuditEntry`  | Classe  | Modelo de uma entrada de log (action, platform, content_hash, status, duration_ms, timestamp) |

**Integracao:** Consumido pelo hook `audit-logger` apos cada chamada MCP.

### 5.7 html_generator

**Arquivo:** `html_generator.py`
**Proposito:** Geracao de landing pages HTML single-file a partir de templates.

| Simbolo                  | Tipo    | Descricao                                  |
|--------------------------|---------|--------------------------------------------|
| `generate_landing_page`  | Funcao  | Gera HTML completo a partir de parametros e estilo escolhido |
| `list_available_styles`  | Funcao  | Lista estilos disponiveis (bold, gradient, minimal) |

**Integracao:** Consumido pelo agente `growth-engineer` e pela skill `landing-page-design`.

### 5.8 scheduler

**Arquivo:** `scheduler.py`
**Proposito:** Agendamento de publicacoes e geracao de cron jobs.

| Simbolo               | Tipo    | Descricao                                     |
|------------------------|---------|-----------------------------------------------|
| `CalendarEntry`        | Classe  | Entrada individual do calendario de conteudo  |
| `ContentStatus`        | Enum    | Status: planned, drafted, scheduled, published |
| `ScheduleConfig`       | Classe  | Configuracao de agendamento                   |
| `ScheduleDefinition`   | Classe  | Definicao de horarios por plataforma          |
| `ScheduledPublisher`   | Classe  | Executor de publicacoes agendadas             |
| `PublishResult`        | Classe  | Resultado de uma publicacao (sucesso/falha)   |
| `RetryConfig`          | Classe  | Configuracao de retry com backoff exponencial |
| `load_schedule_config` | Funcao  | Carrega configuracao de agendamento           |
| `prepare_cron_jobs`    | Funcao  | Gera cron jobs a partir do calendario         |
| `retry_with_backoff`   | Funcao  | Executa funcao com retry e backoff exponencial |

**Integracao:** Consumido pelo agente `social-publisher` para agendar publicacoes
futuras via CronCreate ou similares.

### Diagrama de Dependencias entre Modulos

```
intent_router -----> config
autonomy ----------> config
audit_logger ------> (standalone)
circuit_breaker ---> (standalone)
token_manager -----> config (para rate limits por plataforma)
html_generator ----> (standalone, le templates/)
scheduler ---------> config, token_manager
```

---

## 6. Sistema de Templates

**Localizacao:** `templates/`

O sistema de templates fornece estruturas pre-definidas para os principais tipos de
output do GrowthOS.

### 6.1 Landing Pages

**Localizacao:** `templates/landing-pages/`

Tres estilos de landing page em HTML single-file:

| Template       | Descricao                                              |
|----------------|--------------------------------------------------------|
| `bold.html`    | Design arrojado com cores fortes e tipografia impactante |
| `gradient.html`| Design com gradientes suaves e efeito visual moderno   |
| `minimal.html` | Design limpo e minimalista, foco no conteudo           |

**Contrato de landing page:**

Toda landing page gerada deve cumprir:

- Arquivo unico HTML (sem dependencias externas)
- CSS embutido (embedded)
- Stack de fontes do sistema (sem Google Fonts)
- Tamanho maximo: 100KB
- Sem JavaScript (exceto se estritamente necessario)
- Responsivo
- Acessivel (WCAG 2.1 AA)
- Secoes obrigatorias: meta tags (SEO + Open Graph), hero section (headline + CTA
  above the fold), social proof, features/benefits, CTA repetido, footer
- Elementos obrigatorios: skip link, HTML semantico, alt text em todos os visuais,
  focus states, atributo lang

### 6.2 Reports

**Localizacao:** `templates/reports/`

Templates para relatorios de analise e otimizacao:

| Template                       | Descricao                                     |
|--------------------------------|-----------------------------------------------|
| `ab-test-template.md`         | Plano de teste A/B com hipotese, variantes, metricas, split de trafego e criterios de sucesso |
| `cro-report-template.md`      | Relatorio de CRO com analise de funil, drop-offs, causas identificadas e recomendacoes com ICE score |
| `tracking-plan-template.md`   | Plano de tracking com eventos, propriedades, KPIs e snippets de implementacao (GA4, Plausible, Umami) |

### 6.3 Content

**Localizacao:** `templates/content/`

| Template                          | Descricao                                   |
|-----------------------------------|---------------------------------------------|
| `content-calendar-template.md`   | Modelo de calendario editorial com periodos, entradas por data/plataforma, temas semanais |

### Relacao Templates <-> Skills <-> Agentes

```
growth-engineer ----> landing-page-design ----> templates/landing-pages/
                 \--> landing-page-design ----> templates/reports/ab-test-template.md
                 \--> landing-page-design ----> templates/reports/cro-report-template.md
                 \--> landing-page-design ----> templates/reports/tracking-plan-template.md

growth-strategist --> marketing-strategy ----> templates/content/content-calendar-template.md
content-creator ---> content-creation -------> templates/content/content-calendar-template.md
```

---

## 7. Decisoes de Design

### 7.1 Por que HTML single-file para landing pages?

**Decisao:** Landing pages sao geradas como um unico arquivo HTML com CSS embutido,
sem dependencias externas, sem JavaScript (quando possivel), usando fontes do sistema.

**Justificativas:**

- **Portabilidade** -- Um arquivo unico pode ser aberto em qualquer browser, enviado
  por email, hospedado em qualquer servidor estatico (Netlify, Vercel, S3) sem
  configuracao de build.
- **Velocidade** -- Zero requests externos significa tempo de carregamento minimo.
  Sem Google Fonts, sem CDN de CSS, sem bundle JS.
- **Reprodutibilidade** -- A pagina funciona identicamente hoje e daqui a 5 anos.
  Sem dependencias quebradas, sem CDN fora do ar.
- **Contexto de IA** -- Claude Code gera HTML em uma unica resposta. Fragmentar
  em multiplos arquivos (CSS, JS, imagens) aumentaria a complexidade sem beneficio
  proporcional.
- **Limite de 100KB** -- Forca concisao. Uma landing page eficaz nao precisa de
  megabytes de framework.

### 7.2 Por que CronCreate para agendamento?

**Decisao:** O modulo `scheduler` usa `prepare_cron_jobs()` para gerar definicoes
de cron jobs que podem ser executadas por CronCreate ou sistemas similares.

**Justificativas:**

- **Universalidade** -- Cron e o padrao Unix mais antigo e universal para agendamento.
  Funciona em Linux, macOS, Docker, CI/CD.
- **Desacoplamento** -- O GrowthOS gera a definicao do job (horario + comando),
  mas nao executa diretamente. O runtime (host, container, CI) decide como executar.
- **Observabilidade** -- Jobs de cron sao facilmente monitoraveis com ferramentas
  padrao (logs, alertas, dashboards).
- **Retry com backoff** -- O modulo inclui `retry_with_backoff` para lidar com
  falhas transitorias de API sem bloquear o scheduler principal.

### 7.3 Por que Pydantic para validacao?

**Decisao:** `BrandVoiceConfig` e outros modelos de configuracao usam Pydantic para
validacao.

**Justificativas:**

- **Fail-fast** -- Erros de configuracao sao detectados no momento da carga, nao
  durante a execucao. Se `brand-voice.yaml` esta malformado, o usuario descobre
  imediatamente ao rodar `/grow`, nao 10 minutos depois quando um agente tenta
  publicar.
- **Documentacao implicita** -- O schema Pydantic documenta quais campos existem,
  quais sao obrigatorios e quais sao os tipos. Elimina ambiguidade.
- **Defaults inteligentes** -- Pydantic permite definir valores padrao por campo.
  O usuario so precisa configurar o que difere do padrao.
- **Serializacao** -- Pydantic converte facilmente entre YAML, JSON e objetos Python,
  facilitando a passagem de configuracao entre camadas.

### 7.4 Por que JSONL para audit trail?

**Decisao:** O `AuditLogger` escreve em formato JSONL (JSON Lines) append-only.

**Justificativas:**

- **Append-only** -- Cada linha e uma entrada independente. Nao ha necessidade de
  parsear o arquivo inteiro para adicionar uma entrada. Nao ha risco de corromper
  entradas anteriores.
- **Streaming** -- Ferramentas como `tail -f`, `jq`, `grep` funcionam nativamente.
  Nao precisa de banco de dados ou viewer especializado.
- **Integridade** -- Cada linha e JSON valido independente. Uma linha corrompida
  nao invalida o resto do arquivo.
- **Tamanho previsivel** -- Facil de rotacionar (logrotate), compactar e arquivar.
- **Compatibilidade** -- JSONL e ingerido nativamente por Elasticsearch, Datadog,
  Splunk, BigQuery e praticamente qualquer ferramenta de observabilidade.

### 7.5 Por que 3 niveis de autonomia?

**Decisao:** O sistema oferece tres niveis de autonomia (`manual`, `semi`, `auto`)
configurados em `brand-voice.yaml`.

**Justificativas e comportamentos:**

| Nivel    | Comportamento                                           | Caso de Uso                    |
|----------|---------------------------------------------------------|--------------------------------|
| `manual` | Sempre pede confirmacao antes de qualquer acao externa. Toda publicacao exige aprovacao explicita. | Marcas com politica de compliance rigorosa. Usuarios novos que querem entender o sistema. |
| `semi`   | Auto-delega para agentes individuais sem pedir confirmacao. Pede confirmacao para pipelines multi-agente e para publicacoes reais. | Padrao recomendado. Equilibrio entre produtividade e controle. |
| `auto`   | Executa tudo automaticamente com confirmacoes minimas. Publica sem pedir aprovacao. | Usuarios avancados com confianca no sistema. Execucoes em batch/CI. |

**Principio:** O nivel de autonomia e uma escala de confianca, nao de capacidade.
O sistema pode fazer tudo em qualquer nivel -- a diferenca e quantos checkpoints
humanos existem no caminho.

**Kill switch:** Independente do nivel de autonomia, o kill switch (`kill_switch: true`
em `brand-voice.yaml`) permite ao usuario dizer "stop" a qualquer momento para
interromper toda atividade. Quando ativado, o `AutonomyManager` lanca
`KillSwitchActiveError` e nenhuma operacao externa e permitida.

### 7.6 Por que um unico comando /grow?

**Decisao:** Todo o GrowthOS e acessivel por um unico comando `/grow` com linguagem
natural, ao inves de multiplos comandos especializados.

**Justificativas:**

- **Carga cognitiva zero** -- O usuario nao precisa memorizar 7 nomes de agentes,
  9 nomes de skills ou dezenas de parametros. Basta dizer o que precisa.
- **Roteamento inteligente** -- O CMO classifica a intencao automaticamente. "Escreva
  um post" e "Publique um post" vao para agentes diferentes sem que o usuario
  precise saber quais.
- **Pipelines implicitos** -- "Escreva e publique" aciona automaticamente o pipeline
  correto. O usuario descreve o resultado desejado, nao o processo.
- **Discoverability** -- `/grow` sem argumentos exibe todas as capacidades.
  O usuario descobre funcionalidades por exploracao, nao por documentacao.

### 7.7 Por que output contracts?

**Decisao:** Toda skill tem um contrato de saida rigido definido em
`docs/output-contracts.md`.

**Justificativas:**

- **Interoperabilidade de pipeline** -- Quando content-creator gera um blog post
  e social-publisher precisa adapta-lo para LinkedIn, o contrato garante que a
  saida do primeiro e parseavel pelo segundo.
- **Previsibilidade** -- O usuario sabe exatamente o que esperar de cada skill.
  Um blog post sempre tera frontmatter, introducao, corpo e conclusao.
- **Testabilidade** -- Contratos definidos permitem validacao automatica de output.
  Se um agente gerar um blog post sem meta_description, isso e detectavel.
- **Anti-slop global** -- O constraint `anti_slop: "enforced from brand-voice.yaml"`
  aparece nos contratos de headlines e social posts, garantindo que frases banidas
  sejam filtradas em toda a cadeia.

---

## Apendice: Estrutura de Diretorios

```
growthOS/
|-- plugin.json                  # Manifesto do plugin (skills, agents, hooks, commands)
|-- brand-voice.example.yaml     # Template de configuracao
|-- brand-voice.yaml             # Configuracao do usuario (nao versionado)
|-- docker-compose.yml           # Orquestracao de MCP servers
|-- Dockerfile                   # Build do ambiente
|-- pyproject.toml               # Configuracao Python / dependencias
|
|-- agents/
|   |-- cmo/                     # Orquestrador (router.md)
|   |-- content-creator/         # Criacao de conteudo
|   |-- growth-engineer/         # Landing pages, CRO
|   |-- growth-strategist/       # Estrategia de marketing
|   |-- intelligence-analyst/    # Pesquisa e analise
|   |-- social-publisher/        # Publicacao em plataformas
|   +-- visual-designer/         # Design visual
|
|-- skills/
|   |-- competitive-intelligence/
|   |-- content-creation/
|   |-- copywriting/
|   |-- landing-page-design/
|   |-- marketing-strategy/
|   |-- platform-mastery/
|   |-- seo-growth/
|   |-- social-media-management/
|   +-- video-production/
|
|-- hooks/
|   |-- audit-logger.md
|   |-- circuit-breaker.md
|   |-- dry-run-guard.md
|   +-- preview-before-publish.md
|
|-- commands/
|   +-- grow/
|       +-- COMMAND.md
|
|-- shared-lib/
|   +-- growthOS_shared/
|       |-- __init__.py
|       |-- audit_logger.py
|       |-- autonomy.py
|       |-- circuit_breaker.py
|       |-- config.py
|       |-- html_generator.py
|       |-- intent_router.py
|       |-- scheduler.py
|       +-- token_manager.py
|
|-- templates/
|   |-- landing-pages/
|   |   |-- bold.html
|   |   |-- gradient.html
|   |   +-- minimal.html
|   |-- reports/
|   |   |-- ab-test-template.md
|   |   |-- cro-report-template.md
|   |   +-- tracking-plan-template.md
|   +-- content/
|       +-- content-calendar-template.md
|
|-- mcp-servers/
|   |-- mcp-social-publish/      # Publicacao em redes sociais
|   |-- mcp-social-discover/     # Coleta de dados e analytics
|   +-- mcp-obsidian-vault/      # Knowledge base local
|
|-- docs/
|   |-- output-contracts.md      # Contratos de saida de todas as skills
|   +-- guides/
|       |-- ARCHITECTURE-GUIDE.md  # Este documento
|       |-- CONFIGURATION-GUIDE.md
|       +-- DEVOPS-GUIDE.md
|
|-- content/                     # Conteudo gerado (blog posts, newsletters)
+-- vault/                       # Obsidian vault (knowledge base)
```

---

*GrowthOS Architecture Guide v1.0.0 -- Abril 2026*
