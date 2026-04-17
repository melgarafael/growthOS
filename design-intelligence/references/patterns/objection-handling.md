# Objection Handling Patterns — 5 Variants

> **Purpose:** Objections are the reasons people DON'T buy. These patterns handle objections within the page structure, not just at the bottom in a FAQ dump.
> **Rule:** Objections from Phase 1 `objections[]` must be addressed BEFORE the pricing section. By the time the reader sees the price, their doubts should already be resolved.

---

## 1. FAQ Accordion

**Description:** Expandable question/answer pairs. The most familiar objection-handling format. Includes schema.org markup for SEO.

**When to use:**
- Bottom of page (80-92% scroll depth) for remaining questions
- When you have 5-8 common questions
- When questions are diverse (not all about the same concern)
- Standard in ALL frameworks — every page should have one

**Placement:** After pricing, before final CTA

```html
<section class="faq" aria-label="Frequently asked questions">
  <h2>Questions you might have</h2>

  <div class="faq__list" itemscope itemtype="https://schema.org/FAQPage">
    <details class="faq__item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
      <summary class="faq__question" itemprop="name">
        Can I cancel anytime?
      </summary>
      <div class="faq__answer" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
        <p itemprop="text">Yes. Cancel with one click from your dashboard. No penalties, no questions asked. If you cancel mid-cycle, you keep access until the end of your billing period.</p>
      </div>
    </details>

    <details class="faq__item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
      <summary class="faq__question" itemprop="name">
        Do I need technical skills?
      </summary>
      <div class="faq__answer" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
        <p itemprop="text">No. Our interface is designed for non-technical users. 80% of our customers have zero coding experience. Setup takes 3 minutes with our guided wizard.</p>
      </div>
    </details>

    <!-- Add 3-6 more items -->
  </div>
</section>
```

```css
.faq {
  max-width: 720px;
  margin: 0 auto;
  padding: 6rem 2rem;
}

.faq__list {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-top: 3rem;
}

.faq__item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.faq__question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 0;
  font-size: 1.0625rem;
  font-weight: 500;
  cursor: pointer;
  list-style: none;
}

.faq__question::after {
  content: '+';
  font-size: 1.5rem;
  font-weight: 300;
  color: var(--muted);
  transition: transform 0.2s ease;
}

.faq__item[open] .faq__question::after {
  content: '−';
}

/* Remove default marker */
.faq__question::-webkit-details-marker { display: none; }

.faq__answer {
  padding: 0 0 1.25rem;
  font-size: 1rem;
  line-height: 1.6;
  color: var(--muted);
  max-width: 90%;
}
```

**Copy rules:**
- Write questions in the AUDIENCE's voice: "Can I cancel?" not "What is the cancellation policy?"
- Answers must be specific: "3 minutes" not "quickly", "80% of customers" not "most people"
- First sentence answers the question directly. Supporting details follow.
- 5-8 questions maximum. More = the page isn't doing its job earlier.

---

## 2. "But What If..." Cards

**Description:** Objection → response pairs presented as cards. More conversational than FAQ. Directly names the doubt and addresses it.

**When to use:**
- Mid-page (55-70% scroll depth) before pricing
- When objections are emotional (fear, doubt, skepticism)
- PAS and Story Bridge frameworks
- When you want to feel empathetic, not corporate

**Placement:** After social proof, before pricing

```html
<section class="objection-cards" aria-label="Common concerns">
  <h2>You might be thinking...</h2>

  <div class="objection-cards__grid">
    <div class="objection-card">
      <p class="objection-card__doubt">"I've tried tools like this before and they didn't work."</p>
      <p class="objection-card__response">We hear that a lot. That's why we offer a 30-day free trial with full features — no credit card, no commitment. See the difference yourself. If it doesn't work, you've lost nothing.</p>
    </div>

    <div class="objection-card">
      <p class="objection-card__doubt">"My team won't adopt another tool."</p>
      <p class="objection-card__response">Average onboarding time is 4 minutes. We integrate with the tools your team already uses (Slack, Notion, Jira). Teams tell us adoption happens naturally because it reduces their workload instead of adding to it.</p>
    </div>

    <div class="objection-card">
      <p class="objection-card__doubt">"It's too expensive for what we need right now."</p>
      <p class="objection-card__response">Our starter plan is $19/month — less than a team lunch. Calculate what 15 hours/week of manual work costs your team, and the ROI becomes clear in the first week.</p>
    </div>
  </div>
</section>
```

