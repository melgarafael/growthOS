# AI-SLOP — Visual Anti-Pattern System

> **O equivalente visual do anti-slop de copy.** Todo agente de design DEVE verificar contra este documento antes de entregar qualquer output visual.
> **Versao:** v1.0
> **Ultima atualizacao:** 2026-04-13
> **Regra:** qualquer violacao Tier 1 e auto-reject. Tier 2 flag pra review. Tier 3 be aware.

---

## O que e AI-SLOP visual?

Quando IA gera design sem direcao, converge para um set de padroes default que sao:
- Esteticamente "bonitos" mas genericos
- Indistinguiveis de 10.000 outras landing pages
- Otimizados para agradar olho do gerador, nao para converter
- O equivalente visual de "unlock the power of AI" no copy

**AI-SLOP visual e design que poderia ser de qualquer produto, para qualquer audiencia, em qualquer contexto.** Se voce trocar o logo e o copy e ninguem percebe, e SLOP.

---

## Tier 1 — Hard Bans (Auto-Reject)

Qualquer item abaixo presente no output = rejeicao automatica. Nao ha discussao.

### Palette & Color

| Ban | Por que | O que fazer |
|---|---|---|
| Gradientes coloridos genericos (rainbow, Canva-style) | Nao comunica nada. Decoracao pura. | Usar paleta do archetype. Se precisa gradiente, use mesh sutil ou gradient text. |
| Azul CTA sem justificativa | "#3B82F6 como CTA porque e azul e azul e confianca" e a decisao mais preguicosa possivel | Escolher CTA color baseado no archetype e no contraste com bg. |
| Mais de 2 cores de acento | Poluicao visual. Dilui a atencao. | 1 accent primario. Max 1 secondary pra estados especificos (success, warning). |
| Fundo branco puro (#FFFFFF) com texto preto puro (#000000) | Contraste excessivo causa fadiga. Zero sofisticacao. | Use off-white (#FAFAFA+) e off-black (#1A1A1A-). Reduz contraste ratio de 21:1 pra ~18:1 mantendo WCAG AAA. |

### Typography

| Ban | Por que | O que fazer |
|---|---|---|
| Inter/Roboto como display font | Sao excelentes body fonts. Como display, sao o equivalente de "Dear User" em copy. Zero personalidade. | Usar display fonts do archetype. Inter so como body. |
| Mais de 3 familias de fonte | Caos tipografico. Sem hierarquia. | 1 display + 1 body + 1 mono. Nao mais. |
| Fonte script/handwritten como display principal | Legibilidade zero em tela. Infantiliza. | Reservar pra anotacoes decorativas (Caveat em highlights no conversion-machine, por exemplo). |
| Tamanhos de fonte iguais pra headline e body | Hierarquia zero. Tudo tem o mesmo peso. | Manter ratio minimo de 2:1 entre hero headline e body. |

### Layout

| Ban | Por que | O que fazer |
|---|---|---|
| Tudo centralizado (texto, CTAs, imagens, titulos) | Preguica de layout. Sem ritmo de leitura. Sem hierarquia espacial. | Left-align como default. Center so pra hero headline e CTAs isolados. |
| Cookie-cutter hero: texto esquerda + mockup direita + gradiente bg | O layout mais generico da internet em 2024-2026. | Usar hero_pattern do archetype selecionado. |
| Testimonials em cards identicos numa grid 3x1 | Visto em 100% das landing pages genericas. | Variar: quote grande + avatar, carousel, video depoimento, cite com destaque tipografico. |
| Pricing table padrao sem diferenciacao visual | Tres colunas, highlight no do meio, "Popular" badge. Boring. | Diferenciar visualmente o plano recomendado com bg, escala, ou posicao. |
| Secoes sem espacamento vertical claro | Tudo colado, sensacao de template. | Usar section_gap do archetype (minimo --space-2xl entre secoes). |

### Assets

| Ban | Por que | O que fazer |
|---|---|---|
| Stock photos genericas (handshake, laptop-on-desk, diverse-team-smiling) | Ninguem acredita. Destroi credibilidade. | Foto real, screenshot de produto, ilustracao custom, ou sem imagem (tipografia forte). |
| Icones genericos como hero elements (Lucide/Heroicons default sem customizacao) | Icones default sao placeholder, nao design. | Se precisa icones: custom, ou Phosphor/Tabler com cor/tamanho customizado. Nunca como elemento principal. |
| Rounded corners > 16px em cards | Bubblegum aesthetic. Infantiliza. Canva-coded. | border-radius max 12px em cards. 8px em buttons (exceto pill-shape intencional). |

---

## Tier 2 — Style Rules (Flag for Review)

Items abaixo nao sao auto-reject, mas devem ser flagged e justificados. Se nao ha justificativa, corrigir.

### Composition

| Flag | Quando e OK | Quando e SLOP |
|---|---|---|
| Animacao > 2s em elementos nao-cinematicos | archetype `cinematic` com pin sections | Fade-in de card de feature levando 2.5s |
| Texto sobre background busy sem overlay | Background e blur artistico intencional (cinematic) | Screenshot de produto como bg com texto on top |
| CTAs abaixo do fold sem alternativa sticky | Layout one-page com scroll curto | Sales page longa sem CTA visivel apos hero |
| Sem social proof acima do fold | luxury-minimal (exclusividade > prova) | conversion-machine sem depoimentos/logos no hero |
| Parallax sem proposito narrativo | cinematic showcase de produto | Parallax decorativo em secao de FAQ |
| Secoes sem hierarquia visual clara | | Sempre SLOP — hierarquia e obrigatoria |
| Formulario inline sem estado de loading/success | | Sempre flag — UX incompleta |
| Pricing sem ancora ou comparacao | | Sem referencia, o preco e abstrato |

### Typography Flags

| Flag | Quando e OK | Quando e SLOP |
|---|---|---|
| Line-height < 1.4 em body text | Headlines com line-height apertado (1.0-1.15) | Paragrafos de 3+ linhas com line-height 1.2 |
| Texto com mais de 75 caracteres por linha | Design deliberado com tipografia grande | Body text em container full-width sem max-width |
| Uppercase em mais de 2 elementos por secao | luxury-minimal com labels tracking largo | Tudo em CAPS porque "parece bold" |

### Color Flags

| Flag | Quando e OK | Quando e SLOP |
|---|---|---|
| Dark mode quando audiencia prefere light | Produto tech/dev/IA | Pagina de curso pra empresario nao-tech |
| Accent color cobrindo > 10% da area visual | CTA section intencional | Accent como bg de secoes inteiras |
| Gradiente em mais de 1 elemento por viewport | ai-native com mesh bg (e so bg) | Gradient button + gradient text + gradient bg simultaneos |

---

## Tier 3 — AI Default Traps (Be Aware)

Items abaixo sao tendencias de design que IA adora gerar. Nao sao errados intrinsecamente, mas o uso excessivo/nao-intencional e sinal de design sem direcao.

### Glassmorphism / Frosted Glass

**O trap:** IA ama `backdrop-filter: blur(10px)` com bg semi-transparente. E bonito. E tambem o efeito mais overused de 2023-2026.

**Quando usar:** Cards elevados em `tech-elite` e `ai-native` onde profundidade e intencional.
**Quando e trap:** Em todo card, em todo modal, em todo tooltip. Se tudo e vidro, nada se destaca.

**Regra:** Max 2 elementos com glassmorphism por viewport. E so se o bg atras justifica (tem textura, mesh, imagem).

### Gratuitous Parallax

**O trap:** Parallax em tudo — hero, features, pricing, footer. "Movement creates engagement."

**Quando usar:** `cinematic` archetype, com proposito narrativo (produto revelando features enquanto scrolla).
**Quando e trap:** Parallax em secao de FAQ. Parallax em testimonials. Parallax porque "ficou legal."

**Regra:** Parallax so quando a profundidade serve a narrativa. Se tirar o parallax e nada muda na compreensao, era decorativo.

### Dark Mode as Default

**O trap:** IA tende a gerar dark mode porque screenshots e elementos coloridos "pop" mais.

**Quando usar:** Audiencia tech, produtos de IA, showcases de produto com UI.
**Quando e trap:** Landing page de curso pra empresario que nunca configurou dark mode no celular.

**Regra:** Consultar tabela Dark/Light na DOCTRINE secao D. Audiencia > preferencia pessoal do agente.

### Minimalism that Sacrifices Conversion

**O trap:** Design tao clean que esquece de vender. Sem social proof, sem urgencia, sem CTA claro. "Less is more" levado ao extremo.

**Quando usar:** `luxury-minimal` onde a exclusividade e a proposta.
**Quando e trap:** Qualquer contexto onde o usuario precisa tomar uma acao e nao tem sinalizacao visual pra onde ir.

**Regra:** Todo viewport visivel deve ter ao menos 1 CTA visual ou direcional. Mesmo no luxury-minimal.

### Beautiful but Non-Functional Animations

**O trap:** Animacoes complexas que levam 2s+ pra completar, bloqueando interacao. "Wow effect" que irrita no segundo acesso.

**Quando usar:** Hero sections em `cinematic` (primeira impressao).
**Quando e trap:** Animacao de entrada em CADA secao que bloqueia leitura. Scroll hijacking que previne scroll natural.

**Regra:** Nenhuma animacao deve bloquear interacao. Scroll hijacking e proibido (exceto pin sections em cinematic com escape hatch).

### Over-Designed Empty States

**O trap:** Ilustracoes elaboradas, animacoes e copy espirituosa em telas de estado vazio, antes de ter sequer o fluxo principal funcionando.

**Quando e trap:** Sempre em sales pages — sales pages nao tem empty states.

### Bento Grid Everything

**O trap:** Bento grid layout (Apple WWDC-style) para TODA section. Features, pricing, testimonials — tudo vira bento.

**Quando usar:** Feature showcase em `tech-elite` com 4-6 features de tamanhos diferentes.
**Quando e trap:** Quando cada "tile" do bento tem o mesmo tamanho. Quando bento e usado pra pricing. Quando bento e usado pra texto corrido.

**Regra:** Bento so quando tiles tem hierarquia de tamanho (1 grande + 2-4 menores). Se tudo e igual, use grid normal.

---

## Self-Check Automation

Antes de entregar qualquer design, o agente deve rodar esta checklist mental:

```
TIER 1 CHECK (zero tolerance):
[ ] Nenhum gradiente colorido generico
[ ] Display font nao e Inter/Roboto
[ ] Max 3 familias de fonte
[ ] Nao e tudo centralizado
[ ] Nao e o cookie-cutter hero (texto+mockup+gradiente)
[ ] Sem stock photos
[ ] Sem icones genericos como hero elements
[ ] border-radius nao passa de 16px em cards
[ ] Cores nao sao #FFFFFF puro + #000000 puro
[ ] Max 2 cores de acento

TIER 2 CHECK (justify if present):
[ ] Animacoes < 2s (exceto cinematic)
[ ] CTA visivel em todo viewport
[ ] Social proof acima do fold (exceto luxury-minimal)
[ ] Line-height >= 1.4 em body text
[ ] Max 75 chars por linha em body
[ ] Dark/light mode justificado pela audiencia

TIER 3 CHECK (awareness):
[ ] Glassmorphism nao excessivo (max 2 per viewport)
[ ] Parallax tem proposito narrativo
[ ] Animacoes nao bloqueiam interacao
[ ] Bento grid com hierarquia de tamanho
[ ] Minimalismo nao sacrifica conversao
```

---

## Tag System (para REJECTED-DESIGNS.md e APPROVED-DESIGNS.md)

### Rejection Tags

| Tag | Significado |
|---|---|
| `ai-default` | Design generico, sem direcao |
| `poor-hierarchy` | Falta hierarquia visual |
| `wrong-archetype` | Archetype nao combina com contexto |
| `slop-gradient` | Gradiente generico |
| `slop-typography` | Tipografia sem personalidade |
| `slop-layout` | Layout cookie-cutter |
| `low-contrast` | Contraste insuficiente (WCAG fail) |
| `over-animated` | Animacao excessiva |
| `stock-photo` | Fotos genericas |
| `mobile-broken` | Nao funciona em mobile |
| `cta-invisible` | CTA nao e claro |
| `no-social-proof` | Falta prova social onde necessario |
| `conversion-sacrifice` | Bonito mas nao vende |
| `wrong-audience` | Design nao combina com audiencia |

### Approval Tags

| Tag | Significado |
|---|---|
| `strong-hierarchy` | Hierarquia visual excelente |
| `archetype-fit` | Archetype bem aplicado |
| `custom-touches` | Detalhes unicos que diferenciam |
| `converts-well` | Design otimizado para conversao |
| `mobile-excellent` | Responsividade impecavel |
| `animation-purposeful` | Animacoes com proposito |
| `typography-strong` | Tipografia diferenciada |
| `palette-cohesive` | Paleta coesa e intencional |
| `reference-clear` | Referencia visual clara e bem executada |
