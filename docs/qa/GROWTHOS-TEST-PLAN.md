# GrowthOS — Plano de Testes E2E Completo

**Epic:** EPIC-GROWTHOS
**Data:** 2026-04-01
**Status:** Em Execucao
**Objetivo:** Validar 100% do plugin antes de subir ao GitHub

---

## Resumo Executivo

| Metrica | Valor |
|---------|-------|
| Total de categorias | 13 |
| Arquivos sob teste | 100+ |
| Modulos Python | 11 |
| MCP Servers | 3 |
| Skills | 9 |
| Agents | 8 (7 + CMO) |
| Hooks | 4 |
| Templates HTML | 3 |
| Test suites existentes | 11 |
| Verificacoes estimadas | 300+ |

---

## CAT 1: Unit Tests — Shared Library

**Escopo:** 8 modulos Python com test suites
**Executor:** pytest
**Criterio de sucesso:** 100% dos testes passando, zero failures

| Modulo | Arquivo de Teste | O que testa |
|--------|-----------------|-------------|
| config.py | test_config.py | BrandVoiceConfig, load/validate YAML, defaults, campo validation |
| token_manager.py | test_token_manager.py | Rate limiting, token bucket, cooldown, concurrent access |
| circuit_breaker.py | test_circuit_breaker.py | State machine (closed/open/half-open), thresholds, recovery |
| audit_logger.py | test_audit_logger.py | JSONL logging, entry format, file rotation, flush |
| autonomy.py | test_autonomy.py | AutonomyManager, kill switch, dry-run, level enforcement |
| scheduler.py | test_scheduler.py | Cron parsing, CalendarEntry, retry backoff, ScheduledPublisher |
| html_generator.py | test_html_generator.py | Template rendering, brand integration, output size |
| intent_router.py | test_intent_router.py | Intent classification, subcommand routing, fallback |

**Comando:** `cd shared-lib && python3 -m pytest tests/ -v --tb=short`

---

## CAT 2: Unit Tests — MCP Servers

**Escopo:** 3 MCP servers
**Criterio de sucesso:** Todos os testes passando

| Server | Testes | O que testa |
|--------|--------|-------------|
| mcp-social-publish | test_server.py | Endpoints publish, platform adapters (Twitter, LinkedIn, Reddit, GitHub, Threads) |
| mcp-obsidian-vault | test_server.py, test_vault_ops.py | Vault CRUD, frontmatter parse, file operations |
| mcp-social-discover | (verificar existencia) | Endpoints discover, platform search |

**Comando por server:** `cd mcp-servers/{server} && python3 -m pytest tests/ -v --tb=short`

---

## CAT 3: Import & Module Integrity

**Escopo:** Todos os modulos Python
**Criterio de sucesso:** Zero ImportError, zero circular deps

### Verificacoes:
1. `shared-lib/growthOS_shared/__init__.py` exporta todos os modulos
2. Cada modulo importa sem erro: `python3 -c "from growthOS_shared import X"`
3. Cada MCP server importa sem erro: `python3 -c "import server"`
4. Sem circular imports entre modulos
5. Todas as dependencias externas estao no pyproject.toml/requirements.txt

---

## CAT 4: Linting & Code Quality (Ruff)

**Escopo:** Todo codigo .py (excluindo .venv)
**Criterio de sucesso:** Zero erros ruff, zero warnings criticos

### Verificacoes:
1. `ruff check` sem erros em shared-lib/
2. `ruff check` sem erros em mcp-servers/
3. PEP 8 compliance
4. Unused imports removidos
5. Dead code removido

**Comando:** `ruff check growthOS/ --exclude .venv`

---

## CAT 5: Plugin Structure Validation

**Escopo:** plugin.json e estrutura de diretorios
**Criterio de sucesso:** JSON valido, todas refs resolvem

### Verificacoes:
1. `plugin.json` — JSON valido com campos: name, version, description, commands, agents, skills, hooks
2. `.claude-plugin/plugin.json` — Consistente com o principal
3. Cada entry em commands[] aponta para diretorio existente com COMMAND.md
4. Cada entry em agents[] aponta para diretorio existente com AGENT.md
5. Cada entry em skills[] aponta para diretorio existente com SKILL.md
6. Cada entry em hooks[] aponta para arquivo existente

---

## CAT 6: Markdown Frontmatter Validation

**Escopo:** 23+ arquivos .md com frontmatter YAML
**Criterio de sucesso:** Todos os frontmatters parsam como YAML valido

