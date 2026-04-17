# CTA Patterns — 7 Variants

> **Purpose:** CTAs are the conversion mechanism. Copy, design, and placement must work together. Every CTA on a sales page must follow one of these patterns.
> **Rule:** CTA copy follows the `Action Verb + Outcome` formula. Never "Submit", "Click Here", or "Learn More".

---

## 1. Primary CTA Button

**Description:** High-contrast, bold button. The main conversion action on the page. Only ONE style for primary CTA — consistency trains the user's eye.

**When to use:** Hero section, after value demonstration, final section. Minimum 3 per page.

**Copy formula:** `[Action Verb] + [Outcome]`
Examples: "Start building", "Get your free report", "Launch your first campaign"

```html
<a href="#" class="cta-primary">
  Start your free trial
</a>
```

```css
.cta-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 32px;
  min-height: 48px;
  border-radius: 8px;
  background: var(--accent);
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
}

.cta-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.cta-primary:active {
  transform: translateY(0);
}

/* Focus state for accessibility */
.cta-primary:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

@media (max-width: 768px) {
  .cta-primary {
    width: 100%;
    min-height: 52px;
    font-size: 1.0625rem;
  }
}
```

**A/B test insight:** Button copy that includes the outcome ("Start shipping faster") outperforms generic action ("Get started") by 15-25%.

---

## 2. Ghost CTA (Secondary)

**Description:** Outline/transparent button for secondary actions. Visually subordinate to primary CTA.

**When to use:** Next to a primary CTA when there's a secondary path ("Watch demo", "See pricing", "Contact sales").

```html
<div class="cta-group">
  <a href="#" class="cta-primary">Start free trial</a>
  <a href="#" class="cta-ghost">Watch a demo</a>
</div>
```

```css
.cta-ghost {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 32px;
  min-height: 48px;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.15);
  background: transparent;
  color: var(--text);
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.cta-ghost:hover {
  background: rgba(0, 0, 0, 0.04);
  border-color: rgba(0, 0, 0, 0.25);
}

/* Dark mode variant */
[data-theme="dark"] .cta-ghost {
  border-color: rgba(255, 255, 255, 0.15);
  color: #fff;
}

[data-theme="dark"] .cta-ghost:hover {
  background: rgba(255, 255, 255, 0.06);
}

.cta-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
```

**Rule:** Ghost CTA must NEVER visually compete with primary. It's always lower contrast, lighter weight, no fill.

---

## 3. Sticky CTA

**Description:** CTA fixed at the bottom of the viewport, appearing after the user scrolls past the hero. Ensures the CTA is always reachable.

**When to use:** Long sales pages (8+ sections). Mobile-first pages. When scroll depth data shows users read far but don't scroll back up to convert.

```html
<div class="cta-sticky" id="sticky-cta" aria-label="Purchase action">
  <div class="cta-sticky__inner">
    <span class="cta-sticky__text">Ready to start?</span>
    <a href="#" class="cta-primary cta-primary--compact">Get started — Free</a>
  </div>
</div>
```

```css
.cta-sticky {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding: 12px 16px;
  transform: translateY(100%);
  transition: transform 0.3s ease;
}

.cta-sticky--visible {
  transform: translateY(0);
}

.cta-sticky__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
}

.cta-sticky__text {
  font-size: 0.9375rem;
  font-weight: 500;
}

/* Hide on desktop if desired (mobile-first pattern) */
@media (min-width: 1024px) {
  .cta-sticky { display: none; }
}
```

```javascript
// Show sticky CTA after scrolling past hero
const stickyCta = document.getElementById('sticky-cta');
const hero = document.querySelector('.hero');

const observer = new IntersectionObserver(([entry]) => {
  stickyCta.classList.toggle('cta-sticky--visible', !entry.isIntersecting);
}, { threshold: 0 });

observer.observe(hero);
```

---

## 4. CTA with Micro-Copy

**Description:** Primary button with supporting text underneath — objection handler, trust signal, or friction reducer.

**When to use:** ALWAYS for primary conversion CTAs. Micro-copy addresses the "but what if..." that stops clicks.

```html
<div class="cta-with-micro">
  <a href="#" class="cta-primary">Start your free trial</a>
  <p class="cta-micro">No credit card required. Setup takes 3 minutes.</p>
</div>
```

```css
.cta-with-micro {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.cta-micro {
  font-size: 0.8125rem;
  color: var(--muted);
}
```

**Micro-copy patterns:**

| Objection | Micro-copy |
|-----------|-----------|
| "Is it free?" | "Free forever. No credit card needed." |
| "Is it complicated?" | "Setup takes 3 minutes." |
| "Can I cancel?" | "Cancel anytime. No lock-in." |
| "Is it safe?" | "256-bit encryption. SOC 2 certified." |
| "What if I don't like it?" | "30-day money-back guarantee." |

---

## 5. CTA with Social Proof

**Description:** CTA button with a social proof element directly adjacent — user count, avatars, or rating.