```css
.objection-cards {
  padding: 6rem 2rem;
}

.objection-cards__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  max-width: 1100px;
  margin: 3rem auto 0;
}

.objection-card {
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: var(--surface);
}

.objection-card__doubt {
  font-size: 1.125rem;
  font-weight: 600;
  font-style: italic;
  color: var(--text);
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.objection-card__response {
  font-size: 0.9375rem;
  line-height: 1.65;
  color: var(--muted);
}
```

**Copy pattern: Acknowledge → Reframe → Evidence**
1. "We hear that a lot" (acknowledge — validate the concern)
2. "That's why we..." (reframe — turn the objection into a feature)
3. "Teams tell us..." (evidence — proof the reframe is real)

---

## 3. Comparison Table (You vs. Alternatives)

**Description:** Side-by-side comparison of your product against alternatives (competitors, DIY, or doing nothing).

**When to use:**
- Solution-aware audiences who are actively comparing
- AIDA framework
- When your product has clear, demonstrable advantages
- When competitors are well-known

**Placement:** 50-65% scroll depth, in or near the features section

```html
<section class="comparison" aria-label="Product comparison">
  <h2>Why teams choose us over alternatives</h2>

  <div class="comparison__table" role="table">
    <div class="comparison__header" role="row">
      <div role="columnheader">Feature</div>
      <div role="columnheader" class="comparison__ours">Us</div>
      <div role="columnheader">Competitor A</div>
      <div role="columnheader">DIY / Manual</div>
    </div>

    <div class="comparison__row" role="row">
      <div role="cell">Setup time</div>
      <div role="cell" class="comparison__ours">3 minutes</div>
      <div role="cell">2-3 hours</div>
      <div role="cell">Days/weeks</div>
    </div>

    <div class="comparison__row" role="row">
      <div role="cell">Monthly cost</div>
      <div role="cell" class="comparison__ours">$49/mo</div>
      <div role="cell">$129/mo</div>
      <div role="cell">$2,000+ (staff time)</div>
    </div>

    <div class="comparison__row" role="row">
      <div role="cell">AI-powered</div>
      <div role="cell" class="comparison__ours">✓</div>
      <div role="cell">Partial</div>
      <div role="cell">✗</div>
    </div>

    <div class="comparison__row" role="row">
      <div role="cell">Support</div>
      <div role="cell" class="comparison__ours">Priority (< 2hr)</div>
      <div role="cell">Email only</div>
      <div role="cell">N/A</div>
    </div>
  </div>
</section>
```

```css
.comparison {
  padding: 6rem 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.comparison__table {
  margin-top: 3rem;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  overflow: hidden;
}

.comparison__header {
  display: grid;
  grid-template-columns: 1.5fr repeat(3, 1fr);
  background: rgba(0, 0, 0, 0.03);
  font-weight: 600;
  font-size: 0.875rem;
}

.comparison__row {
  display: grid;
  grid-template-columns: 1.5fr repeat(3, 1fr);
  border-top: 1px solid rgba(0, 0, 0, 0.04);
}

.comparison__header > div,
.comparison__row > div {
  padding: 1rem 1.25rem;
  font-size: 0.9375rem;
}

.comparison__ours {
  background: rgba(59, 130, 246, 0.04);
  font-weight: 600;
  color: var(--accent);
}

@media (max-width: 640px) {
  .comparison__header,
  .comparison__row {
    grid-template-columns: 1.2fr repeat(3, 1fr);
    font-size: 0.8125rem;
  }

  .comparison__header > div,
  .comparison__row > div {
    padding: 0.75rem;
  }
}
```

**Rules:**
- Never mention competitors by name directly (legal risk). Use "Competitor A" or the category ("typical CRM").
- Use SPECIFIC comparisons, not vague claims: "3 minutes" vs "2-3 hours", not "faster" vs "slower"
- The "DIY / Manual" column is powerful — it shows the true cost of not using any tool
- Your column should win clearly on the dimensions that matter most to your audience

---

## 4. Guarantee Section

**Description:** Bold guarantee statement with a visual trust badge. Reverses the risk from buyer to seller.

**When to use:** ALWAYS. Every sales page should have a guarantee section, even if the guarantee is limited.

**Placement:** Near pricing (75-88% scroll depth), immediately after or below the pricing section

