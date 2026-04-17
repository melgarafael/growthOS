# Hero Section Patterns — 8 Variants

> **Purpose:** The hero is the single most important section on any sales page. 50ms to make a first impression. This file defines 8 proven patterns with code, when-to-use rules, and psychological backing.
> **Rule:** Every hero must be chosen from these patterns. Hybrid combinations are allowed when justified.

---

## 1. Gradient Hero (Stripe-style)

**Description:** Mesh or radial gradient background with clean typography floating over it. No images. The gradient IS the visual.

**When to use:**
- SaaS, tech, fintech products
- When you don't have product screenshots yet
- When the brand identity IS the color language
- Clean, modern positioning

**Psychological principle:** Gradients signal innovation and dynamism (color-psychology.md). Mesh gradients specifically signal technical sophistication.

**Example site:** Stripe, Vercel, Supabase

```html
<section class="hero-gradient">
  <div class="hero-gradient__bg" aria-hidden="true"></div>
  <div class="hero-gradient__content">
    <h1 class="hero-gradient__headline">Financial infrastructure for the internet</h1>
    <p class="hero-gradient__sub">Millions of companies use Stripe to accept payments, grow revenue, and accelerate new business opportunities.</p>
    <div class="hero-gradient__actions">
      <a href="#" class="btn btn--primary">Start now</a>
      <a href="#" class="btn btn--ghost">Contact sales</a>
    </div>
  </div>
</section>
```

```css
.hero-gradient {
  position: relative;
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-gradient__bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(120, 80, 255, 0.4) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(255, 100, 80, 0.3) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 80%, rgba(80, 200, 255, 0.3) 0%, transparent 50%);
  background-color: #0a0a0a;
  filter: blur(80px);
  animation: gradient-shift 12s ease-in-out infinite alternate;
}

@keyframes gradient-shift {
  to { transform: rotate(3deg) scale(1.1); }
}

.hero-gradient__content {
  position: relative;
  z-index: 1;
  max-width: 720px;
  text-align: center;
  padding: 2rem;
}

.hero-gradient__headline {
  font-size: clamp(2.5rem, 5vw + 1rem, 4.5rem);
  font-weight: 700;
  line-height: 1.1;
  color: #fff;
  letter-spacing: -0.03em;
}

.hero-gradient__sub {
  margin-top: 1.5rem;
  font-size: clamp(1rem, 1.2vw + 0.5rem, 1.25rem);
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.7);
  max-width: 540px;
  margin-inline: auto;
}

.hero-gradient__actions {
  margin-top: 2.5rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}
```

---

## 2. Video Background Hero (Arc-style)

**Description:** Looping ambient video behind text. Video is atmospheric, not informational — it sets a mood.

**When to use:**
- Products where motion conveys the experience
- Browser/app products with fluid interfaces
- Cinematic brand positioning
- When video assets are available

**Psychological principle:** Motion captures attention (pre-attentive processing). Video backgrounds signal production value and premium quality.

**Example site:** Arc Browser, Loom

```html
<section class="hero-video">
  <video class="hero-video__bg" autoplay loop muted playsinline
         preload="metadata" poster="/assets/hero-poster.webp">
    <source src="/assets/hero.mp4" type="video/mp4">
  </video>
  <div class="hero-video__overlay" aria-hidden="true"></div>
  <div class="hero-video__content">
    <h1>The internet, reimagined</h1>
    <p>Arc is the Chrome replacement you didn't know you needed.</p>
    <a href="#" class="btn btn--primary">Download for free</a>
  </div>
</section>
```

```css
.hero-video {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-video__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-video__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.6) 0%,
    rgba(0, 0, 0, 0.3) 50%,
    rgba(0, 0, 0, 0.7) 100%
  );
}

.hero-video__content {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 640px;
  padding: 2rem;
  color: #fff;
}

/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .hero-video__bg {
    display: none;
  }
  .hero-video {
    background: url('/assets/hero-poster.webp') center/cover no-repeat;
  }
}
```