### Skills (9 arquivos):
| Skill | Arquivo | Campos obrigatorios |
|-------|---------|-------------------|
| marketing-strategy | SKILL.md | name, description |
| content-creation | SKILL.md | name, description |
| copywriting | SKILL.md | name, description |
| seo-growth | SKILL.md | name, description |
| video-production | SKILL.md | name, description |
| landing-page-design | SKILL.md | name, description |
| social-media-management | SKILL.md | name, description |
| competitive-intelligence | SKILL.md | name, description |
| platform-mastery | SKILL.md | name, description |

### Agents (8 arquivos):
| Agent | Arquivo | Campos obrigatorios |
|-------|---------|-------------------|
| cmo | AGENT.md | name, description |
| content-creator | AGENT.md | name, description |
| growth-strategist | AGENT.md | name, description |
| social-publisher | AGENT.md | name, description |
| growth-engineer | AGENT.md | name, description |
| intelligence-analyst | AGENT.md | name, description |
| visual-designer | AGENT.md | name, description |

### Hooks (4 arquivos):
| Hook | Campos obrigatorios |
|------|-------------------|
| audit-logger.md | name, description, hooks[].type |
| circuit-breaker.md | name, description, hooks[].type |
| preview-before-publish.md | name, description, hooks[].type |
| dry-run-guard.md | name, description, hooks[].type |

### Commands (2 arquivos):
| Command | Campos obrigatorios |
|---------|-------------------|
| COMMAND.md | name, description |
| setup.md | name, description |

---

## CAT 7: YAML/Config Validation

**Escopo:** Arquivos de configuracao YAML
**Criterio de sucesso:** Todos parsam, schemas corretos

| Arquivo | Validacoes |
|---------|-----------|
| brand-voice.example.yaml | YAML valido, secoes: brand, tone, platforms, autonomy, anti_slop |
| docker-compose.yml | YAML valido, services definidos, healthchecks, volumes, env_file |
| .github/workflows/ci.yml | YAML valido, on trigger, jobs, steps com run/uses |
| templates/content/content-calendar-template.md | Frontmatter Dataview-compatible |

---

## CAT 8: HTML Template Validation

**Escopo:** 3 landing page templates
**Criterio de sucesso:** HTML valido, zero deps externas, responsive, SEO, < 100KB

| Template | Arquivo | Tamanho max |
|----------|---------|-------------|
| Minimal | minimal.html | < 100KB |
| Bold | bold.html | < 100KB |
| Gradient | gradient.html | < 100KB |

### Verificacoes por template:
1. HTML valido (tags abertas/fechadas corretamente)
2. `<meta name="viewport">` presente (responsive)
3. `<meta name="description">` presente (SEO)
4. `<meta property="og:title">` presente (OG tags)
5. `<meta property="og:description">` presente
6. Zero `<link>` para CDN externo
7. Zero `<script src="http">` externo
8. Placeholders `{{...}}` consistentes entre templates
9. Secoes: hero, features, social proof, CTA, footer
10. Tamanho < 100KB

---

## CAT 9: Docker Build & Compose Validation

**Escopo:** Infraestrutura Docker
**Criterio de sucesso:** Dockerfile valido, compose valido, no secrets baked

### Verificacoes:
1. `Dockerfile` — FROM com imagem base, COPY, RUN, EXPOSE, HEALTHCHECK
2. `Dockerfile` — Multi-stage build (builder + runtime)
3. `docker-compose.yml` — 3 services definidos (social-publish, social-discover, obsidian-vault)
4. `docker-compose.yml` — env_file ou environment com vars
5. `docker-compose.yml` — healthcheck por service
6. `.dockerignore` — Exclui: .env, .git, __pycache__, .venv, *.key, *.pem
7. `.env.example` — Todas vars documentadas, NENHUM valor real
8. `.env.example` — Cobre: API keys (Twitter, LinkedIn, etc), vault path, autonomy, dry_run

---

## CAT 10: Security Audit

**Escopo:** Todo o repositorio
**Criterio de sucesso:** Zero secrets, zero injection vectors

### 10.1 — Credential Scan
1. Nenhum API key hardcoded em .py, .md, .yaml, .json, .html
2. Nenhum password, token, secret em texto plano
3. `.env.example` sem valores reais (apenas placeholders como `your_api_key_here`)
4. `brand-voice.example.yaml` sem dados reais

### 10.2 — Injection Prevention
5. Pydantic models com field_validator em inputs externos
6. YAML loading usa `yaml.safe_load` (nao `yaml.load`)
7. Path traversal prevention em vault_ops.py
8. HTML generator escapa user input (XSS prevention)

