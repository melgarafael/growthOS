# DESIGN DOCTRINE — Sales Page Production System

> **Este documento e o equivalente visual do GOLDEN-DOC.md.** Todo agente de design DEVE ler este arquivo antes de tomar qualquer decisao visual. Sem excecao.
> **Versao:** v1.0
> **Ultima atualizacao:** 2026-04-13
> **Fonte de verdade:** `growthOS/design-intelligence/DESIGN-DOCTRINE.md`
> **Anti-patterns:** `growthOS/design-intelligence/anti-patterns/AI-SLOP.md`
> **RLHF visual:** `growthOS/design-intelligence/approved/STYLE-PROFILE.md`

---

## Instrucao critica para agentes

**Antes de gerar qualquer sales page, landing page ou componente visual:**
1. Leia este DESIGN-DOCTRINE.md inteiro
2. Leia `anti-patterns/AI-SLOP.md` (o que NUNCA fazer)
3. Leia `approved/STYLE-PROFILE.md` (preferencias aprendidas)
4. Leia `approved/APPROVED-DESIGNS.md` + `anti-patterns/REJECTED-DESIGNS.md` (historico)
5. Se houver conflito entre brief e DOCTRINE, a DOCTRINE ganha (exceto override explicito do usuario)

---

## A. Design Philosophy

### Principio central

**IA e DIRIGIDA por referencias, nao generativa do nada.**

Design sem direcao produz design generico. Inter font, rounded corners, blue gradients, shadcn defaults, layouts de template Canva. Isso e o equivalente visual de "bot" e "chatbot" — generico, sem alma, sem conversao.

### 5 Axiomas

1. **Toda decisao visual rastreia para uma referencia ou principio psicologico.** Nada de "achei bonito". Qual site inspirou? Qual principio de Gestalt? Qual dado de eye-tracking?
2. **Beleza serve conversao.** Estetica sem estrategia e decoracao. Cada pixel existe para mover o usuario em direcao a acao desejada.
3. **O banco de referencias cresce a cada projeto.** RLHF visual — designs aprovados alimentam o perfil, rejeitados alimentam anti-patterns. O sistema melhora continuamente.
4. **Restricao gera criatividade.** Archetypes com tokens concretos nao limitam — eles liberam. A decisao e escolher o archetype certo, nao inventar do zero.
5. **Mobile-first nao e opcional.** 70%+ do trafego de sales pages vem de mobile. Se nao funciona no thumb, nao funciona.

### Hierarquia de decisao

```
1. Usuario pede override explicito      → Respeitar
2. STYLE-PROFILE.md tem preferencia      → Aplicar
3. Archetype do DOCTRINE se encaixa      → Usar tokens
4. Nenhum archetype se encaixa           → Justificar criacao (log em APPROVED/REJECTED)
```

---

## B. Visual Identity Spectrum — 7 Archetypes

Cada archetype define um universo visual completo. A escolha do archetype e a primeira decisao de design — tudo mais deriva dele.

### Archetype 1: `tech-elite`

**Quando usar:** SaaS, dev tools, plataformas tecnicas, dashboards
**Referencias:** Linear, Stripe, Vercel, Raycast
**Vibe:** Precisao cirurgica, confianca silenciosa, premium sem gritar

```yaml
archetype: tech-elite
references: [linear.app, stripe.com, vercel.com, raycast.com]

palette:
  bg_primary: "#09090B"         # zinc-950
  bg_secondary: "#18181B"       # zinc-900
  bg_elevated: "#27272A"        # zinc-800
  ink_primary: "#FAFAFA"        # zinc-50
  ink_secondary: "#A1A1AA"      # zinc-400
  ink_muted: "#71717A"          # zinc-500
  accent_primary: "#A78BFA"     # violet-400
  accent_secondary: "#7C3AED"   # violet-600
  border: "rgba(255,255,255,0.08)"
  glow: "rgba(167,139,250,0.15)"

typography:
  display: "'Inter Display', 'Inter', system-ui, sans-serif"
  display_weight: 600
  body: "'Inter', system-ui, sans-serif"
  body_weight: 400
  mono: "'Geist Mono', 'JetBrains Mono', monospace"
  size_scale:
    hero: "clamp(3rem, 5vw + 1rem, 5.5rem)"
    h2: "clamp(2rem, 3vw + 0.5rem, 3.5rem)"
    h3: "clamp(1.5rem, 2vw + 0.5rem, 2rem)"
    body: "clamp(1rem, 1.2vw, 1.25rem)"
    caption: "clamp(0.75rem, 1vw, 0.875rem)"
  line_height:
    heading: 1.1
    body: 1.6

spacing:
  unit: "0.25rem"               # 4px base
  scale: [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
  section_gap: "clamp(4rem, 8vw, 8rem)"
  content_max_width: "1200px"

animation:
  style: "precise"
  micro: "150ms cubic-bezier(0.4, 0, 0.2, 1)"
  transition: "300ms cubic-bezier(0.4, 0, 0.2, 1)"
  reveal: "500ms cubic-bezier(0, 0, 0.2, 1)"
  scroll_driven: true
  blur_effects: true
  glow_on_hover: true

hero_pattern: "headline-left, subtext-below, cta-inline, product-screenshot-right"
cta_style:
  bg: "accent_primary"
  text: "bg_primary"
  border_radius: "8px"
  padding: "12px 24px"
  hover: "brightness(1.1) + subtle-glow"

distinguishing_features:
  - "Blur/backdrop-filter em cards elevados"
  - "Bordas 1px com opacity baixa"
  - "Glow sutil em hovers e focus states"
  - "Grid lines decorativas em background"
  - "Gradients sutis (nao saturados)"
```

