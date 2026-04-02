# GrowthOS -- Guia de DevOps

> Guia completo de implantacao, infraestrutura e operacao do GrowthOS.
> Cobre instalacao, Docker, CI/CD, variaveis de ambiente, troubleshooting e contribuicao.

---

## Indice

1. [Opcoes de Instalacao](#1-opcoes-de-instalacao)
2. [Dockerfile Detalhado](#2-dockerfile-detalhado)
3. [docker-compose.yml Detalhado](#3-docker-composeyml-detalhado)
4. [CI/CD Pipeline](#4-cicd-pipeline)
5. [Variaveis de Ambiente](#5-variaveis-de-ambiente)
6. [Troubleshooting](#6-troubleshooting)
7. [Contribuindo](#7-contribuindo)

---

## 1. Opcoes de Instalacao

O GrowthOS oferece tres metodos de instalacao, do mais simples ao mais flexivel.

### 1.1 Metodo A -- Plugin Claude Code (Recomendado)

A forma mais rapida de comecar. O GrowthOS funciona como plugin nativo do Claude Code.

```bash
# 1. Instale o Claude Code CLI (se ainda nao possui)
npm install -g @anthropic-ai/claude-code

# 2. Clone o repositorio
git clone https://github.com/your-org/growthOS.git
cd growthOS

# 3. Configure as variaveis de ambiente
cp .env.example .env
# Edite .env com suas chaves de API

# 4. Configure o brand voice
cp brand-voice.example.yaml brand-voice.yaml

# 5. Inicie o Claude Code no diretorio do projeto
claude
```

**Requisitos:**
- Node.js 18+
- Python 3.11+
- Claude Code CLI instalado e autenticado

**Quando usar:** Desenvolvimento local, prototipacao rapida, uso individual.

### 1.2 Metodo B -- Docker (Producao)

Ideal para deploys consistentes e ambientes de producao.

```bash
# 1. Clone o repositorio
git clone https://github.com/your-org/growthOS.git
cd growthOS

# 2. Configure as variaveis de ambiente
cp .env.example .env
# Edite .env com suas chaves de API

# 3. Suba todos os servicos
docker-compose up -d

# 4. Verifique o status dos containers
docker-compose ps

# 5. Acompanhe os logs
docker-compose logs -f
```

**Requisitos:**
- Docker 20.10+
- Docker Compose v2+

**Quando usar:** Producao, ambientes compartilhados, CI/CD, deploys reproductiveis.

**Verificacao dos servicos:**

```bash
# Status de todos os containers
docker-compose ps

# Saida esperada:
# NAME                        STATUS              PORTS
# growthos-social-publish     Up (healthy)        0.0.0.0:8001->8001/tcp
# growthos-social-discover    Up (healthy)        0.0.0.0:8002->8002/tcp
# growthos-obsidian-vault     Up (healthy)        0.0.0.0:8003->8003/tcp

# Health check individual
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

### 1.3 Metodo C -- Manual (Desenvolvimento Avancado)

Instalacao componente a componente para quem precisa de controle total.

```bash
# 1. Clone o repositorio
git clone https://github.com/your-org/growthOS.git
cd growthOS

# 2. Crie e ative um ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 3. Instale a shared library em modo desenvolvimento
pip install -e "shared-lib/[dev]"

# 4. Instale as dependencias de cada MCP server
pip install -r mcp-servers/mcp-social-publish/requirements.txt
pip install -r mcp-servers/mcp-social-discover/requirements.txt
pip install -r mcp-servers/mcp-obsidian-vault/requirements.txt

# 5. Configure o ambiente
cp .env.example .env
cp brand-voice.example.yaml brand-voice.yaml

# 6. Execute os testes para validar a instalacao
pytest shared-lib/tests/ -v

# 7. Inicie cada servidor individualmente (em terminais separados)
python -m mcp-servers.mcp-social-publish.server     # porta 8001
python -m mcp-servers.mcp-social-discover.server     # porta 8002
python -m mcp-servers.mcp-obsidian-vault.server      # porta 8003
```

**Requisitos:**
- Python 3.11+
- pip (gerenciador de pacotes)
- Acesso as portas 8001, 8002, 8003

**Quando usar:** Depuracao profunda, desenvolvimento de um unico MCP server, contribuicao ao projeto.

---

## 2. Dockerfile Detalhado

O Dockerfile utiliza **multi-stage build** para produzir imagens minimas e seguras para cada MCP server.

### 2.1 Arquitetura Multi-Stage

```
+------------------+
|   base           |  <-- python:3.11-slim + shared-lib
+------------------+
    |       |       |
    v       v       v
+------+ +--------+ +------+
|publish| |discover| |vault |  <-- Cada target = 1 imagem independente
+------+ +--------+ +------+
```

O Dockerfile define 4 stages:

| Stage                | Proposito                                | Base             |
|----------------------|------------------------------------------|------------------|
| `base`               | Dependencias compartilhadas (shared-lib) | python:3.11-slim |
| `mcp-social-publish` | Servidor de publicacao social            | base             |
| `mcp-social-discover`| Servidor de descoberta de conteudo       | base             |
| `mcp-obsidian-vault` | Servidor de integracao com Obsidian      | base             |

### 2.2 Stage Base

```dockerfile
FROM python:3.11-slim AS base

WORKDIR /app

# Dependencia de sistema minima (apenas curl para health checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala a shared-lib primeiro (camada com cache mais estavel)
COPY shared-lib/ shared-lib/
COPY pyproject.toml .
RUN pip install --no-cache-dir -e shared-lib/
```

**Decisoes de seguranca e performance:**

| Pratica                          | Motivo                                    |
|----------------------------------|-------------------------------------------|
| `python:3.11-slim`               | Imagem menor (~150MB vs ~900MB da full)   |
| `--no-install-recommends`        | Evita pacotes desnecessarios              |
| `rm -rf /var/lib/apt/lists/*`    | Remove cache do apt, reduz tamanho final  |
| `--no-cache-dir` no pip          | Evita cache de pip na imagem              |
| shared-lib copiada primeiro      | Aproveita cache de camadas do Docker      |

### 2.3 Stages dos MCP Servers

Cada MCP server segue o mesmo padrao:

```dockerfile
FROM base AS mcp-social-publish

# 1. Instala dependencias especificas
COPY mcp-servers/mcp-social-publish/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 2. Copia o codigo fonte
COPY mcp-servers/mcp-social-publish/ mcp-servers/mcp-social-publish/

# 3. Expoe a porta do servico
EXPOSE 8001

# 4. Health check nativo do Docker
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# 5. Comando de inicializacao
CMD ["python", "-m", "mcp-servers.mcp-social-publish.server"]
```

**Portas por servico:**

| Servico              | Porta | Endpoint de saude            |
|----------------------|-------|------------------------------|
| mcp-social-publish   | 8001  | `http://localhost:8001/health` |
| mcp-social-discover  | 8002  | `http://localhost:8002/health` |
| mcp-obsidian-vault   | 8003  | `http://localhost:8003/health` |

### 2.4 Health Checks

Todos os servicos possuem health check configurado no Dockerfile:

| Parametro        | Valor  | Significado                                    |
|------------------|--------|------------------------------------------------|
| `--interval`     | 30s    | Verifica a cada 30 segundos                    |
| `--timeout`      | 5s     | Timeout de 5 segundos por verificacao          |
| `--start-period` | 10s    | Aguarda 10 segundos antes da primeira checagem |
| `--retries`      | 3      | 3 falhas consecutivas = container unhealthy    |

### 2.5 Construindo Imagens Individuais

```bash
# Construir apenas um servico especifico
docker build --target mcp-social-publish -t growthos-social-publish:latest .
docker build --target mcp-social-discover -t growthos-social-discover:latest .
docker build --target mcp-obsidian-vault -t growthos-obsidian-vault:latest .
```

### 2.6 .dockerignore

O `.dockerignore` garante que arquivos sensiveis e desnecessarios nao entrem na imagem:

| Categoria      | Arquivos Ignorados                          | Motivo                           |
|----------------|---------------------------------------------|----------------------------------|
| Segredos       | `.env`, `*.key`, `*.pem`, `*.secret`        | Nunca incluir segredos na imagem |
| Config usuario | `brand-voice.yaml`, `.growthOS/`            | Especifico por ambiente          |
| Python         | `__pycache__/`, `*.pyc`, `.venv/`, `dist/`  | Artefatos de build               |
| Git            | `.git/`, `.gitignore`                       | Nao necessario em runtime        |
| IDE            | `.vscode/`, `.idea/`, `*.swp`               | Arquivos de editor               |
| OS             | `.DS_Store`, `Thumbs.db`                    | Metadados do sistema             |
| Docker         | `docker-compose.yml`                        | Nao necessario dentro da imagem  |
| Docs           | `CONTRIBUTING.md`, `SECURITY.md`, `.github/`| Nao necessario em runtime        |

---

## 3. docker-compose.yml Detalhado

### 3.1 Visao Geral dos Servicos

O `docker-compose.yml` (versao 3.9) define 3 servicos conectados em uma rede bridge.

```
growthos-network (bridge)
|
+-- growthos-social-publish   :8001
+-- growthos-social-discover  :8002
+-- growthos-obsidian-vault   :8003 + volume /vault
```

### 3.2 Servico: mcp-social-publish

```yaml
mcp-social-publish:
  build:
    context: .
    target: mcp-social-publish      # Usa o stage especifico do Dockerfile
  container_name: growthos-social-publish
  env_file: .env                     # Carrega todas as variaveis de .env
  ports:
    - "8001:8001"                    # Mapeia porta do host para o container
  networks:
    - growthos                       # Conecta a rede compartilhada
  restart: unless-stopped            # Reinicia automaticamente (exceto stop manual)
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
    interval: 30s
    timeout: 5s
    retries: 3
    start_period: 10s
```

**Funcao:** Publicacao automatizada em redes sociais (Twitter, LinkedIn, Reddit, GitHub, Threads).

### 3.3 Servico: mcp-social-discover

```yaml
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
```

**Funcao:** Descoberta e curadoria de conteudo relevante para publicacao.

### 3.4 Servico: mcp-obsidian-vault

```yaml
mcp-obsidian-vault:
  build:
    context: .
    target: mcp-obsidian-vault
  container_name: growthos-obsidian-vault
  env_file: .env
  ports:
    - "8003:8003"
  volumes:
    - ${GROWTHOS_VAULT_PATH:-./vault}:/vault:rw   # Volume persistente
  networks:
    - growthos
  restart: unless-stopped
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
    interval: 30s
    timeout: 5s
    retries: 3
    start_period: 10s
```

**Funcao:** Integracao com Obsidian Vault para gestao de conhecimento.

**Volume montado:**

| Propriedade | Valor                               | Descricao                                   |
|-------------|--------------------------------------|---------------------------------------------|
| Origem      | `${GROWTHOS_VAULT_PATH}` (padrao: `./vault`) | Caminho no host                      |
| Destino     | `/vault`                             | Caminho dentro do container                 |
| Modo        | `rw` (leitura e escrita)             | Permite alteracoes pelo servidor            |

### 3.5 Rede

```yaml
networks:
  growthos:
    driver: bridge
    name: growthos-network
```

| Propriedade | Valor             | Significado                              |
|-------------|-------------------|------------------------------------------|
| Driver      | `bridge`          | Rede isolada entre containers            |
| Nome        | `growthos-network`| Nome fixo para referencia externa        |

Os servicos se comunicam entre si pelo nome do servico (ex: `http://mcp-social-publish:8001`). O acesso externo e feito via `localhost` nas portas mapeadas.

### 3.6 Politica de Restart

Todos os servicos usam `restart: unless-stopped`:

| Cenario                          | Comportamento            |
|----------------------------------|--------------------------|
| Container falha (crash)          | Reinicia automaticamente |
| Docker daemon reinicia           | Reinicia automaticamente |
| `docker-compose stop` manual     | Nao reinicia             |
| `docker-compose down`            | Remove o container       |

### 3.7 Comandos Uteis

```bash
# Subir todos os servicos
docker-compose up -d

# Subir apenas um servico
docker-compose up -d mcp-social-publish

# Reconstruir imagens apos alteracao no codigo
docker-compose build
docker-compose up -d

# Ver status dos containers e health checks
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um servico especifico
docker-compose logs -f mcp-obsidian-vault

# Parar todos os servicos
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Limpar imagens antigas
docker-compose down --rmi local
```

---

## 4. CI/CD Pipeline

O GrowthOS utiliza **GitHub Actions** com 4 jobs sequenciais definidos em `.github/workflows/ci.yml`.

### 4.1 Visao Geral do Pipeline

```
push/PR para main (paths: growthOS/**)
    |
    v
[1. Lint] ---> [2. Test] ---> [3. Docker Build] ---> [4. Security Scan]
   ruff          pytest         build 3 targets        Trivy (CRITICAL/HIGH)
```

### 4.2 Triggers

```yaml
on:
  push:
    branches: [main]
    paths:
      - "growthOS/**"
  pull_request:
    branches: [main]
    paths:
      - "growthOS/**"
```

O pipeline executa **apenas** quando ha alteracoes dentro do diretorio `growthOS/`. Alteracoes em outros diretorios do monorepo nao disparam o CI.

### 4.3 Job 1: Lint (ruff)

```yaml
lint:
  name: Lint
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.11"
    - run: pip install ruff
    - run: ruff check growthOS/
    - run: ruff format --check growthOS/
```

**O que valida:**
- Regras de linting (imports, convencoes, erros comuns)
- Formatacao consistente do codigo (espacos, indentacao, line length)

**Ferramenta:** [ruff](https://docs.astral.sh/ruff/) -- linter e formatter Python ultra-rapido (escrito em Rust).

### 4.4 Job 2: Test (pytest)

```yaml
test:
  name: Test
  runs-on: ubuntu-latest
  needs: lint
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.11"
    - name: Install dependencies
      run: |
        pip install -e growthOS/shared-lib/
        pip install -r growthOS/mcp-servers/mcp-social-publish/requirements.txt
        pip install -r growthOS/mcp-servers/mcp-social-discover/requirements.txt
        pip install -r growthOS/mcp-servers/mcp-obsidian-vault/requirements.txt
        pip install pytest pytest-asyncio pytest-cov
    - name: Run tests
      run: pytest growthOS/shared-lib/tests/ -v --tb=short
```

**O que valida:**
- Testes unitarios da shared-lib
- Todas as dependencias dos 3 MCP servers instaladas corretamente
- Suporte a codigo async via `pytest-asyncio`
- Cobertura disponivel via `pytest-cov`

**Dependencia:** So executa se o job `lint` passar.

### 4.5 Job 3: Docker Build

```yaml
docker:
  name: Docker Build
  runs-on: ubuntu-latest
  needs: test
  steps:
    - uses: actions/checkout@v4
    - name: Build MCP Social Publish
      run: docker build --target mcp-social-publish -t growthos-social-publish:test growthOS/
    - name: Build MCP Social Discover
      run: docker build --target mcp-social-discover -t growthos-social-discover:test growthOS/
    - name: Build MCP Obsidian Vault
      run: docker build --target mcp-obsidian-vault -t growthos-obsidian-vault:test growthOS/
```

**O que valida:**
- Todas as 3 imagens Docker constroem com sucesso
- Dependencias de sistema e Python resolvem corretamente
- O Dockerfile multi-stage esta funcional

**Dependencia:** So executa se o job `test` passar.

### 4.6 Job 4: Security Scan (Trivy)

```yaml
security:
  name: Security Scan
  runs-on: ubuntu-latest
  needs: docker
  steps:
    - uses: actions/checkout@v4
    - name: Build image for scan
      run: docker build --target mcp-social-publish -t growthos-scan:latest growthOS/
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: growthos-scan:latest
        format: table
        exit-code: "1"
        severity: CRITICAL,HIGH
```

**O que valida:**
- Vulnerabilidades conhecidas (CVEs) nas dependencias do sistema operacional
- Vulnerabilidades em pacotes Python
- Apenas severidades **CRITICAL** e **HIGH** bloqueiam o pipeline (`exit-code: "1"`)

**Ferramenta:** [Trivy](https://trivy.dev/) -- scanner de vulnerabilidades open-source da Aqua Security.

### 4.7 Resumo do Pipeline

| Job      | Depende de | Ferramenta | Bloqueia PR? | Foco                     |
|----------|-----------|------------|-------------|--------------------------|
| Lint     | --        | ruff       | Sim         | Qualidade de codigo      |
| Test     | Lint      | pytest     | Sim         | Corretude funcional      |
| Docker   | Test      | docker     | Sim         | Build reproducivel       |
| Security | Docker    | Trivy      | Sim         | Vulnerabilidades CVE     |

---

## 5. Variaveis de Ambiente

Todas as variaveis de ambiente sao configuradas no arquivo `.env` (copiado de `.env.example`).

### 5.1 Chaves de API -- Publicacao Social

| Variavel                          | Obrigatoria  | Descricao                          |
|-----------------------------------|-------------|-------------------------------------|
| `GROWTHOS_TWITTER_API_KEY`        | Para Twitter | API Key do Twitter/X Developer     |
| `GROWTHOS_TWITTER_API_SECRET`     | Para Twitter | API Secret do Twitter/X Developer  |
| `GROWTHOS_TWITTER_ACCESS_TOKEN`   | Para Twitter | Access Token do Twitter/X          |
| `GROWTHOS_TWITTER_ACCESS_SECRET`  | Para Twitter | Access Token Secret do Twitter/X   |
| `GROWTHOS_LINKEDIN_TOKEN`         | Para LinkedIn| Token de acesso do LinkedIn        |
| `GROWTHOS_LINKEDIN_ORG_ID`        | Para LinkedIn| ID da organizacao no LinkedIn      |
| `GROWTHOS_REDDIT_CLIENT_ID`       | Para Reddit  | Client ID da app Reddit            |
| `GROWTHOS_REDDIT_CLIENT_SECRET`   | Para Reddit  | Client Secret da app Reddit        |
| `GROWTHOS_REDDIT_USERNAME`        | Para Reddit  | Username da conta Reddit           |
| `GROWTHOS_REDDIT_PASSWORD`        | Para Reddit  | Password da conta Reddit           |
| `GROWTHOS_GITHUB_TOKEN`           | Para GitHub  | Personal Access Token do GitHub    |
| `GROWTHOS_THREADS_TOKEN`          | Para Threads | Token de acesso do Threads/Meta    |

> **Nota:** Nenhuma API key e obrigatoria para instalacao. So sao necessarias para publicacao real na plataforma correspondente. O modo dry-run funciona sem nenhuma chave.

### 5.2 Configuracao do Vault

| Variavel                | Padrao     | Descricao                                   |
|-------------------------|------------|---------------------------------------------|
| `GROWTHOS_VAULT_PATH`   | `./vault`  | Caminho para o Obsidian Vault no host        |

### 5.3 Configuracao do Plugin

| Variavel                     | Padrao                | Descricao                              |
|------------------------------|-----------------------|-----------------------------------------|
| `GROWTHOS_BRAND_VOICE_PATH`  | `./brand-voice.yaml`  | Caminho para o arquivo de brand voice  |
| `GROWTHOS_CONFIG_DIR`         | `.`                   | Diretorio de configuracao              |
| `GROWTHOS_AUDIT_DIR`          | `.growthOS/audit`     | Diretorio para logs de auditoria       |

### 5.4 Autonomia e Seguranca

| Variavel                  | Padrao       | Opcoes                     | Descricao                              |
|---------------------------|-------------|----------------------------|----------------------------------------|
| `GROWTHOS_AUTONOMY_LEVEL` | `supervised` | `supervised`, `autonomous` | Nivel de autonomia do agente           |
| `GROWTHOS_DRY_RUN`        | `true`       | `true`, `false`            | Se `true`, simula acoes sem executar   |

### 5.5 Portas dos MCP Servers

| Variavel                  | Padrao | Descricao                     |
|---------------------------|--------|-------------------------------|
| `GROWTHOS_PUBLISH_PORT`    | `8001` | Porta do MCP Social Publish   |
| `GROWTHOS_DISCOVER_PORT`   | `8002` | Porta do MCP Social Discover  |
| `GROWTHOS_VAULT_PORT`      | `8003` | Porta do MCP Obsidian Vault   |

### 5.6 Boas Praticas de Seguranca

1. **Nunca commite o arquivo `.env`** -- ele ja esta no `.gitignore` e no `.dockerignore`
2. **Use `GROWTHOS_DRY_RUN=true`** durante o desenvolvimento para evitar publicacoes reais
3. **Comece com `GROWTHOS_AUTONOMY_LEVEL=supervised`** ate ter confianca no fluxo
4. **Rotacione tokens regularmente** -- especialmente tokens de redes sociais
5. **Use variaveis diferentes por ambiente** (dev, staging, producao)
6. **Verifique antes de commitar** -- `git diff --cached` para confirmar que nenhum secret esta staged
7. **Em producao, prefira Docker secrets** ou vault managers (HashiCorp Vault, AWS Secrets Manager)

---

## 6. Troubleshooting

### 6.1 Container Nao Inicia

**Sintoma:** `docker-compose up` falha ou container reinicia em loop.

```bash
# Verifique os logs do container
docker-compose logs mcp-social-publish

# Verifique o status de saude
docker inspect --format='{{.State.Health.Status}}' growthos-social-publish
```

**Causas comuns:**

| Causa                         | Solucao                                                 |
|-------------------------------|---------------------------------------------------------|
| Porta ja em uso               | `lsof -i :8001` para encontrar o processo; altere a porta no `.env` |
| `.env` ausente                | Execute `cp .env.example .env`                          |
| Dependencia Python faltando   | Reconstrua a imagem: `docker-compose build --no-cache`  |
| Permissao no volume           | Verifique permissoes do `GROWTHOS_VAULT_PATH`           |

### 6.2 Health Check Falhando

**Sintoma:** Container marcado como `unhealthy`.

```bash
# Teste o endpoint manualmente
curl -f http://localhost:8001/health

# Verifique se o servico esta respondendo dentro do container
docker exec growthos-social-publish curl -f http://localhost:8001/health
```

**Causas comuns:**

| Causa                           | Solucao                                        |
|---------------------------------|------------------------------------------------|
| Servico ainda iniciando         | Aguarde o `start_period` (10s)                 |
| Erro no codigo do servidor      | Verifique logs: `docker-compose logs -f`       |
| Curl nao instalado na imagem    | Reconstrua: `docker-compose build --no-cache`  |

### 6.3 Erro de Autenticacao em Rede Social

**Sintoma:** Servidor retorna erro 401/403 ao tentar publicar.

```bash
# Verifique se as variaveis estao carregadas no container
docker-compose exec mcp-social-publish env | grep GROWTHOS
```

**Solucoes:**
1. Verifique se as variaveis de API estao preenchidas no `.env` (nao apenas o nome da variavel)
2. Confirme que os tokens nao expiraram
3. Teste com `GROWTHOS_DRY_RUN=true` primeiro
4. Verifique as permissoes da app na plataforma (scopes/permissions)
5. Confirme que nao ha espacos ao redor do `=` no `.env`

**Erros comuns de API:**

| Erro                  | Causa                        | Solucao                                    |
|-----------------------|------------------------------|--------------------------------------------|
| 401 Unauthorized      | Token expirado ou invalido   | Regenere nas configuracoes da plataforma   |
| 403 Forbidden         | Permissoes insuficientes     | Verifique os scopes do token               |
| 429 Too Many Requests | Rate limit atingido          | O CircuitBreaker protege automaticamente   |

### 6.4 Volume do Vault Nao Monta

**Sintoma:** MCP Obsidian Vault nao encontra os arquivos do vault.

```bash
# Verifique o caminho configurado
echo $GROWTHOS_VAULT_PATH

# Verifique se o diretorio existe
ls -la ${GROWTHOS_VAULT_PATH:-./vault}

# Verifique a montagem dentro do container
docker exec growthos-obsidian-vault ls -la /vault
```

**Causas comuns:**

| Causa                              | Solucao                                     |
|------------------------------------|---------------------------------------------|
| Caminho incorreto no `.env`        | Corrija `GROWTHOS_VAULT_PATH`               |
| Diretorio nao existe               | Crie o diretorio: `mkdir -p ./vault`        |
| Permissao insuficiente             | `chmod 755` no diretorio                    |
| Caminho relativo em ambiente Docker| Use caminho absoluto no `.env`              |

### 6.5 Pipeline CI Falhando

**Lint falha (ruff):**

```bash
# Execute localmente para ver os erros
ruff check growthOS/
ruff format --check growthOS/

# Corrija automaticamente
ruff check --fix growthOS/
ruff format growthOS/
```

**Testes falham (pytest):**

```bash
# Execute os testes localmente com output detalhado
pytest shared-lib/tests/ -v --tb=long

# Execute um teste especifico
pytest shared-lib/tests/test_modulo.py -v
```

**Trivy encontra vulnerabilidades:**

```bash
# Instale o Trivy localmente
brew install trivy   # macOS
# ou
sudo apt install trivy  # Linux

# Escaneie a imagem
docker build --target mcp-social-publish -t growthos-scan:latest .
trivy image growthos-scan:latest --severity CRITICAL,HIGH

# Para corrigir: atualize python:3.11-slim e dependencias no requirements.txt
```

### 6.6 Rede Entre Containers Nao Funciona

**Sintoma:** Um servico nao consegue se comunicar com outro.

```bash
# Verifique se todos estao na mesma rede
docker network inspect growthos-network

# Teste conectividade entre containers
docker exec growthos-social-publish curl -f http://mcp-social-discover:8002/health

# Recrie a rede se necessario
docker-compose down
docker network rm growthos-network
docker-compose up -d
```

### 6.7 Docker Build Falha

```bash
# Erros comuns e solucoes:

# "COPY failed: file not found"
# -> Verifique que os diretorios existem e nao estao no .dockerignore
ls mcp-servers/mcp-social-publish/

# "pip install failed: network error"
# -> Verifique sua conexao de internet e proxy settings
docker build --network=host --target mcp-social-publish .

# "no space left on device"
# -> Limpe imagens e containers antigos
docker system prune -a
```

### 6.8 Tabela de Erros Comuns

| Erro                                | Causa                          | Solucao                                    |
|-------------------------------------|--------------------------------|--------------------------------------------|
| `Connection refused on port 8001`   | Server nao esta rodando        | `docker-compose up -d` e verifique logs    |
| `HEALTHCHECK: curl not found`       | Imagem sem curl                | Reconstrua: `docker-compose build --no-cache` |
| `Permission denied: /vault`         | Permissoes do volume           | `chmod 755` no diretorio do vault          |
| `yaml.scanner.ScannerError`         | brand-voice.yaml invalido      | Valide o YAML: `python -c "import yaml; yaml.safe_load(open('brand-voice.yaml'))"` |
| `CircuitBreaker OPEN`               | API com muitas falhas          | Aguarde o reset (60s) ou verifique a API   |
| `ModuleNotFoundError`               | Dependencia faltando           | Reconstrua imagem ou reinstale dependencias |

---

## 7. Contribuindo

### 7.1 Setup do Ambiente de Desenvolvimento

```bash
# 1. Fork e clone
git clone https://github.com/your-org/growthOS.git
cd growthOS

# 2. Instale a shared-lib em modo dev
pip install -e "shared-lib/[dev]"

# 3. Instale dependencias de todos os MCP servers
pip install -r mcp-servers/mcp-social-publish/requirements.txt
pip install -r mcp-servers/mcp-social-discover/requirements.txt
pip install -r mcp-servers/mcp-obsidian-vault/requirements.txt

# 4. Instale ferramentas de teste e linting
pip install pytest pytest-asyncio pytest-cov ruff

# 5. Configure o ambiente
cp .env.example .env
cp brand-voice.example.yaml brand-voice.yaml
```

### 7.2 Executando Testes

```bash
# Todos os testes da shared-lib
pytest shared-lib/tests/ -v

# Testes de um MCP server especifico
pytest mcp-servers/mcp-social-publish/tests/ -v

# Com cobertura de codigo
pytest --cov=shared-lib/growthOS_shared shared-lib/tests/

# Apenas testes que casam com um padrao
pytest shared-lib/tests/ -k "test_nome_do_teste" -v
```

### 7.3 Padroes de Codigo

**Linting e formatacao (ruff):**

```bash
# Verificar erros de linting
ruff check .

# Corrigir automaticamente
ruff check --fix .

# Verificar formatacao
ruff format --check .

# Formatar automaticamente
ruff format .
```

**Convencoes obrigatorias:**

| Regra                          | Exemplo                              |
|--------------------------------|--------------------------------------|
| Arquivos: `snake_case.py`      | `social_publisher.py`                |
| Classes: `PascalCase`          | `SocialPublisher`                    |
| Funcoes/variaveis: `snake_case`| `publish_post()`, `post_content`     |
| Constantes: `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT`                    |
| Env vars: prefixo `GROWTHOS_`  | `GROWTHOS_DRY_RUN`                   |
| Type hints em todas as funcoes | `def publish(content: str) -> bool:` |
| Docstrings em funcoes publicas | `"""Publica conteudo na rede."""`     |

### 7.4 Organizacao de Arquivos

```
growthOS/
  mcp-servers/
    mcp-social-publish/    # Logica do servidor de publicacao
    mcp-social-discover/   # Logica do servidor de descoberta
    mcp-obsidian-vault/    # Logica do servidor Obsidian
  shared-lib/
    growthOS_shared/       # Utilitarios compartilhados
    tests/                 # Testes da shared-lib
  agents/                  # Definicoes de agentes
  skills/                  # Definicoes de skills
  hooks/                   # Hooks do plugin
```

### 7.5 Processo de Pull Request

1. **Fork** o repositorio e crie uma branch a partir de `main`
2. **Implemente** seguindo os padroes acima
3. **Teste** suas alteracoes:
   ```bash
   ruff check .                  # Lint
   ruff format --check .         # Formatacao
   pytest shared-lib/tests/ -v   # Testes unitarios
   docker-compose build          # Build Docker (se alterou Dockerfile ou MCP servers)
   ```
4. **Documente** novas features, variaveis de ambiente ou configuracoes
5. **Submeta** o PR com descricao clara das mudancas e motivacao

### 7.6 Checklist do PR

Antes de submeter, verifique:

- [ ] Todos os testes passam (`pytest`)
- [ ] Linting passa (`ruff check .`)
- [ ] Formatacao correta (`ruff format --check .`)
- [ ] Nenhum segredo ou chave de API no codigo
- [ ] Novas variaveis de ambiente adicionadas ao `.env.example`
- [ ] README atualizado se adicionou features ou alterou o uso
- [ ] Testes adicionados para novas funcionalidades
- [ ] Docker build funciona (`docker-compose build`)

### 7.7 Convencoes de Commit

Utilize [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adicionar suporte a publicacao no Bluesky
fix: corrigir timeout no health check do vault
docs: atualizar guia de variaveis de ambiente
chore: atualizar dependencias do ruff
test: adicionar testes para brand voice parser
refactor: extrair logica de retry para shared-lib
```

### 7.8 Reportando Problemas

- Use **GitHub Issues** para bugs e feature requests
- Inclua passos de reproducao, comportamento esperado vs real
- Para questoes de seguranca, consulte `SECURITY.md`

---

## Referencia Rapida

| Acao                          | Comando                                          |
|-------------------------------|--------------------------------------------------|
| Subir todos os servicos       | `docker-compose up -d`                           |
| Parar todos os servicos       | `docker-compose down`                            |
| Ver logs                      | `docker-compose logs -f`                         |
| Reconstruir imagens           | `docker-compose build`                           |
| Verificar saude               | `docker-compose ps`                              |
| Rodar testes                  | `pytest shared-lib/tests/ -v`                    |
| Verificar linting             | `ruff check .`                                   |
| Formatar codigo               | `ruff format .`                                  |
| Scan de vulnerabilidades      | `trivy image growthos-scan:latest`               |
| Build de imagem especifica    | `docker build --target <stage> -t <tag> .`       |

---

*GrowthOS DevOps Guide v1.0*