**Performance notes:**
- Video must be <5MB (aim for 2-3MB at 1080p)
- Always include `poster` attribute for LCP
- Always include `prefers-reduced-motion` fallback
- Use `preload="metadata"` to avoid blocking page load

---

## 3. Canvas Animation Hero (Apple-style)

**Description:** Frame sequence animation tied to scroll position. Images play forward/backward as user scrolls, creating a cinematic reveal.

**When to use:**
- Physical products (hardware, devices)
- Products where the visual design IS the selling point
- Cinematic, premium positioning
- High-budget pages where asset creation is justified

**Psychological principle:** Interactive scroll gives user agency (autonomy trigger). Frame sequences create a "discovery" experience that increases time-on-page and engagement.

**Example site:** Apple (iPhone, MacBook product pages)

```html
<section class="hero-canvas">
  <canvas class="hero-canvas__frame" width="1920" height="1080"></canvas>
  <div class="hero-canvas__content">
    <h1>Thinner. Lighter. Faster.</h1>
  </div>
</section>
```

```css
.hero-canvas {
  position: relative;
  height: 300vh; /* Scroll distance = 3x viewport for smooth scrub */
}

.hero-canvas__frame {
  position: sticky;
  top: 0;
  width: 100%;
  height: 100vh;
  object-fit: contain;
}

.hero-canvas__content {
  position: sticky;
  top: 50%;
  transform: translateY(-50%);
  text-align: center;
  z-index: 1;
  pointer-events: none;
}
```

```javascript
// Frame sequence loader (minimal implementation)
const canvas = document.querySelector('.hero-canvas__frame');
const ctx = canvas.getContext('2d');
const frameCount = 120;
const frames = [];

// Preload all frames
for (let i = 0; i < frameCount; i++) {
  const img = new Image();
  img.src = `/assets/frames/frame-${String(i).padStart(4, '0')}.webp`;
  frames.push(img);
}

// Draw frame based on scroll position
function updateFrame() {
  const section = document.querySelector('.hero-canvas');
  const rect = section.getBoundingClientRect();
  const scrollFraction = Math.max(0, Math.min(1,
    -rect.top / (rect.height - window.innerHeight)
  ));
  const frameIndex = Math.floor(scrollFraction * (frameCount - 1));
  if (frames[frameIndex]?.complete) {
    ctx.drawImage(frames[frameIndex], 0, 0, canvas.width, canvas.height);
  }
}

window.addEventListener('scroll', updateFrame, { passive: true });
```

**Performance notes:**
- 120 frames × ~30KB each = ~3.6MB total — lazy-load in chunks
- Use WebP for 60-70% size reduction over JPEG
- Provide a static fallback image for `prefers-reduced-motion`

---

## 4. Product Demo Hero (Figma-style)

**Description:** Interactive or animated product UI embedded directly in the hero. The product IS the hero.

**When to use:**
- SaaS with visually impressive UI
- Products where "seeing is believing"
- When the product demo is more convincing than any copy
- Developer tools, design tools, dashboards

**Psychological principle:** IKEA effect (conversion-psychology.md) — interacting with a product creates ownership feeling. Seeing the real product immediately builds trust (no bait-and-switch).

**Example site:** Figma, Notion, Linear

```html
<section class="hero-demo">
  <div class="hero-demo__text">
    <h1>Design, prototype, and collaborate — all in the browser</h1>
    <p>The collaborative interface design tool.</p>
    <div class="hero-demo__actions">
      <a href="#" class="btn btn--primary">Get started for free</a>
      <a href="#" class="btn btn--ghost">Watch a demo</a>
    </div>
  </div>
  <div class="hero-demo__product">
    <!-- Embedded product screenshot or interactive demo -->
    <img src="/assets/product-hero.webp"
         alt="Product interface showing the main dashboard"
         loading="eager"
         fetchpriority="high"
         width="1200" height="800">
  </div>
</section>
```

```css
.hero-demo {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  align-items: center;
  min-height: 90vh;
  gap: 4rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.hero-demo__product img {
  width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.12);
}

@media (max-width: 768px) {
  .hero-demo {
    grid-template-columns: 1fr;
    text-align: center;
    min-height: auto;
    padding-top: 4rem;
  }
  .hero-demo__product { order: -1; }
}
```

