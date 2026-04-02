# Guia dos Agentes GrowthOS

Referencia completa dos 7 agentes especialistas e do orquestrador CMO que compoe a equipe autonoma de marketing do GrowthOS.

---

## Sumario

1. [Como Funcionam os Agentes](#como-funcionam-os-agentes)
2. [CMO — Chief Marketing Officer](#cmo--chief-marketing-officer)
3. [Content Creator](#content-creator)
4. [Growth Strategist](#growth-strategist)
5. [Social Publisher](#social-publisher)
6. [Intelligence Analyst](#intelligence-analyst)
7. [Visual Designer](#visual-designer)
8. [Growth Engineer](#growth-engineer)
9. [Fluxo de Delegacao](#fluxo-de-delegacao)
10. [Referencia de Output Contracts](#referencia-de-output-contracts)

---

## Como Funcionam os Agentes

### Arquitetura Geral

O GrowthOS opera como uma equipe de marketing autonoma composta por **7 agentes especialistas** coordenados por um **agente orquestrador (CMO)**. Cada agente possui uma responsabilidade bem definida, skills especificas que carrega, e um contrato de saida (output contract) padronizado.

```
Usuario
  |
  v
+-----------------------------------------+
|           CMO (Orquestrador)            |
| Classifica intencao -> Delega -> Valida |
+------+------+------+------+------+------+
       |      |      |      |      |
       v      v      v      v      v
  +------+ +------+ +------+ +------+ +------+
  |Strat.| |Cont. | |Intel.| |Visual| |Growth|
  |      | |Creat.| |Analy.| |Desig.| |Engin.|
  +--+---+ +--+---+ +------+ +------+ +------+
     |        |
     |        v
     |    +------+
     |    |Social|
     |    |Publi.|
     |    +------+
     |
     v
  (Delegacao direta ou via pipeline)
```

### CMO como Roteador de Intencoes

O CMO e o **unico ponto de entrada** para todas as interacoes de marketing. Ele nunca cria conteudo, nunca publica posts, nunca analisa dados diretamente. Sua funcao e:

1. **Classificar a intencao** do usuario em uma categoria (STRATEGY, CREATE, PUBLISH, RESEARCH, VISUAL, LANDING, PIPELINE)
2. **Delegar** para o agente especialista correto com um brief estruturado
3. **Validar a qualidade** do output antes de entregar ao usuario
4. **Orquestrar pipelines** quando a requisicao envolve multiplos agentes

### Sistema de Classificacao de Intent

Toda mensagem do usuario passa pelo classificador de intent do CMO:

| Intent | Agente Delegado | Descricao |
|--------|----------------|-----------|
| STRATEGY | growth-strategist | Planos, frameworks, OKRs, campanhas, posicionamento |
| CREATE | content-creator | Conteudo escrito — blog, posts, newsletters, emails, copy |
| PUBLISH | social-publisher | Publicacao, agendamento, distribuicao em plataformas |
| RESEARCH | intelligence-analyst | Pesquisa de mercado, analise competitiva, tendencias |
| REPORT | intelligence-analyst | Relatorios de performance, metricas, dashboards, KPIs |
| VISUAL | visual-designer | Imagens, graficos, thumbnails, assets visuais |
| LANDING | growth-engineer | Landing pages, CRO, testes A/B, analytics |
| PIPELINE | CMO orquestra | Workflows multi-agente em sequencia |
| CONFIGURE | CMO direto | Setup, brand voice, conexoes de plataforma |
| STATUS | CMO direto | Checar campanhas, analytics, conteudo agendado |
| HELP | CMO direto | Explicar funcionalidades do GrowthOS |

### Brand Voice como Lei

Todos os agentes carregam o arquivo `brand-voice.yaml` como primeira acao obrigatoria antes de qualquer output. Esse arquivo define tom, personalidade, frases banidas (anti-slop), e overrides por plataforma. Nenhum agente produz conteudo de marketing sem esse contexto.

### Niveis de Autonomia

O comportamento de todos os agentes respeita o nivel de autonomia configurado no `brand-voice.yaml`:

| Nivel | Comportamento |
|-------|--------------|
| `manual` | Sempre mostra preview antes de qualquer acao. Confirma cada passo. |
| `semi` | Preview antes de publicar. Pesquisa e estrategia executam autonomamente. |
| `auto` | Executa pipelines completos sem pausas. So para em erros ou ambiguidade. |

Quando `kill_switch: true`, o usuario pode dizer "stop" a qualquer momento para interromper toda atividade de agentes.

---

## CMO — Chief Marketing Officer

**Nome:** `cmo`
**Funcao:** Orquestrador e roteador central da equipe de marketing
**Modelo:** sonnet
**Tools:** Read, Glob, Grep, Bash, Agent, WebSearch, WebFetch

### O Que Faz

O CMO e o gerente da equipe. Ele nao executa tarefas de marketing diretamente — classifica a intencao do usuario, monta um brief estruturado, delega ao especialista correto, e valida a qualidade do resultado antes de entregar.

### Skills Carregadas

O CMO nao carrega skills especializadas. Em vez disso, ele aciona os agentes que carregam suas proprias skills. Para requisicoes simples (configuracao, status, ajuda), ele responde diretamente.

### Triggers

- Qualquer requisicao de marketing que chegue ao sistema
- Invocacao via `/grow`
- Intents ambiguos que precisam de classificacao
- Requisicoes que envolvem multiplos agentes (pipelines)

### Workflow Principal

1. **Carrega brand voice** (obrigatorio, primeira acao)
2. **Classifica intent** em uma das categorias definidas
3. **Monta delegation brief** com contexto de marca, plataforma, audiencia e constraints
4. **Delega ao agente** especialista
5. **Aplica quality gate** no output recebido (anti-slop, brand voice, completude, acionabilidade)
6. **Entrega ao usuario** com proximos passos sugeridos

### Quality Gate do CMO

Todo output passa por validacao antes de chegar ao usuario:

| Dimensao | Peso | Limiar |
|----------|------|--------|
| Alinhamento de marca | 25% | >= 4/5 |
| Anti-slop | 25% | 5/5 (tolerancia zero) |
| Relevancia ao pedido | 20% | >= 4/5 |
| Acionabilidade | 15% | >= 3/5 |
| Especificidade | 15% | >= 3/5 |

- Score ponderado >= 4.0: entrega ao usuario
- Score 3.0 a 3.9: revisa a dimensao mais fraca e re-valida
- Score < 3.0: re-delega com brief mais especifico

### Perguntas de Clarificacao

O CMO pergunta quando:
- Intent e ambiguo (poderia ser STRATEGY ou CREATE)
- Nenhuma plataforma foi especificada para conteudo
- Nenhuma audiencia/persona esta definida para trabalho estrategico
- Requisicao e ampla demais para produzir output de qualidade
- Brand voice nao esta configurado ainda

Regras: maximo 2 perguntas por vez, sempre especificas, multipla escolha quando possivel.

### Exemplos de Uso

**Exemplo 1 — Requisicao simples (single agent):**
> "Escreva um post de LinkedIn sobre como reduzimos latencia de API."
>
> CMO classifica como CREATE, delega ao content-creator com brief incluindo tom profissional, plataforma LinkedIn, e contexto tecnico.

**Exemplo 2 — Pipeline multi-agente:**
> "Crie uma campanha de lancamento com blog, posts sociais e landing page."
>
> CMO classifica como PIPELINE, orquestra: growth-strategist (framework) -> content-creator (copy) -> visual-designer (graficos) -> growth-engineer (landing page) -> social-publisher (distribuicao).

**Exemplo 3 — Intent ambiguo:**
> "Post sobre IA no healthcare."
>
> CMO detecta ambiguidade (criar conteudo ou publicar?), faz pergunta de clarificacao com opcoes A/B/C antes de delegar.

### Dicas

- O CMO faz no maximo 2 perguntas de clarificacao. Se ainda ambiguo, assume a interpretacao mais provavel e informa o usuario.
- Para pipelines, o CMO mostra progresso em cada etapa com status visual (concluido, em andamento, pendente).
- O kill switch (`autonomy.kill_switch: true`) permite parar qualquer pipeline a qualquer momento dizendo "stop".

---

## Content Creator

**Nome:** `content-creator`
**Funcao:** Geracao de conteudo — blogs, posts sociais, newsletters, copy, documentacao
**Modelo:** sonnet
**Tools:** Read, Write, Glob, Grep

### O Que Faz

O Content Creator e o escritor da equipe. Produz conteudo alinhado a marca, otimizado para cada plataforma, e livre de "AI slop" (frases genericas, linguagem corporativa vazia, cliches de IA). Cada peca de conteudo segue templates estruturados e passa por validacao anti-slop obrigatoria.

### Skills Carregadas

| Skill | Proposito | Quando Usada |
|-------|----------|--------------|
| `copywriting` | Escrita persuasiva — headlines, CTAs, hooks emocionais, frameworks AIDA/PAS | Todo conteudo — headlines, aberturas, CTAs |
| `content-creation` | Estrutura de long-form — templates de blog, newsletter, workflow editorial | Blog posts, newsletters, documentacao |
| `seo-growth` | Pesquisa de keywords, SEO on-page, meta descriptions, clusters de conteudo | Conteudo publicado na web (blogs, docs, landing pages) |
| `platform-mastery` | Algoritmos de plataforma, regras de formato, adaptacao de tom | Posts sociais, conteudo especifico por plataforma |

### Triggers

- "Escreva um blog post sobre..."
- "Crie um post para LinkedIn..."
- "Draft de newsletter..."
- "Escreva copy para email..."
- "Crie conteudo sobre..."
- Qualquer requisicao classificada como CREATE pelo CMO

### Workflow de Geracao de Conteudo

1. **Carrega brand voice** — tom, personalidade, frases banidas, overrides por plataforma
2. **Seleciona tipo de conteudo** — blog, newsletter, documentacao, social, copy marketing
3. **Pesquisa e contexto** — busca conteudo existente no vault, keywords, contexto de audiencia
4. **Gera draft** — outline primeiro (H2/H3), hook forte, corpo com valor, CTA claro, elementos SEO
5. **Validacao anti-slop** — checklist obrigatorio de 10 pontos
6. **Adaptacao por plataforma** — aplica regras de formato, tamanho e tom da plataforma alvo
7. **Output como Obsidian Markdown** — frontmatter completo (title, date, tags, type, status, platform, word_count)

### Adaptacao por Plataforma

| Plataforma | Adaptacao |
|-----------|-----------|
| LinkedIn | Tom profissional, insight-led, 150-300 palavras, primeira linha forte |
| Twitter/X | Conciso, opinativo, <280 caracteres, sem threads a menos que pedido |
| Reddit | Autentico, valor primeiro, zero linguagem de marketing, respeitar cultura do subreddit |
| Threads | Casual, com personalidade, 300-500 caracteres |
| GitHub | Precisao tecnica, exemplos de codigo, reproduzivel |
| YouTube | Descricao SEO com timestamps, rica em keywords |
| Instagram | Copy de suporte visual, emocional, hashtags estrategicas |
| Website/Blog | Tratamento SEO completo, estrutura H2/H3, links internos |

### Checklist Anti-Slop (Obrigatorio)

Toda peca de conteudo passa por esta validacao antes de ser finalizada:

- Nenhuma frase banida do `brand-voice.yaml` presente
- Nenhuma palavra da lista `brand.avoid` usada
- Voz ativa predominante
- Sem superlativos sem evidencia ("melhor", "lider", "revolucionario")
- Sem clickbait ou engagement bait
- Sem jargao corporativo ("alavancar", "sinergia", "abordagem holistica")
- Sem afirmacoes vagas — todas apoiadas por dados especificos
- Sem padroes de AI-slop ("no mundo acelerado de hoje", "vale a pena notar", "mergulhar fundo")
- Conteudo soa como humano com conhecimento, nao como modelo de linguagem
- Personalidade da marca presente ao longo do texto

### Repurposing Multi-Plataforma

Quando solicitado a criar conteudo para multiplas plataformas a partir de uma fonte unica:

```
Blog Post (primario)
  +-- LinkedIn: insight principal + angulo pessoal (200 palavras)
  +-- Twitter: frase mais provocativa (<280 chars)
  +-- Reddit: reformulado como valor comunitario, sem promocao
  +-- Newsletter: resumo 300-500 palavras + angulo pessoal
  +-- YouTube: descricao SEO com timestamps (se acompanha video)
```

### Exemplos de Uso

**Exemplo 1 — Blog post:**
> "Escreva um blog post sobre como implementamos CI/CD com GitHub Actions."
>
> Gera outline, pesquisa keywords, produz artigo com frontmatter Obsidian, otimizado para SEO.

**Exemplo 2 — Repurposing multi-plataforma:**
> "Transforme esse blog post em posts para LinkedIn, Twitter e Reddit."
>
> Extrai insight principal para LinkedIn (200 palavras), frase mais provocativa para Twitter (<280 chars), reformula como valor para comunidade no Reddit (sem linguagem de marketing).

**Exemplo 3 — Newsletter:**
> "Crie uma newsletter semanal com os destaques do blog."
>
> Aplica template de newsletter, summariza artigos com angulo pessoal, inclui CTA final.

### Dicas

- O Content Creator sempre gera como `status: draft`. O usuario promove para review/published.
- Para conteudo ambiguo ("crie conteudo sobre X"), ele pergunta o tipo antes de gerar.
- Se `brand-voice.yaml` nao existir, avisa o usuario e sugere criar a partir do template example.
- Colabora com Visual Designer (solicita specs de thumbnail/OG), Social Publisher (entrega conteudo finalizado), Intelligence Analyst (solicita dados competitivos), e Growth Strategist (recebe direcao estrategica).

---

## Growth Strategist

**Nome:** `growth-strategist`
**Funcao:** Planejamento estrategico de marketing e otimizacao de crescimento
**Modelo:** sonnet
**Tools:** Read, Write, Glob, Grep, WebSearch, WebFetch

### O Que Faz

O Growth Strategist e o estrategista da equipe. Cria planos de marketing baseados em dados, frameworks de crescimento, OKRs, calendarios de conteudo, e frameworks de campanha. Pensa em sistemas, mede em metricas, e planeja em fases.

### Skills Carregadas

| Skill | Proposito |
|-------|----------|
| `marketing-strategy` | Frameworks estrategicos, growth models, planejamento de campanhas |

### Triggers

- "Planeje nossa estrategia de Q2..."
- "Defina OKRs de marketing..."
- "Crie um calendario de conteudo..."
- "Desenhe um plano go-to-market..."
- "Qual deve ser nosso roadmap de marketing?"
- "Faca uma analise TAM/SAM/SOM..."
- Qualquer requisicao classificada como STRATEGY pelo CMO

### Competencias Centrais

| Competencia | Framework/Metodo | Quando Usar |
|-------------|-----------------|-------------|
| Diagnostico de crescimento | AARRR (Pirate Metrics) | Avaliar saude do funil e identificar gargalos |
| Estrategia de campanha | JTBD + awareness levels | Planejar campanhas com objetivo, audiencia, canais, metricas |
| Priorizacao | ICE (rapido) ou RICE (com dados) | Priorizar backlog de 10-30 iniciativas |
| Pilares de conteudo | Audit + map + intersect | Definir 3-5 pilares tematicos de conteudo |
| OKRs | Max 3 Obj, 4 KRs cada | Definir objetivos trimestrais de marketing |
| Posicionamento | Positioning Statement + Messaging Hierarchy | Definir diferenciacao e hierarquia de mensagens |
| Mercado | TAM/SAM/SOM top-down + bottom-up | Dimensionar oportunidade de mercado |

### Workflow de Estrategia

1. **Carrega brand voice** — tom e posicionamento influenciam recomendacoes estrategicas
2. **Analisa o brief** recebido do CMO
3. **Identifica contexto faltante** — faz no maximo 2 perguntas via CMO
4. **Aplica framework** adequado ao tipo de requisicao
5. **Produz output estruturado** com frontmatter YAML (type: strategy, subtype, status, date, author)
6. **Inclui obrigatoriamente:** objetivo claro, audiencia especifica, acoes priorizadas, metricas com alvos, timeline, recursos necessarios, avaliacao de risco

### Anti-Padroes Proibidos

| Proibido | Correto |
|----------|---------|
| "Aumentar brand awareness" | "Atingir 50K impressoes organicas mensais no LinkedIn em 90 dias" |
| "Criar mais conteudo" | "Publicar 2 artigos SEO/semana no cluster [keyword]" |
| "Melhorar engajamento" | "Aumentar taxa de comentarios no LinkedIn de 0.8% para 2.5% com posts opinion-led" |
| "Focar em redes sociais" | "Priorizar LinkedIn (70% esforco) e Twitter (30%) baseado em dados de concentracao de audiencia" |
| "Ser mais data-driven" | "Implementar revisao semanal de dashboard com 5 KPIs: [metricas especificas]" |

### Exemplos de Uso

**Exemplo 1 — Diagnostico de crescimento:**
> "Avalie nosso funil e diga onde estamos perdendo mais."
>
> Aplica AARRR em cada estagio, identifica gargalo mais severo proximo a receita, recomenda quick wins e acoes estrategicas.

**Exemplo 2 — OKRs trimestrais:**
> "Defina OKRs de marketing para Q3."
>
> Gera max 3 objetivos qualitativos, cada um com max 4 Key Results metrificados, incluindo baseline atual e target stretch (70% achievement).

**Exemplo 3 — Posicionamento:**
> "Construa nosso positioning statement."
>
> Mapeia estado atual, landscape competitivo, gaps de posicionamento, e gera Positioning Statement + Messaging Hierarchy com proof points e objection handling.

### Dicas

- Toda estrategia inclui secao "Next Steps" como checklist de acoes imediatas (max 7 itens).
- Para requisicoes vagas, o strategist propoe escopo com deliverables especificos e pede confirmacao antes de executar.
- Output sempre em Markdown com frontmatter YAML para integracao com o vault.
- Ao fazer handoff para outros agentes, inclui briefs especificos: content briefs para content-creator, channel allocation para social-publisher, positioning framework para copywriting.

---

## Social Publisher

**Nome:** `social-publisher`
**Funcao:** Publicacao e distribuicao multi-plataforma
**Cor:** `#1DA1F2`
**Tools:** Read, Write, Glob, mcp-social-publish (Wave 4)

### O Que Faz

O Social Publisher e a "ultima milha" entre conteudo e audiencia. Recebe conteudo finalizado (do Content Creator, de pipelines, ou direto do usuario) e adapta para cada plataforma alvo, aplicando convencoes nativas, regras de formato, e gates de seguranca antes de publicar.

### Skills Carregadas

| Skill | Proposito |
|-------|----------|
| `social-media-management` | Estrategia de engajamento, melhores horarios, gestao de comunidade |
| `platform-mastery` | Algoritmos de cada plataforma, formatos, otimizacao de alcance |

### Triggers

- "Publique isso no LinkedIn..."
- "Agende um tweet para amanha 9h..."
- "Poste esse artigo no Reddit r/programming..."
- "Compartilhe em todas as plataformas..."
- "Distribua o conteudo da semana..."
- Qualquer requisicao classificada como PUBLISH pelo CMO

### Principios

1. **Nunca publica sem preview** — a menos que `autonomy.level: auto` E `require_preview: false`
2. **Platform-native, nao cross-posted** — cada plataforma recebe conteudo adaptado, nunca copy-paste
3. **Brand voice e lei** — todo output passa por anti-slop e checagem de tom
4. **Dry run por padrao** — mostra o que SERIA publicado, espera confirmacao

### Workflow de Publicacao

1. **Recebe conteudo** — do usuario, pipeline CMO, ou calendario de conteudo
2. **Carrega configuracao da plataforma** — verifica se esta habilitada no `brand-voice.yaml`, carrega `tone_override`, `max_length`, `post_types`
3. **Adapta conteudo** — ajusta tom, comprimento, formato, hashtags, CTA, posicionamento de links
4. **Apresenta preview** — mostra conteudo formatado exatamente como apareceria na plataforma, incluindo contagem de caracteres, hashtags, status anti-slop
5. **Aguarda confirmacao** — yes (publica), no (cancela preservando draft), edit (aplica mudancas, retorna ao preview)
6. **Publica via MCP** — ou gera artefato pronto para copy-paste (pre-Wave-4)
7. **Confirmacao pos-publicacao** — resume o que foi publicado com sugestoes de follow-up

### Matriz de Adaptacao

| Formato Origem | LinkedIn | Twitter/X | Reddit | Instagram |
|----------------|---------|-----------|--------|-----------|
| Blog post | Insight principal + angulo pessoal (1200-1500 chars) | Frase mais afiada (200-280 chars) | Resumo de valor, convite a discussao | Carrossel com pontos-chave |
| Newsletter | Historia principal como insight standalone | Thread de insights-chave | Analise aprofundada | Sequencia de stories |
| Copy marketing | Angulo thought leadership | Afirmacao ousada + evidencia | Remove TODA linguagem de marketing | Caption visual-first |
| Doc tecnico | Resumo profissional | Takeaway principal | Post estilo tutorial | Carrossel infografico |

### Publicacao Multi-Plataforma

Quando solicitado a publicar em multiplas plataformas simultaneamente:

1. Adapta conteudo **independentemente** para CADA plataforma
2. Apresenta TODOS os previews em um bloco unico
3. Permite aprovacao granular (`yes to all` ou `yes LinkedIn, edit Twitter`)
4. Publica plataformas aprovadas, segura editadas para re-preview

### Exemplos de Uso

**Exemplo 1 — Publicacao simples:**
> "Publique isso no LinkedIn."
>
> Adapta conteudo para tom profissional, aplica limite de caracteres, mostra preview com check anti-slop, aguarda confirmacao.

**Exemplo 2 — Multi-plataforma:**
> "Publique em LinkedIn, Twitter e Reddit."
>
> Adapta independentemente para cada plataforma, apresenta todos os previews em bloco unico, permite aprovacao granular.

**Exemplo 3 — Agendamento:**
> "Agende esse post para amanha as 9h no Twitter."
>
> Adapta para formato Twitter, mostra preview com horario programado, confirma agendamento.

### Dicas

- O kill switch permite dizer "stop" a qualquer momento para cancelar publicacoes pendentes.
- Se a plataforma esta desabilitada no config (`enabled: false`), o publisher bloqueia e sugere alternativas.
- Conteudo que excede `max_length` e reestruturado automaticamente — nunca simplesmente truncado.
- Ate o Wave 4 (MCP social-publish), o output e um artefato markdown pronto para copy-paste manual na plataforma.

---

## Intelligence Analyst

**Nome:** `intelligence-analyst`
**Funcao:** Pesquisa de mercado, inteligencia competitiva, analise de tendencias, insights de audiencia
**Modelo:** sonnet
**Tools:** Read, Write, Glob, Grep, WebSearch, WebFetch

### O Que Faz

O Intelligence Analyst e a espinha dorsal de pesquisa da equipe. Toda estrategia, campanha e peca de conteudo e tao boa quanto a inteligencia que a sustenta. Ele coleta, analisa e sintetiza dados de mercado em insights acionaveis com evidencias e niveis de confianca.

### Skills Carregadas

| Skill | Proposito |
|-------|----------|
| `competitive-intelligence` | Analise de concorrentes, monitoramento de mercado, benchmarking |

### Triggers

- "Analise nossos 3 principais concorrentes..."
- "Quais sao as tendencias atuais em marketing SaaS?"
- "Faca uma analise SWOT..."
- "Benchmark nosso conteudo contra concorrentes..."
- "Pesquise melhores praticas de email B2B..."
- "Gere um relatorio mensal de marketing..."
- "Mostre nossas metricas de performance de conteudo..."
- Qualquer requisicao classificada como RESEARCH ou REPORT pelo CMO

### Competencias Centrais

| Competencia | Descricao |
|-------------|-----------|
| Inteligencia competitiva | Mapeamento de landscape, deep dive em concorrentes, matriz competitiva |
| Pesquisa de mercado | Analise de industria, dimensionamento, validacao de tendencias |
| Pesquisa de audiencia | Profiling demografico/psicografico, JTBD, padroes de linguagem |
| Analise de tendencias | Deteccao de sinais, validacao, escala de maturidade |
| Inteligencia de conteudo | Pesquisa SEO/keyword, auditoria de performance, gap analysis |
| Social listening | Monitoramento de conversas, analise de sentimento, temas recorrentes |

### Niveis de Profundidade

| Nivel | Trigger | Escopo | Tempo |
|-------|---------|--------|-------|
| Quick scan | Pergunta simples, topico unico | 2-3 fontes, superficie | 5 min |
| Standard | Planejamento de campanha, estrategia de conteudo | 5-8 fontes, profundidade moderada | 15-30 min |
| Deep dive | Entrada em mercado, posicionamento, estrategia competitiva | 10+ fontes, abrangente | 30-60 min |

O padrao e **standard** a menos que o brief do CMO ou o usuario especifique outro nivel.

### Escala de Maturidade de Tendencias

```
EMERGING   -> Poucos sinais, alta incerteza, vantagem de early-mover
GROWING    -> Multiplos sinais, certeza moderada, ainda ha tempo de agir
MAINSTREAM -> Bem estabelecido, baixo risco, necessidade competitiva
DECLINING  -> Alem do pico, retornos decrescentes, evitar investimento
```

### Regras de Qualidade de Pesquisa

- **Toda afirmacao factual precisa de fonte** — link para dados, relatorio ou observacao
- **Distinguir fato de interpretacao** — rotular ambos explicitamente
- **Niveis de confianca obrigatorios** — High/Medium/Low em cada achado
- **Lacunas de dados sao achados** — se nao encontrou algo importante, diz explicitamente
- **Recencia importa** — sinaliza dados com mais de 12 meses

### Hierarquia de Fontes

| Tier | Exemplo | Confiabilidade |
|------|---------|---------------|
| Primario | Registros publicos, anuncios oficiais, estudos publicados | Mais alta |
| Secundario | Relatorios de industria (Gartner, Forrester), artigos de noticia | Alta |
| Terciario | Blog posts, redes sociais, discussoes de comunidade | Media — validacao cruzada necessaria |
| Anedotico | Pontos de dados unicos, observacoes isoladas | Baixa — notar como anedotico |

### Anti-Slop em Pesquisa

Outputs de pesquisa sao especialmente vulneraveis a AI slop. Regras rigidas:

- Zero comentarios genericos de mercado ("o mercado esta evoluindo rapidamente")
- Zero estatisticas sem fonte ("estudos mostram que 73% dos marketers...")
- Zero claims hiperbolicos sobre tendencias ("IA esta revolucionando tudo")
- Zero conclusoes vagas ("empresas devem abracar a transformacao digital")
- Substituir cada afirmacao vaga por uma observacao especifica e com fonte

### Exemplos de Uso

**Exemplo 1 — Analise competitiva:**
> "Analise nossos 3 principais concorrentes no espaco de DevTools."
>
> Mapeia landscape (diretos, indiretos, substitutos), faz deep dive em cada um (produto, pricing, marketing, audiencia, ameacas/oportunidades), gera matriz competitiva com scores honestos.

**Exemplo 2 — Tendencias de mercado:**
> "Quais tendencias de marketing de conteudo devo acompanhar em 2026?"
>
> Identifica sinais emergentes, valida com multiplas fontes, classifica maturidade (emerging/growing/mainstream/declining), recomenda acao e timing para cada tendencia.

**Exemplo 3 — Perfil de audiencia:**
> "Quem e nosso publico-alvo ideal para o produto X?"
>
> Profila demograficamente e psicograficamente, mapeia plataformas preferidas, define JTBD, coleta padroes de linguagem reais, documenta processo de compra.

### Dicas

- Outputs de pesquisa frequentemente alimentam outros agentes: Growth Strategist (dados de mercado), Content Creator (insights de audiencia, keywords), CMO (inteligencia competitiva).
- A secao `recommended_actions` mapeia achados a proximos passos especificos para outros agentes.
- Ao produzir matriz competitiva, score honestamente — inflar nossos scores derrota o proposito da analise.

---

## Visual Designer

**Nome:** `visual-designer`
**Funcao:** Especificacoes de design visual para thumbnails, OG images e graficos sociais
**Modelo:** sonnet
**Tools:** Read, Write

### O Que Faz

O Visual Designer produz **especificacoes estruturadas de assets visuais** em formato JSON/YAML. Ele NAO gera imagens diretamente. Em vez disso, produz specs detalhadas de dimensoes, cores, tipografia, layout e composicao — prontas para renderizacao programatica com sharp (Node.js), geradores SVG, ou ferramentas de design.

### Skills Carregadas

| Skill | Proposito |
|-------|----------|
| `video-production` | Conceitos de thumbnail, hooks visuais, design focado em retencao |

### Triggers

- "Crie uma thumbnail para nosso video do YouTube..."
- "Design um OG image para esse blog post..."
- "Faca um grafico social para nosso lancamento..."
- "Design um infografico sobre nossas metricas..."
- "Crie slides de carrossel para Instagram..."
- Qualquer requisicao classificada como VISUAL pelo CMO

### Tipos de Asset

| Tipo | Formato de Saida | Caso de Uso |
|------|-----------------|-------------|
| Thumbnail | JSON spec | Videos YouTube, hero images de blog |
| OG Image | JSON spec | Previews de compartilhamento social (og:image) |
| Social Image | JSON spec | Graficos nativos por plataforma |
| Brand Graphic | JSON spec | Apresentacoes, banners, headers |

### Dimensoes por Plataforma

| Tipo | Largura | Altura | Aspecto |
|------|---------|--------|---------|
| YouTube Thumbnail | 1280 | 720 | 16:9 |
| OG Image (geral) | 1200 | 630 | ~1.91:1 |
| OG Image (Twitter) | 1200 | 600 | 2:1 |
| LinkedIn Post Image | 1200 | 627 | ~1.91:1 |
| Instagram Post | 1080 | 1080 | 1:1 |
| Instagram Story | 1080 | 1920 | 9:16 |
| Twitter Post Image | 1600 | 900 | 16:9 |
| Blog Hero | 1200 | 630 | ~1.91:1 |
| Slide de Apresentacao | 1920 | 1080 | 16:9 |
| Banner (LinkedIn/Twitter) | 1500 | 500 | 3:1 |

### Principios de Design

**Tipografia:**
- Max 2 familias de fonte por spec
- Max 3 elementos de texto — mais cria ruido visual
- Contraste WCAG AA minimo entre texto e fundo
- Texto nunca toca bordas — padding minimo 40px

**Cores:**
- Brand-first: puxa cores primarias do `brand-voice.yaml`
- Maximo 3 cores: fundo + texto primario + cor de destaque
- Fundos escuros como padrao para thumbnails (maior CTR no YouTube)
- Consistencia no mesmo palette ao longo de uma serie

**Composicao:**
- Hierarquia visual clara: um elemento dominante (geralmente titulo principal)
- Whitespace intencional — nao preencher cada pixel
- Regra dos tercos para posicionamento de elementos-chave
- Platform-native: segue o que performa melhor em cada plataforma

**Regras Especificas para Thumbnails YouTube:**
- Max 5-7 palavras — legivel em 168x94px (tamanho mobile)
- Design deve evocar curiosidade, surpresa ou urgencia
- Texto DEVE se destacar do fundo — usar sombras ou overlays
- Sempre gerar 2 variantes para testes

### Variantes

Para toda requisicao de thumbnail ou imagem, o designer gera:
- **Primary:** spec principal com justificativa
- **Variant:** abordagem alternativa (esquema de cores ou layout diferente)
- **Rationale:** razao para cada escolha de design

### Exemplos de Uso

**Exemplo 1 — Thumbnail YouTube:**
> "Crie uma thumbnail para nosso video sobre Kubernetes."
>
> Gera spec JSON com dimensoes 1280x720, fundo escuro com gradiente, titulo em 5-7 palavras legivel em mobile, 2 variantes com justificativas.

**Exemplo 2 — OG Image para blog:**
> "Design um OG image para o artigo 'Como reduzimos latencia de API em 96%'."
>
> Gera spec 1200x630 com titulo, branding sutil, cores da marca, legivel em preview pequeno.

**Exemplo 3 — Grafico social LinkedIn:**
> "Faca um grafico para acompanhar nosso post sobre metricas de Q1."
>
> Gera spec 1200x627 com dado-chave em destaque, fonte bold, palette profissional, handle da marca.

### Dicas

- Outputs sao especificacoes textuais, nao imagens. Precisam de um pipeline de renderizacao para virar arquivos visuais.
- Para thumbnails YouTube, sempre gera 2 variantes — thumbnail e o asset mais critico para CTR.
- Texto em specs visuais tambem passa por validacao anti-slop.
- Colabora com Content Creator (recebe titulos/topicos para gerar specs), Social Publisher (fornece specs visuais para posts), e Growth Engineer (fornece hero/OG specs para landing pages).

---

## Growth Engineer

**Nome:** `growth-engineer`
**Funcao:** Infraestrutura tecnica de growth — landing pages, testes A/B, analytics, CRO
**Cor:** `#10B981`
**Tools:** Read, Write, Glob

### O Que Faz

O Growth Engineer constroi a infraestrutura tecnica que transforma trafego em conversoes. Landing pages production-ready, planos de testes A/B, configuracao de analytics, e otimizacao de taxa de conversao (CRO) sao seu dominio.

### Skills Carregadas

| Skill | Proposito |
|-------|----------|
| `landing-page-design` | Geracao de landing pages, padroes de hero, CRO |

### Triggers

- "Construa uma landing page para nosso novo produto..."
- "Otimize a taxa de conversao da pagina de signup..."
- "Configure um teste A/B para a secao hero..."
- "Crie uma pagina de captura de leads para o webinar..."
- "Analise os pontos de drop-off do nosso funil..."
- Qualquer requisicao classificada como LANDING pelo CMO

### Capacidades

| Capacidade | Descricao |
|-----------|-----------|
| Landing page generation | HTML single-file, <100KB, CSS embutido, responsive, acessivel (WCAG 2.1 AA) |
| A/B testing framework | Formulacao de hipotese, geracao de variantes como HTML separados, plano de medicao |
| Analytics setup | Tracking plan para GA4/Plausible/Umami com eventos, propriedades, KPIs, snippets prontos |
| CRO analysis | Definicao de funil, analise de drop-off, recomendacoes com score ICE, action plan |

### Workflow: Landing Page

1. **Levanta requisitos** — objetivo de conversao, audiencia, value prop, CTA, proof points
2. **Seleciona padrao de hero** — centered (SaaS signup), split (lancamento), minimal (newsletter), gradient (app download)
3. **Gera pagina** — HTML completo com secoes: hero, social proof, features/benefits, how it works, CTA repeat, footer
4. **Plano de variantes A/B** — para cada landing page, produz pelo menos 1 variante com hipotese e metrica
5. **Guia de analytics** — eventos para rastrear (page view, CTA click, scroll depth, time on page, form submission)

### Workflow: Teste A/B

1. **Formulacao de hipotese** — observacao, mudanca, resultado esperado, metrica primaria, efeito minimo detectavel
2. **Geracao de variantes** — arquivos HTML separados, cada um mudando UMA variavel, com comentario `<!-- AB-TEST: [nome] | VARIANT: [id] -->`
3. **Plano de medicao** — tool, eventos, segmentacao, cadencia de reporting, condicoes de parada
4. **Criterios de sucesso** — duracao minima 14 dias, minimo 100 conversoes por variante, nivel de confianca 0.95

### Workflow: CRO

1. **Definicao de funil** — estagios, URLs, acoes de sucesso, taxas atuais
2. **Analise de drop-off** — onde e por que usuarios saem, com severidade:
   - Critical: >80% drop-off
   - High: 60-80%
   - Medium: 40-60%
   - Low: <40%
3. **Recomendacoes ICE** — cada recomendacao com score Impact x Confidence x Ease (max 1000), top 5 priorizadas
4. **Action plan** — quick wins (Ease >= 8), fila de testes, metricas de sucesso com baseline e target

### CRO Audit Checklist

O Growth Engineer valida paginas existentes contra esta lista:

- Proposta de valor clara acima do fold
- CTA unico e primario (sem acoes concorrentes)
- CTA visivel sem scroll
- Social proof presente e especifico (numeros, nomes, logos)
- Risk reversal declarado ("Sem cartao", "Cancele a qualquer momento")
- Pagina carrega em <2 segundos
- Mobile responsive e usavel
- Copy focada em beneficios, nao features
- Anti-slop compliant

### Exemplos de Uso

**Exemplo 1 — Landing page:**
> "Construa uma landing page para nosso produto de analytics."
>
> Levanta requisitos (ou infere do contexto), gera HTML single-file responsivo com hero centered, social proof, 3 features, CTA repeat, + plano A/B + guia de analytics.

**Exemplo 2 — Teste A/B:**
> "Quero testar se mudar o headline melhora conversao."
>
> Gera hipotese estruturada, 2 variantes HTML (control + variant), plano de medicao com GA4, criterios de sucesso, duracao minima 14 dias.

**Exemplo 3 — CRO:**
> "Analise por que nosso funil de signup tem drop-off alto."
>
> Mapeia funil completo, identifica causas de drop-off por estagio, gera top 5 recomendacoes ordenadas por ICE score, separa quick wins de itens que precisam de teste.

### Dicas

- Toda landing page e um unico arquivo HTML, sem dependencias externas, abaixo de 100KB.
- System fonts apenas — sem fontes externas que impactem performance.
- Acessibilidade e inegociavel: contraste >= 4.5:1, focus states em todos elementos interativos.
- Para CRO, use os templates em `templates/reports/` para formatos padronizados de relatorio.
- Ferramentas de analytics recomendadas: GA4 (gratis), Plausible (privacy-friendly), PostHog (open-source), Umami (self-hosted).

---

## Fluxo de Delegacao

### Como o CMO Roteia Requisicoes

O roteamento segue um processo de 4 passos:

```
1. CLASSIFICAR — Identificar o intent primario da mensagem
2. VERIFICAR   — Ambiguidade < 70% confianca? Perguntar clarificacao
3. DELEGAR     — Montar brief e acionar agente especialista
4. VALIDAR     — Aplicar quality gate no output antes de entregar
```

### Regras de Desambiguacao

**Regra 1 — Prioridade do Verbo:**

| Verbo | Intent | Agente |
|-------|--------|--------|
| "escrever", "criar", "redigir" | CREATE | content-creator |
| "publicar", "postar", "compartilhar" | PUBLISH | social-publisher |
| "analisar", "comparar" | RESEARCH | intelligence-analyst |
| "pesquisar", "investigar", "explorar" | RESEARCH | intelligence-analyst |
| "desenhar", "design" | VISUAL | visual-designer |
| "planejar", "estrategia" | STRATEGY | growth-strategist |
| "construir", "otimizar" (pagina) | LANDING | growth-engineer |
| "relatorio", "resumir", "metricas" | REPORT | intelligence-analyst |

**Regra 2 — Checagem de Contexto:**
Quando o verbo e ambiguo (ex: "post"):
- Conteudo ja existe? -> PUBLISH (social-publisher)
- E um pedido de conteudo novo? -> CREATE (content-creator)
- Menciona plataforma pelo nome? -> PUBLISH (social-publisher)

**Regra 3 — Deteccao de Intent Composto:**
Se a requisicao contem multiplos verbos de categorias diferentes, o CMO verifica se existe um pipeline definido. Se sim, executa o pipeline. Se nao, pergunta ao usuario qual fazer primeiro.

**Regra 4 — Clarificacao:**
Quando confianca < 60%, o CMO faz UMA pergunta direcionada com opcoes A/B/C. Nunca faz mais de uma pergunta de clarificacao. Se ainda ambiguo, assume o intent mais provavel e informa a suposicao.

### Pipelines Multi-Agente

O CMO detecta e orquestra workflows que envolvem multiplos agentes em sequencia:

| Pipeline | Trigger | Sequencia |
|----------|---------|-----------|
| Create and Publish | "crie e publique", "escreva e compartilhe", "draft e post" | content-creator -> social-publisher |
| Create and Design | "crie com imagem", "blog post com OG image", "escreva e design" | content-creator -> visual-designer |
| Research and Create | "pesquise e escreva", "explore e crie", "descubra e draft" | intelligence-analyst -> content-creator |
| Strategy to Content | "planeje e comece a criar", "estrategia e execute", "calendario e produza" | growth-strategist -> content-creator |
| Full Publish Pipeline | "crie, design e publique", "pipeline completo", "campanha end to end" | content-creator -> visual-designer -> social-publisher |

### Regras de Execucao de Pipeline

1. **Execucao sequencial** — cada agente completa antes do proximo iniciar
2. **Encaminhamento de output** — saida do agente anterior vira input do proximo
3. **Checkpoints do usuario** — usuario pode revisar/editar entre etapas
4. **Fail-fast** — se qualquer etapa falha, pipeline para e reporta ao usuario
5. **Completude parcial** — etapas concluidas sao preservadas mesmo se etapas posteriores falharem

### Fallback Handling

| Situacao | Acao do CMO |
|----------|------------|
| Nenhum match de intent | Apresenta lista de capacidades disponiveis com exemplos |
| Match parcial | Assume melhor match, informa suposicao, prossegue |
| Erro no agente | Reporta erro, oferece opcoes: retry, abordagem diferente, ou salvar progresso |

### Diagrama de Colaboracao entre Agentes

```
                      +---------+
                      |   CMO   |
                      +---------+
                     /     |     \
                    /      |      \
                   v       v       v
          +----------+ +----------+ +----------+
          | Growth   | | Content  | | Intell.  |
          | Strat.   | | Creator  | | Analyst  |
          +----------+ +----------+ +----------+
               |            |   \        |
               |            |    \       |
               v            v     v      v
          +----------+ +----------+ +----------+
          | Growth   | | Social   | | Visual   |
          | Engineer | | Publisher| | Designer |
          +----------+ +----------+ +----------+
```

**Fluxos de handoff:**
- Growth Strategist -> Content Creator (direcao estrategica, content briefs)
- Growth Strategist -> Growth Engineer (messaging para landing pages)
- Content Creator -> Social Publisher (conteudo finalizado para publicacao)
- Content Creator -> Visual Designer (titulos/topicos para specs visuais)
- Intelligence Analyst -> Growth Strategist (dados de mercado para decisoes)
- Intelligence Analyst -> Content Creator (insights de audiencia, keywords)
- Visual Designer -> Social Publisher (specs visuais para posts)
- Visual Designer -> Growth Engineer (hero/OG specs para landing pages)

---

## Referencia de Output Contracts

Cada agente produz outputs em formatos padronizados e validaveis. Abaixo esta o resumo dos contratos de saida.

### Content Creator

```yaml
formato: Obsidian Markdown com frontmatter
frontmatter_obrigatorio:
  title: string (sem clickbait)
  date: ISO 8601
  tags: lista (3-7, lowercase, hyphenated)
  type: blog | newsletter | documentation | social
  status: draft (sempre na primeira geracao)
  platform: string
  word_count: number
validacao:
  anti_slop: true
  brand_voice: true
```

### Growth Strategist

```yaml
formato: Markdown com frontmatter YAML
frontmatter_obrigatorio:
  type: "strategy"
  subtype: growth-plan | campaign | positioning | okrs | content-pillars | market-sizing | prioritization
  status: string
  date: ISO 8601
  author: "growthOS/growth-strategist"
secoes_obrigatorias:
  - executive_summary (max 150 palavras)
  - analysis (frameworks usados, fontes de dados)
  - recommendations (lista priorizada: action, rationale, priority P0/P1/P2, effort, expected_impact)
  - success_metrics (tabela: metric, baseline, target, timeline)
  - next_steps (checklist, max 7 itens)
validacao:
  anti_slop: true
  brand_voice: true
  no_vague_metrics: true
  min_word_count: 300
```

### Social Publisher

```yaml
formato: Markdown
secoes:
  - platform_preview (conteudo formatado como apareceria)
  - metadata (hashtags, schedule, links)
  - anti_slop_result (PASS/FAIL com detalhes)
  - confirmation_prompt (ponto de decisao do usuario)
  - post_publish_summary (apos publicacao)
artefatos:
  type: social-post
  platform: string
  content: string
  status: draft | preview | published | scheduled
```

### Intelligence Analyst

```yaml
formato: Markdown com frontmatter YAML
frontmatter_obrigatorio:
  type: "intelligence"
  subtype: competitive-analysis | market-research | audience-profile | trend-report | content-audit | social-listening
  status: draft | review | final
  date: ISO 8601
  author: "growthOS/intelligence-analyst"
  confidence: high | medium | low
secoes_obrigatorias:
  - executive_summary (max 200 palavras)
  - methodology (fontes, profundidade, limitacoes)
  - findings (cada um com evidencia, confianca, fonte, relevancia)
  - data_gaps (o que nao foi encontrado e por que importa)
  - recommended_actions (lista priorizada: action, rationale, priority, owner)
  - sources (citacoes numeradas: Autor/Org - Titulo - URL - Data)
validacao:
  anti_slop: true
  all_claims_sourced: true
  confidence_levels_present: true
  no_unsourced_statistics: true
  data_gaps_acknowledged: true
```

### Visual Designer

```yaml
formato: JSON spec
tipos:
  thumbnail: dimensoes, background, text[], elements[], overlay
  og-image: dimensoes, background, text[], branding, elements[]
  social-image: dimensoes, platform, background, text[], branding, elements[]
regras:
  max_font_families: 2
  max_text_elements: 3
  contrast: WCAG AA
  padding_minimo: 40px
  max_cores: 3 (fundo + texto + destaque)
variantes:
  primary: spec principal
  variant: abordagem alternativa
  rationale: justificativa para cada
```

### Growth Engineer

```yaml
landing_page:
  formato: HTML single-file
  max_size: 100KB
  no_external_deps: true
  responsive: true
  accessible: WCAG 2.1 AA

ab_test_plan:
  formato: YAML + HTML (arquivos de variante)
  min_variants: 1
  max_variants: 4
  each_variant_separate_html: true
  hypothesis_required: true

tracking_plan:
  formato: YAML
  events_must_have_kpis: true
  snake_case_event_names: true
  implementation_snippet_required: true

cro_report:
  formato: YAML + Markdown
  ice_scored: true
  recommendations_sorted_by_ice: true
  max_priority_recommendations: 5
```

---

*GrowthOS Agents Guide v1.0 — Referencia completa da equipe autonoma de marketing.*
