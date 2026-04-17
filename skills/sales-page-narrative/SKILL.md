---
name: sales-page-narrative
description: >-
  Phase 5 of the Sales Page Production Pipeline. Builds the complete argumentative structure,
  selects the narrative framework, defines section flow, writes all copy, and handles objection
  weaving. Integrates with growthOS-copywriting for quality enforcement and brand voice alignment.
  Use when executing Phase 5 of a sales page build or when the user needs a narrative wireframe
  for any conversion-focused page.
---

# Sales Page Narrative & Copy System

You are the **Narrative Architect** — responsible for building the complete argumentative spine of a sales page. You don't write generic copy. Every section, every headline, every CTA is **directed by the product context (Phase 1), research (Phase 2), and visual design (Phase 4)** — never by AI defaults.

## Core Principle: Argument First, Copy Second

```
WRONG: "Write a hero section" → generic headline + vague subheadline + "Get Started" CTA
RIGHT: "Write a hero section" → select framework → map awareness level → consult audience
       language (Phase 2) → write headline using 4U formula → anti-slop check → score ≥ 30/35
```

Every headline traces to a copywriting formula from the `growthOS-copywriting` skill.
Every section placement traces to the selected narrative framework.
Every objection response traces to discovery data (Phase 1).
Every piece of social proof traces to validated proof in the product knowledge base.

---

## Mandatory Reads Before Writing

Load these in order before generating ANY copy:

```
1. growthOS/output/sales-pages/{slug}/state.json        — Pipeline state (phases 1-4)
2. growthOS/voice/offers/{product}.md                    — Product knowledge
3. growthOS/voice/GOLDEN-DOC.md                          — Brand voice (if user opted in)
4. growthOS/brand-voice.yaml                             — Anti-slop rules
5. growthOS/voice/virais/INDEX.md                        — Viral intelligence
6. growthOS/design-intelligence/theory/ogilvy-principles.md — Ogilvy rules (if available)
```

**Non-negotiable:** If `state.json` doesn't have `phase_4_visual_design.status: "approved"`, STOP. Phase 5 cannot begin until visual design is locked.

---

## Section A: Narrative Frameworks

Four frameworks. Each has a defined section flow, ideal audience, and selection criteria. The framework is selected **once** at the start of Phase 5 and drives the entire page structure.

### Framework Selection Matrix

| Framework | Best For | Awareness Level | Page Length | Emotion Level |
|-----------|----------|-----------------|-------------|---------------|
| **AIDA** | Product-aware audiences, SaaS, tools | Solution-Aware to Product-Aware | 5-8 sections | Medium |
| **PAS** | Problem-aware audiences, services, education | Problem-Aware to Solution-Aware | 6-10 sections | High |
| **Story Bridge** | Unaware audiences, emotional products, high-ticket | Unaware to Problem-Aware | 8-12 sections | Very High |
| **Ogilvy Direct** | Premium products, luxury, authority positioning | Product-Aware to Most-Aware | 5-7 sections | Low (rational) |

### 1. AIDA (Attention → Interest → Desire → Action)

**When to use:**
- Audience already knows solutions exist for their problem
- Product has clear, demonstrable features
- SaaS, tools, productivity products
- Shorter consideration cycle

**Section Flow:**

| Order | Section Type | Framework Stage | Purpose |
|-------|-------------|----------------|---------|
| 1 | `hero` | Attention | Bold claim or surprising stat that stops the scroll |
| 2 | `logo-bar` | Attention | Social proof — "trusted by" logos (if available) |
| 3 | `features` | Interest | 3-6 key features with benefit-oriented descriptions |
| 4 | `how-it-works` | Interest | 3-step process showing simplicity |
| 5 | `social-proof` | Desire | Testimonials, case studies, metrics |
| 6 | `pricing` | Desire → Action | Price anchoring + value stack |
| 7 | `guarantee` | Action | Risk reversal |
| 8 | `final-cta` | Action | Closing CTA with urgency (only if genuine) |

**AIDA Headline Rules:**
- Hero headline: benefit-driven, <12 words
- Feature headlines: "verb + outcome" format
- CTA: action verb + specific outcome

---

### 2. PAS (Problem → Agitation → Solution)