---

### Archetype 2: `ai-native`

**Quando usar:** Produtos de IA, agentes, automacao inteligente, ML tools
**Referencias:** 11x.ai, anthropic.com, openai.com, huggingface.co
**Vibe:** Futuro proximo, inteligencia tangivel, mesh de possibilidades

```yaml
archetype: ai-native
references: [11x.ai, anthropic.com, openai.com, huggingface.co]

palette:
  bg_primary: "#0C0C0F"
  bg_secondary: "#141419"
  bg_elevated: "#1C1C24"
  ink_primary: "#F0F0F5"
  ink_secondary: "#9898A8"
  ink_muted: "#5C5C6E"
  accent_primary: "#6366F1"     # indigo-500
  accent_secondary: "#EC4899"   # pink-500
  accent_gradient: "linear-gradient(135deg, #6366F1 0%, #EC4899 50%, #F59E0B 100%)"
  border: "rgba(255,255,255,0.06)"
  mesh_bg: "radial-gradient(ellipse at 20% 50%, rgba(99,102,241,0.08) 0%, transparent 50%), radial-gradient(ellipse at 80% 20%, rgba(236,72,153,0.06) 0%, transparent 50%)"

typography:
  display: "'Plus Jakarta Sans', system-ui, sans-serif"
  display_weight: 700
  body: "'Plus Jakarta Sans', system-ui, sans-serif"
  body_weight: 400
  mono: "'Fira Code', 'JetBrains Mono', monospace"
  size_scale:
    hero: "clamp(3.5rem, 6vw + 1rem, 6rem)"
    h2: "clamp(2rem, 3.5vw + 0.5rem, 3.5rem)"
    h3: "clamp(1.5rem, 2vw + 0.5rem, 2rem)"
    body: "clamp(1rem, 1.2vw, 1.25rem)"
    caption: "clamp(0.75rem, 1vw, 0.875rem)"
  line_height:
    heading: 1.05
    body: 1.65

spacing:
  unit: "0.25rem"
  scale: [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
  section_gap: "clamp(5rem, 10vw, 10rem)"
  content_max_width: "1280px"

animation:
  style: "fluid"
  micro: "200ms cubic-bezier(0.25, 0.1, 0.25, 1)"
  transition: "400ms cubic-bezier(0.25, 0.1, 0.25, 1)"
  reveal: "600ms cubic-bezier(0, 0, 0.2, 1)"
  cinematic: "1200ms cubic-bezier(0.16, 1, 0.3, 1)"
  scroll_driven: true
  mesh_animation: true
  gradient_shift: true
  particle_effects: "subtle"

hero_pattern: "centered-headline, gradient-text-accent, animated-mesh-bg, cta-center"
cta_style:
  bg: "accent_gradient"
  text: "#FFFFFF"
  border_radius: "12px"
  padding: "14px 32px"
  hover: "scale(1.02) + shadow-glow"

distinguishing_features:
  - "Mesh gradients animados no background"
  - "Gradient text em headlines (accent_gradient)"
  - "Orbs/blobs suaves em movimento lento"
  - "Tipografia maior que o normal — confianca"
  - "Espacamento generoso entre secoes"
```

---

### Archetype 3: `clean-authority`

**Quando usar:** Educacao, consultoria, infoprodutos, SaaS de produtividade
**Referencias:** Cal.com, Notion, Linear (docs), Basehub
**Vibe:** Clareza que gera confianca, estrutura visivel, profissionalismo acessivel

