# Social Proof Layout Patterns — 6 Variants

> **Purpose:** Social proof is the #3 most powerful persuasion principle (Cialdini). These patterns define HOW to display proof for maximum trust transfer.
> **Rule:** Only use real proof. If no real proof exists, skip the section entirely. Fabricated social proof destroys trust permanently.

---

## 1. Logo Wall (Trusted-By)

**Description:** Horizontal row of grayscale client/partner logos. Minimal text. Logos do the talking.

**When to use:**
- When you have 4+ recognizable brand clients
- Immediately below the hero for instant credibility
- When brand association is your strongest proof

**Placement:** 3-5% scroll depth (immediately below hero)
**Conversion impact:** Logo walls increase landing page conversion by 10-15% when logos are recognizable (CXL, 2024).

```html
<section class="logo-wall" aria-label="Trusted by leading companies">
  <p class="logo-wall__label">Trusted by 2,400+ teams worldwide</p>
  <div class="logo-wall__grid">
    <img src="/logos/acme.svg" alt="Acme Corp" width="120" height="40" loading="lazy">
    <img src="/logos/globex.svg" alt="Globex" width="120" height="40" loading="lazy">
    <img src="/logos/initech.svg" alt="Initech" width="120" height="40" loading="lazy">
    <img src="/logos/massive.svg" alt="Massive Dynamic" width="120" height="40" loading="lazy">
    <img src="/logos/wayne.svg" alt="Wayne Enterprises" width="120" height="40" loading="lazy">
    <img src="/logos/stark.svg" alt="Stark Industries" width="120" height="40" loading="lazy">
  </div>
</section>
```

```css
.logo-wall {
  padding: 3rem 2rem;
  text-align: center;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.logo-wall__label {
  font-size: 0.875rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 2rem;
}

.logo-wall__grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 2.5rem 3rem;
  max-width: 900px;
  margin: 0 auto;
}

.logo-wall__grid img {
  opacity: 0.5;
  filter: grayscale(100%);
  transition: opacity 0.3s ease;
  height: 28px;
  width: auto;
}

.logo-wall__grid img:hover {
  opacity: 0.8;
}
```

**Rules:**
- 4-8 logos maximum (more = cluttered)
- Always grayscale (color logos compete with your brand)
- All logos same height (28-40px)
- Label above: "Trusted by [metric]" or "Used by teams at"

---

## 2. Testimonial Carousel / Grid

**Description:** Customer quotes with name, photo, role, and specific result. Can be displayed as a scrolling carousel or a static grid.

**When to use:**
- When you have 3+ strong testimonials with specific outcomes
- After features or how-it-works sections (validates claims)
- When individual stories are more compelling than aggregate metrics

**Placement:** 40-55% scroll depth (mid-page, after building the case)

```html
<section class="testimonials" aria-label="Customer testimonials">
  <h2>What our customers say</h2>
  <div class="testimonials__grid">
    <blockquote class="testimonial-card">
      <p class="testimonial-card__quote">"We cut our content production time by 60% in the first month. The ROI was immediate."</p>
      <footer class="testimonial-card__author">
        <img src="/avatars/sarah.webp" alt="" width="48" height="48" class="testimonial-card__avatar">
        <div>
          <cite class="testimonial-card__name">Sarah Chen</cite>
          <span class="testimonial-card__role">VP Marketing, Acme Corp</span>
        </div>
      </footer>
    </blockquote>
    <!-- Repeat for additional testimonials -->
  </div>
</section>
```

```css
.testimonials__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.testimonial-card {
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: var(--surface);
}

.testimonial-card__quote {
  font-size: 1.0625rem;
  line-height: 1.6;
  color: var(--text);
}

.testimonial-card__author {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.testimonial-card__avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.testimonial-card__name {
  display: block;
  font-weight: 600;
  font-style: normal;
}

.testimonial-card__role {
  display: block;
  font-size: 0.875rem;
  color: var(--muted);
}
```

**Rules:**
- Quotes must include a SPECIFIC result (number, metric, timeframe)
- Real name + real role + real company (anonymous quotes have near-zero trust impact)
- Photo if possible (increases trust by 35%)
- 3-6 testimonials displayed — more creates diminishing returns

---

## 3. Metric Counters

**Description:** Large animated numbers that count up on scroll — users, revenue, uptime, etc. Visual shorthand for scale and reliability.

**When to use:**
- When you have impressive quantitative metrics
- Hero section or logo bar position (instant credibility)
- When numbers are more compelling than individual stories

**Placement:** Hero section (0-5%) or as standalone section (30-40%)

```html
<section class="metrics" aria-label="Key metrics">
  <div class="metrics__grid">
    <div class="metric" data-target="14000" data-suffix="+">
      <span class="metric__number" aria-live="polite">14,000+</span>
      <span class="metric__label">Teams worldwide</span>
    </div>
    <div class="metric" data-target="99.9" data-suffix="%">
      <span class="metric__number">99.9%</span>
      <span class="metric__label">Uptime SLA</span>
    </div>
    <div class="metric" data-target="4.9" data-suffix="/5">
      <span class="metric__number">4.9/5</span>
      <span class="metric__label">Average rating</span>
    </div>
  </div>
</section>
```

