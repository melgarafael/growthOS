# GrowthOS -- Guia do Usuario

> Versao 2.0 | Ultima atualizacao: Abril 2026

---

## Sumario

1. [Introducao](#1-introducao)
2. [Primeiro Uso](#2-primeiro-uso)
3. [Comando /grow -- Referencia Completa](#3-comando-grow--referencia-completa)
4. [Niveis de Autonomia](#4-niveis-de-autonomia)
5. [Modo Dry Run](#5-modo-dry-run)
6. [Fluxo Tipico de Trabalho](#6-fluxo-tipico-de-trabalho)
7. [FAQ](#7-faq)

---

## 1. Introducao

### O que e o GrowthOS?

GrowthOS e a sua equipe de marketing autonoma dentro do Claude Code. Em vez de alternar entre ferramentas de escrita, agendamento de posts, analise de concorrentes e dashboards de metricas, voce usa um unico comando -- `/grow` -- e descreve o que precisa em linguagem natural. O sistema identifica a intencao, aciona o agente correto e entrega o resultado ja formatado para a plataforma de destino.

Todo conteudo produzido respeita a voz da sua marca, passa por um filtro anti-cliche (anti-slop) e pode ser revisado antes de qualquer publicacao.

### O que voce pode fazer com ele

| Necessidade | O que voce digita | O que acontece |
|---|---|---|
| Planejar conteudo do trimestre | `/grow strategy plano de conteudo Q3` | O Growth Strategist gera um calendario editorial com OKRs |
| Escrever um artigo | `/grow create blog sobre onboarding de usuarios` | O Content Creator redige o post completo na voz da sua marca |
| Publicar no LinkedIn | `/grow publish linkedin este artigo` | O Social Publisher formata e adapta para o LinkedIn |
| Analisar concorrentes | `/grow analyze nossos 5 principais concorrentes` | O Intelligence Analyst gera um relatorio SWOT |
| Pesquisar um topico | `/grow research ROI de podcast marketing` | O Intelligence Analyst compila dados, fontes e recomendacoes |
| Gerar relatorio mensal | `/grow report monthly` | O Intelligence Analyst compila KPIs e metricas do mes |

### Arquitetura em 30 segundos

```
Voce  -->  /grow "sua intencao"  -->  CMO (router)  -->  Agente especializado  -->  Resultado
```

O CMO recebe sua solicitacao, classifica a intencao via analise de linguagem natural, e delega para o agente correto. Voce nao precisa saber qual agente usar.

### Os 7 Agentes

| Agente | Papel | Quando atua |
|---|---|---|
| **CMO** | Orquestrador e router central | Sempre (ponto de entrada) |
| **Growth Strategist** | Planejamento estrategico, OKRs, calendarios | `/grow strategy` |
| **Content Creator** | Redacao de blog posts, newsletters, threads, emails | `/grow create` |
| **Intelligence Analyst** | Analise competitiva, pesquisa e relatorios | `/grow analyze`, `/grow research`, `/grow report` |
| **Social Publisher** | Distribuicao de conteudo para plataformas | `/grow publish` |
| **Visual Designer** | Graficos sociais, banners, thumbnails, infograficos | `/grow design` ou `/grow visual` |
| **Growth Engineer** | Landing pages, testes A/B, otimizacao de conversao | `/grow landing` |

### Brand Voice: conteudo com a voz da sua marca

O arquivo `brand-voice.yaml` e o DNA da sua marca dentro do GrowthOS. Ele define:

- **Tom e personalidade** -- como sua marca fala (profissional, casual, tecnico, etc.)
- **Filtro anti-slop** -- lista de frases banidas como "game-changer", "revolutionary", "unlock the power"
- **Regras por plataforma** -- tom, comprimento maximo e formato especificos para cada rede
- **Nivel de autonomia** -- quanto o sistema pode agir sem pedir confirmacao

---

## 2. Primeiro Uso

### Passo 1: Instalar o plugin GrowthOS

O GrowthOS funciona como um plugin do Claude Code. Certifique-se de que o diretorio do plugin esta acessivel no seu projeto. Apos a instalacao, o comando `/grow` ficara disponivel na sua sessao.

### Passo 2: Executar o Setup Wizard

Na primeira vez que voce rodar qualquer comando `/grow`, o sistema detecta que nao existe um arquivo `brand-voice.yaml` e exibe:

```
Welcome to GrowthOS! It looks like this is your first time here.

To get started, you need to configure your brand voice:

  /grow setup

This will walk you through setting up your brand name, tone, platforms,
and content preferences. It takes about 2 minutes.
```

Execute o wizard:

```
/grow setup
```

O assistente apresenta um banner de boas-vindas e faz 5 perguntas, uma por vez:

#### Pergunta 1 -- Nome da marca (obrigatorio)

```
Step 1/5 -- Brand Name

What's your brand or product name?
```

Exemplo de resposta: `Acme Analytics`

#### Pergunta 2 -- Tagline (opcional)

```
Step 2/5 -- Tagline

Got a one-line tagline or slogan? (press Enter to skip)

Examples:
  "Ship faster, learn faster"
  "The open-source analytics platform"
```

Exemplo de resposta: `Dados que fazem sentido`

Pressione Enter para pular.

#### Pergunta 3 -- Tom da marca (obrigatorio, com padrao)

```
Step 3/5 -- Brand Tone

Pick the tone that best matches your brand:

  1. professional  -- Polished, trustworthy, enterprise-ready
  2. casual        -- Friendly, conversational, relatable
  3. technical     -- Precise, detailed, developer-focused
  4. witty         -- Clever, sharp, personality-driven
  5. authoritative -- Expert, confident, thought-leader

Enter a number (1-5) or press Enter for default [1. professional]:
```

Cada opcao gera uma lista de adjetivos de tom:

| Escolha | Tom gerado |
|---|---|
| professional | professional, approachable |
| casual | casual, friendly, conversational |
| technical | technical, precise, developer-focused |
| witty | witty, sharp, engaging |
| authoritative | authoritative, confident, expert |

Se voce pressionar Enter sem digitar nada, o padrao sera `professional`.

#### Pergunta 4 -- Industria (obrigatorio, com padrao)

```
Step 4/5 -- Industry

What industry are you in?

  1. saas       -- Software as a Service
  2. devtools   -- Developer Tools & Infrastructure
  3. fintech    -- Financial Technology
  4. ecommerce  -- E-Commerce & Retail
  5. other      -- Something else (specify)

Enter a number (1-5) or press Enter for default [1. saas]:
```

Se voce escolher `5. other`, o sistema perguntara qual e a sua industria (ex: healthcare, education, gaming).

#### Pergunta 5 -- Plataformas (multi-selecao)

```
Step 5/5 -- Platforms

Which platforms do you want to create content for?
Select all that apply (comma-separated numbers):

  1. LinkedIn    -- Professional networking, thought leadership
  2. Twitter/X   -- Short-form, real-time engagement
  3. Reddit      -- Community discussions, authentic engagement
  4. GitHub      -- Technical content, READMEs, releases
  5. Threads     -- Casual social, short-form

Enter numbers (e.g., 1,2,4) or press Enter for all:
```

Exemplo de resposta: `1,2,4` (LinkedIn, Twitter/X e GitHub). Pressionar Enter habilita todas.

### Passo 3: Resultado do setup

Apos as 5 perguntas, o GrowthOS:

1. **Gera o arquivo `brand-voice.yaml`** no diretorio raiz do projeto
2. **Cria um post de demonstracao** na primeira plataforma selecionada, usando o tom e industria que voce configurou
3. **Exibe um resumo** da configuracao com sugestoes de proximos comandos:

```
Setup Complete!

  Brand:      Acme Analytics
  Tone:       professional, approachable
  Industry:   saas
  Platforms:  linkedin, twitter, github
  Config:     brand-voice.yaml

What you can do now:

  /grow create a blog post about [your topic]
  /grow create a LinkedIn post announcing [news]
  /grow create a Twitter thread about [insight]
  /grow strategy plan our content calendar
  /grow analyze our competitors in saas
  /grow research trends in saas

  /grow setup --reset    Re-run this wizard anytime
```

### Passo 4: Seu primeiro comando real

Agora teste com algo concreto:

```
/grow create um post no LinkedIn anunciando o lancamento da versao 2.0
```

O Content Creator vai redigir o post usando o tom, personalidade e regras anti-slop que voce acabou de configurar.

### Reconfigurando a qualquer momento

Se voce precisar alterar a configuracao da marca:

```
/grow setup --reset
```

Isso faz backup do `brand-voice.yaml` atual (com timestamp, ex: `brand-voice.backup-2026-04-01-143022.yaml`) e reinicia o wizard do zero.

Se o setup for executado sem `--reset` e ja existir um `brand-voice.yaml`, o sistema pergunta se voce quer reconfigurar ou cancelar.

### Nota de seguranca

O wizard de setup **nunca pede API tokens, credenciais, senhas ou secrets**. Ele configura apenas a identidade da marca. Chaves de API de plataformas pertencem ao seu arquivo `.env` e sao responsabilidade sua.

---

## 3. Comando /grow -- Referencia Completa

### Linguagem natural

Voce nao precisa decorar subcomandos. O GrowthOS aceita linguagem natural e roteia automaticamente para o agente correto:

```
/grow escreva um artigo sobre metricas de produto
/grow quero analisar o que nossos concorrentes estao fazendo no LinkedIn
/grow gere um relatorio semanal de performance
/grow planeje nossa estrategia de conteudo para o proximo trimestre
/grow pesquise tendencias de IA generativa em 2026
/grow crie um post anunciando nosso novo recurso
```

O CMO classifica a intencao usando palavras-chave e contexto semantico:

| Intencao | Palavras-gatilho |
|---|---|
| strategy | plan, strategy, OKR, roadmap, calendar, campaign, go-to-market, GTM |
| create | write, create, draft, blog, article, newsletter, email, thread, content |
| publish | publish, post (distribuir), share, schedule, distribute, send |
| analyze | analyze, competitor, market, trend, SWOT, benchmark, compare |
| research | research, find, explore, discover, investigate, look into |
| report | report, summary, metrics, performance, dashboard, KPIs |
| visual | design, visual, image, graphic, thumbnail, banner, infographic |
| landing | landing page, conversion, A/B test, CRO, funnel |

**Regras de desambiguacao:**

- O verbo principal determina a intencao. "Escreva um post" = create. "Publique um post" = publish.
- Se o conteudo ja existe na conversa, "post" roteia para publish. Se e novo, roteia para create.
- Se a confianca for baixa (abaixo de 60%), o CMO faz UMA pergunta de esclarecimento e segue em frente.

### Pipelines automaticos

Se o seu pedido envolve mais de um agente, o GrowthOS detecta e executa em sequencia:

| Padrao detectado | Exemplo | Pipeline |
|---|---|---|
| "crie e publique" | `/grow crie um post e publique no LinkedIn` | Content Creator -> Social Publisher |
| "escreva com imagem" | `/grow blog post com OG image` | Content Creator -> Visual Designer |
| "pesquise e escreva" | `/grow pesquise sobre PLG e escreva um artigo` | Intelligence Analyst -> Content Creator |
| "crie, desenhe e publique" | `/grow campanha completa end-to-end` | Content Creator -> Visual Designer -> Social Publisher |

O progresso e exibido entre as etapas:

```
Pipeline: Research -> Create -> Publish
[1/3] Intelligence Analyst -- pesquisando...
[2/3] Content Creator -- escrevendo...
[3/3] Social Publisher -- aguardando confirmacao...
```

### Sem argumentos

Se voce digitar `/grow` sem nada, o sistema exibe o menu de boas-vindas com exemplos e todos os subcomandos disponiveis.

---

### 3.1 Subcomando: `strategy`

**Sintaxe:** `/grow strategy [topico]`
**Agente:** Growth Strategist
**Funcao:** Planejamento estrategico, OKRs, calendarios de conteudo, go-to-market

**Sem argumentos** (`/grow strategy`): exibe a ajuda com exemplos.

**Exemplo 1 -- Calendario editorial:**

```
/grow strategy calendario de conteudo Q3 focado em developer marketing
```

Gera um plano trimestral com temas semanais, formatos sugeridos por semana (blog, thread, carousel, newsletter) e KPIs de acompanhamento por canal.

**Exemplo 2 -- OKRs de marketing:**

```
/grow strategy OKRs de marketing para o proximo semestre
```

Cria objetivos e resultados-chave alinhados a metas de crescimento. Inclui metricas de acompanhamento, responsaveis sugeridos e cadencia de revisao.

**Exemplo 3 -- Go-to-market:**

```
/grow strategy go-to-market para lancamento do produto Enterprise
```

Monta um plano de lancamento com fases (pre-launch, launch day, post-launch), canais prioritarios, mensagens-chave por audiencia e cronograma detalhado.

---

### 3.2 Subcomando: `create`

**Sintaxe:** `/grow create [tipo] [topico]`
**Agente:** Content Creator
**Funcao:** Redacao de conteudo com brand voice aplicada automaticamente

**Tipos disponiveis:**

| Tipo | Descricao |
|---|---|
| `blog` | Post longo / artigo para blog |
| `social` | Post otimizado para rede social |
| `newsletter` | Edicao de newsletter por email |
| `email` | Copy de email (onboarding, outreach, etc.) |
| `thread` | Thread multi-post (Twitter/X, LinkedIn) |
| `article` | Artigo aprofundado / thought leadership |
| `carousel` | Conteudo em slides para carousel |

**Sem argumentos** (`/grow create`): exibe a ajuda com tipos e exemplos.

**Exemplo 1 -- Blog post:**

```
/grow create blog como medir product-market fit com dados reais
```

Redige um artigo completo com titulo otimizado, introducao com gancho, secoes com subtitulos, exemplos praticos e conclusao com CTA. O filtro anti-slop garante que nenhuma frase banida apareca no texto.

**Exemplo 2 -- Thread:**

```
/grow create thread 7 licoes que aprendemos escalando de 0 a 10k usuarios
```

Gera uma thread com 7+ posts encadeados. Cada post tem seu proprio gancho e flui como narrativa, respeitando o limite de caracteres da plataforma.

**Exemplo 3 -- Newsletter:**

```
/grow create newsletter digest semanal para assinantes
```

Monta uma edicao de newsletter com destaques da semana, links curados, secoes tematicas e CTA final. O tom segue a configuracao do `brand-voice.yaml`.

**Dica:** voce pode omitir o tipo e descrever naturalmente:

```
/grow create um post no LinkedIn sobre tendencias de trabalho remoto
```

O agente infere o formato mais adequado com base no contexto.

---

### 3.3 Subcomando: `publish`

**Sintaxe:** `/grow publish [plataforma] [conteudo]`
**Agente:** Social Publisher
**Funcao:** Distribuicao de conteudo para plataformas configuradas

**Plataformas suportadas:**

| Plataforma | Keyword | Max Length | Tom Override |
|---|---|---|---|
| LinkedIn | `linkedin` | 3000 chars | Usa o tom padrao da marca |
| Twitter/X | `twitter` ou `x` | 280 chars | `concise_witty` |
| Reddit | `reddit` | 10000 chars | `authentic_casual` |
| GitHub | `github` | Sem limite | `technical_precise` |
| Threads | `threads` | 500 chars | Usa o tom padrao da marca |
| YouTube | `youtube` | 5000 chars | Usa o tom padrao da marca |
| Instagram | `instagram` | 2200 chars | `visual_engaging` |
| StackOverflow | `stackoverflow` | 30000 chars | `technical_helpful` |

**Sem argumentos** (`/grow publish`): exibe a ajuda com plataformas e exemplos.

**Exemplo 1 -- LinkedIn:**

```
/grow publish linkedin este blog post
```

Adapta o conteudo recem-criado para o formato do LinkedIn (ate 3000 caracteres), adiciona hashtags relevantes (se habilitado na config) e apresenta o resultado como preview.

**Exemplo 2 -- Twitter thread:**

```
/grow publish twitter thread sobre nosso lancamento
```

Formata o conteudo como uma thread no Twitter/X, respeitando o limite de 280 caracteres por post e aplicando o tom `concise_witty`.

**Exemplo 3 -- Reddit:**

```
/grow publish reddit r/programming este artigo
```

Adapta o tom para `authentic_casual` (override configurado para o Reddit) e formata para o subreddit indicado. Remove jargao corporativo automaticamente.

**Dica:** apos criar conteudo com `/grow create`, basta referenciar o que acabou de ser gerado:

```
/grow publish this to linkedin
```

O agente detecta o conteudo recem-criado na conversa e o utiliza automaticamente.

---

### 3.4 Subcomando: `analyze`

**Sintaxe:** `/grow analyze [assunto]`
**Agente:** Intelligence Analyst
**Funcao:** Analise competitiva, pesquisa de mercado, SWOT, benchmarking

**Sem argumentos** (`/grow analyze`): exibe a ajuda com tipos de analise e exemplos.

**Exemplo 1 -- Concorrentes:**

```
/grow analyze nossos 3 principais concorrentes no mercado de analytics
```

Gera um relatorio comparativo com pontos fortes, fracos, oportunidades e ameacas (SWOT) de cada concorrente, posicionamento relativo e recomendacoes.

**Exemplo 2 -- Gaps de conteudo:**

```
/grow analyze gaps de conteudo no nosso blog vs concorrentes
```

Identifica topicos que concorrentes cobrem e voce nao, com sugestoes de conteudo para preencher as lacunas e estimativa de impacto por topico.

**Exemplo 3 -- Precificacao:**

```
/grow analyze posicionamento de preco no segmento SaaS mid-market
```

Compara modelos de precificacao, faixas de preco, estrategias de empacotamento e posicionamento de valor dos competidores no segmento.

---

### 3.5 Subcomando: `research`

**Sintaxe:** `/grow research [topico]`
**Agente:** Intelligence Analyst
**Funcao:** Pesquisa aprofundada, exploracao de topicos, coleta de dados com fontes

**Sem argumentos** (`/grow research`): exibe a ajuda com exemplos.

**Exemplo 1 -- Melhores praticas:**

```
/grow research melhores praticas de email marketing B2B em 2026
```

Pesquisa e compila as praticas mais atuais com estatisticas, estudos de caso, recomendacoes acionaveis e fontes citadas.

**Exemplo 2 -- Atividade de concorrentes:**

```
/grow research o que concorrentes estao publicando no LinkedIn esta semana
```

Investiga a atividade recente de concorrentes na plataforma, identifica padroes de conteudo, frequencia de publicacao e temas dominantes.

**Exemplo 3 -- ROI de canal:**

```
/grow research ROI de podcast como canal de marketing para devtools
```

Coleta dados sobre custos medios de producao, metricas de alcance, taxas de conversao e casos reais de empresas do setor.

**Dica:** os resultados de pesquisa alimentam a criacao de conteudo. Use em sequencia:

```
/grow research tendencias de IA em marketing
```

Depois:

```
/grow create blog com base na pesquisa anterior sobre IA em marketing
```

---

### 3.6 Subcomando: `report`

**Sintaxe:** `/grow report [periodo] [foco]`
**Agente:** Intelligence Analyst
**Funcao:** Relatorios de performance, metricas, KPIs

**Periodos disponiveis:**

| Periodo | Keyword | Abrangencia |
|---|---|---|
| Semanal | `weekly` ou `last-week` | Ultimos 7 dias |
| Mensal | `monthly` ou `last-month` | Ultimos 30 dias |
| Trimestral | `quarterly` ou `last-quarter` | Ultimos 90 dias |
| Anual | `yearly` | Ultimos 365 dias |
| Acumulado no ano | `ytd` | Do inicio do ano ate hoje |

**Sem argumentos** (`/grow report`): gera um relatorio mensal por padrao.

**Exemplo 1 -- Mensal geral:**

```
/grow report monthly
```

Gera um relatorio mensal completo com metricas de todos os canais habilitados, comparativo com o mes anterior, top posts e recomendacoes.

**Exemplo 2 -- Semanal com foco:**

```
/grow report weekly social media performance
```

Foca nas metricas de redes sociais da ultima semana: engajamento, alcance, crescimento de seguidores, melhores horarios de publicacao.

**Exemplo 3 -- Trimestral de ROI:**

```
/grow report quarterly ROI de conteudo
```

Compila o retorno sobre investimento em conteudo dos ultimos 3 meses, com grafico de tendencia, custo por lead e recomendacoes de otimizacao.

---

### 3.7 Subcomando: `setup`

**Sintaxe:** `/grow setup [--reset]`
**Funcao:** Wizard interativo de configuracao da marca

Ja coberto em detalhes na secao [Primeiro Uso](#2-primeiro-uso).

| Uso | Efeito |
|---|---|
| `/grow setup` | Inicia o wizard (ou pergunta se quer reconfigurar, caso ja exista config) |
| `/grow setup --reset` | Faz backup do `brand-voice.yaml` atual e reinicia o wizard do zero |

---

## 4. Niveis de Autonomia

O GrowthOS oferece 3 niveis de autonomia, configurados no campo `autonomy.level` do `brand-voice.yaml`.

### Manual (`manual`)

```yaml
autonomy:
  level: manual
  require_preview: true
  dry_run_default: true
  kill_switch: true
```

**Comportamento:**

- O sistema pede confirmacao antes de CADA acao
- Todo conteudo e apresentado como preview antes de ser finalizado
- Dry run ativado por padrao (simula sem executar)
- Maximo controle, ideal para quem esta comecando

**Fluxo na pratica:**

```
Voce: /grow create social anuncio de nova feature
GrowthOS: [mostra draft] Aprovar? (s/n)
Voce: s
GrowthOS: [conteudo salvo] Publicar em alguma plataforma? (s/n)
Voce: s, LinkedIn
GrowthOS: [mostra preview adaptado] Confirmar publicacao? (s/n)
Voce: s
GrowthOS: [publicado]
```

**Quando usar:** Primeiras semanas de uso, lancamentos de marca, comunicacoes de crise, conteudo regulado (fintech, saude).

### Semi-automatico (`semi`) -- padrao recomendado

```yaml
autonomy:
  level: semi
  require_preview: true
  dry_run_default: true
  kill_switch: true
```

**Comportamento:**

- Criacao de conteudo, pesquisa e analise rodam automaticamente
- Publicacao e distribuicao sempre pedem confirmacao
- Apresenta preview antes de acoes externas
- Equilibrio entre velocidade e controle

**Fluxo na pratica:**

```
Voce: /grow create social anuncio de nova feature
GrowthOS: [cria o conteudo automaticamente e exibe o resultado]

Voce: /grow publish linkedin
GrowthOS: [mostra preview adaptado] Confirmar publicacao? (s/n)
Voce: s
GrowthOS: [publicado]
```

**Quando usar:** Operacao do dia a dia, maioria dos cenarios.

### Automatico (`auto`)

```yaml
autonomy:
  level: auto
  require_preview: false
  dry_run_default: false
  kill_switch: true
```

**Comportamento:**

- O sistema cria, formata e publica sem pedir confirmacao
- Nao exibe preview intermediario
- Executa pipelines completos de ponta a ponta
- Maximo velocidade, menor controle intermediario

**Fluxo na pratica:**

```
Voce: /grow crie um post sobre IA e publique no LinkedIn
GrowthOS: [cria -> adapta -> publica -> loga no audit trail]
          Publicado com sucesso no LinkedIn.
```

**Quando usar:** Fluxos ja validados, conteudo de rotina, alta confianca na brand voice.

### Como alterar o nivel

Edite diretamente o campo `autonomy.level` no arquivo `brand-voice.yaml`:

```yaml
autonomy:
  level: semi   # Opcoes: manual | semi | auto
```

Ou execute o setup novamente para reconfigurar tudo:

```
/grow setup --reset
```

A alteracao no YAML e aplicada imediatamente na proxima execucao de qualquer comando `/grow`.

### Kill Switch

O campo `kill_switch: true` garante que voce pode interromper qualquer operacao a qualquer momento, em qualquer nivel de autonomia. Mesmo no modo `auto`, se voce intervir durante a execucao, o sistema para imediatamente e aguarda instrucoes. Nenhuma acao parcial e publicada.

```yaml
autonomy:
  kill_switch: true   # Sempre habilitado por padrao
```

Recomendacao: **nunca desabilite o kill switch.** Ele e sua ultima linha de defesa contra publicacoes acidentais.

---

## 5. Modo Dry Run

### O que e?

O modo Dry Run simula a execucao completa de um comando sem realizar acoes permanentes. E como um ensaio geral -- voce ve exatamente o que o GrowthOS faria, mas nada e publicado, enviado ou salvo definitivamente.

### O que ele simula?

| Acao | No modo normal | No Dry Run |
|---|---|---|
| Criacao de conteudo | Gera e salva o conteudo | Gera o conteudo e exibe como preview, sem salvar |
| Publicacao em plataformas | Publica na plataforma | Mostra como o post ficaria, sem publicar |
| Pipelines multi-agente | Executa todas as etapas | Executa todas as etapas e mostra o resultado de cada uma |
| Relatorios | Gera o relatorio completo | Gera e marca como simulacao |
| Alteracoes em arquivos | Salva no disco | Mostra o diff do que seria alterado, sem salvar |

Quando o Dry Run esta ativo, as saidas sao prefixadas com `[DRY RUN]`:

```
[DRY RUN] Post simulado no LinkedIn -- nenhum conteudo foi publicado.
[DRY RUN] Conteudo gerado com sucesso. Deseja aplicar? (sim/nao)
```

### Como ativar

O Dry Run e controlado pelo campo `dry_run_default` no `brand-voice.yaml`:

```yaml
autonomy:
  dry_run_default: true    # true = dry run ativo por padrao
```

Quando `dry_run_default: true`, toda execucao e uma simulacao ate que voce confirme explicitamente. O sistema apresenta o resultado completo e permite que voce decida se quer prosseguir.

### Quando usar o Dry Run

| Cenario | Por que usar Dry Run |
|---|---|
| Primeiros dias com o GrowthOS | Entender o que cada comando faz antes de confiar no automatico |
| Conteudo novo ou experimental | Ver o resultado antes de comprometer com publicacao |
| Testes de brand voice | Verificar se o tom esta correto apos mudancas no `brand-voice.yaml` |
| Demonstracoes para a equipe | Mostrar o GrowthOS para colegas sem risco de publicar algo por acidente |
| Treinamento de novos membros | Permitir que explorem o sistema livremente |

### Desativando o Dry Run

Para desativar o modo de simulacao:

```yaml
autonomy:
  dry_run_default: false
```

Com `dry_run_default: false`, os comandos executam diretamente (ainda respeitando o nivel de autonomia). No modo `semi`, voce ainda recebe previews antes de publicacoes. No modo `manual`, toda acao pede confirmacao. O Dry Run e uma camada adicional de protecao, nao um substituto para os niveis de autonomia.

---

## 6. Fluxo Tipico de Trabalho

Vamos percorrer um ciclo completo de marketing de conteudo usando o GrowthOS. O cenario: voce precisa planejar, criar, publicar e medir o resultado de uma campanha de conteudo mensal sobre Product-Led Growth.

### Etapa 1: Estrategia

Comece planejando o que voce vai produzir este mes:

```
/grow strategy calendario de conteudo para abril focado em product-led growth
```

**O que acontece:** O Growth Strategist analisa o contexto da sua marca (industria, tom, plataformas habilitadas) e gera um plano completo:

```
Calendario de Conteudo -- Abril 2026
Tema central: Product-Led Growth

Semana 1: "O que e PLG e por que importa"
  - Blog post (terca) + Thread LinkedIn (quarta) + Newsletter (sexta)

Semana 2: "Metricas que importam em PLG"
  - Blog post (terca) + Carousel LinkedIn (quinta)

Semana 3: "Estudo de caso: como empresas cresceram com PLG"
  - Artigo longo (terca) + Thread Twitter (quarta)

Semana 4: "Checklist: sua empresa esta pronta para PLG?"
  - Blog post (terca) + Post social em todas as plataformas (quinta)

KPIs do mes:
  - 4 blog posts publicados
  - 8 posts sociais
  - 2 newsletters
  - Meta: 15% aumento em trafego organico
```

### Etapa 2: Pesquisa

Antes de escrever, aprofunde-se no topico da primeira semana:

```
/grow research melhores exemplos de product-led growth em SaaS em 2026
```

**O que acontece:** O Intelligence Analyst pesquisa fontes atuais e compila empresas referencia em PLG com dados de crescimento, estatisticas relevantes, citacoes e fontes para usar no conteudo, e tendencias emergentes do setor.

### Etapa 3: Criacao de conteudo

Use a pesquisa como base para o primeiro blog post:

```
/grow create blog o que e product-led growth e por que sua empresa SaaS deveria adotar
```

**O que acontece:** O Content Creator redige o artigo completo com titulo otimizado, introducao com gancho, secoes com subtitulos, exemplos concretos (alimentados pela pesquisa da etapa anterior), conclusao com CTA, tudo no tom definido no `brand-voice.yaml` e com filtro anti-slop aplicado.

### Etapa 4: Publicacao

Publique o conteudo adaptado para cada plataforma:

```
/grow publish linkedin este artigo
```

O Social Publisher adapta o conteudo para o formato do LinkedIn (ate 3000 caracteres, com hashtags) e apresenta o preview. No modo `semi`, aguarda sua confirmacao antes de publicar.

Para o Twitter, crie uma thread complementar:

```
/grow publish twitter thread resumindo o artigo sobre PLG
```

O agente cria uma thread separada, otimizada para o formato do Twitter/X (280 caracteres por post, tom `concise_witty`).

### Etapa 5: Analise

No meio do mes, veja como os concorrentes estao se posicionando:

```
/grow analyze o que concorrentes estao publicando sobre product-led growth
```

**O que acontece:** O Intelligence Analyst mapeia o conteudo recente de concorrentes sobre o tema, identifica lacunas e oportunidades, e sugere ajustes na estrategia para as semanas restantes do mes.

### Etapa 6: Relatorio

No final do mes, compile os resultados:

```
/grow report monthly performance de conteudo
```

**O que acontece:** O Intelligence Analyst gera um relatorio com metricas de cada canal (alcance, engajamento, cliques), comparativo com o mes anterior, posts de melhor performance, recomendacoes para o proximo mes e resumo executivo.

### Resumo visual do fluxo

```
strategy --> research --> create --> publish --> analyze --> report
    |            |           |          |           |          |
 Planeja o   Pesquisa o  Escreve o  Distribui   Monitora   Compila
 que fazer   tema a      conteudo   nas redes   resultados metricas
             fundo
```

Esse ciclo se repete mensalmente. Com o tempo, os relatorios alimentam a estrategia do proximo ciclo, criando um loop de melhoria continua.

---

## 7. FAQ

### 1. Preciso de API keys de redes sociais para usar o GrowthOS?

Nao para comecar. O GrowthOS cria e formata conteudo localmente. A publicacao efetiva em plataformas depende de integracoes que voce configura separadamente via MCP servers ou APIs no seu arquivo `.env`. O comando `/grow setup` nunca pede credenciais -- ele configura apenas a identidade da marca.

### 2. O GrowthOS publica automaticamente nas minhas redes?

Depende do nivel de autonomia. No modo `manual` e `semi` (padrao), publicacao sempre pede confirmacao. No modo `auto`, pode publicar diretamente se as integracoes estiverem configuradas. Em qualquer modo, o kill switch permite interromper a qualquer momento.

### 3. Posso usar o GrowthOS para mais de uma marca?

Sim. Cada projeto ou diretorio pode ter seu proprio `brand-voice.yaml`. Navegue ate o diretorio do projeto e execute `/grow setup` para configurar uma brand voice diferente. O sistema tambem aceita a variavel de ambiente `GROWTHOS_CONFIG_DIR` para apontar para um diretorio de configuracao customizado.

### 4. O que e o filtro anti-slop e posso personaliza-lo?

E uma lista de frases cliche e vazias de significado que o GrowthOS bloqueia automaticamente no conteudo gerado. Frases como "game-changer", "revolutionary", "unlock the power" e "in today's fast-paced" sao removidas e substituidas por linguagem mais especifica. Voce pode personalizar adicionando frases ao campo `anti_slop.custom_banned` no `brand-voice.yaml`:

```yaml
anti_slop:
  custom_banned:
    - "de ponta"
    - "solucao inovadora"
    - "lider de mercado"
```

### 5. O que acontece se eu digitar algo que o GrowthOS nao entende?

Se a confianca da classificacao for baixa, o CMO faz UMA pergunta de esclarecimento. Se mesmo assim nao for possivel determinar a intencao, ele exibe a lista de capacidades disponiveis para voce escolher. O sistema nunca executa uma acao ambigua sem confirmacao.

### 6. Posso personalizar o tom por plataforma?

Sim. Cada plataforma no `brand-voice.yaml` tem um campo `tone_override` que permite ajustar o tom especificamente para aquela rede:

```yaml
platforms:
  twitter:
    tone_override: "concise_witty"    # Mais curto e espirituoso
  reddit:
    tone_override: "authentic_casual" # Mais casual e autentico
  github:
    tone_override: "technical_precise" # Tecnico e preciso
  linkedin:
    tone_override: null                # Usa o tom padrao da marca
```

Se `tone_override` for `null`, o tom padrao definido em `brand.tone` e utilizado.

### 7. Qual a diferenca entre `/grow analyze` e `/grow research`?

`analyze` foca em avaliar algo que ja existe -- um concorrente, um mercado, a performance do seu conteudo. `research` foca em descobrir e aprender sobre um topico novo -- melhores praticas, tendencias, oportunidades. Ambos usam o Intelligence Analyst, mas em modos diferentes.

### 8. Como vejo o que o GrowthOS faria sem executar nada?

Ative o modo Dry Run no `brand-voice.yaml`:

```yaml
autonomy:
  dry_run_default: true
```

Toda execucao se torna uma simulacao. Voce ve o resultado completo, prefixado com `[DRY RUN]`, e decide se quer aplicar. Consulte a secao [Modo Dry Run](#5-modo-dry-run) para detalhes.

### 9. Perdi minha configuracao. Como recupero?

Se voce usou `/grow setup --reset` anteriormente, existe um backup automatico com timestamp, por exemplo: `brand-voice.backup-2026-04-01-143022.yaml`. Renomeie o backup para `brand-voice.yaml` e esta pronto. Se nao houver backup, execute `/grow setup` novamente -- leva cerca de 2 minutos.

### 10. O GrowthOS funciona para empresas fora do setor de tecnologia?

Sim. Na etapa de industria do setup, escolha `5. other` e especifique sua area (educacao, saude, varejo, gastronomia, etc.). O GrowthOS adapta o conteudo, exemplos e contexto a sua industria. As plataformas, tipos de conteudo e todas as funcionalidades operam da mesma forma independentemente do setor.

---

## Referencia Rapida

| Acao | Comando |
|---|---|
| Configurar marca | `/grow setup` |
| Reconfigurar marca | `/grow setup --reset` |
| Planejar estrategia | `/grow strategy [topico]` |
| Criar conteudo | `/grow create [tipo] [topico]` |
| Publicar conteudo | `/grow publish [plataforma] [conteudo]` |
| Analisar concorrentes | `/grow analyze [assunto]` |
| Pesquisar topico | `/grow research [topico]` |
| Gerar relatorio | `/grow report [periodo] [foco]` |
| Ver ajuda geral | `/grow` (sem argumentos) |

---

> **Precisa de ajuda?** Use `/grow` sem argumentos para ver o menu com todos os comandos disponiveis.
>
> **GrowthOS** -- Sua equipe de marketing autonoma.