```yaml
archetype: clean-authority
references: [cal.com, notion.so, basehub.com, resend.com]

palette:
  bg_primary: "#FFFFFF"
  bg_secondary: "#FAFAFA"
  bg_elevated: "#F4F4F5"
  ink_primary: "#09090B"        # zinc-950
  ink_secondary: "#52525B"      # zinc-600
  ink_muted: "#A1A1AA"          # zinc-400
  accent_primary: "#18181B"     # zinc-900 (dark accent on light bg)
  accent_secondary: "#6366F1"   # indigo-500 (for interactive)
  border: "rgba(0,0,0,0.08)"
  shadow: "0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06)"

typography:
  display: "'Instrument Serif', 'Georgia', serif"
  display_weight: 400
  body: "'Inter', system-ui, sans-serif"
  body_weight: 400
  mono: "'Geist Mono', monospace"
  size_scale:
    hero: "clamp(3rem, 5vw + 1rem, 5rem)"
    h2: "clamp(2rem, 3vw + 0.5rem, 3rem)"
    h3: "clamp(1.25rem, 2vw + 0.25rem, 1.75rem)"
    body: "clamp(1rem, 1.1vw, 1.125rem)"
    caption: "clamp(0.75rem, 0.9vw, 0.875rem)"
  line_height:
    heading: 1.15
    body: 1.7

spacing:
  unit: "0.25rem"
  scale: [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
  section_gap: "clamp(4rem, 8vw, 7rem)"
  content_max_width: "960px"

animation:
  style: "minimal"
  micro: "150ms ease"
  transition: "250ms ease"
  reveal: "400ms ease-out"
  scroll_driven: false
  prefer_no_animation: true
  only_essential: true

hero_pattern: "centered-headline, serif-display, illustrations, clean-cta-below"
cta_style:
  bg: "accent_primary"
  text: "bg_primary"
  border_radius: "6px"
  padding: "12px 24px"
  hover: "opacity(0.9)"

distinguishing_features:
  - "Serif display + sans body = contraste de hierarquia classico"
  - "Ilustracoes custom (nao icones genericos)"
  - "Muito white space — respira"
  - "Shadows sutis em cards (nao borders pesados)"
  - "Layout estreito (960px max) para leitura confortavel"
```

---

### Archetype 4: `cinematic`

**Quando usar:** Produtos premium, lancamentos, experiencias imersivas
**Referencias:** apple.com, arc.net, nothing.tech, teenage.engineering
**Vibe:** Cada scroll e uma cena, storytelling visual, pin sections

```yaml
archetype: cinematic
references: [apple.com/macbook-pro, arc.net, nothing.tech, teenage.engineering]

palette:
  bg_primary: "#000000"
  bg_secondary: "#0A0A0A"
  bg_elevated: "#141414"
  ink_primary: "#FFFFFF"
  ink_secondary: "#999999"
  ink_muted: "#666666"
  accent_primary: "#FFFFFF"     # white-on-black e o accent
  accent_secondary: "#3B82F6"   # blue-500 (sparingly)
  border: "rgba(255,255,255,0.1)"

typography:
  display: "'SF Pro Display', 'Inter Display', system-ui, sans-serif"
  display_weight: 700
  body: "'SF Pro Text', 'Inter', system-ui, sans-serif"
  body_weight: 400
  mono: "'SF Mono', 'Geist Mono', monospace"
  size_scale:
    hero: "clamp(4rem, 8vw + 1rem, 8rem)"
    h2: "clamp(2.5rem, 4vw + 1rem, 5rem)"
    h3: "clamp(1.5rem, 2vw + 0.5rem, 2.5rem)"
    body: "clamp(1.05rem, 1.3vw, 1.25rem)"
    caption: "clamp(0.8rem, 1vw, 0.9rem)"
  line_height:
    heading: 1.0
    body: 1.6

spacing:
  unit: "0.25rem"
  scale: [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96]
  section_gap: "100vh"          # cada secao ocupa a tela inteira
  content_max_width: "1440px"

animation:
  style: "cinematic"
  micro: "200ms cubic-bezier(0.25, 0.1, 0.25, 1)"
  transition: "500ms cubic-bezier(0.25, 0.1, 0.25, 1)"
  reveal: "800ms cubic-bezier(0.16, 1, 0.3, 1)"
  cinematic: "1500ms cubic-bezier(0.16, 1, 0.3, 1)"
  scroll_driven: true
  pin_sections: true
  parallax: true
  video_backgrounds: true
  canvas_animations: true

hero_pattern: "fullscreen-video-or-canvas, headline-centered-massive, scroll-indicator"
cta_style:
  bg: "transparent"
  text: "ink_primary"
  border: "1px solid rgba(255,255,255,0.3)"
  border_radius: "999px"        # pill shape
  padding: "14px 32px"
  hover: "bg-white, text-black (invert)"

distinguishing_features:
  - "Secoes full-viewport com scroll snapping ou pin"
  - "Video/canvas como background de hero"
  - "Headlines MASSIVAS (8rem+)"
  - "Parallax com proposito narrativo"
  - "Transicoes entre secoes sao eventos"
  - "Minimal UI — conteudo e a interface"
```

---

### Archetype 5: `conversion-machine`

**Quando usar:** Vendas diretas, infoprodutos, lancamentos com urgencia, direct response
**Referencias:** VSL classicas, Hormozi-style, Russell Brunson funnels
**Vibe:** Cada elemento otimizado para acao, urgencia real, prova social pesada

