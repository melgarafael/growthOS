---
name: instagram-carousel
description: Instagram carousel expertise — 6 carousel structures, slide-by-slide blueprints, IG algorithm optimization, engagement triggers, visual hierarchy rules, and platform-specific anti-patterns
---

# Instagram Carousel Skill

Specialized knowledge base for creating high-performing Instagram carousels. Covers structure selection, slide-by-slide content architecture, visual design rules, algorithm optimization, and engagement mechanics. This skill is consumed by the carousel-designer agent and integrates with the copywriting and platform-mastery skills.

## 🔒 MANDATORY — Read before generating any carousel

Before producing any carousel structure, read in this order:

1. `growthOS/voice/GOLDEN-DOC.md` — canonical voice for @melgarafael / AutomatikLabs
2. `growthOS/voice/LINHA-EDITORIAL.md` — pillars, angulações
3. `growthOS/voice/virais/INDEX.md` — master viral index
4. `growthOS/voice/virais/PATTERNS/{category}.md` for the editorial category of the request (viralizacao / lead-capture / saves-retencao / venda)
5. `growthOS/design-system/DESIGN-SYSTEM.md` — visual DS (default lime-geist variant)
6. `brand-voice.yaml` sections: `voice`, `anti_slop`, `viral_intelligence`, `design_system`

**Viral intelligence rules:**
- Apply patterns tagged `voice_fit: aligns` and `replicable: yes` directly
- NEVER copy patterns tagged `voice_fit: conflicts`
- Patterns with `seen_count >= 3` and aligned voice have priority
- Each carousel cites the inspiring viral in a comment for traceability

---

## Trigger Conditions

Use this skill when the user asks to:
- Create an Instagram carousel or carrossel
- Design slide content for Instagram posts
- Optimize carousel posts for engagement
- Build educational, storytelling, or listicle carousels
- Create before/after transformation posts
- Design tutorial or step-by-step carousel content
- Create quote-series carousels
- Adapt content into carousel format for Instagram
- Improve an existing carousel's structure or copy
- Select the right carousel type for a given topic

---

## Brand Voice Integration

**MANDATORY:** Before generating ANY carousel content, load the brand voice configuration.

```python
from growthOS_shared.config import load_brand_voice
brand = load_brand_voice()
```

Every slide must:
1. Match `brand.tone` descriptors in headline and body text
2. Avoid all terms in `brand.avoid` and `anti_slop.banned_phrases`
3. Follow `anti_slop.style_rules` — carousels are especially vulnerable to slop because each slide has limited space and every word must earn its place
4. Respect `brand.visual_identity` for colors, fonts, and logo placement
5. Use the brand's language register (formal vs casual, technical vs accessible)

### Anti-Slop in Slide Text

Carousel slides have 50 words maximum per slide. With so few words, a single slop phrase wastes 10-20% of available space. Apply these additional carousel-specific anti-slop rules:

| Slop Pattern | Problem | Replacement |
|--------------|---------|-------------|
| "Voce sabia que..." on every slide | Repetitive filler | Use only once, on slide 2 max |
| "Nesse post voce vai aprender" | Wastes cover real estate | Jump straight to the hook |
| "Vamos la?" | Empty filler | Cut entirely or replace with a specific promise |
| "Confira as dicas" | Generic, zero information | Name the specific benefit |
| "Fique ate o final" | Begging, not compelling | Create curiosity that pulls naturally |
| "Dica de ouro" | Overused cliche | State the tip directly |
| Excessive emoji chains | Visual noise, not hierarchy | 1 emoji per concept max |

---

## 6 Carousel Structures

Each structure below includes a complete slide-by-slide blueprint. The number of slides is flexible (3-10), but the structural logic must be preserved.

### 1. Educativo (Educational)

**Best for:** Teaching a concept, sharing expertise, establishing authority.
**Typical slides:** 7-10
**Algorithm strength:** High save rate (people save to reference later).

#### Slide-by-Slide Blueprint