---

## 5. Split Hero (Text Left, Visual Right)

**Description:** Classic two-column hero. Text on one side, visual on the other. Reliable, scannable, proven.

**When to use:**
- Any product type — the most versatile pattern
- When you have a strong product screenshot or illustration
- B2B pages where clarity > creativity
- Default choice when other patterns don't clearly apply

**Psychological principle:** Z-pattern reading (visual-hierarchy.md) — text on left aligns with natural reading start, visual on right provides the focal point and memory anchor.

**Example site:** Slack, HubSpot, most B2B SaaS

```html
<section class="hero-split">
  <div class="hero-split__text">
    <span class="hero-split__badge">New: AI-powered workflows</span>
    <h1>Work smarter, not harder</h1>
    <p>Automate repetitive tasks and focus on what matters.</p>
    <a href="#" class="btn btn--primary">Start free trial</a>
    <p class="hero-split__trust">Trusted by 10,000+ teams worldwide</p>
  </div>
  <div class="hero-split__visual">
    <img src="/assets/hero-product.webp"
         alt="Product dashboard"
         loading="eager" fetchpriority="high"
         width="600" height="400">
  </div>
</section>
```

```css
.hero-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  min-height: 80vh;
  gap: 4rem;
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
}

.hero-split__badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 100px;
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.hero-split__trust {
  margin-top: 1.5rem;
  font-size: 0.875rem;
  color: var(--muted);
}

@media (max-width: 768px) {
  .hero-split {
    grid-template-columns: 1fr;
    min-height: auto;
    padding-top: 4rem;
    text-align: center;
  }
}
```

---

## 6. Full-Bleed Image Hero (Ogilvy Editorial)

**Description:** Dominant, full-viewport image with text overlaid. The image carries the emotional weight. Inspired by Ogilvy's layout formula.

**When to use:**
- Physical products with beautiful photography
- Lifestyle/aspirational brands
- Editorial positioning (premium, luxury, authority)
- When the image alone makes the case
- Ogilvy Direct narrative framework

**Psychological principle:** Ogilvy's 3/4 visual rule (ogilvy-principles.md) — the image does the selling, copy closes the deal. Large visuals increase perceived quality and emotional engagement.

**Example site:** Apple (product launches), luxury brands, high-end agency sites

```html
<section class="hero-editorial">
  <img class="hero-editorial__image"
       src="/assets/hero-editorial.webp"
       alt="Product in natural setting"
       loading="eager" fetchpriority="high">
  <div class="hero-editorial__overlay" aria-hidden="true"></div>
  <div class="hero-editorial__content">
    <p class="hero-editorial__caption">The new standard in precision</p>
    <h1>Crafted for those who notice the difference</h1>
    <a href="#" class="btn btn--primary">Explore</a>
  </div>
</section>
```

```css
.hero-editorial {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: flex-end; /* Content at bottom (Ogilvy layout) */
  overflow: hidden;
}

.hero-editorial__image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-editorial__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.8) 0%,
    rgba(0, 0, 0, 0.2) 40%,
    transparent 70%
  );
}

.hero-editorial__content {
  position: relative;
  z-index: 1;
  padding: 4rem;
  max-width: 600px;
  color: #fff;
}

.hero-editorial__caption {
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.7;
  margin-bottom: 1rem;
}
```

---

## 7. Minimal Text Hero (Superhuman-style)

**Description:** Extreme reduction. Just a headline, maybe a subheadline, and a CTA. Massive whitespace. The confidence to say less IS the message.

**When to use:**
- Products with strong brand awareness (most-aware audience)
- When the product name/promise is self-explanatory
- Premium positioning through restraint
- Single, focused CTA pages

**Psychological principle:** Whitespace signals premium quality (visual-hierarchy.md). Fewer elements = faster Hick's Law decision time. The restraint itself communicates confidence.

**Example site:** Superhuman, Basecamp, Linear