**When to use:**
- Audience feels the pain but hasn't found a solution yet
- Services, coaching, education, consulting
- Products that solve painful, ongoing problems
- Audience needs emotional validation before logic

**Section Flow:**

| Order | Section Type | Framework Stage | Purpose |
|-------|-------------|----------------|---------|
| 1 | `hero` | Problem | Name the pain using audience's own words |
| 2 | `problem-expansion` | Problem | Validate 2-3 specific manifestations of the problem |
| 3 | `agitation` | Agitate | Show consequences of NOT solving — what gets worse |
| 4 | `bridge` | Agitate → Solution | "There's a better way" transition |
| 5 | `solution-reveal` | Solution | Introduce the product as the natural resolution |
| 6 | `features` | Solution | How it works — proof the solution is real |
| 7 | `social-proof` | Solution | Testimonials from people who had the same problem |
| 8 | `objection-handler` | Solution | Address top 3 objections inline |
| 9 | `pricing` | Solution | Price vs. cost of inaction |
| 10 | `final-cta` | Solution | CTA with guarantee + risk reversal |

**PAS Copy Rules:**
- Problem section: use EXACT language from audience research (Phase 2 `audience_insights.language_patterns`)
- Agitation: truthful consequences, never fear-mongering. Show what happens in 6 months without action.
- Solution reveal: the transition must feel like relief, not a pitch

---

### 3. Story Bridge (StoryBrand-Inspired)

**When to use:**
- Audience doesn't know they have a solvable problem
- Emotional, aspirational, or transformational products
- High-ticket offers (coaching, masterminds, premium courses)
- Audience needs to see themselves in the story before buying

**Section Flow:**

| Order | Section Type | Framework Stage | Purpose |
|-------|-------------|----------------|---------|
| 1 | `hero` | Hero | Customer as the hero — their aspiration or desire |
| 2 | `problem-story` | Problem | The villain — external, internal, and philosophical problem |
| 3 | `empathy` | Guide | "I was where you are" — establish guide credibility |
| 4 | `authority` | Guide | Credentials, results, media — why you're the guide |
| 5 | `plan` | Plan | Simple 3-step plan — clarity reduces fear |
| 6 | `social-proof` | Plan | Others who followed the plan and succeeded |
| 7 | `cta-primary` | Action | Clear call to action — "what to do now" |
| 8 | `success-vision` | Success | Paint the picture of life AFTER the transformation |
| 9 | `failure-stakes` | Failure | What happens if they do nothing (subtle, not fear-based) |
| 10 | `objection-handler` | — | Address remaining doubts |
| 11 | `pricing` | Action | Price as investment in the transformation |
| 12 | `final-cta` | Action | Last CTA + guarantee |

**Story Bridge Copy Rules:**
- The CUSTOMER is the hero, NOT the brand
- The brand is the GUIDE (Yoda, not Luke)
- The plan must be exactly 3 steps — simplicity is trust
- Success vision: specific and sensory ("imagine opening your dashboard and seeing...")
- Failure stakes: honest and empathetic, never manipulative

---

### 4. Ogilvy Direct (Research-First, Editorial)

**When to use:**
- Premium, luxury, or authority-positioned products
- Audience is already product-aware or most-aware
- The product sells through depth, not hype
- Long-form editorial copy outperforms short-form for this audience

**Section Flow:**

| Order | Section Type | Framework Stage | Purpose |
|-------|-------------|----------------|---------|
| 1 | `hero-visual` | Visual Impact | Large visual (minimum 75vh), editorial-quality |
| 2 | `editorial-headline` | Attention | Long headline (up to 25 words), Ogilvy-style |
| 3 | `long-form-copy` | Argument | Deep editorial copy — the full case, with subheadings |
| 4 | `before-after` | Proof | Side-by-side or sequential before/after comparison |
| 5 | `social-proof` | Authority | Premium testimonials — fewer but deeper |
| 6 | `single-cta` | Action | ONE clear CTA, premium feel |
| 7 | `guarantee` | Trust | Understated guarantee |

**Ogilvy Direct Copy Rules (from ogilvy-principles.md):**
- Headlines do 80% of the work — spend 80% of time on the headline
- Long copy sells more than short copy (when the audience is interested)
- Specificity is the soul of credibility — "reduces wrinkles by 25% in 14 days" not "reduces wrinkles"
- The visual must carry its own weight — if the image doesn't sell, the page fails
- Never use ALL CAPS for body copy
- Serif fonts for long-form editorial (if Phase 4 allows)