```yaml
archetype: conversion-machine
references: [acquisition.com, clickfunnels-style, classic-VSL-pages]

palette:
  bg_primary: "#FFFFFF"
  bg_secondary: "#F8F9FA"
  bg_elevated: "#FFF8E1"        # warm highlight sections
  bg_urgency: "#FEF2F2"         # red-tinted urgency bands
  ink_primary: "#1A1A1A"
  ink_secondary: "#4A4A4A"
  ink_muted: "#8A8A8A"
  accent_primary: "#DC2626"     # red-600 (urgency/CTA)
  accent_secondary: "#16A34A"   # green-600 (money/success)
  accent_tertiary: "#EAB308"    # yellow-500 (highlight)
  border: "rgba(0,0,0,0.1)"

typography:
  display: "'DM Sans', 'Inter', system-ui, sans-serif"
  display_weight: 800
  body: "'DM Sans', system-ui, sans-serif"
  body_weight: 400
  mono: "'JetBrains Mono', monospace"
  highlight_font: "'Caveat', cursive"   # handwritten annotations
  size_scale:
    hero: "clamp(2.5rem, 4vw + 1rem, 4.5rem)"
    h2: "clamp(1.75rem, 3vw + 0.5rem, 3rem)"
    h3: "clamp(1.25rem, 2vw + 0.25rem, 1.75rem)"
    body: "clamp(1.05rem, 1.2vw, 1.2rem)"
    caption: "clamp(0.8rem, 1vw, 0.9rem)"
  line_height:
    heading: 1.2
    body: 1.75

spacing:
  unit: "0.25rem"
  scale: [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
  section_gap: "clamp(3rem, 6vw, 5rem)"
  content_max_width: "800px"    # estreito — forca leitura vertical

animation:
  style: "functional"
  micro: "150ms ease"
  transition: "250ms ease"
  reveal: "300ms ease-out"
  scroll_driven: false
  countdown_timers: true
  attention_pulses: true
  no_decorative_animation: true

hero_pattern: "pain-headline, subheadline-promise, video-vsl-or-testimonial, cta-below"
cta_style:
  bg: "accent_primary"
  text: "#FFFFFF"
  border_radius: "4px"
  padding: "16px 40px"
  font_size: "1.25rem"
  font_weight: 800
  hover: "brightness(1.1) + scale(1.02)"
  shadow: "0 4px 14px rgba(220,38,38,0.4)"

distinguishing_features:
  - "CTA repetido a cada 2-3 secoes (sticky + inline)"
  - "Social proof acima do fold (logos, numeros, depoimentos)"
  - "Highlight com 'marker' amarelo em texto-chave"
  - "Setas e anotacoes handwritten apontando para CTAs"
  - "Secoes de urgencia com bg diferenciado"
  - "Garantia com selo visual proeminente"
  - "FAQ como objection-handling (nao informativo)"
  - "Layout narrow (800px) para leitura tipo carta"
```

---

### Archetype 6: `builder-maker`

**Quando usar:** Open-source, developer tools, CLI tools, APIs
**Referencias:** n8n.io, github.com, supabase.com, deno.com
**Vibe:** Transparente, tecnico mas acessivel, show-don't-tell com codigo

```yaml
archetype: builder-maker
references: [n8n.io, supabase.com, deno.com, github.com]

palette:
  bg_primary: "#0D1117"         # github-dark
  bg_secondary: "#161B22"
  bg_elevated: "#21262D"
  bg_code: "#1C2128"
  ink_primary: "#E6EDF3"
  ink_secondary: "#8B949E"
  ink_muted: "#6E7681"
  accent_primary: "#58A6FF"     # blue link-style
  accent_secondary: "#3FB950"   # green (success/available)
  accent_tertiary: "#F78166"    # orange (warning/highlight)
  border: "rgba(240,246,252,0.1)"
  syntax:
    keyword: "#FF7B72"
    string: "#A5D6FF"
    function: "#D2A8FF"
    comment: "#8B949E"
    variable: "#FFA657"

typography:
  display: "'Space Grotesk', system-ui, sans-serif"
  display_weight: 700
  body: "'Inter', system-ui, sans-serif"
  body_weight: 400
  mono: "'JetBrains Mono', 'Fira Code', monospace"
  size_scale:
    hero: "clamp(2.5rem, 4vw + 1rem, 4.5rem)"
    h2: "clamp(1.75rem, 3vw + 0.5rem, 2.5rem)"
    h3: "clamp(1.25rem, 2vw + 0.25rem, 1.75rem)"
    body: "clamp(0.95rem, 1.1vw, 1.125rem)"
    caption: "clamp(0.75rem, 0.9vw, 0.875rem)"
    code: "clamp(0.85rem, 1vw, 0.95rem)"
  line_height:
    heading: 1.15
    body: 1.65
    code: 1.5

spacing:
  unit: "0.25rem"
  scale: [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
  section_gap: "clamp(4rem, 8vw, 7rem)"
  content_max_width: "1100px"

animation:
  style: "subtle"
  micro: "150ms ease"
  transition: "200ms ease"
  reveal: "400ms ease-out"
  scroll_driven: false
  terminal_typing: true
  code_highlight_on_scroll: true

hero_pattern: "headline-left, code-block-right, terminal-aesthetic, install-command"
cta_style:
  bg: "accent_primary"
  text: "#FFFFFF"
  border_radius: "6px"
  padding: "10px 20px"
  hover: "brightness(1.1)"
  secondary_cta:
    bg: "transparent"
    text: "ink_primary"
    border: "1px solid rgba(240,246,252,0.2)"

distinguishing_features:
  - "Code blocks com syntax highlighting proeminentes"
  - "Terminal/CLI demos animados"
  - "Comando de install copiavel no hero"
  - "Tabs de linguagem (JS/Python/Go/etc)"
  - "GitHub-style contributor stats"
  - "Architecture diagrams inline"
```

