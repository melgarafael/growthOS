---
name: copywriting
description: Persuasive copywriting using AIDA, PAS, 4U headline formulas, CTA patterns, emotional triggers, anti-slop enforcement, and brand voice awareness
---

# Copywriting Skill

## Trigger Conditions

Use this skill when the user asks to:
- Write marketing copy, headlines, or taglines
- Create social media posts or captions
- Draft email subject lines or email body copy
- Write landing page copy or product descriptions
- Craft CTAs (calls-to-action)
- Improve or rewrite existing copy
- Generate ad copy (paid social, search ads)
- Write newsletter content

---

## Brand Voice Integration

**MANDATORY:** Before writing ANY copy, load the brand voice configuration.

```python
from growthOS_shared.config import load_brand_voice
brand = load_brand_voice()
```

Every piece of copy must:
1. Match `brand.tone` descriptors
2. Avoid all terms in `brand.avoid` and `anti_slop.banned_phrases`
3. Follow `anti_slop.style_rules`
4. Respect platform-specific `tone_override` when targeting a specific channel
5. Stay within platform `max_length` limits

---

## Anti-Slop Enforcement Rules

Anti-slop is the single most important quality gate for AI-generated copy. Without it, all output converges to the same generic AI voice.

### Tier 1: Hard Banned (auto-reject)

These phrases are NEVER acceptable in any context. If they appear in output, the copy fails validation:

- "game-changer", "revolutionary", "cutting-edge", "best-in-class"
- "synergy", "leverage" (as verb for non-physical things), "disrupt"
- "innovative solution", "transform your", "unlock the power"
- "dive deep", "it's worth noting", "in today's fast-paced"
- "at the end of the day", "think outside the box"
- "move the needle", "low-hanging fruit", "paradigm shift"
- "holistic approach", "seamlessly integrate"

Plus any terms in `brand-voice.yaml → anti_slop.banned_phrases` and `brand.avoid`.

### Tier 2: Conditional Ban (require evidence)

These patterns are allowed ONLY when backed by specific data:

| Pattern | Banned Form | Acceptable Form |
|---------|------------|-----------------|
| Superlatives | "The best tool for..." | "Rated #1 by G2 in Q3 2025" |
| Speed claims | "Lightning fast" | "Deploys in under 90 seconds" |
| Scale claims | "Used by millions" | "Used by 14,000+ teams in 42 countries" |
| Ease claims | "Effortless setup" | "3-step setup, average 4 minutes" |
| ROI claims | "Massive ROI" | "Teams report 3.2x return within 90 days" |

### Tier 3: Style Rules (always enforce)

1. **Active voice** — "We built X" not "X was built by us"
2. **Specific over vague** — Numbers, names, timeframes beat adjectives
3. **No clickbait** — Headlines must deliver on their promise
4. **No hedging** — Remove "just", "simply", "actually", "basically", "essentially"
5. **No filler** — Remove "in order to" (use "to"), "due to the fact that" (use "because")
6. **Concrete verbs** — "Ship", "build", "cut", "grow" over "utilize", "facilitate", "enable"
7. **Reader-first** — "You" before "We". Address the reader's situation, not your product.

### Slop Detection Prompt

Before finalizing any copy, run this mental checklist:
- Could a competitor say the exact same sentence about their product? → Too generic, rewrite.
- Does this sentence contain information or just vibes? → If vibes only, add specifics or cut.
- Would a real human say this in conversation? → If not, simplify.
- Is any word here only because it "sounds professional"? → Cut it.

---

## Copywriting Frameworks

### AIDA — Attention, Interest, Desire, Action

The foundational framework for persuasive copy. Works for: landing pages, emails, ads, long-form sales pages.

| Stage | Goal | Techniques |
|-------|------|-----------|
| **Attention** | Stop the scroll. Break the pattern. | Bold claim, surprising stat, provocative question, pattern interrupt |
| **Interest** | Keep them reading. Build relevance. | Specific details, "imagine if" scenarios, relatable problems |
| **Desire** | Make them want it. Show transformation. | Social proof, benefits (not features), before/after, exclusivity |
| **Action** | Tell them exactly what to do. | Clear CTA, urgency (real, not fake), risk reversal |

**AIDA Template — Landing Page Hero:**
```
[ATTENTION] — Headline: Bold claim or question that addresses their biggest pain
[INTEREST] — Subheadline: How you solve it, with one specific detail
[DESIRE] — Social proof: "Join [X] teams who [specific result]"
[ACTION] — CTA button: Action verb + outcome ("Start shipping faster")
```

**AIDA Template — Email:**
```
Subject: [ATTENTION — curiosity or benefit hook]
Line 1: [INTEREST — relatable problem or scenario]
Body: [DESIRE — how your solution changes their situation]
CTA: [ACTION — single clear next step]
PS: [Reinforce urgency or add secondary benefit]
```

### PAS — Problem, Agitate, Solution

The most effective framework for copy that converts through empathy. Works for: emails, ads, social posts, product descriptions.