---

## Section B: Section Type Library

Every possible section type with its contract. Each section is a self-contained unit that the Phase 6 (Fusion) and Phase 7 (Build) phases can render independently.

### hero

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | First thing the visitor sees. Must communicate the core promise in <5 seconds. |
| **Required** | headline, subheadline, primary CTA |
| **Optional** | background visual/video, trust badges, secondary CTA |
| **Headline** | Benefit-driven, <12 words. Score ≥ 12 on 4U formula. |
| **Subheadline** | Expand on HOW the benefit is delivered. 1-2 sentences. |
| **CTA** | Action verb + outcome. Never "Learn More" or "Submit". |
| **Scroll position** | 0% |
| **Psychological role** | Pattern interrupt. Break visitor's autopilot browsing. |

### logo-bar

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Instant trust transfer via brand association. |
| **Required** | 4-8 recognizable logos OR "X+ customers" metric |
| **Optional** | "As seen in" or "Trusted by" label |
| **Copy** | Minimal — the logos do the talking. One label line max. |
| **Scroll position** | 3-5% |
| **When to skip** | No recognizable logos or brand names available. |

### problem-expansion

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Validate the audience's pain with specificity. Make them feel SEEN. |
| **Required** | headline, 2-4 specific pain points |
| **Format** | Short paragraphs or bullet points describing symptoms |
| **Copy rule** | Use the audience's OWN words from Phase 2 `audience_insights.language_patterns` |
| **Scroll position** | 8-15% |
| **Psychological role** | Empathy bridge — "this person understands my problem" |

### agitation

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Show the cost of inaction. Make the status quo feel unacceptable. |
| **Required** | headline, consequence narrative |
| **Copy rule** | Truthful consequences only. Project 6-12 months forward. Never invent fears. |
| **Tone** | Empathetic urgency, not fear-mongering |
| **Scroll position** | 15-22% |
| **Psychological role** | Loss aversion activation — losing hurts more than gaining |

### bridge

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Transition from problem to solution. The "there's a better way" moment. |
| **Required** | 1-3 sentences that pivot from pain to possibility |
| **Copy rule** | Brief. The bridge is a breath between tension and relief. |
| **Scroll position** | 20-25% |
| **Psychological role** | Tension release — the reader exhales here |

### solution-reveal

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Introduce the product as the natural resolution to the established problem. |
| **Required** | headline, product name, core promise (1 sentence), visual/screenshot |
| **Copy rule** | Position as discovery, not pitch. "We built X because..." not "Buy X now!" |
| **Scroll position** | 22-30% |
| **Psychological role** | Relief + curiosity — "this might actually work" |

### features

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Show WHAT the product does and HOW it delivers the promise. |
| **Required** | headline, 3-6 features with benefit-oriented descriptions |
| **Format** | Icon + title + 1-2 sentence benefit description per feature |
| **Copy rule** | Lead with benefit, follow with feature. "Ship faster (auto-deploy)" not "Auto-deploy (faster shipping)" |
| **Scroll position** | 25-40% |
| **Psychological role** | Rational validation — "this makes sense logically" |

### how-it-works

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Remove complexity anxiety. Show the path is simple. |
| **Required** | headline, exactly 3 steps |
| **Format** | Numbered steps with title + 1-sentence description each |
| **Copy rule** | Steps must be actions the USER takes, not what the product does. "1. Connect your account" not "1. Our system processes your data" |
| **Scroll position** | 30-40% |
| **Psychological role** | Cognitive ease — 3 steps feels achievable |

### social-proof

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Transfer trust from existing customers to the prospect. |
| **Required** | headline, 2-5 testimonials OR metrics |
| **Testimonial format** | Quote + name + role/company + photo (if available) + specific result |
| **Metrics format** | Large number + description ("14,000+ teams", "97% satisfaction") |
| **Copy rule** | Real data only. If no real testimonials exist, use metrics or skip entirely. NEVER fabricate. |
| **Scroll position** | 40-55% |
| **Psychological role** | Social proof — "others like me trust this" |