---

### Archetype 7: `luxury-minimal`

**Quando usar:** Servicos high-end, consultoria premium, 1-on-1, whitelabel
**Referencias:** superhuman.com, linear.app (marketing), monaspace.githubnext.com
**Vibe:** Exclusividade implicita, menos e mais, cada pixel e intencional

```yaml
archetype: luxury-minimal
references: [superhuman.com, monaspace.githubnext.com, family-offices]

palette:
  bg_primary: "#FAFAF9"         # stone-50
  bg_secondary: "#F5F5F4"       # stone-100
  bg_elevated: "#FFFFFF"
  bg_dark_section: "#1C1917"    # stone-900 (para secoes de contraste)
  ink_primary: "#1C1917"        # stone-900
  ink_secondary: "#57534E"      # stone-600
  ink_muted: "#A8A29E"          # stone-400
  ink_on_dark: "#FAFAF9"
  accent_primary: "#1C1917"     # dark-as-accent (no bright colors)
  accent_secondary: "#B45309"   # amber-700 (warm, subtle)
  border: "rgba(0,0,0,0.06)"
  divider: "rgba(0,0,0,0.08)"

typography:
  display: "'Playfair Display', 'Georgia', serif"
  display_weight: 400
  body: "'Satoshi', 'Inter', system-ui, sans-serif"
  body_weight: 400
  mono: "'Geist Mono', monospace"
  letter_spacing:
    heading: "-0.02em"
    body: "0"
    label: "0.1em"              # uppercase labels com tracking
  size_scale:
    hero: "clamp(3rem, 5vw + 1rem, 5rem)"
    h2: "clamp(2rem, 3vw + 0.5rem, 3rem)"
    h3: "clamp(1.25rem, 1.5vw + 0.5rem, 1.5rem)"
    body: "clamp(1rem, 1.1vw, 1.125rem)"
    caption: "clamp(0.7rem, 0.8vw, 0.8rem)"
    label: "clamp(0.65rem, 0.75vw, 0.75rem)"
  line_height:
    heading: 1.1
    body: 1.75

spacing:
  unit: "0.25rem"
  scale: [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96]
  section_gap: "clamp(6rem, 12vw, 10rem)"
  content_max_width: "880px"    # muito estreito — exclusividade

animation:
  style: "restrained"
  micro: "200ms cubic-bezier(0.4, 0, 0.2, 1)"
  transition: "350ms cubic-bezier(0.4, 0, 0.2, 1)"
  reveal: "600ms cubic-bezier(0.16, 1, 0.3, 1)"
  scroll_driven: true
  fade_only: true               # so fade-in, nada de slide/bounce
  no_bounce: true
  no_overshoot: true

hero_pattern: "centered-serif-headline, massive-whitespace, single-cta, no-image"
cta_style:
  bg: "transparent"
  text: "accent_primary"
  border: "1px solid currentColor"
  border_radius: "0px"          # sharp corners = luxury
  padding: "14px 32px"
  font_weight: 400
  letter_spacing: "0.05em"
  text_transform: "uppercase"
  hover: "bg-fills-to-dark, text-inverts-to-white"

distinguishing_features:
  - "Negative space EXTREMO — 60%+ da pagina e espaco vazio"
  - "Serif display + sans body = classe"
  - "Sem cores vibrantes — palette neutra/warm"
  - "Labels uppercase com tracking largo"
  - "Dividers sutis horizontais entre secoes"
  - "CTA discreto (nao grita, convida)"
  - "Secoes dark intercaladas com light"
```

---

## Archetype Selection Matrix

| Contexto do produto | Archetype primario | Fallback |
|---|---|---|
| SaaS / Dev Tools | `tech-elite` | `builder-maker` |
| Produto de IA / Agentes | `ai-native` | `tech-elite` |
| Educacao / Curso / Mentoria | `clean-authority` | `conversion-machine` |
| Lancamento premium / Apple-like | `cinematic` | `luxury-minimal` |
| Venda direta / Infoproduto | `conversion-machine` | `clean-authority` |
| Open-source / API / CLI | `builder-maker` | `tech-elite` |
| Servico high-end / Consultoria | `luxury-minimal` | `clean-authority` |

**Regra:** Se em duvida entre dois archetypes, escolha pelo **publico-alvo** (quem vai comprar), nao pelo produto em si.

---

## C. Typography Rules

### Display Fonts — Ranked by Emotional Impact