| Stage | Goal | How |
|-------|------|-----|
| **Problem** | Name the pain they're feeling | Use their exact words (from reviews, interviews, support tickets) |
| **Agitate** | Make the problem feel urgent | Show consequences of inaction. "And it gets worse..." |
| **Solution** | Present your answer | Position as the natural resolution to the agitated problem |

**PAS Example:**
```
[PROBLEM] You're spending 15+ hours a week on content that gets 200 views.
[AGITATE] Meanwhile, your competitors are posting daily and dominating
your keywords. Every week you delay, they build more authority that's
harder to overcome.
[SOLUTION] GrowthOS generates a full content calendar in 10 minutes,
optimized for your actual audience — not generic AI slop.
```

**PAS Calibration:**
- Agitation should be truthful, not manipulative. Describe real consequences, not fear-mongering.
- The transition from Agitate → Solution should feel like relief, not a hard sell.
- The problem should be recognizable to the reader in the first 3 seconds.

### 4U Headline Formula

Every headline should score high on at least 3 of the 4U criteria:

| U | Question | Score 1-4 |
|---|----------|-----------|
| **Useful** | Does it promise a benefit the reader cares about? | 1 = no benefit, 4 = solves their #1 problem |
| **Urgent** | Is there a reason to read/act now? | 1 = whenever, 4 = time-sensitive |
| **Ultra-specific** | Does it include numbers, names, or details? | 1 = vague, 4 = precise metrics |
| **Unique** | Is this perspective fresh or differentiated? | 1 = generic, 4 = never seen before |

**Scoring:** Total ≥ 12 = strong headline. 8-11 = needs work. <8 = rewrite.

**Examples:**
```
❌ "Improve Your Marketing" (Useful: 2, Urgent: 1, Specific: 1, Unique: 1 = 5)
✅ "How 3 B2B Teams Cut Content Costs 40% in 30 Days" (U:4, Ur:3, S:4, Un:3 = 14)
```

### Additional Headline Formulas

**How-to:** "How to [achieve desired outcome] without [common objection]"
```
How to Build a Content Engine Without Hiring a Content Team
```

**Number list:** "[Number] [unexpected adjective] ways to [benefit]"
```
7 Counterintuitive Ways to Double Your LinkedIn Engagement
```

**Question:** Direct question that the reader answers "yes" to mentally
```
Still writing social posts one at a time?
```

**Negative:** "Stop [common mistake that costs them]"
```
Stop Writing Content Nobody Searches For
```

**Proof:** "[Specific result] in [specific timeframe]"
```
From 0 to 50K Organic Visits in 6 Months: Our Playbook
```

---

## CTA Patterns

### CTA Formula

**Structure:** `[Action Verb] + [Outcome/Benefit]`

| Weak CTA | Strong CTA | Why |
|----------|-----------|-----|
| Submit | Get Your Free Report | Focuses on what they receive |
| Learn More | See How It Works | Sets expectation |
| Sign Up | Start Your Free Trial | Implies action + value |
| Download | Grab the Playbook | Active, ownership language |
| Click Here | Build Your First Campaign | Outcome-oriented |

### CTA Context Rules

| Funnel Stage | CTA Tone | Examples |
|-------------|----------|---------|
| **TOFU** (awareness) | Low commitment, curiosity | "See examples", "Read the guide", "Watch the demo" |
| **MOFU** (consideration) | Medium commitment, value exchange | "Get the free template", "Try it free", "Compare plans" |
| **BOFU** (decision) | High commitment, confidence | "Start building", "Choose your plan", "Launch your first campaign" |

### CTA Placement Rules

1. **Above the fold** — Primary CTA visible without scrolling
2. **After value demonstration** — Place CTA after showing a benefit or proof point
3. **End of content** — Always close with a CTA
4. **One primary CTA per section** — Don't compete with yourself
5. **Sticky CTA on mobile** — For landing pages, keep CTA accessible during scroll

### Micro-copy Around CTAs

The words around the button matter as much as the button text:

```
[Trust signal] "Join 2,400+ marketing teams"
[Button] Start Free — No Credit Card
[Objection handler] "Cancel anytime. Setup takes 3 minutes."
```

---

## Emotional Triggers

### The 7 Core Emotional Triggers for Marketing Copy

Use these deliberately and ethically — manipulative copy backfires long-term.

| Trigger | How It Works | Ethical Application |
|---------|-------------|-------------------|
| **Fear of Missing Out (FOMO)** | People hate losing more than they love gaining | Show what competitors or peers are already doing. Use real data, not fake urgency. |
| **Belonging** | People want to be part of something | Community language: "Join", "fellow", "together". Show the tribe they'll belong to. |
| **Status** | People want to feel successful/competent | Position your product as what smart/successful people use. "Used by teams at [brands]". |
| **Curiosity** | Open loops drive engagement | Start with a surprising fact, leave the resolution after the CTA. Don't bait-and-switch. |
| **Trust** | People buy from those they trust | Social proof, specificity (vague claims erode trust), transparency about limitations. |
| **Reciprocity** | Give value first, ask second | Free tools, templates, insights before asking for anything. |
| **Autonomy** | People want to feel in control | "Choose your plan", "customize your", "on your schedule". Never pressure. |

