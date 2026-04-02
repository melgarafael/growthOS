# GrowthOS — Guia de Configuracao

Guia completo de todas as opcoes de configuracao do GrowthOS. Cobre arquivos de configuracao, variaveis de ambiente, niveis de autonomia, modo dry-run e hooks de seguranca.

---

## Visao Geral

O GrowthOS utiliza tres camadas de configuracao, em ordem de prioridade:

| Prioridade | Fonte | Descricao |
|-----------|-------|-----------|
| 1 (maior) | Variaveis de ambiente (`.env`) | Credenciais, paths, overrides de runtime |
| 2 | `brand-voice.yaml` | Identidade da marca, tom, plataformas, autonomia |
| 3 (menor) | Defaults no codigo | Valores padrao definidos nos models Pydantic |

### Arquivos de Configuracao

| Arquivo | Obrigatorio | Funcao |
|---------|------------|--------|
| `brand-voice.yaml` | Sim | Configuracao principal da marca e comportamento |
| `.env` | Para publicacao | Credenciais de API e configuracao de infraestrutura |
| `plugin.json` | Sim (nao editar) | Manifesto do plugin — registra skills, agents, hooks, commands |
| `brand-voice.example.yaml` | — | Template de referencia (nao editar, copiar para `brand-voice.yaml`) |

### Primeiro Uso

```bash
# 1. Copiar templates
cp brand-voice.example.yaml brand-voice.yaml
cp .env.example .env

# 2. Editar brand-voice.yaml com dados da sua marca
# 3. Editar .env com suas credenciais de API

# 4. Iniciar via plugin
claude plugin add ./growthOS
claude
> /grow setup
```

Alternativa: execute `/grow setup` diretamente — o GrowthOS detecta a ausencia do `brand-voice.yaml` e inicia o wizard de configuracao interativo.

---

## brand-voice.yaml — Referencia Completa

Arquivo central de configuracao. Controla a identidade da marca, tom de comunicacao, plataformas habilitadas, filtro anti-slop e niveis de autonomia.

**Localizacao:** O GrowthOS procura o arquivo nesta ordem:
1. Path explicito passado via codigo
2. Variavel de ambiente `GROWTHOS_BRAND_VOICE_PATH`
3. `brand-voice.yaml` na raiz do plugin

### brand — Identidade da Marca

Campos que definem quem e a sua marca. Usados por todos os agents para manter consistencia no conteudo gerado.

```yaml
brand:
  name: "MinhaEmpresa"        # OBRIGATORIO — nome da marca/produto
  tagline: "Slogan aqui"      # Opcional — tagline/slogan
  tone:                        # OBRIGATORIO — lista de descritores de tom (minimo 1)
    - professional
    - approachable
    - innovative
  avoid:                       # Opcional — palavras/frases que a marca evita
    - synergy
    - disrupt
  personality: "Amigavel..."  # Opcional — descricao da personalidade
  industry: "SaaS / B2B"     # Opcional — setor de atuacao (contexto para agents)
```

| Campo | Tipo | Obrigatorio | Default | Descricao |
|-------|------|------------|---------|-----------|
| `name` | string | Sim | — | Nome da marca. Nao pode ser vazio. |
| `tagline` | string | Nao | `""` | Tagline ou slogan da marca. |
| `tone` | list[string] | Sim | — | Descritores de tom. Exemplos: `professional`, `casual`, `witty`, `technical`, `friendly`, `authoritative`. |
| `avoid` | list[string] | Nao | `[]` | Palavras/frases que a marca nunca usa. Complementa o `anti_slop`. |
| `personality` | string | Nao | `""` | Descricao livre da personalidade da marca. |
| `industry` | string | Nao | `""` | Setor de atuacao. Ajuda agents a contextualizar conteudo. |

### platforms — Plataformas

Configuracao individual para cada plataforma de publicacao. Controla quais plataformas estao habilitadas, limites de caracteres e overrides de tom.

