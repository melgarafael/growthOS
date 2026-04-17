# Pricing Section Patterns — 5 Variants

> **Purpose:** The pricing section is where the buying decision happens. Layout, psychology, and copy must work together to make the price feel justified.
> **Rule:** Always show value BEFORE showing price. The first number the reader sees anchors all subsequent price evaluation (anchoring effect — conversion-psychology.md).

---

## 1. Comparison Table (3-Tier)

**Description:** Side-by-side tiers with feature comparison. The "recommended" tier is visually highlighted to guide the decision.

**When to use:**
- SaaS with distinct plan levels
- When feature differentiation justifies the tiers
- Solution-aware and product-aware audiences who are comparing

**Psychology:** Decoy effect + default effect. The middle tier is the target. The outer tiers exist to make it the obvious choice. Highlighting "recommended" increases selection of that tier by 22%.

```html
<section class="pricing-table" aria-label="Pricing plans">
  <h2>Choose your plan</h2>
  <p class="pricing-table__sub">Start free. Upgrade when you're ready.</p>

  <div class="pricing-table__toggle">
    <span>Monthly</span>
    <label class="toggle">
      <input type="checkbox" id="billing-toggle" checked>
      <span class="toggle__slider"></span>
    </label>
    <span>Annual <span class="pricing-table__savings">Save 20%</span></span>
  </div>

  <div class="pricing-table__grid">
    <!-- Tier 1: Basic -->
    <div class="pricing-card">
      <h3 class="pricing-card__name">Starter</h3>
      <p class="pricing-card__desc">For individuals getting started</p>
      <div class="pricing-card__price">
        <span class="pricing-card__amount" data-monthly="19" data-annual="15">$15</span>
        <span class="pricing-card__period">/month</span>
      </div>
      <a href="#" class="cta-ghost">Start free trial</a>
      <ul class="pricing-card__features">
        <li>1 user</li>
        <li>5 projects</li>
        <li>1GB storage</li>
        <li>Email support</li>
      </ul>
    </div>

    <!-- Tier 2: Recommended -->
    <div class="pricing-card pricing-card--recommended">
      <span class="pricing-card__badge">Most popular</span>
      <h3 class="pricing-card__name">Pro</h3>
      <p class="pricing-card__desc">For growing teams</p>
      <div class="pricing-card__price">
        <span class="pricing-card__amount" data-monthly="49" data-annual="39">$39</span>
        <span class="pricing-card__period">/month</span>
      </div>
      <a href="#" class="cta-primary">Start free trial</a>
      <ul class="pricing-card__features">
        <li>5 users</li>
        <li>Unlimited projects</li>
        <li>50GB storage</li>
        <li>Priority support</li>
        <li>API access</li>
        <li>Advanced analytics</li>
      </ul>
    </div>

    <!-- Tier 3: Enterprise -->
    <div class="pricing-card">
      <h3 class="pricing-card__name">Enterprise</h3>
      <p class="pricing-card__desc">For large organizations</p>
      <div class="pricing-card__price">
        <span class="pricing-card__amount">Custom</span>
      </div>
      <a href="#" class="cta-ghost">Contact sales</a>
      <ul class="pricing-card__features">
        <li>Unlimited users</li>
        <li>Unlimited everything</li>
        <li>Dedicated support</li>
        <li>SLA guarantee</li>
        <li>Custom integrations</li>
        <li>On-premise option</li>
      </ul>
    </div>
  </div>
</section>
```