```css
.metrics__grid {
  display: flex;
  justify-content: center;
  gap: 4rem;
  flex-wrap: wrap;
  padding: 4rem 2rem;
}

.metric {
  text-align: center;
}

.metric__number {
  display: block;
  font-size: clamp(2.5rem, 4vw, 4rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--text);
  font-variant-numeric: tabular-nums;
}

.metric__label {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.9375rem;
  color: var(--muted);
}
```

**Rules:**
- 3-4 metrics maximum (more = noise)
- Numbers must be REAL and CURRENT
- Use `font-variant-numeric: tabular-nums` to prevent layout shift during animation
- Counter animation only on first scroll into view (see scroll-animations.md #6)

---

## 4. Case Study Cards

**Description:** Mini case studies showing before/after results from specific customers. More depth than testimonials, less commitment than full case studies.

**When to use:**
- When you have documented customer results with data
- Solution-aware to product-aware audiences who need proof
- After features section to validate specific claims

**Placement:** 45-60% scroll depth

```html
<section class="case-studies" aria-label="Customer results">
  <h2>Real results from real teams</h2>
  <div class="case-studies__grid">
    <article class="case-card">
      <div class="case-card__header">
        <img src="/logos/acme.svg" alt="Acme Corp" class="case-card__logo">
        <span class="case-card__industry">E-commerce</span>
      </div>
      <div class="case-card__result">
        <span class="case-card__metric">+340%</span>
        <span class="case-card__metric-label">organic traffic growth</span>
      </div>
      <p class="case-card__summary">Acme went from 2,000 to 8,800 monthly organic visits in 90 days using our content engine.</p>
      <a href="#" class="case-card__link">Read full story →</a>
    </article>
    <!-- Repeat -->
  </div>
</section>
```

```css
.case-studies__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.case-card {
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: var(--surface);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.case-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.case-card__logo {
  height: 24px;
  opacity: 0.7;
}

.case-card__industry {
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.05);
  color: var(--muted);
}

.case-card__metric {
  display: block;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
}

.case-card__metric-label {
  display: block;
  font-size: 0.875rem;
  color: var(--muted);
  margin-top: 0.25rem;
}

.case-card__link {
  margin-top: auto;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--accent);
}
```

---

## 5. Star Ratings

**Description:** Aggregate review scores from third-party platforms (G2, Capterra, Trustpilot, App Store).

**When to use:**
- When you have strong ratings on recognized review platforms
- Near pricing (reduces purchase anxiety)
- When third-party validation matters more than individual testimonials

**Placement:** Near pricing section (70-80%) or hero sub-element (2-3%)

```html
<div class="rating-bar">
  <div class="rating-bar__platform">
    <img src="/badges/g2.svg" alt="G2" width="24" height="24">
    <div class="rating-bar__stars" aria-label="4.8 out of 5 stars">
      ★★★★★
    </div>
    <span class="rating-bar__score">4.8/5 on G2</span>
  </div>
  <div class="rating-bar__platform">
    <img src="/badges/capterra.svg" alt="Capterra" width="24" height="24">
    <div class="rating-bar__stars" aria-label="4.7 out of 5 stars">
      ★★★★★
    </div>
    <span class="rating-bar__score">4.7/5 on Capterra</span>
  </div>
</div>
```

```css
.rating-bar {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  justify-content: center;
  padding: 1.5rem;
}

.rating-bar__platform {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.rating-bar__stars {
  color: #f59e0b; /* amber-500 */
  font-size: 1rem;
  letter-spacing: 2px;
}

.rating-bar__score {
  font-size: 0.8125rem;
  color: var(--muted);
}
```

---

## 6. "As Seen In" (Media Mentions)

**Description:** Logos of publications or media outlets that have featured the product. Transfers authority from established media brands.

**When to use:**
- When you have genuine media coverage
- Authority-positioning brands
- B2B products where industry publications matter

**Placement:** Below hero (3-5%) or in authority section (25-30%)

```html
<section class="media-mentions" aria-label="Media coverage">
  <p class="media-mentions__label">As featured in</p>
  <div class="media-mentions__logos">
    <img src="/media/techcrunch.svg" alt="TechCrunch" width="140" height="28">
    <img src="/media/forbes.svg" alt="Forbes" width="100" height="28">
    <img src="/media/producthunt.svg" alt="Product Hunt" width="140" height="28">
  </div>
</section>
```

```css
.media-mentions {
  text-align: center;
  padding: 2.5rem 2rem;
}

.media-mentions__label {
  font-size: 0.8125rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 1.5rem;
}

.media-mentions__logos {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3rem;
  flex-wrap: wrap;
}

.media-mentions__logos img {
  height: 24px;
  width: auto;
  opacity: 0.4;
  filter: grayscale(100%);
}
```

**Rules:**
- Only logos the audience would recognize as authoritative
- Same grayscale treatment as logo wall
- "As featured in" or "As seen in" label
- Link to the actual article when possible