| Slide | Type | Content | Design Rules |
|-------|------|---------|-------------|
| 1 | Cover | Hook question or bold claim. 3-7 words max. Must create a knowledge gap. | Largest text on any slide. Single focal point. No subtitle. |
| 2 | Context | Frame the problem or topic. "Voce ja percebeu que..." or a surprising statistic. | Slightly smaller headline. 1-2 sentences body. Optional icon. |
| 3-8 | Points | One concept per slide. Icon + headline (5-8 words) + 2-3 bullet points (8-12 words each). | Consistent layout across all point slides. Visual hierarchy: icon > headline > bullets. Progress indicator visible. |
| 9 | Summary | (Optional) Quick recap of all points — numbered list, one line each. | Condensed layout. All points visible at once. |
| 10 | CTA | "Salva esse post" + "Segue @handle pra mais conteudo". | Two clear actions. Brand handle prominent. Optional: "Manda pra alguem que precisa". |

#### Educativo Example Structure (7 slides)

```
Slide 1: "5 erros que matam seu engajamento"
Slide 2: "87% dos perfis cometem pelo menos 3 desses erros"
Slide 3: Erro 1 — Postar sem horario estrategico
Slide 4: Erro 2 — Ignorar os saves como metrica
Slide 5: Erro 3 — CTA generico ou ausente
Slide 6: Erro 4 — Slides sem hierarquia visual
Slide 7: CTA — "Salva pra revisar antes de postar | Segue @handle"
```

---

### 2. Storytelling (Narrative)

**Best for:** Personal stories, case studies, brand origin stories, lessons learned.
**Typical slides:** 6-8
**Algorithm strength:** High time-spent (people read through the entire story), high share rate.

#### Slide-by-Slide Blueprint

| Slide | Type | Content | Design Rules |
|-------|------|---------|-------------|
| 1 | Cover | Intriguing statement that creates curiosity. Not a question — a statement that demands explanation. "Eu perdi R$40k em 3 meses." | Bold, large text. Dark or dramatic background. No context — just the hook. |
| 2 | Setup | Set the scene. Who, when, where. Establish the status quo before the conflict. | Narrative text, 2-3 short sentences. Conversational tone. |
| 3 | Conflict | The problem, the mistake, the challenge. Escalate tension. Make the reader feel the weight. | Can use slightly more text. Emotional language. Visual contrast (darker tones or red accents). |
| 4 | Turning Point | The moment of change. What happened? What did you realize? What decision did you make? | Shorter text — one powerful sentence or two. Transitional visual. |
| 5 | Resolution | The outcome. What changed? Show the transformation. Use specifics (numbers, timelines, results). | Lighter/brighter visual tone. Concrete data. Before/after contrast if applicable. |
| 6 | Lesson | The takeaway. One clear, actionable lesson the reader can apply to their own life. | Framed differently — quote style, highlighted box, or different typography. |
| 7 | CTA | "Manda pra alguem que precisa ouvir isso" + "Comenta se voce ja passou por algo parecido". | Engagement-focused CTA. Invite the reader into the story. |

#### Storytelling Narrative Arc

```
Cover: CURIOSITY (stop the scroll)
  ↓
Setup: CONTEXT (ground the reader)
  ↓
Conflict: TENSION (make them care)
  ↓
Turning Point: PIVOT (the aha moment)
  ↓
Resolution: PAYOFF (deliver the goods)
  ↓
Lesson: TAKEAWAY (make it actionable)
  ↓
CTA: CONNECTION (bring them closer)
```

---

### 3. Listicle (List)

**Best for:** Tips, tools, resources, habits, mistakes, examples.
**Typical slides:** 7-10
**Algorithm strength:** High save rate, predictable swipe pattern keeps time-spent high.

#### Slide-by-Slide Blueprint

| Slide | Type | Content | Design Rules |
|-------|------|---------|-------------|
| 1 | Cover | Number + hook. "7 ferramentas gratuitas que uso todo dia." The number is the anchor. | Large number (oversized, accent color). Hook text below. |
| 2-8 | Items | One item per slide. Number prominent + title (3-6 words) + description (1-2 sentences, 15-25 words). | Consistent layout: number in accent color, title bold, description regular weight. Each slide self-contained. |
| 9 | Bonus | (Optional) "Bonus: [extra item]" — rewards the reader for swiping to the end. | Same layout as items but visually distinguished (different accent or "BONUS" badge). |
| 10 | CTA | "Salva pra consultar depois" + "Qual desses voce ja usa? Comenta ai". | Save-focused CTA (listicles are reference material). |

