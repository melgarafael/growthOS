---
name: sales-page-persona-simulator
description: >-
  Simulates how distinct buyer personas would read a built sales page — predicting objections,
  drop-off points, and conversion likelihood before the page ships. Grounded in
  design-intelligence/theory/conversion-psychology.md and
  design-intelligence/references/patterns/objection-handling.md, not generic AI guesses.
  Use when a sales page (Phase 7 build output, or any standalone HTML page) needs a
  pre-publish read on how real visitors will react.
---

# Sales Page Persona Simulator

You are running a **visitor reaction simulation** against a built sales page. You are not another QA pass — `sales-page-qa` already checks that the page works and matches spec. Your job is to predict what happens in a *reader's head* as they scroll: where curiosity turns to doubt, where an objection fires, whether the page resolves it, and where they'd close the tab.

This skill is **independent and manually triggered** — it is not a phase in the 8-phase pipeline, does not gate the build, and never edits `state.json`. Run it whenever the user wants a pre-publish read on conversion risk.

## Core Principle

```
WRONG: "As an AI, I think this page feels trustworthy and would convert well."
RIGHT: "The Skeptic persona hits the pricing section with zero authority signals shown yet
        (no credentials, no press, no data-backed claims — see conversion-psychology.md
        Principle 4: Authority). They bounce here. Fix: add a authority signal above the
        fold per the Authority section, or move existing founder credentials up from the footer."
```

Every objection you assign to a persona must trace to a real psychological principle. Every fix you recommend must trace to a documented objection-handling pattern. Never invent unsourced psychology.

## Trigger Conditions

Run this skill when the user asks things like:
- "Simulate how visitors would react to this sales page"
- "Run the persona simulator on {slug}"
- "What objections will people have before buying?"
- "Predict conversion for this page before we publish"

## Mandatory Reads

1. **Built page** — `growthOS/output/sales-pages/{slug}/index.html`
   If missing, ask whether the user has a different HTML file to point at (this skill also works on any standalone sales page HTML, not just pipeline output). If neither exists, HALT and say so.
2. **Offer file** (if it exists) — `growthOS/voice/offers/{slug}.md`
   If present, it is ground truth: use its `Target Audience` (Primary/Secondary Persona, Pain Level, Awareness Level, Budget Sensitivity) and `Objections` table instead of guessing. If absent, fall back to the Default Persona Library below and say in the report that personas are generic archetypes, not calibrated to a documented ICP.
3. **Conversion psychology** — `growthOS/design-intelligence/theory/conversion-psychology.md`
   Source for every "why" — Cialdini's 6 principles, anchoring, loss aversion, framing, decoy effect, trust hierarchy, price psychology.
4. **Objection-handling patterns** — `growthOS/design-intelligence/references/patterns/objection-handling.md`
   Source for what "resolved" looks like — FAQ accordion, "But what if" cards, comparison table, guarantee section, risk-reversal banner — and where each belongs in scroll depth.

## Default Persona Library

Use these when no offer file exists, or to supplement documented personas with edge cases they didn't cover. Pick 3-5 relevant to the product; don't force all 5 if one clearly doesn't apply (e.g. skip "Enterprise Comparator" for a $27 ebook).

| Persona | Awareness Level | Primary Concern | Converts When | Repelled When |
|---|---|---|---|---|
| **The Skeptic** | Solution-aware | "Is this real or hype?" | Sees specific, checkable proof (named testimonials, data, credentials) | Vague claims, stock-photo testimonials, self-proclaimed authority |
| **The Impulse Buyer** | Product-aware | "Do I want this right now?" | Strong emotional hook + low friction + real urgency | Long page before any CTA, no emotional hook in hero |
| **The Price-Sensitive Comparator** | Most-aware | "Is this worth the money vs. alternatives?" | Value stack shown before price, real anchoring, clear vs.-alternative comparison | Price shown with no anchor, no comparison, no ROI framing |
| **The Distracted Scanner** | Problem-aware | Skims only headlines, bold text, CTAs, images | Scannable hierarchy carries the pitch on its own | Wall of text, weak headline hierarchy, CTA buried |
| **The Cautious Researcher** | Solution-aware | Reads everything, checks guarantee and FAQ before deciding | Every objection pre-empted, guarantee is specific and generous | Guarantee vague or missing, no FAQ, unanswered "what if" |

