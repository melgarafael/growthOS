# Guia Completo de Skills — GrowthOS

> Referencia completa das 9 skills do GrowthOS. Cada skill e um modulo especializado de marketing
> que o Claude Code ativa automaticamente com base no contexto da sua solicitacao.

---

## Sumario

1. [O que sao Skills](#o-que-sao-skills)
2. [marketing-strategy](#1-marketing-strategy)
3. [content-creation](#2-content-creation)
4. [copywriting](#3-copywriting)
5. [seo-growth](#4-seo-growth)
6. [video-production](#5-video-production)
7. [landing-page-design](#6-landing-page-design)
8. [social-media-management](#7-social-media-management)
9. [competitive-intelligence](#8-competitive-intelligence)
10. [platform-mastery](#9-platform-mastery)
11. [Combinando Skills](#combinando-skills)

---

## O que sao Skills

### Conceito

Skills sao modulos de conhecimento especializado que estendem as capacidades do Claude Code.
No contexto do GrowthOS, cada skill e um arquivo `SKILL.md` dentro de um subdiretorio em
`growthOS/skills/`. Quando voce faz uma solicitacao ao Claude Code, o sistema identifica
automaticamente qual skill (ou combinacao de skills) e mais relevante e carrega o conhecimento
correspondente para gerar a melhor resposta possivel.

### Como funcionam na pratica

1. **Ativacao automatica**: Voce nao precisa "chamar" uma skill manualmente. Basta descrever
   o que precisa — por exemplo, "crie um roteiro para um video no YouTube" — e o Claude Code
   ativa a skill `video-production` automaticamente.

2. **Conhecimento profundo**: Cada skill contem frameworks, templates, checklists e regras
   especificas do seu dominio. Nao e um conhecimento generico — e metodologia estruturada.

3. **Brand Voice integrada**: Todas as 9 skills carregam obrigatoriamente o arquivo
   `brand-voice.yaml` antes de gerar qualquer conteudo. Isso garante que tudo o que sai
   do GrowthOS respeita o tom, a personalidade e as restricoes da marca.

4. **Anti-Slop enforced**: Toda saida passa por validacao contra frases banidas e padroes
   genericos de IA. Se o texto parece "conteudo de IA generico", ele e reescrito antes
   da entrega.

5. **Output padronizado**: Cada skill define um "output contract" — um schema YAML que
   garante que o resultado sempre tem frontmatter valido, secoes obrigatorias e metadados
   completos.

### Estrutura de uma Skill

```
growthOS/skills/
  marketing-strategy/
    SKILL.md          # Definicao completa da skill
    README.md         # Descricao curta
  content-creation/
    SKILL.md
    README.md
  ...
```

Cada `SKILL.md` contem:

- **Trigger conditions**: Quando a skill deve ser ativada
- **Brand voice integration**: Regras de voz da marca especificas para o dominio
- **Frameworks e metodologias**: Conhecimento tecnico do dominio
- **Templates**: Modelos prontos para uso
- **Output contract**: Schema de saida padronizado
- **Anti-patterns**: O que evitar

### Quando usar este guia

Use este documento como referencia para:

- Entender o que cada skill faz e quando ela e ativada
- Saber quais frameworks e templates estao disponiveis
- Aprender a combinar skills para fluxos de trabalho complexos
- Consultar exemplos praticos de uso

---

## 1. marketing-strategy

**Arquivo**: `growthOS/skills/marketing-strategy/SKILL.md`

### Descricao

Skill de planejamento estrategico de marketing. Cobre growth frameworks (AARRR, ICE, RICE),
posicionamento, OKRs, planejamento de campanhas, pilares de conteudo e analise de mercado.
E a skill mais abrangente — funciona como o "cerebro estrategico" do GrowthOS.

### Quando ativa

- Criar ou refinar uma estrategia de marketing
- Planejar uma campanha ou lancamento
- Definir OKRs ou KPIs de marketing
- Analisar posicao de mercado ou cenario competitivo
- Construir pilares de conteudo ou calendarios editoriais
- Priorizar iniciativas de marketing
- Conduzir analise TAM/SAM/SOM
- Desenhar um modelo de crescimento ou funil

### Capacidades principais

| Capacidade | Framework/Ferramenta |
|------------|---------------------|
| Diagnostico de crescimento | AARRR (Pirate Metrics) — 5 estagios com playbooks |
| Priorizacao rapida | ICE Scoring (Impact, Confidence, Ease) |
| Priorizacao com dados | RICE (Reach, Impact, Confidence, Effort) |
| Posicionamento | Category Design, Jobs-to-be-Done (JTBD), Positioning Canvas |
| Pilares de conteudo | Metodologia de 5 passos para definir pilares |
| Campanhas | Template de brief com timeline, metricas e riscos |
| Matriz competitiva | Analise de dimensoes, scoring e wedge strategy |
| OKRs | Templates para growth, retencao e brand building |
| Dimensionamento | TAM/SAM/SOM com template de calculo |

### 3 exemplos praticos

**Exemplo 1 — Diagnostico de funil**
> "Meu SaaS tem 5.000 signups por mes mas so 200 viram pagantes. Onde esta o problema?"
>
> A skill aplica o AARRR, identifica o gargalo entre Activation e Revenue, e sugere um
> playbook especifico: mapear os primeiros 5 minutos de experiencia do usuario, identificar
> o "aha moment" e reduzir os passos para alcanca-lo.

**Exemplo 2 — Priorizacao de backlog**
> "Tenho 15 ideias de marketing e nao sei por onde comecar."
>
> A skill aplica ICE ou RICE scoring, pede que voce classifique cada ideia em Impact,
> Confidence e Ease (ou Reach + Effort), calcula os scores e entrega uma lista priorizada
> com justificativa.

**Exemplo 3 — Posicionamento com JTBD**
> "Como me posiciono num mercado com 10 concorrentes parecidos?"
>
> A skill usa o framework Jobs-to-be-Done para extrair o "job" que o cliente quer resolver,
> identifica jobs sub-atendidos pela concorrencia, e gera um Positioning Canvas com
> diferenciador, provas e proposta unica de valor.

### Dicas de uso

- Sempre forneca dados reais quando possivel — os frameworks funcionam melhor com numeros
  concretos do que com estimativas vagas.
- Para TAM/SAM/SOM, traga pelo menos 2 fontes de dados — a skill faz cross-validation.
- OKRs devem ter no maximo 3-4 Key Results por Objective. Se precisa de mais, divida o Objective.
- Ao priorizar com ICE, faca scoring cego (cada pessoa pontua separadamente) para evitar anchoring.

### Skills relacionadas

- **competitive-intelligence**: Para analise competitiva profunda que alimenta o posicionamento
- **content-creation**: Para executar os pilares de conteudo definidos na estrategia
- **seo-growth**: Para fundamentar estrategia de conteudo com dados de busca

---

## 2. content-creation

**Arquivo**: `growthOS/skills/content-creation/SKILL.md`

### Descricao

Skill de criacao de conteudo em todos os formatos — blog posts, newsletters, documentacao,
conteudo social e workflows editoriais. Produz saida compativel com Obsidian (frontmatter YAML)
e integra brand voice em cada peca.

### Quando ativa

- Criar, escrever ou rascunhar conteudo (blog posts, artigos, newsletters, docs)
- Planejar um calendario de conteudo ou plano editorial
- Adaptar conteudo existente para diferentes formatos ou plataformas
- Criar conteudo otimizado para SEO ou engajamento
- Quando um agente solicita geracao de conteudo long-form

### Capacidades principais

| Capacidade | Detalhe |
|------------|---------|
| Blog posts | Template completo com hook, secoes, CTA. 800-2000 palavras |
| Newsletters | Estrutura: abertura pessoal, historia principal, quick takes, recurso da semana |
| Documentacao | Step-by-step, troubleshooting tables, prerequisites |
| Conteudo social | Adaptado por plataforma (LinkedIn, Twitter, Reddit, Threads, GitHub, YouTube, Instagram) |
| Workflow editorial | Processo de 7 etapas: brief > pesquisa > outline > draft > anti-slop > frontmatter > review |
| Adaptacao cruzada | Blog para newsletter, newsletter para social, docs para blog, etc. |
| SEO integration | Title tags, meta descriptions, headers com keywords, internal links |

### 3 exemplos praticos

**Exemplo 1 — Blog post com SEO**
> "Escreva um blog post sobre content marketing para B2B SaaS."
>
> A skill gera um post completo com: titulo otimizado (<60 chars), frontmatter Obsidian,
> hook nos primeiros 200 palavras, secoes H2/H3 com keywords, pelo menos 1 exemplo concreto,
> e CTA final. Tudo passa pelo filtro anti-slop antes da entrega.

**Exemplo 2 — Adaptacao de blog para newsletter**
> "Adapte o blog post que criamos para uma newsletter semanal."
>
> A skill extrai o insight principal, reduz para 300-500 palavras, adiciona angulo pessoal,
> cria secao de Quick Takes com 3 insights complementares, e formata para email com subject
> line (<50 chars) e link acionavel.

**Exemplo 3 — Documentacao tecnica**
> "Crie a documentacao de setup do nosso SDK."
>
> A skill gera docs no padrao: prerequisitos, step-by-step com code blocks copy-pasteable,
> tabela de troubleshooting (Problema | Causa | Solucao), e links para docs relacionados.

### Dicas de uso

- Sempre especifique a plataforma alvo — a skill adapta tom e formato automaticamente.
- Para conteudo web, a skill integra automaticamente com SEO (titles, metas, internal links).
- O Quality Checklist de 10 pontos roda antes de qualquer entrega — inclui verificacao de
  brand voice, anti-slop, hierarquia de headings e word count.
- Newsletters devem ter UMA historia principal, nao 5 concorrentes.

### Skills relacionadas

- **copywriting**: Para copy persuasivo dentro do conteudo (headlines, CTAs)
- **seo-growth**: Para pesquisa de keywords que guia a criacao de conteudo
- **social-media-management**: Para distribuicao do conteudo nas plataformas
- **marketing-strategy**: Para os pilares de conteudo que definem a pauta editorial

---

## 3. copywriting

**Arquivo**: `growthOS/skills/copywriting/SKILL.md`

### Descricao

Skill de copywriting persuasivo. Cobre AIDA, PAS, formula 4U para headlines, padroes de CTA,
gatilhos emocionais, validacao anti-slop e guidelines por plataforma. E a skill focada em
conversao — cada palavra precisa "pagar sua estadia" no texto.

### Quando ativa

- Escrever copy de marketing, headlines ou taglines
- Criar posts ou captions para redes sociais
- Redigir subject lines ou copy de email
- Escrever copy de landing page ou descricoes de produto
- Criar CTAs (calls-to-action)
- Melhorar ou reescrever copy existente
- Gerar copy de anuncios (paid social, search ads)

### Capacidades principais

| Capacidade | Framework |
|------------|-----------|
| Copy persuasivo long-form | AIDA (Attention, Interest, Desire, Action) |
| Copy persuasivo short-form | PAS (Problem, Agitate, Solution) |
| Headlines | Formula 4U (Useful, Urgent, Ultra-specific, Unique) — scoring 1-16 |
| CTAs | Formula: Action Verb + Outcome/Benefit, por estagio de funil |
| Gatilhos emocionais | 7 triggers: FOMO, Belonging, Status, Curiosity, Trust, Reciprocity, Autonomy |
| Anti-Slop | 3 tiers: Hard Banned, Conditional Ban (requer dados), Style Rules |
| Copy scoring | Rubrica de 7 dimensoes (35 pontos max) |
| Guidelines por plataforma | LinkedIn, Twitter/X, Reddit, Email |

### 3 exemplos praticos

**Exemplo 1 — Landing page hero**
> "Escreva o hero copy para uma landing page do nosso produto de automacao de conteudo."
>
> A skill aplica AIDA: headline bold com claim especifico (nao generico), subheadline
> com 1 detalhe concreto, social proof ("Usado por 2.400+ times"), e CTA com verbo de
> acao + beneficio ("Comece a publicar mais rapido"). Entrega 2-3 variantes para A/B test.

**Exemplo 2 — Email sequence com PAS**
> "Crie um email de nurturing para leads que nao converteram."
>
> A skill usa PAS: Problem (nomeia a dor com as palavras do cliente), Agitate (mostra
> as consequencias de nao agir — sem manipulacao, com fatos reais), Solution (apresenta
> o produto como resolucao natural). Subject line testada com formula 4U.

**Exemplo 3 — CTA optimization**
> "Nossos CTAs estao com taxa de clique baixa. Ajude a melhorar."
>
> A skill analisa os CTAs atuais contra a formula (Action Verb + Outcome), sugere
> alternativas por estagio de funil (TOFU: "Veja exemplos", MOFU: "Baixe o template gratis",
> BOFU: "Comece seu trial"), e adiciona micro-copy de suporte ("Sem cartao de credito.
> Setup em 3 minutos.").

### Dicas de uso

- Sempre peca variantes — a skill entrega 2-3 alternativas por padrao para A/B testing.
- Use o scoring de 7 dimensoes para avaliar copy existente antes de reescrever.
- O teste mais importante: "Um concorrente poderia dizer a mesma frase sobre o produto
  dele?" Se sim, a copy e generica demais.
- Gatilhos emocionais devem ser usados com etica — a skill calibra PAS para "agitacao
  verdadeira", nao manipulacao.

### Skills relacionadas

- **landing-page-design**: Para gerar a pagina completa com o copy otimizado
- **content-creation**: Para conteudo long-form que contem copy persuasivo
- **social-media-management**: Para adaptar copy em posts plataforma-nativos
- **platform-mastery**: Para entender restricoes e cultura de cada plataforma

---

## 4. seo-growth

**Arquivo**: `growthOS/skills/seo-growth/SKILL.md`

### Descricao

Skill de SEO completo — pesquisa de keywords, checklist on-page, estrategia de content
clusters, templates de meta description, internal linking, analise de SERP e sinais E-E-A-T.
E a skill que conecta dados de busca com estrategia de conteudo.

### Quando ativa

- Pesquisar keywords ou construir estrategia de keywords
- Otimizar conteudo para motores de busca
- Construir um content cluster ou topic hub
- Escrever ou melhorar meta descriptions e title tags
- Planejar estrategia de internal linking
- Analisar SERPs ou performance de busca de concorrentes
- Melhorar sinais E-E-A-T
- Auditar elementos on-page de SEO

### Capacidades principais

| Capacidade | Detalhe |
|------------|---------|
| Keyword research | Processo de 5 camadas: seed > expansao > classificacao de intent > priorizacao > mapeamento |
| Checklist on-page | 30+ items: title tag, meta description, headings, body, URL, imagens, internal links, tecnico |
| Content clusters | Modelo Hub-and-Spoke com regras de internal linking |
| SERP analysis | Template para analisar top 3, identificar gaps e oportunidades de featured snippet |
| E-E-A-T | Checklists em 3 niveis: conteudo, site e tecnico |
| Internal linking | Regras de distribuicao de anchor text (50/30/20) e audit de orphan pages |
| Technical SEO | Core Web Vitals, schema markup, crawl budget |
| Calendario SEO | Template YAML com keyword, formato, intent e status por semana |

### 3 exemplos praticos

**Exemplo 1 — Pesquisa de keywords para novo cluster**
> "Preciso de um keyword research completo para o tema 'content marketing automation'."
>
> A skill executa o processo de 5 camadas: extrai seeds do produto e da linguagem do
> cliente, expande via autocomplete/PAA/forums, classifica por intent (informacional,
> comercial, transacional), pontua cada keyword por relevancia e dificuldade, e mapeia
> para URLs e tipos de conteudo.

**Exemplo 2 — Audit on-page de artigo existente**
> "Analise o SEO deste artigo e diga o que melhorar."
>
> A skill roda a checklist de 30+ itens: verifica title tag (50-60 chars, keyword na frente),
> meta description (150-160 chars, com CTA), hierarquia de headings, keyword density no body,
> URL structure, alt text de imagens, internal links, e schema markup.

**Exemplo 3 — Estrategia de content cluster**
> "Monte um content cluster em torno do tema 'social media strategy'."
>
> A skill cria a pagina pilar (guia abrangente, 3000-5000 palavras), mapeia 8-15 spoke
> articles com keywords long-tail, define a estrategia de internal linking (cada spoke
> linka para o pilar, pilar linka para todos os spokes), e sugere a ordem de publicacao.

### Dicas de uso

- Sempre classifique intent antes de criar conteudo — mismatching de intent e o erro
  de SEO mais comum. Google o keyword e veja o que ja rankeia.
- Para content clusters, publique a pagina pilar primeiro (mesmo como rascunho) e
  adicione spokes progressivamente.
- Featured snippets sao oportunidades de alto impacto: responda a pergunta em 40-50
  palavras logo abaixo de um H2 que espelhe a query.
- E-E-A-T para conteudo AI: adicione camada de experiencia real (dados proprios, case
  studies, screenshots) que IA nao pode fabricar.

### Skills relacionadas

- **content-creation**: Para escrever o conteudo otimizado que o SEO research definiu
- **marketing-strategy**: Para alinhar clusters de conteudo com pilares estrategicos
- **copywriting**: Para title tags e meta descriptions persuasivas
- **platform-mastery**: Para SEO especifico de YouTube (tags, chapters, descriptions)

---

## 5. video-production

**Arquivo**: `growthOS/skills/video-production/SKILL.md`

### Descricao

Skill de producao de conteudo em video (text-based). Cobre roteiros (formato YouTube),
descricoes, specs de thumbnail (texto para sharp/SVG), storyboarding, SEO de video
(tags, chapters) e metodologia hook-first com padroes de retencao. Todas as saidas sao
texto — nao gera imagens ou videos reais.

### Quando ativa

- Escrever roteiros de video (YouTube, social video)
- Criar descricoes otimizadas para YouTube
- Especificar conceitos de thumbnail
- Fazer storyboarding cena a cena
- Otimizar SEO de video (tags, chapters)
- Planejar estrategia de retencao para videos longos

### Capacidades principais

| Capacidade | Detalhe |
|------------|---------|
| Roteiro | Formato: Hook (0-5s) > Setup (5-30s) > Body (com retention triggers) > CTA final |
| Retention triggers | 5 tipos: pattern interrupt, open loop, social proof, direct address, B-roll cue |
| YouTube description | Template com hook, recursos, chapters, takeaways, CTA |
| Thumbnail spec | YAML para geracao via sharp/SVG: layout, texto, expressao, cores, contraste |
| Storyboarding | YAML por cena: visual, audio, narration, texto overlay, transicoes |
| Video SEO | Tags (10-15), chapters (minimo 3, comecando em 0:00), signals do algoritmo |
| Algorithm signals | CTR, watch time, session time, engagement rate, upload consistency |

### 3 exemplos praticos

**Exemplo 1 — Roteiro completo para YouTube**
> "Escreva o roteiro de um video de 10 minutos sobre 'como criar um calendario de conteudo'."
>
> A skill gera: hook de 5 segundos (pattern interrupt, sem "oi pessoal"), setup de 25
> segundos (contexto + promessa de valor), body dividido em secoes com retention trigger
> a cada 60-90 segundos, e CTA final unico. Inclui metadados SEO (titulo, descricao, tags,
> chapters).

**Exemplo 2 — Spec de thumbnail**
> "Crie 2 conceitos de thumbnail para o video acima."
>
> A skill entrega 2 specs YAML: layout (split ou centered), headline (3-5 palavras max),
> expressao facial sugerida, paleta de cores com contraste alto, e nota de legibilidade
> mobile (deve ser legivel em 100px de largura).

**Exemplo 3 — Storyboard para video curto**
> "Faca o storyboard de um Reel de 30 segundos sobre nosso produto."
>
> A skill gera storyboard cena a cena em YAML: cada cena com timestamp, tipo de visual
> (talking head, screen recording, b-roll), narracao, texto overlay, transicao e
> dispositivo de retencao.

### Dicas de uso

- Nunca comece um roteiro com intro/logo/saudacao generica — hook primeiro, intro depois.
- Mantenha UM unico CTA por video. Multiplos CTAs diluem a acao.
- Para thumbnails, a regra de 3 palavras e sagrada — se nao e legivel a 100px, nao funciona.
- Chapters com keyword no titulo aparecem no Google Search — otimize cada titulo de chapter.
- Tags genericas como "tutorial" ou "how to" nao ajudam — use termos especificos.

### Skills relacionadas

- **platform-mastery**: Para entender o algoritmo do YouTube em detalhe
- **copywriting**: Para headlines e hooks de alta conversao
- **seo-growth**: Para keyword research que alimenta titulos e tags
- **social-media-management**: Para distribuir trechos do video nas redes sociais

---

## 6. landing-page-design

**Arquivo**: `growthOS/skills/landing-page-design/SKILL.md`

### Descricao

Skill de design de landing pages otimizadas para conversao. Gera arquivos HTML
auto-contidos (single-file) com CSS embedado, zero dependencias externas,
design responsivo, acessibilidade e performance abaixo de 100KB. Sem JavaScript
desnecessario, sem Google Fonts, sem CDNs.

### Quando ativa

- Gerar uma landing page
- Criar uma pagina de conversao (signup, trial, download)
- Precisar de um hero section otimizado
- Implementar uma pagina com social proof e CTA
- Gerar variantes para A/B testing

### Capacidades principais

| Capacidade | Detalhe |
|------------|---------|
| Single-file HTML | 1 arquivo, CSS em `<style>`, SVG inline, max 100KB |
| Estrutura de secoes | Hero > Social Proof > Features/Benefits > How It Works > CTA repeat > Footer |
| Hero patterns | Centered, Split, Gradient, Minimal |
| CRO | CTA unico repetido 2-3x, above the fold, risk reversal |
| Social proof | 3 formatos: logo bar, testimonials, stats |
| Responsivo | Mobile-first com breakpoints em 768px e 1024px |
| Acessibilidade | Semantic HTML, contraste 4.5:1, skip link, alt text, focus states |
| Performance | LCP <1.0s, 0 requests externas, CSS <15KB, SVG total <20KB |
| A/B variants | Specs de teste para headline, CTA e layout |
| Design system | CSS custom properties para tipografia, espacamento, cores, radius |

### 3 exemplos praticos

**Exemplo 1 — Landing page de SaaS**
> "Crie uma landing page para nosso produto de automacao de marketing."
>
> A skill gera um HTML completo (<100KB) com: hero section (headline benefit-first,
> subheadline, CTA "Start Free Trial", trust signal), social proof (logo bar ou stats),
> 3-4 beneficios com icones SVG inline, secao "How it works" em 3 passos, CTA repeat
> com risk reversal ("Sem cartao, cancele quando quiser"), e footer minimo.

**Exemplo 2 — Variantes para A/B test**
> "Quero testar headlines diferentes nesta landing page."
>
> A skill entrega a pagina principal + specs de variantes YAML: control vs variant
> para headline, CTA text e layout do hero, cada uma com hipotese do por que pode
> converter melhor.

**Exemplo 3 — Landing page com dark mode**
> "Preciso de uma landing page com suporte a dark mode."
>
> A skill usa `prefers-color-scheme` media query para gerar variante dark automatica,
> mantendo contraste acessivel em ambos os modos, tudo dentro do mesmo arquivo HTML.

### Dicas de uso

- Nunca adicione barra de navegacao em landing page — o objetivo e conversao, nao navegacao.
- Um CTA primario por pagina. Se voce precisa de 2 CTAs, provavelmente precisa de 2 paginas.
- O hero section e 80% da conversao — invista tempo nele.
- Teste sempre headline E CTA text como primeira prioridade de A/B.
- Evite pop-ups no carregamento — eles destroem a primeira impressao.
- O budget de 100KB forca simplicidade — simplicidade converte.

### Skills relacionadas

- **copywriting**: Para o copy da landing page (headlines, CTAs, social proof)
- **seo-growth**: Para meta tags, Open Graph e schema markup
- **marketing-strategy**: Para alinhar a landing page com a campanha e o funil
- **platform-mastery**: Para adaptar se a landing page sera compartilhada em redes especificas

---

## 7. social-media-management

**Arquivo**: `growthOS/skills/social-media-management/SKILL.md`

### Descricao

Skill de gestao de redes sociais — estrategias de engajamento, gestao de comunidade,
agendamento, interpretacao de analytics, adaptacao de conteudo por plataforma e
presenca social alinhada com brand voice. Cobre LinkedIn, Twitter/X, Reddit, Threads,
GitHub, YouTube e Instagram.

### Quando ativa

- Criar, planejar ou agendar conteudo para redes sociais
- Definir estrategia de engajamento ou gestao de comunidade
- Analisar performance ou metricas de redes sociais
- Adaptar conteudo para plataformas especificas
- Definir schedules, frequencia ou timing de postagens
- Gerenciar crises de comunicacao em redes sociais

### Capacidades principais

| Capacidade | Detalhe |
|------------|---------|
| Engajamento por plataforma | Padroes especificos para LinkedIn, Twitter/X, Reddit, Threads, GitHub, Instagram, YouTube |
| Scheduling | Tabela de melhores dias/horarios/frequencia por plataforma |
| Community management | Framework de resposta por cenario (feedback, duvida, reclamacao, troll, crise) |
| Gestao de crise | Protocolo de 6 passos: Stop > Assess > Escalate > Respond > Monitor > Debrief |
| Analytics | Template de relatorio com highlights, breakdown por plataforma e recomendacoes |
| Adaptacao de conteudo | Matriz de transformacao: Blog > LinkedIn, Blog > Twitter, Newsletter > Reddit, etc. |
| Batch creation | Estrategia de criacao em lote por formato e tema |
| Calendario semanal | Framework: Mon (plan) > Tue-Thu (publish) > Fri (engage + review) > Weekend (evergreen) |

### 3 exemplos praticos

**Exemplo 1 — Calendario semanal completo**
> "Monte um calendario de redes sociais para a proxima semana com base nos nossos
> pilares de conteudo."
>
> A skill gera: segunda para planejamento, terca a quinta com posts agendados por
> plataforma (LinkedIn as 8-10h, Twitter 9-11h, Instagram 11-13h), sexta para
> engajamento e review de analytics, fim de semana com conteudo evergreen agendado.
> Cada post e adaptado para a plataforma (tom, comprimento, hashtags).

**Exemplo 2 — Protocolo de crise**
> "Um cliente insatisfeito esta gerando thread negativa no Twitter. O que faco?"
>
> A skill ativa o protocolo de crise: (1) para todos os posts agendados, (2) avalia
> a situacao, (3) escala para stakeholders antes de responder, (4) responde com fatos
> e empatia, (5) monitora por 48 horas, (6) faz debrief e atualiza o playbook.

**Exemplo 3 — Interpretacao de analytics**
> "Nosso engagement rate no LinkedIn caiu 30% no ultimo mes. Analise."
>
> A skill gera relatorio com: top post (o que funcionou e por que), tendencia de
> engagement, breakdown por formato (imagem vs texto vs carousel), recomendacoes
> especificas (ex: "trocar de link posts para text-only posts com link no primeiro
> comentario"), e foco para o proximo periodo.

### Dicas de uso

- Anti-slop e MAIS RIGOROSO em social media — cada palavra conta num post curto.
- Nunca poste o mesmo conteudo em todas as plataformas sem adaptar — isso e o oposto
  de ser "platform-native".
- No Reddit, a regra 90/10 e sagrada: 90% de interacoes genuinas, 10% do seu conteudo.
- Tempo de resposta importa: reclamacoes em menos de 1 hora, perguntas em menos de 2 horas.
- Links externos no corpo do post do LinkedIn matam o alcance — coloque no primeiro comentario.

### Skills relacionadas

- **platform-mastery**: Para conhecimento profundo de cada algoritmo
- **content-creation**: Para o conteudo que sera distribuido nas redes
- **copywriting**: Para copy persuasivo nos posts
- **competitive-intelligence**: Para monitorar o que concorrentes fazem nas redes

---

## 8. competitive-intelligence

**Arquivo**: `growthOS/skills/competitive-intelligence/SKILL.md`

### Descricao

Skill de inteligencia competitiva e pesquisa de mercado. Cobre tracking de concorrentes,
analise SWOT, tendencias de mercado, inteligencia de precos e geracao de relatorios
estruturados com executive summaries. E a skill que transforma informacao em insight
acionavel.

### Quando ativa

- Analisar concorrentes ou cenario competitivo
- Conduzir pesquisa de mercado, analise de tendencias ou mapeamento de industria
- Fazer analise SWOT para qualquer produto, empresa ou mercado
- Levantar inteligencia de precos ou analise de posicionamento
- Gerar relatorio de inteligencia competitiva

### Capacidades principais

| Capacidade | Detalhe |
|------------|---------|
| Identificacao de concorrentes | 3 tipos: diretos, indiretos, emergentes — com criterios de identificacao |
| Competitor profile | Template completo: overview, produto, mercado, fontes de inteligencia |
| Monitoramento | Cadencia por fonte: website (semanal), job postings (quinzenal), reviews (mensal), patents (trimestral) |
| SWOT | Template com evidencias obrigatorias, implicacoes estrategicas e regras de qualidade |
| Deteccao de tendencias | Framework de sinais (forte/medio/fraco) com checklist de validacao |
| Inteligencia de precos | Template de landscape, padroes de pricing e analise de posicao |
| Relatorio completo | Estrutura: executive summary > landscape > deep dives > SWOT > trends > pricing > recomendacoes |
| Metodologia de pesquisa | Primaria (entrevistas, trials, monitoring) + secundaria (reports, filings, social) |
| Hierarquia de qualidade | 5 tiers de confiabilidade de dados: pesquisa primaria (mais alta) a rumores (mais baixa) |

### 3 exemplos praticos

**Exemplo 1 — Relatorio competitivo completo**
> "Faca uma analise competitiva do mercado de ferramentas de automacao de marketing."
>
> A skill gera relatorio completo: executive summary (3-5 bullets decisorios), mapa
> de concorrentes por tier, deep dives com perfis estruturados, SWOT evidenciado,
> tendencias validadas com niveis de confianca, analise de precos, e recomendacoes
> em 3 horizontes (0-30 dias, 30-90 dias, 90-365 dias).

**Exemplo 2 — SWOT rapido**
> "Faca um SWOT do nosso produto versus os 3 principais concorrentes."
>
> A skill gera SWOT com regra de qualidade: cada celula tem evidencia (ou e marcada
> como "hipotese nao verificada"), forcas devem ser defensaveis (nao replicaveis em
> 6 meses), fraquezas devem ser materiais, oportunidades devem ter sinais concretos,
> ameacas devem ter probabilidade.

**Exemplo 3 — Monitoramento de tendencia**
> "Estou vendo muitos concorrentes adicionando IA generativa. Isso e tendencia ou hype?"
>
> A skill aplica o framework de deteccao de tendencias: busca 3+ fontes independentes,
> avalia suporte quantitativo, trajectoria temporal, contra-evidencia, e actionability.
> Entrega trend report com nivel de confianca (High/Medium/Low) e acao recomendada
> especifica.

### Dicas de uso

- Toda afirmacao sobre concorrente precisa de fonte — sem fonte, marca como "nao verificado".
- Dados com mais de 90 dias devem ser sinalizados como potencialmente desatualizados.
- O executive summary deve ser lido isoladamente por um executivo ocupado e permitir
  uma decisao.
- Anti-slop especifico para inteligencia: "lider do mercado", "crescimento rapido",
  "bem posicionado" devem ser substituidos por dados concretos.
- Use a hierarquia de qualidade de dados: pesquisa primaria > analistas > imprensa >
  social media > rumores.

### Skills relacionadas

- **marketing-strategy**: Para transformar insights competitivos em estrategia
- **seo-growth**: Para analise de keywords e performance de busca dos concorrentes
- **platform-mastery**: Para monitorar presenca social dos concorrentes por plataforma
- **copywriting**: Para posicionamento diferenciado com base na analise competitiva

---

## 9. platform-mastery

**Arquivo**: `growthOS/skills/platform-mastery/SKILL.md`

### Descricao

Skill de conhecimento profundo de algoritmos e melhores praticas por plataforma —
YouTube, LinkedIn, Twitter/X, Reddit, Instagram, GitHub, Threads e StackOverflow.
Garante que o conteudo seja nativo de cada plataforma em vez de cross-posted genericamente.

### Quando ativa

- Otimizar conteudo para uma plataforma especifica
- Adaptar conteudo entre plataformas (cross-platform)
- Entender o algoritmo de uma plataforma
- Criar conteudo plataforma-nativo
- Precisar de best practices especificas de uma plataforma

### Capacidades principais

| Capacidade | Plataformas cobertas |
|------------|---------------------|
| Algorithm signals | YouTube (CTR, watch time, session), LinkedIn (comments, dwell time), Twitter (engagement rate, media), Reddit (upvote ratio, authenticity), Instagram (saves, shares), GitHub (stars, README quality), Threads (reposts, conversation), StackOverflow (answer score) |
| Content rules | Formatos, tamanhos, tons e anti-patterns por plataforma |
| Optimal format specs | YAML com parametros ideais de cada plataforma |
| Cross-platform adaptation | Matriz de transformacao: como converter conteudo entre plataformas |
| Algorithm update awareness | Diferencia principios duraveis de pesos temporais |

### Plataformas cobertas (resumo rapido)

| Plataforma | Sinal principal | Sweet spot de conteudo | Tom |
|------------|----------------|----------------------|-----|
| YouTube | Watch time + CTR | 8-15 min long-form | Educacional, com personalidade |
| LinkedIn | Comments > reactions | 1200-1500 chars + imagem | Profissional, insight-driven |
| Twitter/X | Engagement rate | 200-280 chars + midia | Conciso, opiniao forte |
| Reddit | Upvote ratio + autenticidade | Text posts, valor genuino | Autentico, sem marketing |
| Instagram | Saves + shares | Carousel (10 slides) | Visual-first, aspiracional |
| GitHub | Stars + community | README de qualidade + releases | Tecnico, preciso |
| Threads | Conversa + reposts | 300-500 chars | Conversacional, casual |
| StackOverflow | Answer quality score | Respostas canonicas | Tecnico, factual |

### 3 exemplos praticos

**Exemplo 1 — Otimizacao para LinkedIn**
> "Como otimizo meus posts de LinkedIn para mais engajamento?"
>
> A skill explica os sinais do algoritmo em ordem de prioridade (comments > dwell time >
> reactions > shares), fornece o template de post (hook nas 3 primeiras linhas, line
> breaks, pergunta no final, 3-5 hashtags, link no primeiro comentario), e lista anti-patterns
> ("I'm excited to announce...", wall of text, links no corpo do post).

**Exemplo 2 — Adaptacao cross-platform**
> "Tenho um blog post. Adapte para LinkedIn, Twitter e Reddit."
>
> A skill aplica a matriz de transformacao: LinkedIn recebe o insight-chave com angulo
> pessoal (1200-1500 chars), Twitter recebe a frase mais provocativa (<280 chars) com
> imagem, Reddit recebe um resumo dos findings com pergunta para discussao (tom autentico,
> zero marketing). Cada adaptacao respeita cultura, formato e tom da plataforma.

**Exemplo 3 — GitHub README otimizado**
> "O README do nosso projeto open-source esta fraco. Melhore."
>
> A skill aplica o template otimizado: badges (CI, version, license), quickstart copiavel
> em 3-5 linhas, lista de features, instalacao step-by-step, link para docs completos,
> contributing guide, e social preview (1280x640). Trata o README como uma landing page
> de conversao.

### Dicas de uso

- Cada plataforma tem cultura propria — o que funciona no LinkedIn pode ser toxico no Reddit.
- Sinais de algoritmo mudam, mas comportamento de usuario e mais estavel. Foque em sinais
  de usuario (tempo de leitura, saves, comentarios de qualidade) sobre mecanicas de algoritmo.
- No Reddit, nunca soe como marketing. Se parecer press release, vai tomar downvote.
- No YouTube, os primeiros 5 segundos decidem tudo — nao desperdice com intro/logo.
- No Instagram, saves sao o sinal mais forte — crie conteudo que vale salvar (educacional,
  referencia, templates).
- No StackOverflow, responda direto primeiro, explique depois. Codigo e obrigatorio.

### Skills relacionadas

- **social-media-management**: Para gestao operacional das plataformas
- **video-production**: Para conteudo especifico de YouTube
- **content-creation**: Para gerar conteudo que sera adaptado por plataforma
- **seo-growth**: Para SEO de YouTube e otimizacao de conteudo pesquisavel

---

## Combinando Skills

O verdadeiro poder do GrowthOS aparece quando multiplas skills trabalham juntas em
um fluxo de trabalho integrado. Abaixo estao os workflows multi-skill mais comuns.

### Workflow 1: Da Estrategia ao Conteudo Publicado

```
marketing-strategy  →  seo-growth  →  content-creation  →  copywriting  →  social-media-management
      |                    |                 |                   |                    |
  Define pilares     Pesquisa keywords  Escreve o artigo   Refina headlines     Distribui nas
  de conteudo        e mapeia intent    com SEO integrado  e CTAs               plataformas
```

**Como funciona na pratica:**

1. `marketing-strategy` define os 3-5 pilares de conteudo baseados em posicionamento e JTBD
2. `seo-growth` faz keyword research para cada pilar, classifica por intent e prioriza
3. `content-creation` escreve o blog post seguindo o keyword map e aplicando SEO on-page
4. `copywriting` refina headline (4U scoring), meta description e CTAs do artigo
5. `social-media-management` adapta o artigo para cada plataforma e agenda publicacao

> **Prompt exemplo:** "Quero lancar uma serie de conteudo sobre automacao de marketing.
> Comece da estrategia ate ter posts prontos para cada rede social."

### Workflow 2: Lancamento de Produto

```
marketing-strategy  →  competitive-intelligence  →  copywriting  →  landing-page-design  →  video-production
      |                        |                        |                  |                       |
  Planeja campanha       Analisa concorrentes      Escreve copy      Gera landing page      Roteiro de
  e define OKRs          e posicionamento          do lancamento     de conversao            video demo
```

**Como funciona na pratica:**

1. `marketing-strategy` cria o brief da campanha com objetivo SMART, timeline e metricas
2. `competitive-intelligence` analisa como concorrentes se posicionam para definir o "wedge"
3. `copywriting` cria o copy de lancamento usando AIDA e gatilhos emocionais
4. `landing-page-design` gera a pagina de conversao com hero, social proof e CTA
5. `video-production` cria roteiro de video demo com hook-first e retention triggers

> **Prompt exemplo:** "Vamos lancar nosso novo recurso de IA. Preciso de analise competitiva,
> landing page e roteiro de video de lancamento."

### Workflow 3: Conteudo Full-Funnel

```
seo-growth  →  content-creation  →  copywriting  →  platform-mastery  →  social-media-management
     |                |                  |                 |                       |
  Define cluster   TOFU: blog post    MOFU: email       Adapta cada peca      Agenda e
  e keywords       (awareness)        nurture (PAS)     para a plataforma     monitora
                   BOFU: comparison
```

**Como funciona na pratica:**

1. `seo-growth` monta o content cluster com pilar e spokes, mapeados por intent de funil
2. `content-creation` produz conteudo para cada estagio: blog de awareness (TOFU),
   guia comparativo (MOFU), case study (BOFU)
3. `copywriting` cria email nurture sequence com PAS para converter leads do TOFU ao BOFU
4. `platform-mastery` adapta cada peca para a plataforma certa (blog no site, insights
   no LinkedIn, dados no Twitter, discussao no Reddit)
5. `social-media-management` agenda, publica e monitora performance

> **Prompt exemplo:** "Monte um funil de conteudo completo para nosso novo cluster de SEO
> sobre 'growth hacking para SaaS'."

### Workflow 4: Inteligencia para Acao

```
competitive-intelligence  →  marketing-strategy  →  content-creation + copywriting
         |                          |                         |
   Identifica gaps e          Transforma insights       Executa a estrategia
   oportunidades              em plano de acao          com conteudo e copy
```

**Como funciona na pratica:**

1. `competitive-intelligence` faz analise completa: SWOT, tendencias, pricing, gaps
2. `marketing-strategy` transforma os insights em OKRs, pilares de conteudo e campanhas
3. `content-creation` + `copywriting` executam a estrategia com conteudo e copy alinhados

> **Prompt exemplo:** "Faca uma analise competitiva e, com base nos resultados, crie uma
> estrategia de conteudo para os proximos 3 meses."

### Workflow 5: YouTube como Canal de Crescimento

```
seo-growth  →  video-production  →  platform-mastery  →  social-media-management
     |                |                    |                       |
  Keyword research   Roteiro + SEO       Otimiza para           Distribui trechos
  para YouTube       de video             algoritmo YouTube      nas redes sociais
```

**Como funciona na pratica:**

1. `seo-growth` faz keyword research focado em YouTube (video keywords, PAA com "how to")
2. `video-production` escreve roteiro com hook-first, retention triggers, description e tags
3. `platform-mastery` otimiza para sinais do algoritmo YouTube (CTR, watch time, session time)
4. `social-media-management` cria cortes/trechos do video para LinkedIn, Twitter e Instagram

> **Prompt exemplo:** "Quero criar um canal de YouTube sobre marketing digital. Comece com
> keyword research e me entregue o roteiro completo do primeiro video."

### Dicas para combinar skills

1. **Comece sempre pela estrategia** — `marketing-strategy` ou `competitive-intelligence`
   devem informar as decisoes antes de criar conteudo.

2. **SEO vem antes da criacao** — `seo-growth` define keywords e intent antes de
   `content-creation` comecar a escrever.

3. **Copywriting refina, nao cria do zero** — Use `content-creation` para a peca base
   e `copywriting` para polir headlines, CTAs e copy de conversao.

4. **Platform-mastery e o filtro final** — Antes de publicar em qualquer plataforma,
   passe pelo conhecimento de algoritmo da `platform-mastery`.

5. **Social media management opera** — `social-media-management` e quem agenda, publica,
   monitora e responde. As outras skills criam, ela distribui.

6. **Competitive intelligence alimenta tudo** — Use `competitive-intelligence` nao
   apenas para relatorios, mas para informar posicionamento, copy e estrategia de conteudo.

---

## Referencia rapida

| Skill | Foco principal | Frameworks-chave |
|-------|---------------|-------------------|
| marketing-strategy | Planejamento estrategico | AARRR, ICE, RICE, JTBD, Category Design |
| content-creation | Criacao de conteudo | 4 templates (blog, newsletter, docs, social), workflow editorial |
| copywriting | Texto persuasivo | AIDA, PAS, 4U Headlines, 7 gatilhos emocionais |
| seo-growth | Busca organica | 5-Layer Keyword Research, Content Clusters, E-E-A-T |
| video-production | Video (text-based) | Hook-First, Retention Triggers, Thumbnail Specs |
| landing-page-design | Paginas de conversao | Single-file HTML, CRO, A/B Variants |
| social-media-management | Gestao de redes sociais | Engagement patterns, Crisis Protocol, Analytics |
| competitive-intelligence | Inteligencia de mercado | SWOT, Trend Detection, Pricing Intelligence |
| platform-mastery | Algoritmos de plataformas | Signals por plataforma, Cross-Platform Adaptation |

---

*GrowthOS Skills Guide v1.0 — Referencia interna da equipe.*