```css
.pricing-table {
  text-align: center;
  padding: 6rem 2rem;
}

.pricing-table__toggle {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  margin: 2rem auto;
  font-size: 0.9375rem;
}

.pricing-table__savings {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 100px;
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
  font-size: 0.75rem;
  font-weight: 600;
}

.toggle {
  position: relative;
  width: 44px;
  height: 24px;
}

.toggle input { opacity: 0; width: 0; height: 0; }

.toggle__slider {
  position: absolute;
  inset: 0;
  background: var(--muted);
  border-radius: 12px;
  cursor: pointer;
  transition: 0.3s;
}

.toggle__slider::before {
  content: '';
  position: absolute;
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: 0.3s;
}

.toggle input:checked + .toggle__slider {
  background: var(--accent);
}

.toggle input:checked + .toggle__slider::before {
  transform: translateX(20px);
}

.pricing-table__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  max-width: 1100px;
  margin: 3rem auto 0;
  align-items: start;
}

.pricing-card {
  padding: 2.5rem 2rem;
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  text-align: left;
}

.pricing-card--recommended {
  position: relative;
  border-color: var(--accent);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  transform: scale(1.02);
}

.pricing-card__badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  padding: 4px 16px;
  border-radius: 100px;
  background: var(--accent);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.pricing-card__amount {
  font-size: 3rem;
  font-weight: 700;
  letter-spacing: -0.03em;
}

.pricing-card__period {
  font-size: 1rem;
  color: var(--muted);
}

.pricing-card__features {
  list-style: none;
  padding: 0;
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.pricing-card__features li::before {
  content: '✓ ';
  color: var(--accent);
  font-weight: 600;
}

@media (max-width: 768px) {
  .pricing-table__grid {
    grid-template-columns: 1fr;
    max-width: 400px;
  }
  .pricing-card--recommended {
    transform: none;
    order: -1; /* Show recommended first on mobile */
  }
}
```

---

## 2. Single Plan Spotlight

**Description:** One plan, one price, no choice paralysis. Maximum clarity for products with a single offering.

**When to use:**
- Products with one pricing tier
- Courses, coaching, communities
- High-ticket offers where the price needs full context
- When the paradox of choice would hurt conversion

**Psychology:** Hick's Law — one option = instant decision. No comparison anxiety.

```html
<section class="pricing-spotlight">
  <h2>Simple pricing, no surprises</h2>
  <div class="pricing-spotlight__card">
    <div class="pricing-spotlight__header">
      <span class="pricing-spotlight__name">Full Access</span>
      <div class="pricing-spotlight__price">
        <span class="pricing-spotlight__amount">$97</span>
        <span class="pricing-spotlight__period">/month</span>
      </div>
      <p class="pricing-spotlight__desc">Everything you need to grow. Cancel anytime.</p>
    </div>
    <ul class="pricing-spotlight__features">
      <li>Unlimited projects</li>
      <li>All integrations</li>
      <li>Priority support</li>
      <li>Team collaboration</li>
      <li>Advanced analytics</li>
      <li>API access</li>
    </ul>
    <a href="#" class="cta-primary" style="width: 100%;">Get started — 14 days free</a>
    <p class="pricing-spotlight__micro">No credit card required. Cancel anytime.</p>
  </div>
</section>
```

```css
.pricing-spotlight {
  text-align: center;
  padding: 6rem 2rem;
}

.pricing-spotlight__card {
  max-width: 480px;
  margin: 3rem auto 0;
  padding: 3rem;
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: var(--surface);
  text-align: left;
}

.pricing-spotlight__amount {
  font-size: 4rem;
  font-weight: 700;
  letter-spacing: -0.04em;
}

.pricing-spotlight__micro {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.8125rem;
  color: var(--muted);
}
```

---

## 3. Toggle Pricing (Monthly vs Annual)

**Description:** Switch between billing periods with a savings badge highlighting the annual discount.

**When to use:** SaaS products offering both monthly and annual billing. Annual-plan uptake increases 25-35% when a toggle is present.

**Psychology:** Default effect — pre-selecting annual makes it the default choice. Loss aversion — the "Save 20%" badge frames monthly as "losing" savings.

Toggle implementation is included in the Comparison Table pattern above. Key CSS for the savings badge:

```css
.pricing-table__savings {
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
  padding: 2px 8px;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 600;
}
```

**Rules:**
- Default to annual (pre-selected)
- Show savings as percentage AND absolute ("Save 20% — $96/year")
- Animation between prices should be smooth, not jarring
- Monthly price should still be visible (not hidden) to maintain trust

---

## 4. Enterprise CTA

**Description:** For high-ticket products where the price is custom/negotiable. No public pricing — instead, a "Contact sales" flow.

**When to use:**
- Enterprise-tier SaaS
- Custom services, consulting packages
- Products >$10K/year where pricing is complex
- When usage-based pricing makes a flat number misleading