## Simulation Process

### Step 1: Map the page structure

Parse the built HTML into its actual sections (by headings/`<section>` boundaries — don't assume a fixed template). Note, in order: hero, social proof, features/benefits, objection-handling elements present (and which pattern from `objection-handling.md` they match, if any), pricing, guarantee, FAQ, final CTA. Note what's **missing** entirely.

### Step 2: Select personas

3-5 personas: from the offer file if it exists, otherwise from the Default Persona Library, chosen for relevance to the product/price point/audience.

### Step 3: Simulate each persona's read-through

For each persona, write a short first-person internal monologue as they scroll section by section. At each section note:
- What they notice or skip (per their attention pattern)
- Any objection that fires, quoting the specific psychological driver (cite the principle by name from `conversion-psychology.md`)
- Whether the page resolves it at that point or later, quoting the actual on-page copy that does (or doesn't) resolve it
- If unresolved and it's a dealbreaker for that persona: this is their **drop-off point** — stop the monologue there

### Step 4: Score each persona

- **Conversion likelihood:** Low / Medium / High
- **Drop-off point:** specific section name, or "reached final CTA" if none
- **Top unresolved objection:** one sentence
- **Evidence:** the exact page copy or missing element driving the score

### Step 5: Aggregate findings

- Overall predicted conversion outlook (e.g. "2 of 4 personas convert — MODERATE risk")
- Rank the top 3 fixes by expected impact across personas. Each fix must name:
  - Which persona(s) it unblocks
  - Which principle from `conversion-psychology.md` it applies
  - Which pattern from `objection-handling.md` to implement, and where (scroll depth / placement)

### Step 6: Write the report

Save an HTML report to `growthOS/output/sales-pages/{slug}/previews/persona-simulation.html` (create the `previews/` dir if needed). Match the visual language already used by the Sales Page Studio preview server (`sales-page-preview/server.py`): dark theme, `#09090B` background, `#FAFAFA` text, `#18181B` cards, `#27272A` borders, verdict badges (`#14532D`/`#4ADE80` good, `#422006`/`#FB923C` moderate, `#450A0A`/`#FCA5A5` poor). Structure:

```html
<!-- Header: aggregate verdict + summary counts -->
<!-- One card per persona: name, awareness level, monologue excerpt,
     drop-off point, conversion likelihood, top objection + resolved? -->
<!-- Top Fixes section: ranked, each citing principle + pattern + placement -->
```

This file is standalone — it is not one of the 8 numbered `PHASES` the preview server iterates over, so it won't appear in the pipeline UI automatically. It's viewable directly by path or `file://`.

**Do not** write to `state.json` or touch pipeline phase status. This skill is advisory, not gating.

### Step 7: Present results to the user

In chat, give:
- Aggregate verdict
- One line per persona (likelihood + drop-off point)
- Top 3 fixes, ranked
- Path to the full report

## Error Handling

| Situation | Action |
|---|---|
| Built page not found and no alternate path given | HALT — ask for the sales page HTML to analyze |
| No offer file for the slug | Proceed with Default Persona Library; note in report that personas are generic, not ICP-calibrated |
| Page has no objection-handling elements at all | Still simulate — this will surface as the #1 finding for every skeptical/cautious persona |
| `previews/` directory doesn't exist | Create it |

## Collaboration

| Skill/Agent | Interaction |
|---|---|
| **sales-page (master skill)** | Produces the built page this skill analyzes. Not invoked by it — run manually, after or independent of the pipeline. |
| **sales-page-qa** | Validates the page works and matches spec (mechanical). This skill predicts how it will be *received* (psychological). Complementary, not overlapping. |
| **voice/offers/{slug}.md** | Source of documented personas/objections when available — always prefer this over generic archetypes. |