```html
<section class="hero-minimal">
  <h1>Blazingly fast email</h1>
  <p>The fastest email experience ever made.</p>
  <a href="#" class="btn btn--primary">Get started</a>
</section>
```

```css
.hero-minimal {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  text-align: center;
  padding: 4rem 2rem;
}

.hero-minimal h1 {
  font-size: clamp(3rem, 7vw, 6rem);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.04em;
  max-width: 12ch; /* Very tight line width for impact */
}

.hero-minimal p {
  margin-top: 1.5rem;
  font-size: clamp(1.125rem, 1.5vw, 1.5rem);
  color: var(--muted);
  max-width: 35ch;
}

.hero-minimal .btn {
  margin-top: 3rem;
}
```

---

## 8. Dark Cinematic Hero (Linear-style)

**Description:** Dark background with glow effects, glassmorphism, and subtle light leaks. Creates a premium, cinematic atmosphere.

**When to use:**
- Developer tools, technical products
- Products that position as "the premium alternative"
- Dark-mode-first brands
- When the aesthetic IS part of the brand promise

**Psychological principle:** Dark backgrounds increase perceived value by 15-25% (color-psychology.md). Glow effects create focal points that guide attention. Glassmorphism creates depth (figure-ground separation).

**Example site:** Linear, Raycast, Warp

```html
<section class="hero-cinematic">
  <div class="hero-cinematic__glow" aria-hidden="true"></div>
  <div class="hero-cinematic__content">
    <div class="hero-cinematic__badge">
      <span class="badge-dot"></span>
      Introducing Linear Insights
    </div>
    <h1>Build software<br>at the speed of thought</h1>
    <p>Streamline issues, projects, and product roadmaps.</p>
    <div class="hero-cinematic__actions">
      <a href="#" class="btn btn--glow">Get started</a>
      <a href="#" class="btn btn--ghost">See a demo</a>
    </div>
  </div>
  <div class="hero-cinematic__product">
    <div class="hero-cinematic__glass">
      <img src="/assets/product.webp" alt="Product interface"
           loading="eager" fetchpriority="high">
    </div>
  </div>
</section>
```

```css
.hero-cinematic {
  position: relative;
  min-height: 100vh;
  background: #0a0a0a;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 4rem 2rem;
}

.hero-cinematic__glow {
  position: absolute;
  top: -20%;
  left: 50%;
  transform: translateX(-50%);
  width: 800px;
  height: 600px;
  background: radial-gradient(
    ellipse,
    rgba(100, 120, 255, 0.15) 0%,
    transparent 70%
  );
  pointer-events: none;
}

.hero-cinematic__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  border-radius: 100px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  margin-bottom: 2rem;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.hero-cinematic__glass {
  margin-top: 4rem;
  padding: 2px;
  border-radius: 16px;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.1),
    rgba(255, 255, 255, 0.02));
  backdrop-filter: blur(20px);
}

.hero-cinematic__glass img {
  border-radius: 14px;
  width: 100%;
  max-width: 1000px;
}

.btn--glow {
  background: #fff;
  color: #0a0a0a;
  padding: 12px 32px;
  border-radius: 8px;
  font-weight: 600;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
  transition: box-shadow 0.3s ease;
}

.btn--glow:hover {
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
}
```

---

## Hero Selection Decision Tree

```
What is the audience's awareness level?

MOST-AWARE → Minimal Text (#7) or Dark Cinematic (#8)
PRODUCT-AWARE → Product Demo (#4) or Split (#5)
SOLUTION-AWARE → Split (#5) or Gradient (#1)
PROBLEM-AWARE → Full-Bleed Editorial (#6) or Video (#2)
UNAWARE → Video (#2) or Canvas Animation (#3) or Full-Bleed (#6)

What is the product type?

SaaS/Tech → Gradient (#1), Product Demo (#4), Dark Cinematic (#8)
Physical product → Canvas Animation (#3), Full-Bleed (#6)
Service/Education → Split (#5), Full-Bleed (#6)
Premium/Luxury → Full-Bleed (#6), Dark Cinematic (#8)
Developer tool → Dark Cinematic (#8), Gradient (#1)
```