```html
<div class="pricing-enterprise">
  <h3>Enterprise</h3>
  <p>Custom solutions for large teams</p>
  <div class="pricing-enterprise__features">
    <span>Unlimited users</span>
    <span>Custom SLA</span>
    <span>Dedicated support</span>
    <span>On-premise option</span>
  </div>
  <a href="#" class="cta-ghost">Talk to sales →</a>
</div>
```

```css
.pricing-enterprise {
  padding: 2.5rem;
  border-radius: 16px;
  background: linear-gradient(135deg, #0a0a0a, #1a1a2e);
  color: #fff;
}

.pricing-enterprise__features {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin: 1.5rem 0;
}

.pricing-enterprise__features span {
  padding: 4px 12px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.08);
  font-size: 0.875rem;
}
```

**Copy rule:** Never use "Contact us" (passive). Use "Talk to sales" or "Schedule a demo" (active, sets expectation).

---

## 5. Value Stack

**Description:** List every component of the offer with its individual value, then reveal the total value, then reveal the actual price. The gap between value and price creates perceived deal.

**When to use:**
- Courses, bundles, information products
- High-ticket offers where justifying the price is critical
- Audiences in the Problem-Aware to Solution-Aware range (need convincing)
- PAS and Story Bridge frameworks

**Psychology:** Anchoring effect — the total value number (highest) becomes the reference point. The actual price feels like a fraction of the value.

```html
<section class="value-stack">
  <h2>Everything you get</h2>
  <div class="value-stack__items">
    <div class="value-stack__item">
      <span class="value-stack__name">Complete Course Library (47 lessons)</span>
      <span class="value-stack__value">R$ 2.970</span>
    </div>
    <div class="value-stack__item">
      <span class="value-stack__name">Private Community Access (12 months)</span>
      <span class="value-stack__value">R$ 1.200</span>
    </div>
    <div class="value-stack__item">
      <span class="value-stack__name">Monthly Live Q&A Sessions</span>
      <span class="value-stack__value">R$ 600</span>
    </div>
    <div class="value-stack__item">
      <span class="value-stack__name">Template Pack (47 templates)</span>
      <span class="value-stack__value">R$ 497</span>
    </div>
    <div class="value-stack__divider"></div>
    <div class="value-stack__total">
      <span>Total Value</span>
      <span class="value-stack__total-amount">R$ 5.267</span>
    </div>
  </div>

  <div class="value-stack__price">
    <p class="value-stack__label">Your investment today</p>
    <span class="value-stack__actual">R$ 997</span>
    <p class="value-stack__installments">or 12x R$ 97</p>
  </div>

  <a href="#" class="cta-primary" style="width: 100%;">Quero começar agora</a>
  <p class="value-stack__guarantee">30 dias de garantia incondicional</p>
</section>
```

```css
.value-stack {
  max-width: 560px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.value-stack__items {
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  overflow: hidden;
}

.value-stack__item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.value-stack__value {
  font-weight: 500;
  color: var(--muted);
  text-decoration: line-through;
  font-size: 0.9375rem;
}

.value-stack__divider {
  height: 2px;
  background: var(--accent);
}

.value-stack__total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  font-weight: 600;
}

.value-stack__total-amount {
  font-size: 1.25rem;
  text-decoration: line-through;
  color: var(--muted);
}

.value-stack__price {
  text-align: center;
  padding: 3rem 0 2rem;
}

.value-stack__label {
  font-size: 0.9375rem;
  color: var(--muted);
  margin-bottom: 0.5rem;
}

.value-stack__actual {
  display: block;
  font-size: 4rem;
  font-weight: 700;
  letter-spacing: -0.04em;
  color: var(--accent);
}

.value-stack__installments {
  font-size: 1rem;
  color: var(--muted);
  margin-top: 0.25rem;
}

.value-stack__guarantee {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.8125rem;
  color: var(--muted);
}
```

**Rules:**
- Individual values must be defensible (not inflated 10x)
- Strikethrough on individual values, NOT on the actual price
- Actual price is highlighted in accent color
- Guarantee text immediately below CTA
- Installment option always shown when available