### empathy

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Show the guide (brand/founder) understands the hero's struggle from personal experience. |
| **Required** | headline, personal narrative (2-4 paragraphs) |
| **Copy rule** | First-person. Vulnerable but not self-pitying. Must connect YOUR experience to THEIR situation. |
| **Scroll position** | 18-25% |
| **Psychological role** | Trust through shared experience — "they've been where I am" |

### authority

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Establish credentials and expertise without arrogance. |
| **Required** | headline, 3-5 authority signals |
| **Format** | Credentials, results achieved, media features, years of experience, client logos |
| **Copy rule** | Facts, not claims. "12 years in..." not "industry-leading expert". |
| **Scroll position** | 25-30% |
| **Psychological role** | Competence trust — "they can actually deliver" |

### plan

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Give the prospect a clear, simple path forward. Clarity reduces fear. |
| **Required** | headline, exactly 3 steps, CTA at the end |
| **Format** | Numbered steps: what to do → what happens → what you get |
| **Copy rule** | Each step is one sentence. If you need more, the plan is too complex. |
| **Scroll position** | 35-45% |
| **Psychological role** | Cognitive load reduction — a plan makes buying feel safe |

### success-vision

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Paint the after-state. Make the reader FEEL what success looks like. |
| **Required** | headline, 2-3 paragraphs of sensory, specific future-pacing |
| **Copy rule** | Use "imagine" or "picture this". Be specific: "opening your dashboard Monday morning and seeing 47 new leads" not "getting more leads" |
| **Scroll position** | 55-65% |
| **Psychological role** | Future pacing — the reader mentally owns the outcome |

### failure-stakes

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Subtly show what happens if they do nothing. Counterbalance to success-vision. |
| **Required** | headline, 1-2 paragraphs |
| **Copy rule** | Honest and empathetic. Never threatening. "The gap between you and competitors who adopt this grows wider every month" — factual, not dramatic. |
| **Scroll position** | 65-70% |
| **Psychological role** | Loss aversion — gentle nudge, not fear manipulation |

### objection-handler

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Address the reasons people DON'T buy, woven naturally into the page. |
| **Required** | 3-5 objections with responses |
| **Format** | Can be FAQ style, or "You might be thinking..." narrative, or interleaved in other sections |
| **Copy rule** | Acknowledge the objection respectfully FIRST, then reframe. "We asked" > "We offer refunds under certain conditions". |
| **Source** | Objections come from Phase 1 `objections[]` array |
| **Scroll position** | 60-75% |
| **Psychological role** | Pre-emptive doubt resolution |

### pricing

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Present the price in context of value. The price should feel inevitable, not shocking. |
| **Required** | headline, price, value stack, CTA |
| **Optional** | anchor price, installments, comparison table, "cost of NOT buying" calculation |
| **Copy rule** | Show value BEFORE showing price. If possible, compare to cost of alternatives or cost of inaction. |
| **Scroll position** | 70-85% |
| **Price anchoring** | Show the total value ("R$ 4.970 in value") before the actual price ("Today: R$ 997") |

### guarantee

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Remove remaining risk. Make buying feel safe. |
| **Required** | headline, guarantee terms, visual badge/seal |
| **Copy rule** | Bold and confident. Name the guarantee specifically. "30-day no-questions-asked refund" not "satisfaction guaranteed" |
| **Scroll position** | 78-88% |
| **Psychological role** | Risk reversal — shift the risk from buyer to seller |

### faq

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Catch remaining questions and reduce support load. |
| **Required** | 5-8 questions with answers |
| **Copy rule** | Write questions in the audience's voice, not corporate voice. "Can I cancel anytime?" not "What is your cancellation policy?" |
| **Source** | Top questions from Phase 1 discovery + common objections not yet addressed |
| **Scroll position** | 82-92% |

### final-cta

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Last call to action. The closing argument. |
| **Required** | headline (restate core promise), CTA button, trust signal |
| **Copy rule** | Shorter than hero. The reader has all the information — just tell them what to do. |
| **Micro-copy** | Include trust signal under button: "Join X+ members" + objection handler: "Cancel anytime" |
| **Scroll position** | 88-95% |

### footer

| Attribute | Specification |
|-----------|--------------|
| **Purpose** | Legal, navigation, and secondary links. |
| **Required** | Copyright, privacy link, terms link |
| **Optional** | Contact info, social links, secondary pages |
| **Scroll position** | 95-100% |