| Rank | Font | Emotion | Best For |
|---|---|---|---|
| 1 | Playfair Display | Elegancia, autoridade | luxury-minimal, premium |
| 2 | Space Grotesk | Tecnico, moderno | builder-maker, tech |
| 3 | Plus Jakarta Sans | Amigavel, profissional | ai-native, clean |
| 4 | DM Sans | Neutro, versátil | conversion-machine |
| 5 | Instrument Serif | Classico, editorial | clean-authority |
| 6 | Bricolage Grotesque | Expressivo, unico | branding forte |
| 7 | Inter Display | Neutro, seguro | fallback universal |
| 8 | Geist | Tecnico, clean | tech-elite, builder |
| 9 | Satoshi | Humanista, modern | luxury-minimal body |
| 10 | Cabinet Grotesk | Bold, impactful | headlines de impacto |

### Body Fonts — Ranked by Readability

| Rank | Font | Size Range Optima | Best For |
|---|---|---|---|
| 1 | Inter | 14-18px | Universal |
| 2 | DM Sans | 15-18px | Textos longos |
| 3 | Plus Jakarta Sans | 15-18px | Friendly contexts |
| 4 | Satoshi | 15-17px | Premium contexts |
| 5 | System UI stack | 14-18px | Performance-first |

### Mono Fonts

| Font | Use Case |
|---|---|
| Geist Mono | Dados, numeros, badges |
| JetBrains Mono | Code blocks, terminal |
| Fira Code | Code com ligatures |
| SF Mono | Apple-like contexts |

### Font Pairing Rules

1. **Serif display + Sans body** = Hierarquia classica (Playfair + Inter, Instrument + Inter)
2. **Grotesk display + Sans body** = Moderno (Space Grotesk + Inter, Cabinet + DM Sans)
3. **Same family different weights** = Coesao (Inter Display 600 + Inter 400)
4. **NUNCA:** Duas serifs. Duas scripts. Duas mono para texto corrido.
5. **Max 3 familias:** 1 display + 1 body + 1 mono. Sem excecao.

### Fluid Type Scale (Utopia-style)

```css
/* Base: 16px at 320vw → 20px at 1440vw */
--step--2: clamp(0.6944rem, 0.6532rem + 0.2063vi, 0.8rem);
--step--1: clamp(0.8333rem, 0.7703rem + 0.315vi, 1rem);
--step-0:  clamp(1rem, 0.9048rem + 0.4762vi, 1.25rem);
--step-1:  clamp(1.2rem, 1.0591rem + 0.7043vi, 1.5625rem);
--step-2:  clamp(1.44rem, 1.2359rem + 1.0205vi, 1.9531rem);
--step-3:  clamp(1.728rem, 1.4387rem + 1.4463vi, 2.4414rem);
--step-4:  clamp(2.0736rem, 1.6711rem + 2.0127vi, 3.0518rem);
--step-5:  clamp(2.4883rem, 1.9373rem + 2.7553vi, 3.8147rem);
```

---

## D. Color Psychology Rules

### Color → Emotion → Sales Context

| Color Family | Emocao Primaria | Uso em Sales | Cuidado |
|---|---|---|---|
| **Azul** | Confianca, seguranca | Pricing, garantias, SaaS | Azul generico e SLOP — diferencie o tom |
| **Verde** | Sucesso, dinheiro, go | CTAs de compra, resultados, savings | Nao use verde pra features tech |
| **Vermelho** | Urgencia, atencao | Countdown, limitacao, CTA de urgencia | Usar com moderacao — muito = panico |
| **Amarelo/Amber** | Destaque, atencao | Highlights, warnings, badges "novo" | Nunca como bg de secao inteira |
| **Violeta/Indigo** | Premium, inovacao | Tiers premium, features de IA | Combina com dark bg |
| **Rosa/Pink** | Energia, modernidade | Acento em gradients, badges | Nao como primaria em B2B |
| **Preto** | Poder, elegancia | Bgs premium, CTAs luxury | Precisa de tipografia forte |
| **Branco** | Clareza, abertura | Light mode, documentacao | Precisa de hierarquia forte |
| **Stone/Warm Neutral** | Sofisticacao, acessibilidade | Luxury, consultoria | Pode parecer "vazio" sem tipografia forte |

### Primary Palette Selection Framework

```
1. Audiencia e tecnica? → Dark bg (tech-elite, builder-maker, ai-native)
2. Audiencia e consumer/SMB? → Light bg (clean-authority, conversion-machine)
3. Produto e premium? → Neutral palette (luxury-minimal)
4. Produto e urgente/lancamento? → Accent forte (conversion-machine)
```

### Accent Color Rules

- **1 accent primario** por pagina. MAXIMO 2 se justificado (primary + success).
- Accent ocupa **no maximo 10%** da area visual total.
- Accent so aparece em: CTAs, highlights de texto, badges, hovers, focus states.
- Accent NUNCA em: backgrounds de secao inteira, imagens, grandes blocos de cor.

### Gradient Rules

**Quando usar:**
- Mesh backgrounds em `ai-native` (sutil, animado)
- Text gradients em headlines quando archetype permite
- Hover states com gradients sutis