```yaml
platforms:
  linkedin:
    enabled: true
    tone_override: null          # Usa tom padrao da marca
    hashtags: true               # Incluir hashtags automaticamente
    max_length: 3000             # Limite de caracteres
    post_types: [article, post, carousel]
  twitter:
    enabled: true
    tone_override: "concise_witty"  # Override de tom para esta plataforma
    threads: true                    # Habilitar threads
    max_length: 280
  reddit:
    enabled: true
    tone_override: "authentic_casual"
    max_length: 10000
  threads:
    enabled: true
    tone_override: null
    max_length: 500
  github:
    enabled: true
    tone_override: "technical_precise"
    max_length: null             # Sem limite
  youtube:
    enabled: true
    tone_override: null
    max_length: 5000
  instagram:
    enabled: true
    tone_override: "visual_engaging"
    max_length: 2200
  stackoverflow:
    enabled: false               # Desabilitado por padrao
    tone_override: "technical_helpful"
    max_length: 30000
```

| Campo | Tipo | Default | Descricao |
|-------|------|---------|-----------|
| `enabled` | bool | `true` | Se a plataforma esta ativa para publicacao. |
| `tone_override` | string ou null | `null` | Override de tom especifico para esta plataforma. `null` = usa `brand.tone`. |
| `max_length` | int ou null | varia | Limite maximo de caracteres. `null` = sem limite. |
| `hashtags` | bool | `false` | Incluir hashtags automaticamente (LinkedIn). |
| `threads` | bool | `false` | Habilitar formato de thread (Twitter). |
| `post_types` | list[string] | `[]` | Tipos de post suportados (LinkedIn: article, post, carousel). |

**Plataformas suportadas:** `linkedin`, `twitter`, `reddit`, `threads`, `github`, `youtube`, `instagram`, `stackoverflow`.

Para desabilitar uma plataforma, defina `enabled: false`. Plataformas desabilitadas nao aparecem nas opcoes de publicacao.

### anti_slop — Filtro de Qualidade

Previne linguagem generica de marketing tipica de IA. Todo conteudo gerado e verificado contra estas regras antes da entrega.

```yaml
anti_slop:
  enabled: true
  banned_phrases:
    - "game-changer"
    - "revolutionary"
    - "cutting-edge"
    - "best-in-class"
    - "synergy"
    - "leverage"
    - "disrupt"
    - "innovative solution"
    - "transform your"
    - "unlock the power"
    - "dive deep"
    - "it's worth noting"
    - "in today's fast-paced"
    - "at the end of the day"
    - "think outside the box"
    - "move the needle"
    - "low-hanging fruit"
    - "paradigm shift"
    - "holistic approach"
    - "seamlessly integrate"
  style_rules:
    - "Use active voice"
    - "Avoid superlatives without evidence"
    - "No clickbait headlines"
    - "Prefer specific numbers over vague claims"
  custom_banned: []
```

| Campo | Tipo | Default | Descricao |
|-------|------|---------|-----------|
| `enabled` | bool | `true` | Ativar/desativar o filtro anti-slop globalmente. |
| `banned_phrases` | list[string] | 20 frases padrao | Frases proibidas. Verificacao case-insensitive. |
| `style_rules` | list[string] | 4 regras padrao | Regras de estilo que os agents devem seguir. |
| `custom_banned` | list[string] | `[]` | Frases adicionais banidas especificas da sua marca. Somadas as `banned_phrases`. |

**Dica:** Adicione termos especificos do seu setor em `custom_banned` em vez de editar `banned_phrases` — assim voce mantem as protecoes padrao e adiciona as suas.

### autonomy — Niveis de Autonomia

Controla quanto o GrowthOS pode fazer sozinho vs. quanto precisa de confirmacao do usuario.

```yaml
autonomy:
  level: semi                  # manual | semi | auto
  require_preview: true        # Exibir preview antes de publicar
  dry_run_default: true        # Simular operacoes sem chamadas reais
  kill_switch: true            # Habilitar botao de emergencia
```