### 10.3 — Safety Hooks
9. preview-before-publish intercepta ANTES de publicar
10. dry-run-guard bloqueia chamadas externas em modo dry-run
11. audit-logger registra TODAS operacoes externas
12. circuit-breaker protege contra falhas cascata

### 10.4 — Docker Security
13. Dockerfile nao copia .env para imagem
14. .dockerignore exclui credenciais
15. Nenhum USER root no container final (ou justificativa)

---

## CAT 11: Cross-Reference Integrity

**Escopo:** Referencias entre componentes
**Criterio de sucesso:** 100% das referencias resolvem para arquivos existentes

### Verificacoes:
1. CMO router.md referencia agentes que existem em agents/
2. COMMAND.md subcommands delegam a agentes que existem
3. plugin.json commands[] → commands/grow/ existe
4. plugin.json skills[] → skills/*/ existem
5. plugin.json agents[] → agents/*/ existem
6. plugin.json hooks[] → hooks/*.md existem
7. output-contracts.md referencia skills existentes
8. Hooks referenciam tool names MCP validos
9. scheduler.py agent references existem em agents/
10. __init__.py exporta modulos que existem no filesystem

---

## CAT 12: Documentation Completeness

**Escopo:** Todos os docs
**Criterio de sucesso:** Todas secoes obrigatorias presentes

### README.md (principal):
1. Descricao do projeto
2. Features list
3. Quick start guide (3 opcoes: plugin, Docker, manual)
4. Configuracao (brand-voice.yaml)
5. Usage examples (/grow commands)
6. Arquitetura (diagrama ou descricao)

### CONTRIBUTING.md:
7. Setup instructions
8. Coding standards
9. PR process
10. Testing requirements

### Subdiretorios:
11. Cada diretorio principal tem README.md (agents, skills, hooks, commands, mcp-servers, shared-lib, templates, docs)

---

## CAT 13: Functional Integration (Cross-Module)

**Escopo:** Chains entre modulos
**Criterio de sucesso:** Fluxos end-to-end funcionam

### Chains a testar:
1. **Config → Autonomy:** load_brand_voice() alimenta AutonomyManager corretamente
2. **Autonomy → Scheduler:** ScheduledPublisher respeita autonomy level do config
3. **Config → HTML Generator:** html_generator usa brand voice para personalizar copy
4. **CircuitBreaker → Retry:** retry_with_backoff integra com circuit_breaker states
5. **CalendarEntry → Frontmatter:** Serializa/deserializa roundtrip sem perda
6. **ScheduleConfig → CronJobs:** prepare_cron_jobs gera prompts validos
7. **AuditLogger → All Operations:** Todas operacoes externas geram audit entries

---

## Distribuicao de Execucao (Maestri Terminals)

| Terminal | Categorias | Tipo |
|----------|-----------|------|
| Backend Senior | CAT 1 (shared-lib pytest) | Automated |
| Data Egineer | CAT 2 (MCP server pytest) | Automated |
| Dev - Tech Lead | CAT 3-4 (imports + ruff) | Automated |
| CMO | CAT 5-6-7 (plugin + frontmatter + YAML) | Validation |
| Pesquisador | CAT 8 (HTML templates) | Validation |
| DevOps - Senior | CAT 9 (Docker) | Validation |
| Architect Master Senior | CAT 10 (security) | Audit |
| Roteirista | CAT 11-12 (cross-refs + docs) | Validation |
| LLM Expert | CAT 13 (integration tests) | Automated |
| Scrum Master | Documentacao de resultados | Tracking |

---

## Criterios de Aceite Global

O projeto esta **PRONTO PARA GITHUB** quando:

- [ ] CAT 1: 100% unit tests shared-lib passing
- [ ] CAT 2: 100% unit tests MCP servers passing
- [ ] CAT 3: Zero ImportError em todos os modulos
- [ ] CAT 4: Zero erros ruff (ou apenas warnings aceitos)
- [ ] CAT 5: plugin.json valido com todas refs resolvidas
- [ ] CAT 6: 100% frontmatters YAML validos
- [ ] CAT 7: Todos YAMLs de config validos
- [ ] CAT 8: 3 templates HTML validos, < 100KB, zero deps externas
- [ ] CAT 9: Dockerfile e docker-compose validos
- [ ] CAT 10: Zero secrets hardcoded, zero injection vectors
- [ ] CAT 11: 100% cross-references resolvidas
- [ ] CAT 12: Docs completos com todas secoes
- [ ] CAT 13: Integration chains funcionando

**Resultado esperado:** Projeto pronto, testado, seguro e documentado para GitHub.