**Quando NAO usar:**
- Gradients como bg de secao (exceto mesh sutil)
- Gradients em mais de 2 cores (vira Canva)
- Gradients em CTAs (exceto `ai-native`)
- Gradients "bonitos mas sem proposito"

### Dark Mode vs Light Mode

| Decisao | Dark | Light |
|---|---|---|
| Audiencia tech | X | |
| Audiencia consumer | | X |
| Produto premium | X (com cuidado) | X (com cuidado) |
| Demonstracao de produto (screenshots) | X (screenshots brilham) | |
| Texto longo / educativo | | X |
| Lancamento / evento | X | |
| Fallback se nao sabe | | X |

---

## E. Motion & Animation Rules

### Speed Scale

| Categoria | Duracao | Easing | Uso |
|---|---|---|---|
| **Micro** | 100-200ms | `ease` ou `cubic-bezier(0.4, 0, 0.2, 1)` | Hover, toggle, tooltip |
| **Transition** | 250-400ms | `cubic-bezier(0.4, 0, 0.2, 1)` | Menu, modal, accordion |
| **Reveal** | 400-700ms | `cubic-bezier(0, 0, 0.2, 1)` ou `cubic-bezier(0.16, 1, 0.3, 1)` | Scroll-triggered entry |
| **Cinematic** | 800-1500ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Hero animations, transitions de secao |
| **Loop** | 3000-8000ms | `linear` ou custom | Mesh gradients, particles, orbs |

### Quando Animar

| Trigger | Animar? | Tipo |
|---|---|---|
| **Hover** | Sim | Micro (150ms). Scale, color, glow |
| **Focus** | Sim | Micro. Outline/ring visivel |
| **Scroll entry** | Sim (1x) | Reveal. Fade-in + translate sutil |
| **Scroll progress** | Depende do archetype | Cinematic/AI-native sim. Clean-authority nao |
| **Page load** | Hero sim, resto nao | Reveal no hero. Resto carrega normal |
| **Interaction (click/tap)** | Sim | Micro. Feedback tactil |
| **Background** | Depende do archetype | AI-native sim (mesh). Clean-authority nao |

### Quando NAO Animar

1. **Texto corrido/body** — nunca anima paragrafo inteiro entrando. Pesa e distrai.
2. **Elementos repetidos** — se tem 6 cards, nao faz 6 animacoes staggered de 800ms cada. Fade-in grupo.
3. **Performance-killing** — se blur + parallax + video bg + particles ao mesmo tempo, corta 2.
4. **Mobile com bateria** — reduzir animacoes. `prefers-reduced-motion` e obrigatorio.
5. **Formularios** — zero animacao decorativa. Foco e funcao.

### prefers-reduced-motion (OBRIGATORIO)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Todos os archetypes DEVEM implementar este media query.** Sem excecao.

### Scroll-Driven Animation Decision Tree

```
O archetype permite scroll-driven?
├── NAO (clean-authority, conversion-machine) → Nao use. Fade-in basico so.
└── SIM (cinematic, ai-native, tech-elite)
    ├── E hero section? → Pin + parallax permitidos
    ├── E feature showcase? → Progress-linked animation permitido
    ├── E decorativo? → So se nao impacta performance (< 16ms frame)
    └── E mobile? → Desliga pin/parallax. Mantem fade-in.
```

---

## F. Layout Rules

### Every Layout Primitives