### Applying Emotional Triggers by Platform

| Platform | Primary Trigger | Secondary | Copy Style |
|----------|----------------|-----------|-----------|
| **LinkedIn** | Status + Trust | Belonging | Professional, data-backed, thought leadership |
| **Twitter/X** | Curiosity + FOMO | Status | Concise, provocative, thread-worthy |
| **Reddit** | Trust + Reciprocity | Autonomy | Authentic, value-first, no self-promotion |
| **Email** | Curiosity + Reciprocity | FOMO | Personal, conversational, value-driven |
| **Landing Page** | Trust + Status | FOMO | Benefit-focused, proof-heavy, clear CTA |

---

## Platform-Specific Copy Guidelines

### LinkedIn

- Lead with insight, not promotion
- First line is the headline — make it stop the scroll
- Use line breaks liberally (mobile readability)
- End with a question to drive comments
- Hashtags: 3-5 max, specific to topic
- Carousel posts: 1 key point per slide, 8-12 slides max
- Character limit: 3,000 (but aim for 800-1,500 for engagement)

### Twitter/X

- One idea per tweet
- Front-load the value — most people won't read past line 1
- Threads: Hook tweet → Value tweets → CTA tweet
- No hashtags in body text (put in reply if needed)
- Character limit: 280

### Reddit

- NEVER sound like marketing copy
- Lead with value, context, or genuine question
- Acknowledge limitations — Redditors respect honesty
- Include your methodology or thinking process
- Character limit: 10,000 (but frontload value)

### Email

- Subject line: 40-60 characters. Curiosity or benefit.
- Preview text: Complement the subject, don't repeat it.
- One CTA per email. One clear ask.
- P.S. line: Second most-read element after subject line.
- Tone: Conversational, as if writing to one person.

---

## Copy Testing Framework

### A/B Testing Priorities

Test in this order (highest impact first):

1. **Headline / Subject Line** — Biggest impact on whether anything else gets read
2. **CTA text and placement** — Directly affects conversion
3. **Social proof format** — How trust is communicated
4. **Opening line** — Determines if they keep reading
5. **Body structure** — Long vs short, bullets vs paragraphs

### Copy Scoring Rubric

Rate copy 1-5 on each dimension:

| Dimension | 1 (Weak) | 5 (Strong) |
|-----------|---------|-----------|
| **Clarity** | Confusing, jargon-heavy | Crystal clear on first read |
| **Specificity** | Vague claims, no data | Numbers, names, timeframes |
| **Relevance** | Generic, could be any product | Speaks to specific audience's specific pain |
| **Emotion** | Flat, informational only | Creates a feeling (curiosity, desire, relief) |
| **Action** | No clear next step | Obvious, low-friction CTA |
| **Voice** | Generic AI tone | Distinctly matches brand voice |
| **Anti-slop** | Multiple banned phrases | Zero slop, every word earns its place |

**Score ≥ 30/35:** Ship it.
**Score 25-29:** Polish and ship.
**Score < 25:** Rewrite.

---

## Copy Generation Workflow

### Step-by-Step Process

1. **Load brand voice** — Read `brand-voice.yaml` first
2. **Identify context** — Platform, funnel stage, audience segment
3. **Choose framework** — AIDA for long-form, PAS for short-form, 4U for headlines
4. **Draft** — Write the first version following the framework
5. **Anti-slop pass** — Scan for all banned phrases and patterns, replace with specifics
6. **Brand voice check** — Verify tone matches, avoid list respected
7. **Score** — Rate on the 7-dimension rubric
8. **Iterate** — If score < 30, identify weakest dimensions and rewrite those sections
9. **Platform check** — Verify length limits and platform-specific rules

---

## Output Contract

### Copy Output Schema

```yaml
output_contract:
  format: markdown
  required_sections:
    - frontmatter:
        type: string  # "copy"
        subtype: string  # "headline" | "social-post" | "email" | "landing-page" | "ad" | "cta"
        status: string  # "draft" | "review" | "approved"
        date: string  # ISO 8601
        author: string  # "growthOS/copywriting"
        platform: string  # target platform
        funnel_stage: string  # "tofu" | "mofu" | "bofu"
    - copy_content:
        primary: string  # the main copy piece
        variants: list  # 2-3 alternative versions
        headline_score:  # 4U score if applicable
          useful: integer  # 1-4
          urgent: integer  # 1-4
          ultra_specific: integer  # 1-4
          unique: integer  # 1-4
          total: integer
    - quality_scores:
        clarity: integer  # 1-5
        specificity: integer  # 1-5
        relevance: integer  # 1-5
        emotion: integer  # 1-5
        action: integer  # 1-5
        voice: integer  # 1-5
        anti_slop: integer  # 1-5
        total: integer  # sum of above
    - anti_slop_report:
        passed: boolean
        violations_found: list  # any phrases that were caught and replaced
        replacements_made: list  # what they were replaced with
  validation:
    anti_slop: true
    brand_voice: true
    platform_length: true  # must respect max_length
    min_variants: 2  # always provide alternatives
```