#### Listicle Numbering Rules

- Always use the number on every slide — it creates momentum ("3/7" makes people want to reach 7/7)
- The cover number must match the total items (if you say "7 ferramentas", deliver exactly 7)
- Order matters: strongest or most surprising items at positions 1, 2, and last
- The middle items (positions 3-5) should maintain quality — no filler

---

### 4. Antes-Depois (Before/After)

**Best for:** Transformations, results, comparisons, upgrades, redesigns.
**Typical slides:** 6-8
**Algorithm strength:** High share rate (visual contrast is inherently shareable), high save rate.

#### Slide-by-Slide Blueprint

| Slide | Type | Content | Design Rules |
|-------|------|---------|-------------|
| 1 | Cover | Transformation hook. "De [before state] pra [after state] em [timeframe]." | Split visual or arrow motif. Before/after implied but not shown yet. |
| 2 | Before Context | Set the "before" scene. What was the situation? Pain points, metrics, or visual state. | Muted colors, gray tones, or desaturated palette. "ANTES" label visible. |
| 3-4 | Before Details | Specific problems, screenshots, metrics, or descriptions of the "before" state. One problem per slide. | Same muted palette. Use icons or small visuals to illustrate each problem. |
| 5 | Transition | "O que mudou" or "O que fizemos" — brief description of the action taken. | Visual bridge: half muted, half vibrant. Arrow or divider element. |
| 6-7 | After Details | Specific improvements, new metrics, visual results. One improvement per slide. | Vibrant colors, brand palette at full saturation. "DEPOIS" label visible. |
| 8 | CTA | "Quer o mesmo resultado? Link na bio" or "Salva pra quando precisar". | Result-focused CTA. Can include a mini before/after summary. |

#### Before/After Contrast Rules

- The visual difference between "before" and "after" slides must be immediately obvious
- Use color temperature: cool/gray for before, warm/vibrant for after
- Include at least one concrete metric in the after section (percentage, time, money)
- Never fake results — anti-slop applies to transformation claims too

---

### 5. Tutorial (Step-by-Step)

**Best for:** How-to content, processes, recipes, workflows, setup guides.
**Typical slides:** 7-10
**Algorithm strength:** Highest save rate of all types (people save tutorials for later execution).

#### Slide-by-Slide Blueprint

| Slide | Type | Content | Design Rules |
|-------|------|---------|-------------|
| 1 | Cover | "Como [achieve result]" or "Passo a passo: [outcome]." Tell them exactly what they will learn. | Clear outcome promise. "Tutorial" or "Passo a passo" badge optional. |
| 2 | Overview | (Optional) What they need before starting — tools, prerequisites, context. | Checklist format. Keep short — 3-5 items max. |
| 3-8 | Steps | One step per slide. "Passo [N]:" + instruction headline + 1-2 sentences of detail. Include a visual example, screenshot, or illustration. | Numbered prominently. Instruction text clear and actionable. Use imperative verbs: "Abra", "Clique", "Escreva", "Configure". |
| 9 | Result | Show the expected outcome. "Pronto! Agora voce tem [result]." | Celebratory visual. Show the finished product or result. |
| 10 | CTA | "Salva esse tutorial pra fazer depois" + "Marca alguem que precisa aprender isso". | Save-heavy CTA. Tutorials are the #1 saved format on Instagram. |

#### Tutorial Writing Rules

- Every step must be independently actionable — someone following along should be able to execute it
- Use imperative verbs at the start of each step ("Abra o app", "Selecione a opcao", "Digite o valor")
- Include one visual reference per step when possible (screenshot, diagram, icon)
- Number every step — sequential numbering creates a sense of progress
- If a step is complex, split it into two slides rather than cramming

---

### 6. Quote-Series (Curated Quotes)

**Best for:** Motivation, thought leadership, curated wisdom, niche quotes.
**Typical slides:** 6-8
**Algorithm strength:** High share rate (people share quotes via DM), moderate save rate.

#### Slide-by-Slide Blueprint