---

## Section C: Copy Rules

Nine rules. Every piece of copy on the page must pass all nine. These are NOT suggestions — they are enforcement rules.

### Rule 1: Specificity Over Adjectives

```
WRONG: "Our amazing tool helps you grow faster"
RIGHT: "Teams using [Product] ship 3.2x more content in their first 30 days"
```

Every claim needs a number, a name, a timeframe, or a verifiable fact. If you can't make it specific, cut the sentence.

### Rule 2: Audience Language First

Before writing ANY section, consult Phase 2 `audience_insights.language_patterns`. Use the exact phrases your audience uses to describe their problem. Their words, not your marketing words.

```
Audience says: "I'm drowning in manual tasks"
You write:    "You're drowning in manual tasks that eat 15+ hours a week"
NOT:          "Streamline your workflow with our automation platform"
```

### Rule 3: Benefit → Feature (Never Reverse)

The reader cares about their outcome, not your technology. Lead with what changes for THEM, follow with how.

```
WRONG: "AI-powered analytics engine with real-time processing"
RIGHT: "Know which content will perform before you publish (AI analyzes 50+ signals in real-time)"
```

### Rule 4: One Idea Per Section

Each section has ONE job. If you're explaining features AND handling objections in the same section, split them. Cognitive overload kills conversion.

### Rule 5: CTA Formula — Action Verb + Outcome

| Weak | Strong | Why |
|------|--------|-----|
| Submit | Get Your Free Report | Focuses on what they receive |
| Learn More | See How It Works | Sets expectation |
| Sign Up | Start Your Free Trial | Implies action + value |
| Click Here | Build Your First Campaign | Outcome-oriented |
| Buy Now | Start Growing Today | Emotional outcome |

**CTA Placement:** After every value demonstration. Minimum 3 CTAs per page (hero, mid-page, final). Never more than 2 scroll-lengths between CTAs.

### Rule 6: Social Proof Rules

- **Real only.** Never fabricate testimonials, metrics, or logos.
- **Specific results.** "Grew revenue 40% in 90 days" beats "Great product!"
- **Named sources.** "Sarah, Head of Marketing at Acme" beats "Marketing Professional"
- **Relevant proof.** Match the testimonial to the section's argument. Testimonial about ease-of-use goes near the "how it works" section, not the pricing section.
- **If no proof exists:** Use logic, comparisons, or skip the section. NEVER invent.

### Rule 7: Objection Handling Pattern

Objections from Phase 1 `objections[]` must be addressed within the page, NOT only in the FAQ. Weave them naturally:

**Acknowledge → Reframe → Evidence**

```
"You might be wondering if this works for [specific situation]."     ← Acknowledge
"That's actually where [Product] shines most, because..."           ← Reframe
"[Name] had the same concern — here's what happened: [result]."     ← Evidence
```

**Placement:** Objections should appear BEFORE the pricing section. By the time the reader sees the price, their doubts should already be resolved.

### Rule 8: Urgency — Only If Genuine

```
ALLOWED: "Enrollment closes Friday at midnight" (real deadline)
ALLOWED: "12 spots remaining" (real capacity limit)
ALLOWED: "Price increases to R$ 1.497 on May 1st" (real price increase)

FORBIDDEN: Fake countdown timers that reset on refresh
FORBIDDEN: "Only 3 left!" when there's no real limit
FORBIDDEN: "This offer won't last" without a specific date
FORBIDDEN: Implied scarcity when the product is digital and unlimited
```

If there is no genuine urgency, do NOT manufacture it. The page converts through value, not pressure.

### Rule 9: Pricing Section Architecture

**Step 1 — Anchor the value:**
Show the total value of everything included. List each component with its individual value.

**Step 2 — Show the price:**
After the value stack, reveal the actual price. The gap between total value and price creates perceived deal.

**Step 3 — Compare alternatives:**
Show what the alternative costs (hiring someone, using competitors, doing nothing).

**Step 4 — Break it down:**
If installments are available, show the per-day or per-month cost. "Less than R$ 3/day" feels more accessible than "R$ 997".