```html
<section class="guarantee" aria-label="Our guarantee">
  <div class="guarantee__badge" aria-hidden="true">
    <svg viewBox="0 0 80 80" width="80" height="80">
      <circle cx="40" cy="40" r="38" fill="none" stroke="currentColor" stroke-width="2"/>
      <text x="40" y="35" text-anchor="middle" font-size="18" font-weight="700" fill="currentColor">30</text>
      <text x="40" y="52" text-anchor="middle" font-size="10" fill="currentColor">DAYS</text>
    </svg>
  </div>
  <h2>30-Day Money-Back Guarantee</h2>
  <p>Try it risk-free for 30 days. If you're not completely satisfied, email us and we'll refund every cent. No questions asked, no hoops to jump through. We believe in what we built — and we want you to experience it without risk.</p>
</section>
```

```css
.guarantee {
  text-align: center;
  padding: 5rem 2rem;
  max-width: 640px;
  margin: 0 auto;
}

.guarantee__badge {
  color: var(--accent);
  margin-bottom: 1.5rem;
}

.guarantee h2 {
  font-size: clamp(1.5rem, 2.5vw, 2rem);
  font-weight: 700;
}

.guarantee p {
  margin-top: 1rem;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--muted);
}
```

**Copy rules:**
- Name the guarantee specifically: "30 days", "60 days", "lifetime"
- State the process: "email us" or "click one button"
- Use confident language: "We'll refund every cent" not "We may offer a refund"
- NO fine print that contradicts the headline guarantee
- The guarantee copy should feel GENEROUS, not legal

---

## 5. Risk-Reversal Banner

**Description:** A focused banner strip that communicates zero risk in one visual line. Compact version of the guarantee for placement near CTAs.

**When to use:**
- Near every primary CTA (especially pricing and final CTA)
- As micro-copy enhancement
- When the full guarantee section is elsewhere but you need a reminder

**Placement:** Directly below CTA buttons, or as a strip between pricing and final CTA

```html
<div class="risk-banner" role="note">
  <div class="risk-banner__items">
    <span class="risk-banner__item">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0a8 8 0 100 16A8 8 0 008 0zm3.5 5.3l-4 5a.75.75 0 01-1.1.1l-2-2a.75.75 0 011.1-1l1.4 1.3 3.4-4.4a.75.75 0 011.2 1z"/></svg>
      30-day money-back guarantee
    </span>
    <span class="risk-banner__item">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0a8 8 0 100 16A8 8 0 008 0zm3.5 5.3l-4 5a.75.75 0 01-1.1.1l-2-2a.75.75 0 011.1-1l1.4 1.3 3.4-4.4a.75.75 0 011.2 1z"/></svg>
      Cancel anytime
    </span>
    <span class="risk-banner__item">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0a8 8 0 100 16A8 8 0 008 0zm3.5 5.3l-4 5a.75.75 0 01-1.1.1l-2-2a.75.75 0 011.1-1l1.4 1.3 3.4-4.4a.75.75 0 011.2 1z"/></svg>
      No credit card required
    </span>
  </div>
</div>
```

```css
.risk-banner {
  padding: 1.5rem 2rem;
  text-align: center;
}

.risk-banner__items {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.risk-banner__item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8125rem;
  color: var(--muted);
}

.risk-banner__item svg {
  color: #22c55e;
  flex-shrink: 0;
}
```

**Placement strategy:**
```
┌── CTA Button ──────────────┐
│   Start your free trial     │
└─────────────────────────────┘
✓ 30-day guarantee  ✓ Cancel anytime  ✓ No credit card

This pattern should appear below EVERY primary CTA on the page.
```

---

## Objection Handling Placement by Framework

| Framework | Where Objections Live | Patterns Used |
|-----------|----------------------|---------------|
| **AIDA** | FAQ at bottom + risk banners near CTAs | #1 + #5 |
| **PAS** | "But what if..." cards before pricing + FAQ | #2 + #1 + #5 |
| **Story Bridge** | Woven into failure-stakes section + FAQ | #2 + #4 + #1 |
| **Ogilvy Direct** | Addressed in long-form copy + guarantee | #4 + #5 |

**The golden rule:** Objections must be RESOLVED before the reader sees the price. Place the heaviest objection-handling between social proof and pricing. FAQ at the bottom catches the stragglers.