Usar composable layout primitives em vez de magic numbers. Baseado em Every Layout (https://every-layout.dev):

| Primitive | Uso | CSS Pattern |
|---|---|---|
| **Stack** | Vertical flow com gap uniforme | `display: flex; flex-direction: column; gap: var(--space)` |
| **Box** | Padding interno uniforme | `padding: var(--space)` |
| **Center** | Centralizar conteudo com max-width | `max-width: var(--measure); margin-inline: auto` |
| **Cluster** | Itens inline com wrap | `display: flex; flex-wrap: wrap; gap: var(--space)` |
| **Sidebar** | Layout sidebar-main responsivo | `display: flex; flex-wrap: wrap; > :first-child { flex-basis: 20rem }` |
| **Switcher** | Switch row→column baseado em threshold | `display: flex; flex-wrap: wrap; > * { flex-grow: 1; flex-basis: calc((var(--threshold) - 100%) * 999) }` |
| **Cover** | Elemento centrado em container de altura fixa | `display: flex; flex-direction: column; min-height: 100vh; > * { margin-block: auto }` |
| **Frame** | Aspect ratio fixo | `aspect-ratio: 16/9; overflow: hidden` |
| **Grid** | Auto-fit grid responsivo | `display: grid; grid-template-columns: repeat(auto-fit, minmax(min(var(--min), 100%), 1fr))` |
| **Reel** | Scroll horizontal | `display: flex; overflow-x: auto; scroll-snap-type: x mandatory` |

### Fluid Spacing Scale (Utopia-style)

```css
/* Space: 4px at 320vw → 8px at 1440vw (base) */
--space-3xs: clamp(0.25rem, 0.2262rem + 0.119vi, 0.3125rem);
--space-2xs: clamp(0.5rem, 0.4524rem + 0.2381vi, 0.625rem);
--space-xs:  clamp(0.75rem, 0.6786rem + 0.3571vi, 0.9375rem);
--space-s:   clamp(1rem, 0.9048rem + 0.4762vi, 1.25rem);
--space-m:   clamp(1.5rem, 1.3571rem + 0.7143vi, 1.875rem);
--space-l:   clamp(2rem, 1.8095rem + 0.9524vi, 2.5rem);
--space-xl:  clamp(3rem, 2.7143rem + 1.4286vi, 3.75rem);
--space-2xl: clamp(4rem, 3.619rem + 1.9048vi, 5rem);
--space-3xl: clamp(6rem, 5.4286rem + 2.8571vi, 7.5rem);
```

### Section Spacing Hierarchy

| Nivel | Space | Uso |
|---|---|---|
| **Secao** | `--space-3xl` a `--space-2xl` | Entre secoes principais |
| **Bloco** | `--space-xl` a `--space-l` | Entre blocos dentro de secao |
| **Grupo** | `--space-m` a `--space-s` | Entre elementos relacionados |
| **Inline** | `--space-xs` a `--space-3xs` | Entre items inline, icons+text |

### Responsive Strategy

**Intrinsic design, nao device-based:**

```css
/* NAO faca isso: */
@media (max-width: 768px) { ... }  /* arbitrary breakpoint */

/* Faca isso: */
.grid {
  grid-template-columns: repeat(auto-fit, minmax(min(20rem, 100%), 1fr));
}

/* Ou com container queries: */
@container (min-width: 40rem) { ... }
```

**Breakpoints, quando necessarios, sao baseados em conteudo:**
- Quando o texto "quebra" de forma ruim → add breakpoint
- Quando a imagem fica proporcao errada → add breakpoint
- NAO adicionar breakpoint porque "iPad tem X pixels"

### Golden Ratio Applications

| Proporcao | Uso |
|---|---|
| `1:1.618` | Hero split (texto:imagem) |
| `1:2.618` | Sidebar ratio |
| `3:5:8` | Three-column weight distribution |
| `61.8% : 38.2%` | Feature section split |

---

## G. Mandatory Consultation Flow

Este e o fluxo que todo agente de design DEVE seguir antes de produzir qualquer visual.

```
STEP 1 — CONTEXT GATHERING
├── Qual e o produto?
├── Quem e o publico-alvo?
├── Qual a acao desejada? (comprar, agendar, baixar, inscrever)
├── Existe referencia visual do usuario?
└── Qual o tom do copy? (ver GOLDEN-DOC.md)

STEP 2 — ARCHETYPE SELECTION
├── Consultar "Archetype Selection Matrix" acima
├── Se em duvida: decidir pelo publico-alvo
├── Se usuario deu referencia: qual archetype mais proximo?
└── Logar a decisao

STEP 3 — STYLE-PROFILE CHECK
├── Ler approved/STYLE-PROFILE.md
├── Preferencias aprendidas override tokens default?
├── Anti-patterns ativos aplicam aqui?
└── Se sim, ajustar tokens

STEP 4 — TOKEN APPLICATION
├── Carregar tokens do archetype selecionado
├── Aplicar overrides do STYLE-PROFILE
├── Gerar CSS custom properties
└── Definir layout primitives

STEP 5 — DESIGN EXECUTION
├── Estruturar sections seguindo hero_pattern do archetype
├── Aplicar spacing scale
├── Implementar animacoes conforme regras do archetype
├── Verificar AI-SLOP.md (zero Tier 1 violations)
└── Verificar mobile responsiveness

STEP 6 — REVIEW & LOG
├── Self-review contra AI-SLOP.md (3 tiers)
├── Se aprovado pelo usuario → logar em APPROVED-DESIGNS.md
├── Se rejeitado → logar em REJECTED-DESIGNS.md com tags
└── Rodar update de STYLE-PROFILE.md
```

### Archetype Override

O usuario pode combinar archetypes com justificativa:

```
"Use tech-elite como base mas com a tipografia de luxury-minimal"
```

Nesse caso:
1. Carregar tokens completos do archetype base (`tech-elite`)
2. Override SOMENTE os tokens solicitados (typography)
3. Logar a decisao como `archetype: tech-elite + luxury-minimal/typography`

Combinacoes nao justificadas (ex: "mistura tudo") sao rejeitadas. O agente deve pedir clarificacao.

---

## Appendix: Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│                  DESIGN DOCTRINE v1                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. LEIA este doc antes de qualquer decisao visual  │
│  2. ESCOLHA um archetype (nao invente)              │
│  3. USE os tokens concretos (nao improvise)         │
│  4. VERIFIQUE contra AI-SLOP.md                     │
│  5. LOGUE no APPROVED ou REJECTED                   │
│  6. ATUALIZE o STYLE-PROFILE                        │
│                                                     │
│  Beleza serve conversao.                            │
│  IA e DIRIGIDA, nao generativa.                     │
│  Restricao gera criatividade.                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```