**When to use:** When social proof is your strongest asset. Hero sections. Pricing sections.

```html
<div class="cta-with-proof">
  <a href="#" class="cta-primary">Join 10,000+ teams</a>
  <div class="cta-proof">
    <div class="cta-proof__avatars">
      <img src="/avatars/1.webp" alt="" width="32" height="32">
      <img src="/avatars/2.webp" alt="" width="32" height="32">
      <img src="/avatars/3.webp" alt="" width="32" height="32">
      <img src="/avatars/4.webp" alt="" width="32" height="32">
      <span class="cta-proof__count">+10K</span>
    </div>
    <div class="cta-proof__rating">
      <span class="cta-proof__stars">★★★★★</span>
      <span>4.8/5 from 2,400 reviews</span>
    </div>
  </div>
</div>
```

```css
.cta-with-proof {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.cta-proof__avatars {
  display: flex;
  align-items: center;
}

.cta-proof__avatars img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid var(--bg);
  margin-left: -8px;
}

.cta-proof__avatars img:first-child {
  margin-left: 0;
}

.cta-proof__count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-size: 0.6875rem;
  font-weight: 600;
  margin-left: -8px;
}

.cta-proof__rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: var(--muted);
}

.cta-proof__stars {
  color: #f59e0b;
  letter-spacing: 1px;
}
```

---

## 6. Exit-Intent CTA

**Description:** Overlay or banner triggered when the user moves to leave the page (cursor toward browser chrome on desktop, rapid scroll-up on mobile).

**When to use:** CAREFULLY. Exit-intent popups have high conversion but can annoy users. Use only when:
- Offering genuine additional value (discount, free resource)
- Frequency-capped (once per session)
- Easy to dismiss

**Not recommended for:** Premium brands, authority positioning, developer audiences (they hate popups).

```html
<div class="exit-modal" id="exit-modal" role="dialog" aria-label="Special offer" hidden>
  <div class="exit-modal__backdrop"></div>
  <div class="exit-modal__content">
    <button class="exit-modal__close" aria-label="Close">&times;</button>
    <h3>Wait — here's 15% off your first month</h3>
    <p>Use code <strong>WELCOME15</strong> at checkout.</p>
    <a href="#" class="cta-primary">Claim your discount</a>
    <button class="exit-modal__dismiss">No thanks, I'll pay full price</button>
  </div>
</div>
```

```css
.exit-modal__backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 100;
}

.exit-modal__content {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 101;
  background: var(--bg);
  padding: 3rem;
  border-radius: 16px;
  max-width: 480px;
  text-align: center;
}

.exit-modal__close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--muted);
}

.exit-modal__dismiss {
  display: block;
  margin: 1rem auto 0;
  background: none;
  border: none;
  color: var(--muted);
  font-size: 0.8125rem;
  cursor: pointer;
  text-decoration: underline;
}
```

**Rules:**
- Show once per session only (use `sessionStorage`)
- Must be easily dismissible (close button + backdrop click + Escape key)
- The offer must be GENUINE (real discount, real resource)
- "No thanks" dismissal must NOT guilt-trip ("No, I don't want to grow my business" = manipulative)

---

## 7. Negative-Space CTA (Stripe-style)

**Description:** Small, understated CTA button surrounded by generous whitespace. The emptiness draws the eye. Confidence through restraint.

**When to use:** Premium positioning. After a powerful statement or proof section. When you want the CTA to feel like an invitation, not a demand.

```html
<section class="cta-negative-space">
  <p class="cta-negative-space__text">Ready to see the difference?</p>
  <a href="#" class="cta-negative-space__button">Get started →</a>
</section>
```

```css
.cta-negative-space {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8rem 2rem;
  text-align: center;
}

.cta-negative-space__text {
  font-size: 1.125rem;
  color: var(--muted);
  margin-bottom: 2rem;
}

.cta-negative-space__button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border-radius: 6px;
  background: transparent;
  border: 1px solid rgba(0, 0, 0, 0.12);
  color: var(--text);
  font-size: 0.9375rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.cta-negative-space__button:hover {
  background: var(--text);
  color: var(--bg);
  border-color: var(--text);
}
```

**Rule:** The whitespace IS the design. Minimum 8rem vertical padding. No competing elements within the section. The button is small and subtle — the emptiness makes it the focal point.

---

## CTA Placement Strategy

```
0%    ┌─ Hero CTA ──────────────────────────┐ (primary, always)
      │                                      │
25%   │                                      │
      │  (No CTA needed in features section) │
35%   │                                      │
      ├─ Mid-page CTA ─────────────────────┤ (after proof/how-it-works)
      │                                      │
55%   │                                      │
      │                                      │
70%   ├─ Pricing CTA ──────────────────────┤ (inside pricing section)
      │                                      │
85%   ├─ Final CTA ────────────────────────┤ (closing argument)
      │                                      │
100%  └─────────────────────────────────────┘

RULE: Never more than 2 full viewport-heights between CTAs.
```