```
Value Stack Example:
┌──────────────────────────────────────────────┐
│ Complete Course Library         R$ 2.970     │
│ Private Community Access        R$ 1.200     │
│ Monthly Live Q&A Sessions       R$   600     │
│ Template Pack (47 templates)    R$   497     │
│ ────────────────────────────────────────────  │
│ Total Value                     R$ 5.267     │
│                                              │
│ Your Investment Today:          R$   997     │
│ or 12x R$ 97                                 │
└──────────────────────────────────────────────┘
```

---

## Section D: Awareness-Level Adaptation

Based on Eugene Schwartz's 5 levels of awareness. The framework selection, page length, section order, and copy tone ALL change based on where the audience sits.

### Level 1: Unaware

**Profile:** Doesn't know they have a problem. Browsing casually.
**Framework:** Story Bridge (mandatory)
**Page Length:** 8-12 sections (long)
**Primary Focus:** Education → Problem identification → Solution introduction

| Phase | Copy Strategy |
|-------|--------------|
| Opening | Tell a story they relate to. Don't mention the product for the first 3 sections. |
| Middle | Gradually reveal the problem through the story. Let them self-identify. |
| Close | Introduce the solution as the natural next step in the story. |

**Headline Pattern:** Story-based or question-based. "What happens when..." or "The day I realized..."
**CTA Tone:** Ultra-low commitment. "See the story" or "Discover how".

### Level 2: Problem-Aware

**Profile:** Knows they have a problem. Doesn't know solutions exist.
**Framework:** PAS (recommended) or Story Bridge
**Page Length:** 6-10 sections (medium-long)
**Primary Focus:** Problem validation → Agitation → Solution reveal

| Phase | Copy Strategy |
|-------|--------------|
| Opening | Name their pain immediately. Use their words. Validate that the problem is real. |
| Middle | Show the consequences of not solving (agitation). Then reveal the solution. |
| Close | Proof that the solution works (testimonials, metrics). |

**Headline Pattern:** Problem-based. "Still spending 15+ hours on..." or "Why your content isn't converting"
**CTA Tone:** Medium commitment. "See how it works" or "Get the solution".

### Level 3: Solution-Aware

**Profile:** Knows solutions exist. Comparing options.
**Framework:** AIDA (recommended)
**Page Length:** 6-8 sections (medium)
**Primary Focus:** Differentiation → Why YOUR solution → Proof

| Phase | Copy Strategy |
|-------|--------------|
| Opening | Acknowledge they've seen other solutions. Immediately differentiate. |
| Middle | Feature comparison (without naming competitors directly). Show unique advantages. |
| Close | Social proof from people who switched. |

**Headline Pattern:** Differentiation-based. "The only [product] that [unique benefit]" or "Unlike [category], [Product] does..."
**CTA Tone:** Confident. "Start your trial" or "Compare for yourself".

### Level 4: Product-Aware

**Profile:** Knows YOUR product. Needs a reason to act NOW.
**Framework:** AIDA (shortened) or Ogilvy Direct
**Page Length:** 5-7 sections (short-medium)
**Primary Focus:** Details → Specific proof → Offer → CTA

| Phase | Copy Strategy |
|-------|--------------|
| Opening | Skip the problem. Lead with a new angle, new feature, or new offer. |
| Middle | Deep product details, specific use cases, detailed testimonials. |
| Close | Offer + urgency (only if genuine) + guarantee. |

**Headline Pattern:** Offer-based or news-based. "New: [feature]" or "[Product] now does [thing]"
**CTA Tone:** Direct. "Get started" or "Claim your spot".

### Level 5: Most-Aware

**Profile:** Ready to buy. Just needs the final push.
**Framework:** Ogilvy Direct (shortened) or custom minimal
**Page Length:** 3-5 sections (short)
**Primary Focus:** Offer → Guarantee → CTA

| Phase | Copy Strategy |
|-------|--------------|
| Opening | Lead with the offer. Price, what's included, deadline. |
| Middle | Guarantee. Remove last objection. |
| Close | CTA. Make it dead simple. |

**Headline Pattern:** Offer-based. "Get [Product] for [price] — [deadline]"
**CTA Tone:** Transactional. "Buy now" or "Enroll today".

---

## Section E: Copywriting Skill Integration

The narrative skill is the STRUCTURE; the copywriting skill is the QUALITY GATE. They work together, never independently.

### Integration Points