| Slide | Type | Content | Design Rules |
|-------|------|---------|-------------|
| 1 | Cover | Theme statement. "5 frases que mudaram minha forma de pensar sobre [topic]." | Clean design. Theme text prominent. No quote on the cover. |
| 2-7 | Quotes | One quote per slide. Quote text (15-30 words) + attribution (name, optional title or context). | Quote in large, elegant typography. Attribution smaller, below or beside. Consistent layout. Optional: decorative quotation marks. |
| 8 | CTA | "Qual frase mais te impactou? Comenta o numero" + "Manda pra alguem que precisa ler isso". | Engagement CTA — asking them to pick a favorite drives comments. |

#### Quote Selection Rules

- Curate for coherence — all quotes should orbit the same theme
- Mix well-known and lesser-known sources for freshness
- Avoid over-quoted cliches ("Be the change you wish to see" is not stopping anyone's scroll)
- Add context when needed: "Sobre disciplina:" or "Sobre comecar:" before the quote
- Attribution is mandatory — unattributed quotes lose credibility

---

## Instagram Rules & Constraints

### Hard Limits

| Parameter | Value | Notes |
|-----------|-------|-------|
| Max slides per carousel | 10 | Instagram enforces this. Plan for 7-10. |
| Min slides per carousel | 3 | Fewer than 3 defeats the carousel purpose. |
| Optimal aspect ratio | 4:5 (1080x1350px) | Takes maximum vertical feed space. More visibility = more engagement. |
| Alternative ratios | 1:1 (1080x1080), 9:16 (1080x1920 for Stories) | Square for clean aesthetic, 9:16 for Story-adapted carousels. |
| Max file size per image | 30MB | Stay well under this. |
| Supported formats | JPEG, PNG | PNG for text-heavy slides (sharper). JPEG for photo-heavy. |

### Typography Constraints

| Element | Minimum Size | Recommended Size | Notes |
|---------|-------------|-----------------|-------|
| Body text | 28px | 32-36px | Must be legible on a phone screen held at arm's length. |
| Headlines | 48px | 56-72px | Larger = more scroll-stopping power. |
| Cover hook | 56px | 64-96px | The cover text should dominate the slide. |
| Caption/attribution | 20px | 24-28px | For sources, fine print, or secondary info. |
| Progress indicator | 14px | 16-18px | Small but visible. |

### Content Density Rules

| Metric | Limit | Rationale |
|--------|-------|-----------|
| Words per slide (content) | Max 50 | More than 50 words = wall of text, people skip. |
| Words per slide (cover) | Max 7 | Cover must be scannable in under 1 second. |
| Bullet points per slide | Max 4 | 3 is ideal. More than 4 loses readability. |
| Words per bullet | Max 12 | Bullets are scannable fragments, not sentences. |
| Ideas per slide | 1 | One concept. One takeaway. Period. |

---

## Cover Slide Mastery

The cover slide is the single most important element of your carousel. It determines whether someone swipes or scrolls past. Invest 50% of your creative energy here.

### Cover Slide Principles

1. **One message, large text.** The cover should communicate a single idea that creates a knowledge gap or emotional reaction.
2. **3-7 words maximum.** If your cover needs more than 7 words, you haven't distilled the hook enough.
3. **Curiosity over information.** The cover's job is NOT to inform — it is to make them swipe. The information comes on slides 2+.
4. **No metadata on the cover.** Never waste cover space on "Slide 1 de 7", "Deslize para o lado", or "Novo post". The user knows how carousels work.
5. **Visual dominance.** Text should occupy 60-80% of the visual weight of the cover. Background should support, not compete.

### Hook Patterns That Work

| Pattern | Template | Example |
|---------|----------|---------|
| Error/Mistake | "X erros que [negative consequence]" | "5 erros que matam seu engajamento" |
| How-To + Result | "Como [result] em [timeframe]" | "Como dobrar seus saves em 30 dias" |
| Stop Doing | "Pare de [common mistake]" | "Pare de postar sem estrategia" |
| Number + Bold Claim | "[Number] [things] que [unexpected outcome]" | "3 habitos que separam amadores de profissionais" |
| Question | "[Provocative question]?" | "Voce esta jogando conteudo fora?" |
| Contrarian | "[Common belief] esta errado" | "Postar todo dia nao funciona" |
| Confession | "Eu [vulnerable admission]" | "Eu perdi 10k seguidores em 1 mes" |
| Challenge | "Voce consegue [difficult thing]?" | "Voce consegue criar conteudo sem essas 5 muletas?" |

### Cover Slide Anti-Patterns

- "Deslize para o lado" — patronizing, wastes space
- "Novo post!" — zero information, zero curiosity
- "Slide 1 de 7" — metadata, not content
- "Voce precisa ver isso" — vague clickbait
- Using a stock photo as the cover with small overlaid text — text must dominate
- Putting the CTA on the cover — kills curiosity, inverts the funnel
- Using more than 2 fonts on the cover — visual noise

---

## CTA Patterns (Last Slide)

The CTA slide converts passive viewers into engaged followers. Every carousel must end with a clear call to action.

### Primary CTA Templates

| CTA Type | Template | Algorithm Signal |
|----------|----------|-----------------|
| Save | "Salva esse post pra consultar depois" | Saves (strongest IG signal) |
| Share | "Manda pra alguem que precisa ouvir isso" | Shares (second strongest signal) |
| Follow | "Segue @handle pra mais conteudo como esse" | Follower growth |
| Comment | "Comenta [emoji] se voce ja passou por isso" | Comments (engagement depth) |
| Link | "Link na bio pra [specific resource]" | Off-platform conversion |

### Double CTA Strategy

Always combine two CTAs for maximum algorithm impact:

```
Primary: Save + Follow
"Salva esse post pra revisar depois e segue @handle pra mais conteudo como esse"

Primary: Share + Comment
"Manda pra um amigo que precisa e comenta qual dica voce vai aplicar primeiro"

Primary: Save + Comment
"Salva pra consultar e me conta: qual ponto mais te surpreendeu?"
```

### CTA Slide Design Rules

- CTA text should be visually distinct from content slides (different layout, centered, or boxed)
- Include the brand handle (@handle) prominently
- Keep the CTA under 25 words total
- Use imperative verbs: "Salva", "Manda", "Segue", "Comenta"
- Optional: include a small visual summary or key takeaway alongside the CTA

---

## Anti-Patterns (What NOT To Do)

### Content Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| More than 50 words per slide | Wall of text, people skip | Ruthlessly edit. One idea per slide. |
| Font smaller than 28px | Illegible on mobile | Increase font size, reduce text amount. |
| No visual hierarchy | Everything looks the same, nothing stands out | Use 3 levels: headline (large, bold), body (medium, regular), caption (small, light). |
| Inconsistent design between slides | Looks unprofessional, breaks immersion | Use a template. Same fonts, colors, layout grid across all slides. |
| No progress indicator | Reader has no sense of position or completion | Add dots, slide numbers, or a progress bar. |
| CTA on the first slide | Kills curiosity, puts the ask before the value | CTA belongs on the LAST slide only. |
| Generic stock photo backgrounds | Looks like every other carousel | Use solid colors, gradients, or brand-specific imagery. |

### Design Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| More than 3 fonts | Visual chaos | 1 headline font + 1 body font. Max 2. |
| Text touching slide edges | Looks cramped, gets clipped on some devices | Maintain 60-80px safe margin on all sides. |
| Low contrast text | Fails accessibility, hard to read outdoors | Minimum 4.5:1 contrast ratio for body text, 3:1 for large text. |
| Decorative elements competing with text | Distracts from the message | Background elements at 10-20% opacity max. Text always wins. |
| Different text alignment per slide | Inconsistent, disorienting | Pick one alignment (left or center) and stick with it. |
| Busy gradients behind text | Reduces readability | Gradient as accent only, never behind body text. Use solid overlay if needed. |

### Strategic Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Carousel with only 2-3 slides | Too short for algorithm engagement | Minimum 5 slides for meaningful swipe-through. |
| All text, no visual variety | Monotonous swipe experience | Vary slide types: text, icon+text, quote, visual example. |
| No carousel type / mixed structure | Confusing narrative, reader drops off | Pick one structure and follow it consistently. |
| Repurposing a blog post word-for-word | Too dense, not designed for slide format | Rewrite for slides: one idea per slide, visual hierarchy, scannable text. |
| Same CTA on every post | Audience fatigue | Rotate CTAs: save, share, comment, follow. |

---

## Palette by Niche

Color palette selection significantly impacts carousel performance. The right palette signals the content niche before a single word is read.

### Tech / SaaS

```yaml
palette:
  background: "#0a0a0a" or "#1a1a2e"
  text_primary: "#ffffff"
  text_secondary: "#a0a0b0"
  accent_primary: "#6c5ce7"  # purple
  accent_secondary: "#00cec9"  # teal
  style: dark-premium or gradient
  mood: "innovative, technical, premium"
```

### Health / Wellness

```yaml
palette:
  background: "#ffffff" or "#f5f5f0"
  text_primary: "#2d3436"
  text_secondary: "#636e72"
  accent_primary: "#00b894"  # green
  accent_secondary: "#dfe6e9"  # light gray
  style: clean-educator or minimal
  mood: "natural, trustworthy, calming"
```

### Finance / Business

```yaml
palette:
  background: "#0a1628" or "#ffffff"
  text_primary: "#ffffff" or "#1a1a2e"
  text_secondary: "#8395a7"
  accent_primary: "#d4a574"  # gold
  accent_secondary: "#2c3e50"  # navy
  style: dark-premium or minimal
  mood: "authoritative, premium, trustworthy"
```

### Creative / Design

```yaml
palette:
  background: "#ff6b6b" or "#a29bfe" or "#fdcb6e"  # vibrant solid color
  text_primary: "#ffffff" or "#2d3436"
  text_secondary: varies by background
  accent_primary: contrasting vibrant
  accent_secondary: complementary vibrant
  style: vibrant-creator or bold
  mood: "energetic, bold, expressive"
```

### Education

```yaml
palette:
  background: "#f8f9fa" or "#edf2f7"
  text_primary: "#2d3436"
  text_secondary: "#636e72"
  accent_primary: "#0984e3"  # blue
  accent_secondary: "#74b9ff"  # light blue
  style: clean-educator
  mood: "accessible, clear, professional"
```

### Personal Brand

```yaml
palette:
  background: "from brand-voice.yaml → visual_identity.colors.background"
  text_primary: "from brand-voice.yaml → visual_identity.colors.text"
  text_secondary: derived from text_primary at 60% opacity
  accent_primary: "from brand-voice.yaml → visual_identity.colors.primary"
  accent_secondary: "from brand-voice.yaml → visual_identity.colors.secondary"
  style: auto-selected from brand tone
  mood: "consistent with brand personality"
```

### Palette Application Rules

1. **Cover slide:** Accent color dominant (background or large text). Maximum visual impact.
2. **Content slides:** Neutral background, accent for headlines and icons only. Readability first.
3. **CTA slide:** Accent color returns prominently. Bookend visual consistency with cover.
4. **Never use more than 4 colors** in a single carousel (background, text, primary accent, secondary accent).
5. **Test in dark mode:** Many users browse Instagram in dark mode. Ensure colors work on both light and dark device screens.

---

## Narrative Progression Framework

Every carousel, regardless of type, follows a fundamental narrative arc. This framework ensures the swipe experience feels satisfying rather than random.

### The 5-Stage Progression

```
HOOK → PROBLEM → SOLUTION(S) → PROOF/EXAMPLE → CTA
```

| Stage | Slides | Purpose | Engagement Goal |
|-------|--------|---------|----------------|
| Hook | Slide 1 | Stop the scroll. Create a gap. | Impression → Swipe |
| Problem | Slide 2 | Frame why this matters. Make it personal. | Swipe → Investment |
| Solution(s) | Slides 3-7 | Deliver the value. One point per slide. | Investment → Time Spent |
| Proof/Example | Slide 8-9 | Validate with data, screenshots, or story. | Time Spent → Trust |
| CTA | Slide 10 | Convert attention into action. | Trust → Save/Share/Follow |

### Progression Rules

1. **Never front-load all value on slide 2.** Distribute insights across slides to maximize swipe-through.
2. **Create micro-hooks between slides.** End each slide with an implicit "and here's another one..." to pull them forward.
3. **The middle slides must maintain quality.** Slides 4-6 are where drop-off happens. Keep these strong.
4. **Slide 2 is the commitment point.** If they swipe past slide 1 and read slide 2, they are likely to complete the carousel. Slide 2 must reward the initial swipe.
5. **The last content slide before the CTA should be the strongest point.** It is the freshest in memory when they reach the CTA.

---

## Engagement Triggers

Specific techniques to increase saves, shares, comments, and swipe-through rate.

### Question Triggers (Drive Comments)

Place on slide 2 or the CTA slide to maximize comment engagement:

| Trigger | Example | Where |
|---------|---------|-------|
| Relatable question | "Voce ja cometeu esse erro?" | Slide 2 |
| This-or-that | "Voce prefere [A] ou [B]?" | CTA slide |
| Self-identification | "Comenta 1 se [option A], 2 se [option B]" | CTA slide |
| Confession prompt | "Conta aqui: qual desses voce ainda faz?" | CTA slide |
| Opinion poll | "Concorda ou discorda? Comenta ai" | CTA slide |

### Data Triggers (Build Credibility)

Concrete numbers stop the scroll and build trust:

| Trigger | Example | Where |
|---------|---------|-------|
| Surprising statistic | "87% dos marketers nao medem saves" | Slide 2 or 3 |
| Specific result | "Cresci 4.200 seguidores em 60 dias" | Cover or slide 2 |
| Time-bound claim | "Em 30 dias, sem anuncios" | Cover modifier |
| Comparison metric | "2x mais engajamento que posts estaticos" | Supporting slide |

### Contrast Triggers (Create Visual/Conceptual Tension)

| Trigger | Example | Where |
|---------|---------|-------|
| Before/after | Visual comparison of transformation | Slides 2-3 vs 6-7 |
| Right/wrong | "O que a maioria faz vs o que funciona" | Point slides |
| Myth/reality | "Mito: postar mais = crescer mais. Realidade: ..." | Slide 2-3 |
| Expectation/result | "O que eu esperava vs o que aconteceu" | Storytelling slides |

### Curiosity Triggers (Increase Swipe-Through)

| Trigger | Example | Where |
|---------|---------|-------|
| Open loop | "E o terceiro erro e o mais perigoso..." | End of a slide, resolved on next |
| Numbered list promise | "7 ferramentas (a #5 mudou meu jogo)" | Cover — promises value ahead |
| "Voce sabia que..." | Unexpected fact that reframes the topic | Slide 2 |
| Controversy/contrarian | "[Common belief] esta errado. Veja por que:" | Cover or slide 2 |
| Incomplete revelation | "O segredo esta em..." (continued on next slide) | Any content slide |

### Emoji as Visual Anchors

Emoji serve as rapid visual cues, not decoration. Rules:

- 1 emoji per headline or key point maximum
- Use consistently: same emoji for same concept type across slides
- Functional emoji: checkmarks for tips, X for errors, arrows for steps, numbers for lists
- Never: emoji chains, random emoji, emoji replacing words entirely
- Recommended set: check, x, arrow_right, brain, bulb, fire, chart, star, warning, point_right

---

## Platform-Specific Optimization

### Best Posting Times for Carousels

Carousels need more time-on-content than static posts. Post when your audience has time to swipe, not just scroll.

| Day | Best Times (BRT) | Notes |
|-----|------------------|-------|
| Monday | 11:00-13:00 | People settling into the week, consuming content at lunch |
| Tuesday-Thursday | 11:00-13:00, 19:00-21:00 | Lunch break + evening wind-down are peak carousel times |
| Friday | 10:00-12:00 | Morning focus, engagement drops after lunch as weekend starts |
| Saturday | 10:00-12:00 | Casual morning browsing |
| Sunday | 17:00-20:00 | Sunday evening prep-for-the-week consumption |

**Important:** These are baselines. Always check your own Instagram Insights for your specific audience's active hours.

### Caption Strategy

The caption complements the carousel — it does not repeat it.

#### Caption Structure

```
[Hook line — first 125 characters visible before "...mais"]

[1-2 paragraphs expanding on the carousel's topic. Add context,
a personal angle, or bonus information not in the slides.]

[CTA that mirrors the last slide's CTA]

.
.
.
[Hashtags — in a separate block, visually separated]
```

#### Caption Rules

1. **First line is the hook.** It appears below the carousel in the feed. Must complement the cover slide, not repeat it.
2. **Add value beyond the slides.** The caption should give a reason to read even after swiping through all slides.
3. **Include a CTA in the caption.** Reinforce the slide CTA: "Salva esse post" or "Marca alguem".
4. **Keep it scannable.** Line breaks between paragraphs. No walls of text.
5. **Caption length:** 300-800 characters for carousels. Longer than static posts, shorter than Reels.

### Hashtag Strategy for Carousel Posts

| Category | Count | Examples |
|----------|-------|---------|
| Niche-specific | 3-5 | #marketingdigitalbr, #dicasdeinstagram, #conteudoeducativo |
| Topic-specific | 3-5 | #carouselpost, #dicasparaempreendedores, #socialmediatips |
| Branded | 1-2 | #suamarca, #suaserie |
| Total | 8-12 | Sweet spot. More than 15 looks spammy. |

#### Hashtag Placement

- **Option A:** At the end of the caption, separated by line breaks
- **Option B:** In the first comment (cleaner caption, same reach)
- **Never:** Inline with caption text ("Aprenda #marketing #digital hoje")

### Alt Text for Accessibility

Every carousel slide should have descriptive alt text. This also improves discoverability through Instagram search.

#### Alt Text Rules

- Describe the visual content AND the text content of each slide
- Format: "Slide [N] of [carousel title]: [description of visual] with text reading '[key text]'"
- Keep under 100 characters per slide
- Do not stuff keywords — write for screen reader users first
- Instagram allows alt text per image in the carousel

#### Alt Text Example

```
Slide 1: Cover slide with dark background and large white text reading "5 erros que matam seu engajamento"
Slide 2: Infographic showing 87% statistic with text "87% dos perfis cometem pelo menos 3 desses erros"
Slide 3: Educational slide with warning icon and text "Erro 1: Postar sem horario estrategico"
```

### Cross-Posting Adaptation

Carousel content can be repurposed, but each platform has different rules.

| Platform | Format | Key Differences |
|----------|--------|----------------|
| **LinkedIn** | PDF carousel (document post) | Professional tone, more text per slide acceptable (up to 80 words), no emoji anchors, add source citations |
| **Twitter/X** | Thread or image series (4 max per tweet) | Condense to key points, more provocative hooks, no progress indicators needed |
| **Pinterest** | Long-form infographic (2:3 or 1:2.1 ratio) | Combine all slides into one tall image, keyword-rich description, link to source |
| **TikTok** | Photo carousel or slideshow video | Add trending audio, text overlays instead of embedded text, vertical 9:16 format |
| **Blog** | Embedded or expanded into article | Expand each slide into a paragraph, add internal links, SEO-optimize |

#### Cross-Posting Anti-Patterns

- Posting the exact same images on LinkedIn (different audience, different tone)
- Posting Instagram carousels as Twitter images without condensing the message
- Forgetting to adjust aspect ratio for Pinterest (Instagram 4:5 crops wrong on Pinterest)
- Not removing Instagram-specific CTAs ("Salva esse post") when posting elsewhere

---

## Output Contract

### Carousel Output Schema

```yaml
output_contract:
  skill: instagram-carousel
  format: structured_slide_plan
  required_sections:
    - slide_plan:
        type: string  # carousel type (educativo|storytelling|listicle|antes-depois|tutorial|quote-series)
        total_slides: integer  # 3-10
        slides:
          - slide_number: integer
            type: string  # cover | content | context | transition | summary | cta
            headline: string  # max 10 words (7 for cover)
            body: string  # max 50 words per slide
            bullets: list  # max 4 items, max 12 words each
            icon: string  # emoji or icon name
            cta_text: string  # for CTA slides only
            cta_action: string  # save | share | follow | comment | link
    - design_spec:
        palette: string  # niche palette name or custom
        style: string  # minimal | bold | gradient | clean-educator | dark-premium | vibrant-creator
        dimensions: string  # "1080x1350" default
        fonts:
          headline: string
          body: string
    - quality_checks:
        cover_words: integer  # must be <= 7
        max_words_per_slide: integer  # must be <= 50
        total_slides: integer  # must be 3-10
        has_progress_indicator: boolean
        has_cta: boolean
        anti_slop_passed: boolean
        brand_voice_matched: boolean
        visual_hierarchy_consistent: boolean
  validation:
    anti_slop: true
    brand_voice: true
    platform_constraints: true
    accessibility_alt_text: true
```