| Campo | Tipo | Default | Valores Validos | Descricao |
|-------|------|---------|----------------|-----------|
| `level` | string | `"semi"` | `manual`, `semi`, `auto` | Nivel de autonomia global. |
| `require_preview` | bool | `true` | — | Mostrar preview formatado antes de publicar. |
| `dry_run_default` | bool | `true` | — | Modo simulacao ativo por padrao. |
| `kill_switch` | bool | `true` | — | Habilitar mecanismo de parada de emergencia. |

Detalhes completos na secao [Niveis de Autonomia](#niveis-de-autonomia--guia-detalhado).

---

## Variaveis de Ambiente (.env)

Copie `.env.example` para `.env` e preencha os valores. Nunca commite o `.env` no repositorio.

### Chaves de API — Plataformas Sociais

Necessarias apenas para as plataformas que voce deseja publicar. Se uma plataforma nao tem credenciais configuradas, o MCP server retorna um erro claro indicando qual variavel falta.

#### Twitter/X

```env
GROWTHOS_TWITTER_API_KEY=
GROWTHOS_TWITTER_API_SECRET=
GROWTHOS_TWITTER_ACCESS_TOKEN=
GROWTHOS_TWITTER_ACCESS_SECRET=
```

| Variavel | Obrigatorio | Descricao |
|----------|------------|-----------|
| `GROWTHOS_TWITTER_API_KEY` | Para Twitter | API Key do app Twitter/X |
| `GROWTHOS_TWITTER_API_SECRET` | Para Twitter | API Secret do app Twitter/X |
| `GROWTHOS_TWITTER_ACCESS_TOKEN` | Para Twitter | Access Token do usuario |
| `GROWTHOS_TWITTER_ACCESS_SECRET` | Para Twitter | Access Token Secret do usuario |

**Como obter:** Acesse [developer.x.com](https://developer.x.com), crie um projeto, gere as chaves em "Keys and Tokens".

#### LinkedIn

```env
GROWTHOS_LINKEDIN_TOKEN=
GROWTHOS_LINKEDIN_ORG_ID=
```

| Variavel | Obrigatorio | Descricao |
|----------|------------|-----------|
| `GROWTHOS_LINKEDIN_TOKEN` | Para LinkedIn | Access token OAuth 2.0 |
| `GROWTHOS_LINKEDIN_ORG_ID` | Para posts corporativos | ID da organizacao no LinkedIn |

**Como obter:** Crie um app em [linkedin.com/developers](https://www.linkedin.com/developers/), solicite os escopos `w_member_social` e `r_liteprofile`.

#### Reddit

```env
GROWTHOS_REDDIT_CLIENT_ID=
GROWTHOS_REDDIT_CLIENT_SECRET=
GROWTHOS_REDDIT_USERNAME=
GROWTHOS_REDDIT_PASSWORD=
```

| Variavel | Obrigatorio | Descricao |
|----------|------------|-----------|
| `GROWTHOS_REDDIT_CLIENT_ID` | Para Reddit | Client ID do app Reddit |
| `GROWTHOS_REDDIT_CLIENT_SECRET` | Para Reddit | Client Secret do app Reddit |
| `GROWTHOS_REDDIT_USERNAME` | Para Reddit | Username da conta Reddit |
| `GROWTHOS_REDDIT_PASSWORD` | Para Reddit | Senha da conta Reddit |

**Como obter:** Acesse [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps), crie um app do tipo "script".

#### GitHub

```env
GROWTHOS_GITHUB_TOKEN=
```

| Variavel | Obrigatorio | Descricao |
|----------|------------|-----------|
| `GROWTHOS_GITHUB_TOKEN` | Para GitHub | Personal Access Token (classic ou fine-grained) |

**Como obter:** Em Settings > Developer Settings > Personal Access Tokens. Escopos necessarios: `repo`, `read:user`.

#### Threads

```env
GROWTHOS_THREADS_TOKEN=
```

| Variavel | Obrigatorio | Descricao |
|----------|------------|-----------|
| `GROWTHOS_THREADS_TOKEN` | Para Threads | Access token da API do Threads (via Meta) |

**Como obter:** Acesse [developers.facebook.com](https://developers.facebook.com), configure o app com permissoes do Threads API.

### Configuracao do Obsidian Vault

```env
GROWTHOS_VAULT_PATH=./vault
```

| Variavel | Obrigatorio | Default | Descricao |
|----------|------------|---------|-----------|
| `GROWTHOS_VAULT_PATH` | Nao | `./vault` | Caminho para o vault Obsidian. Usado pelo MCP obsidian-vault para ler/escrever notas, drafts e calendario de conteudo. |

### Configuracao do Plugin

```env
GROWTHOS_BRAND_VOICE_PATH=./brand-voice.yaml
GROWTHOS_CONFIG_DIR=.
GROWTHOS_AUDIT_DIR=.growthOS/audit
```

| Variavel | Obrigatorio | Default | Descricao |
|----------|------------|---------|-----------|
| `GROWTHOS_BRAND_VOICE_PATH` | Nao | `brand-voice.yaml` na raiz do plugin | Caminho para o arquivo de configuracao da marca. |
| `GROWTHOS_CONFIG_DIR` | Nao | `.` (diretorio atual) | Diretorio base para configuracoes e estado do plugin. |
| `GROWTHOS_AUDIT_DIR` | Nao | `.growthOS/audit` | Diretorio onde os logs de auditoria JSONL sao gravados. |

### Autonomia e Seguranca

```env
GROWTHOS_AUTONOMY_LEVEL=supervised
GROWTHOS_DRY_RUN=true
```

| Variavel | Obrigatorio | Default | Valores | Descricao |
|----------|------------|---------|---------|-----------|
| `GROWTHOS_AUTONOMY_LEVEL` | Nao | `semi` | `supervised`, `assisted`, `delegated`, `autonomous` | Override do nivel de autonomia via env var. |
| `GROWTHOS_DRY_RUN` | Nao | `true` | `true`, `false` | Override global do modo dry-run. |

### Portas dos MCP Servers

```env
GROWTHOS_PUBLISH_PORT=8001
GROWTHOS_DISCOVER_PORT=8002
GROWTHOS_VAULT_PORT=8003
```

| Variavel | Obrigatorio | Default | Descricao |
|----------|------------|---------|-----------|
| `GROWTHOS_PUBLISH_PORT` | Nao | `8001` | Porta do MCP server social-publish. |
| `GROWTHOS_DISCOVER_PORT` | Nao | `8002` | Porta do MCP server social-discover. |
| `GROWTHOS_VAULT_PORT` | Nao | `8003` | Porta do MCP server obsidian-vault. |

---

## plugin.json

Manifesto do plugin GrowthOS. Registra todos os componentes que o Claude Code deve carregar. **Nao edite este arquivo** a menos que esteja adicionando novos componentes ao plugin.

```json
{
  "name": "growthOS",
  "version": "1.0.0",
  "description": "Autonomous marketing team for Claude Code",
  "author": "GrowthOS Community",
  "license": "MIT",
  "skills": [ ... ],     // 9 skills registradas
  "agents": [ ... ],     // 7 agents registrados
  "hooks": [ ... ],      // 4 hooks de seguranca
  "commands": [ ... ]    // 1 comando (/grow)
}
```

| Secao | Quantidade | Funcao |
|-------|-----------|--------|
| `skills` | 9 | Skills especializadas carregadas sob demanda pelo Claude Code. |
| `agents` | 7 | Agents autonomos com personas e ferramentas especificas. |
| `hooks` | 4 | Hooks de seguranca (PreToolUse/PostToolUse) que interceptam chamadas MCP. |
| `commands` | 1 | O comando `/grow` — ponto de entrada unico do plugin. |

Para adicionar um novo componente: crie o diretorio com o arquivo de definicao (SKILL.md, AGENT.md, ou hook .md) e adicione o `{"path": "..."}` na secao correspondente.

---

## Niveis de Autonomia — Guia Detalhado

O GrowthOS classifica toda acao em tres tiers de impacto:

| Tier | Acoes | Risco |
|------|-------|-------|
| **INTERNAL** | `read_note`, `search_notes`, `get_analytics`, `list_drafts`, `get_config` | Nenhum — leitura apenas |
| **CREATION** | `create_note`, `generate_content`, `create_draft`, `edit_draft` | Baixo — cria artefatos internos |
| **EXTERNAL** | `publish_post`, `schedule_post`, `delete_post`, `update_post`, `send_notification` | Alto — acao visivel externamente |

### manual — Controle Total

**Quando usar:** Configuracao inicial, primeiros dias de uso, marcas com alto risco reputacional.

| Tier | Requer Aprovacao? |
|------|------------------|
| INTERNAL | Nao |
| CREATION | **Sim** |
| EXTERNAL | **Sim** |

Toda acao que cria ou modifica conteudo exige confirmacao explicita do usuario. Apenas leituras sao automaticas.

### semi — Equilibrio (Padrao)

**Quando usar:** Uso cotidiano apos confianca inicial no sistema.

| Tier | Requer Aprovacao? |
|------|------------------|
| INTERNAL | Nao |
| CREATION | Nao |
| EXTERNAL | **Sim** |

Criacao de conteudo e automatica. Publicacao e acoes externas exigem confirmacao. Este e o nivel padrao recomendado.

### auto — Autonomia Total

**Quando usar:** Pipelines automatizados, campanhas pre-aprovadas, workflows de alta velocidade.

| Tier | Requer Aprovacao? |
|------|------------------|
| INTERNAL | Nao |
| CREATION | Nao |
| EXTERNAL | Nao |

Todas as acoes sao executadas sem confirmacao. O circuit breaker e o audit trail continuam ativos como rede de seguranca.

### Como Alterar o Nivel

**Via brand-voice.yaml (persistente):**
```yaml
autonomy:
  level: semi    # Altere para: manual | semi | auto
```

**Via variavel de ambiente (override de runtime):**
```env
GROWTHOS_AUTONOMY_LEVEL=manual
```

**Prioridade:** Variavel de ambiente sobrescreve o valor do YAML.

### Kill Switch — Parada de Emergencia

O kill switch e um mecanismo de seguranca que **reverte imediatamente para o modo `manual`**, independente do nivel configurado.

**Ativacao:** Diga "stop" ou "para" durante qualquer interacao com o GrowthOS.

**O que acontece:**
1. Nivel de autonomia muda para `manual` instantaneamente
2. Todas as acoes CREATION e EXTERNAL passam a exigir aprovacao
3. Estado e persistido em disco (`.growthOS/kill-switch.json`) — sobrevive reinicializacoes
4. O nivel anterior e salvo para restauracao

**Desativacao:**
1. O usuario desativa explicitamente via comando ou configuracao
2. O GrowthOS restaura o nivel de autonomia anterior

**Arquivo de estado:**
```json
{
  "activated": true,
  "timestamp": "2026-04-01T14:30:00+00:00",
  "previous_level": "semi"
}
```

Mesmo com `kill_switch: false` no YAML, o kill switch ainda pode ser ativado manualmente — a config apenas controla se ele esta habilitado por padrao.

---

## Dry Run Mode

O modo dry-run simula todas as operacoes sem fazer chamadas reais de API. Nenhum conteudo e publicado, nenhuma nota e criada, nenhum dado externo e acessado.

### Ativacao

O dry-run esta ativo quando **qualquer** condicao e verdadeira:

| Fonte | Configuracao | Exemplo |
|-------|-------------|---------|
| `brand-voice.yaml` | `autonomy.dry_run_default: true` | Ativo globalmente por padrao |
| Variavel de ambiente | `GROWTHOS_DRY_RUN=true` | Override de runtime |
| Parametro na chamada | `dry_run: true` no input da tool | Por invocacao |

**Padrao:** `dry_run_default: true` — o GrowthOS comeca em modo seguro. Voce precisa desativar explicitamente para publicar de verdade.

### O Que e Simulado

| MCP Server | Operacoes Simuladas | Resposta Sintetica |
|-----------|--------------------|--------------------|
| social-publish | `publish_post`, `schedule_post` | `{"status": "dry_run", "would_publish": true}` |
| social-discover | `search_trends`, `analyze_topic` | `{"status": "dry_run", "simulated_results": []}` |
| obsidian-vault | `save_note`, `create_draft` | `{"status": "dry_run", "operation": "..."}` |

### Lendo a Saida [DRY RUN]

Toda saida simulada e prefixada com `[DRY RUN]` para distincao visual:

```
[DRY RUN] ─────────────────────────────────────────
  Tool:     mcp__growthOS-social-publish__publish_post
  Server:   social-publish
  Platform: twitter
  Content:  "Excited to announce our new feature..."
  Length:   142/280 chars
  Media:    0 attachments
  Result:   Simulated success (no API call made)
────────────────────────────────────────────────────
```

### Quando Usar

| Cenario | Dry Run? |
|---------|---------|
| Testando um novo pipeline de conteudo | Sim |
| Validando formatacao antes de publicar | Sim |
| Campanha de producao aprovada | Nao |
| Primeiro uso do GrowthOS | Sim (padrao) |
| Ambiente de desenvolvimento/CI | Sim |

### Desativando para Producao

```yaml
# brand-voice.yaml
autonomy:
  dry_run_default: false    # Desativar globalmente
```

Ou por invocacao, passando `dry_run: false` como parametro.

---

## Seguranca e Hooks

O GrowthOS possui 4 hooks que interceptam chamadas MCP para garantir seguranca, auditoria e controle.

### Visao Geral dos Hooks

| Hook | Tipo | Dispara Em | Funcao |
|------|------|-----------|--------|
| **dry-run-guard** | PreToolUse | Toda chamada MCP | Intercepta e simula quando dry-run esta ativo |
| **preview-before-publish** | PreToolUse | `publish_post` apenas | Mostra preview e pede confirmacao |
| **audit-logger** | PostToolUse | Toda chamada MCP | Registra acao no trail de auditoria |
| **circuit-breaker** | PostToolUse | Toda chamada MCP | Protege contra falhas em cascata |

### Ordem de Execucao

```
Chamada MCP iniciada
  │
  ├─ [PreToolUse] dry-run-guard
  │   └─ Se dry-run ativo: BLOQUEIA, retorna resposta sintetica
  │
  ├─ [PreToolUse] preview-before-publish (se publish_post)
  │   └─ Se manual/semi: exibe preview, pede confirmacao
  │   └─ Se auto: exibe preview, permite automaticamente
  │   └─ Se usuario recusa: salva como draft no vault
  │
  ├─ [Execucao real da tool MCP]
  │
  ├─ [PostToolUse] audit-logger
  │   └─ Registra acao, redige campos sensiveis
  │
  └─ [PostToolUse] circuit-breaker
      └─ Registra sucesso/falha, abre circuito se necessario
```

### Preview Before Publish

Quando o nivel de autonomia e `manual` ou `semi`, o hook intercepta toda tentativa de publicacao e mostra um preview formatado por plataforma:

```
┌─ Twitter Preview ─────────────────────────────┐
│ Excited to announce our new AI-powered...      │
│                                                 │
│ Characters: 142/280                             │
│ Media: 0 attachment(s)                          │
└─────────────────────────────────────────────────┘

Publish to twitter? (autonomy: semi)
   [Y] Publish now  |  [N] Cancel and save as draft
```

Se o usuario recusa, o conteudo e salvo como draft em `GrowthOS/Drafts/{platform}/{date}-blocked-draft.md` no vault Obsidian.

No modo `auto`, o preview e exibido com o header `[AUTO-PUBLISH]` e a publicacao prossegue automaticamente.

### Audit Trail

Todo chamada MCP do GrowthOS e registrada em arquivos JSONL diarios:

**Localizacao:** `$GROWTHOS_AUDIT_DIR/audit-YYYY-MM-DD.jsonl` (default: `.growthOS/audit/`)

**Formato de cada linha:**
```json
{
  "timestamp": "2026-04-01T14:30:00Z",
  "action": "mcp__growthOS__social_publish__post_tweet",
  "platform": "social_publish",
  "content_hash": "a1b2c3",
  "user": "system",
  "status": "success",
  "metadata": {
    "duration_ms": 1200,
    "redacted_fields": ["access_token"]
  }
}
```

**Campos sensiveis redatados automaticamente:** Qualquer campo cujo nome contenha `_token`, `_secret`, `_key`, `_password`, `authorization` ou `cookie` e substituido por `[REDACTED]`.

**Garantias:**
- Append-only — entradas nunca sao editadas ou removidas
- Se a gravacao falhar (disco cheio, permissoes), o erro e logado em stderr mas **nunca bloqueia** a operacao do usuario

### Circuit Breaker

Protege contra falhas em cascata usando uma maquina de estados por MCP server:

```
CLOSED  ──(3 falhas consecutivas)──▸  OPEN
OPEN    ──(apos 60s timeout)───────▸  HALF_OPEN
HALF_OPEN ──(1 sucesso)────────────▸  CLOSED
HALF_OPEN ──(1 falha)──────────────▸  OPEN
```

**Configuracao padrao:**

| Parametro | Valor | Descricao |
|-----------|-------|-----------|
| `failure_threshold` | 3 | Falhas consecutivas para abrir o circuito |
| `recovery_timeout` | 60s | Tempo ate tentar reconexao (HALF_OPEN) |
| `half_open_max` | 1 | Maximo de chamadas de teste em HALF_OPEN |

**Breakers independentes por servidor:**
- `social_publish` — publicacao em redes sociais
- `social_discover` — descoberta de tendencias
- `obsidian_vault` — operacoes no vault

**Mensagens de estado:**

Quando o circuito abre:
```
Circuit breaker OPEN for social_publish (3 consecutive failures).
   Last failure: 45s ago. Will allow retry in 15s.
   Tip: Check API credentials and rate limits for this service.
```

Quando recupera:
```
Circuit breaker for social_publish CLOSED — service recovered.
```

**Persistencia:** O estado do circuit breaker e mantido em memoria por sessao. Uma nova sessao do Claude Code comeca com todos os circuitos CLOSED — isso e intencional para que falhas transientes nao persistam entre sessoes.

**Interacao com dry-run:** Chamadas em dry-run nao afetam o estado do circuit breaker, pois nenhuma chamada real e feita.

---

## Resumo de Seguranca

| Mecanismo | Protege Contra | Ativo Por Padrao |
|-----------|---------------|-----------------|
| Dry-run mode | Publicacoes acidentais | Sim (`dry_run_default: true`) |
| Preview hook | Conteudo publicado sem revisao | Sim (`require_preview: true`) |
| Audit trail | Falta de rastreabilidade | Sim (sempre ativo) |
| Circuit breaker | Falhas em cascata, gasto de API | Sim (sempre ativo) |
| Kill switch | Situacoes de emergencia | Sim (`kill_switch: true`) |
| Anti-slop filter | Linguagem generica de IA | Sim (`enabled: true`) |
| Redacao de segredos | Vazamento de credenciais em logs | Sim (automatico no audit-logger) |