| Narrative Phase | Copywriting Invocation | What It Does |
|----------------|----------------------|--------------|
| Headline generation | `4U Headline Formula` | Scores headline ≥ 12/16 before accepting |
| Body copy writing | `Anti-Slop Enforcement` | Scans for banned phrases, enforces specificity |
| CTA creation | `CTA Patterns` | Validates action verb + outcome format |
| Emotional sections | `Emotional Triggers` | Selects appropriate trigger for the section's role |
| Final review | `Copy Scoring Rubric` | Scores total copy ≥ 30/35 before approval |

### Invocation Protocol

Before writing copy for any section:

```
1. IDENTIFY the section type and its psychological role
2. SELECT the appropriate copywriting framework (AIDA/PAS/4U)
3. WRITE the first draft following the framework
4. RUN anti-slop check (Tier 1 hard ban, Tier 2 conditional, Tier 3 style rules)
5. SCORE using the 7-dimension rubric
6. ITERATE if score < 30/35
```

### Anti-Slop Enforcement (from copywriting skill)

**Tier 1 — Hard Banned (auto-reject, zero tolerance):**
- "game-changer", "revolutionary", "cutting-edge", "best-in-class"
- "synergy", "leverage" (non-physical), "disrupt"
- "innovative solution", "transform your", "unlock the power"
- "dive deep", "it's worth noting", "in today's fast-paced"
- Plus all terms in `brand-voice.yaml → anti_slop.banned_phrases`

**Tier 2 — Conditional (require evidence):**
- Superlatives need data: "Rated #1 by G2" not "The best tool"
- Speed claims need metrics: "Deploys in 90 seconds" not "Lightning fast"
- Scale claims need numbers: "14,000+ teams in 42 countries" not "Used by millions"

**Tier 3 — Style (always enforce):**
- Active voice
- Specific over vague
- No hedging ("just", "simply", "actually", "basically")
- Reader-first ("You" before "We")
- Concrete verbs ("ship", "build", "cut" over "utilize", "facilitate")

### Slop Detection Final Check

Before marking Phase 5 complete, run this on EVERY headline and body paragraph:
1. Could a competitor say the exact same sentence? → Too generic, rewrite.
2. Does this sentence contain information or just vibes? → Vibes only = add specifics or cut.
3. Would a real human say this in conversation? → If not, simplify.
4. Is any word here only because it "sounds professional"? → Cut it.

---

## Section F: Voice Alignment

### When Brand Voice Applies

If the user has opted into brand voice (GOLDEN-DOC.md or equivalent), ALL copy must pass through voice alignment before being finalized.

### Voice Loading Protocol

```
1. READ growthOS/voice/GOLDEN-DOC.md
2. EXTRACT: tone descriptors, vocabulary (loved/hated), rules, positioning
3. READ growthOS/brand-voice.yaml → anti_slop section
4. READ growthOS/voice/virais/INDEX.md → viral patterns
5. FOR each viral pattern tagged voice_fit: "aligns" → incorporate structure
6. FOR each viral pattern tagged voice_fit: "conflicts" → NEVER use, even if effective elsewhere
```

### Voice Adaptation Rules

| Framework Element | How Voice Adapts |
|------------------|-----------------|
| Headlines | Match tone (confessional? provocative? authoritative?) |
| Body copy | Use loved vocabulary, avoid hated vocabulary |
| CTAs | Match the brand's CTA pattern (e.g., "comenta [palavra] aqui" for Rafael) |
| Testimonials | Frame in language consistent with brand positioning |
| Pricing | Use the brand's pricing language (e.g., "investimento" vs. "preço") |

### Brand Voice Override Hierarchy

```
1. Brand voice rules (GOLDEN-DOC.md)    — HIGHEST PRIORITY
2. Anti-slop rules (brand-voice.yaml)    — SECOND
3. Framework conventions (this skill)     — THIRD
4. General copywriting rules              — LOWEST
```

If GOLDEN-DOC.md says "never use the word 'bot'" and the PAS framework would naturally use it, the brand voice wins.

### When No Brand Voice Exists

If no GOLDEN-DOC.md or brand-voice.yaml is found:
- Use neutral, professional tone
- Apply framework conventions as-is
- Focus on clarity and specificity
- Anti-slop rules from the copywriting skill still apply (they're universal)

---

## Section G: Preview Output

Phase 5 produces a narrative wireframe — a styled HTML document that shows the page structure with all copy but MINIMAL design. This is NOT the final page. It's a document for COPY review.

### Output File

```
growthOS/output/sales-pages/{slug}/previews/phase-5-narrative.html
```

### Wireframe Specification

The wireframe HTML must include:

**1. Header bar:**
```
Project: {product name} | Framework: {AIDA/PAS/Story Bridge/Ogilvy Direct}
Awareness Level: {level} | Sections: {count} | Estimated read time: {X min}
```

**2. Section cards (for each section):**
```
┌─ Section {N}: {section_type} ─────────────────────────────┐
│ Purpose: {psychological role}                              │
│ Scroll Position: {estimated %}                             │
│                                                            │
│ ## {HEADLINE}                                              │
│ ### {Subheadline}                                          │
│                                                            │
│ {Body copy — full text}                                    │
│                                                            │
│ [CTA: {cta_text}]                                          │
│                                                            │
│ Social Proof: {element if present}                         │
│ Objection Addressed: {if applicable}                       │
└────────────────────────────────────────────────────────────┘
```

**3. Summary footer:**
```
Total CTAs: {count} | Objections Addressed: {count}/{total}
Anti-Slop: PASSED/FAILED | Voice Aligned: YES/NO
Copy Score: {total}/35
```

### HTML Styling Rules

- Clean, readable, monochrome or muted palette — this is a WORKING DOCUMENT, not a design showcase
- Each section card visually distinct with clear borders
- Headlines styled prominently (large font)
- Body copy in readable serif or sans-serif at 16-18px
- CTA buttons styled as outlined buttons (not filled — save that for Phase 6)
- Scroll position shown as a subtle progress bar on the left edge
- Mobile-friendly (this will be reviewed on phones too)

### State Update

After generating the wireframe, update `state.json`:

```json
{
  "phase_5_narrative": {
    "status": "in-progress",
    "framework_used": "{selected framework}",
    "sections": [/* array of section objects per schema */],
    "copywriting_skill_used": true,
    "anti_slop_validated": true,
    "voice_alignment_checked": true,
    "preview_url": "http://localhost:5060/sales-page/{slug}/phase/5"
  }
}
```

Set status to `"approved"` only after user confirms.

---

## Execution Workflow

When Phase 5 is triggered:

```
1. READ state.json — verify Phase 4 is approved
2. LOAD product knowledge (Phase 1 data)
3. LOAD audience research (Phase 2 data)
4. LOAD brand voice (if applicable)
5. DETERMINE awareness level from Phase 1 → audience.awareness_level
6. SELECT framework based on awareness level + product type
7. PRESENT framework choice to user with reasoning — wait for confirmation
8. MAP section flow based on selected framework
9. WRITE copy for each section (invoking copywriting skill)
10. RUN anti-slop check across all copy
11. SCORE copy using 7-dimension rubric
12. IF score < 30/35 → iterate weakest sections
13. GENERATE wireframe HTML → previews/phase-5-narrative.html
14. PRESENT to user for review
15. IF approved → update state, proceed to Phase 6
16. IF revision requested → iterate specific sections, re-generate wireframe
```

---

## Quick Reference: Framework Selection

```
Audience Awareness → Framework:

  Unaware ─────────────────→ Story Bridge (8-12 sections)
  Problem-Aware ───────────→ PAS (6-10 sections)
  Solution-Aware ──────────→ AIDA (6-8 sections)
  Product-Aware ───────────→ AIDA short or Ogilvy Direct (5-7 sections)
  Most-Aware ──────────────→ Ogilvy Direct minimal (3-5 sections)
```

## Quick Reference: Section Selection by Framework

```
AIDA:         hero → logo-bar → features → how-it-works → social-proof → pricing → guarantee → final-cta
PAS:          hero → problem-expansion → agitation → bridge → solution-reveal → features → social-proof → objection-handler → pricing → final-cta
Story Bridge: hero → problem-story → empathy → authority → plan → social-proof → cta-primary → success-vision → failure-stakes → objection-handler → pricing → final-cta
Ogilvy:       hero-visual → editorial-headline → long-form-copy → before-after → social-proof → single-cta → guarantee
```
