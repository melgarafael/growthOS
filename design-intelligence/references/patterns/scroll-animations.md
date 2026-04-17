# Scroll Animation Patterns — 6 Variants

> **Purpose:** Scroll-driven animations enhance engagement and guide attention through the page. These patterns use modern CSS-only techniques where possible, with JS fallbacks.
> **Rule:** Every animation must serve a PURPOSE (reveal content, guide attention, demonstrate product). Decorative-only animations are AI slop.
> **Performance:** All animations must use GPU-accelerated properties only (`transform`, `opacity`). Respect `prefers-reduced-motion`.

---

## Browser Support Note

CSS Scroll-Driven Animations (`animation-timeline: scroll()` / `view()`) are supported in Chromium browsers (Chrome 115+, Edge 115+). Safari and Firefox have partial/flag support as of 2026. All patterns below include `@supports` progressive enhancement and JS fallbacks.

---

## 1. Fade-Up on Enter

**Description:** Elements fade in and slide up as they scroll into view. The most common and safest scroll animation.

**When to use:** Section headings, feature cards, testimonials, any content block that benefits from a reveal moment.

**Psychology:** Elements that "arrive" feel intentional and draw momentary attention. Creates a sense of progression.

```css
/* Progressive enhancement: CSS Scroll-Driven */
@supports (animation-timeline: view()) {
  .fade-up {
    animation: fade-up-anim both;
    animation-timeline: view();
    animation-range: entry 0% entry 40%;
  }
}

@keyframes fade-up-anim {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Fallback: IntersectionObserver adds class */
.fade-up:not([style*="animation-timeline"]) {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.fade-up.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  .fade-up {
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }
}
```

**JS Fallback (for non-Chromium):**
```javascript
if (!CSS.supports('animation-timeline', 'view()')) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
}
```

**Performance:** Excellent. Only `opacity` and `transform` — fully GPU-composited.

---

## 2. Stagger Reveal

**Description:** Multiple items in a group appear sequentially with a delay between each. Creates a cascade effect.

**When to use:** Feature grids, pricing tiers, step-by-step sections, any list of 3-6 items.

**Psychology:** Sequential reveal creates a narrative — items feel ordered and intentional. The eye follows the cascade, ensuring each item gets momentary attention.

```html
<div class="stagger-group">
  <div class="stagger-item" style="--i: 0">Feature 1</div>
  <div class="stagger-item" style="--i: 1">Feature 2</div>
  <div class="stagger-item" style="--i: 2">Feature 3</div>
  <div class="stagger-item" style="--i: 3">Feature 4</div>
</div>
```

```css
@supports (animation-timeline: view()) {
  .stagger-item {
    animation: stagger-in both;
    animation-timeline: view();
    animation-range: entry 0% entry 50%;
    /* Stagger effect via custom property */
    animation-delay: calc(var(--i, 0) * 80ms);
  }
}

@keyframes stagger-in {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* JS fallback with stagger */
.stagger-item {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.5s ease, transform 0.5s ease;
  transition-delay: calc(var(--i, 0) * 100ms);
}

.stagger-group.is-visible .stagger-item {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .stagger-item {
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }
}
```

**Performance:** Same as fade-up — GPU-composited. The stagger delay is CSS-only, no runtime cost.

---

## 3. Parallax Background

**Description:** Background elements move at a different speed than foreground content during scroll, creating depth and an immersive feel.

**When to use:** Section backgrounds, hero decorative elements, visual interest between content sections.

**Psychology:** Parallax creates perceived depth (figure-ground separation). It makes the page feel three-dimensional and interactive.

```html
<section class="parallax-section">
  <div class="parallax-bg" aria-hidden="true">
    <img src="/assets/bg-pattern.webp" alt="" loading="lazy">
  </div>
  <div class="parallax-content">
    <h2>Built for scale</h2>
    <p>From startup to enterprise, our infrastructure grows with you.</p>
  </div>
</section>
```

```css
/* CSS Scroll-Driven Parallax */
@supports (animation-timeline: scroll()) {
  .parallax-bg img {
    animation: parallax-shift both linear;
    animation-timeline: scroll();
  }
}

@keyframes parallax-shift {
  from { transform: translateY(-15%); }
  to   { transform: translateY(15%); }
}

/* Fallback: pure CSS perspective trick */
.parallax-section {
  position: relative;
  overflow: hidden;
}

.parallax-bg {
  position: absolute;
  inset: -20% 0;
  z-index: 0;
}

.parallax-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.parallax-content {
  position: relative;
  z-index: 1;
  padding: 8rem 2rem;
}

@media (prefers-reduced-motion: reduce) {
  .parallax-bg img {
    animation: none !important;
    transform: none !important;
  }
  .parallax-bg { inset: 0; }
}
```

**Performance notes:**
- Parallax on images is safe (GPU layer)
- Never parallax text — it degrades readability
- Keep movement subtle (±15% max) — extreme parallax causes nausea
- `inset: -20% 0` on the background prevents gaps during scroll movement

---

## 4. Pin-and-Animate

**Description:** A section pins to the viewport while content within it animates (slide, swap, transform). Creates a "storytelling" scroll experience.

**When to use:** Feature showcases (show different features as user scrolls), product demos, before/after comparisons. High-impact sections.

**Psychology:** Pinning creates focused attention — the user can't passively scroll past. Each scroll increment reveals new information, creating a sense of discovery (curiosity trigger).

```html
<section class="pin-section" style="--steps: 3">
  <div class="pin-section__sticky">
    <div class="pin-section__frame" data-step="0">
      <h3>Step 1: Connect</h3>
      <img src="/features/connect.webp" alt="Connect your tools">
    </div>
    <div class="pin-section__frame" data-step="1">
      <h3>Step 2: Configure</h3>
      <img src="/features/configure.webp" alt="Set up your workflow">
    </div>
    <div class="pin-section__frame" data-step="2">
      <h3>Step 3: Launch</h3>
      <img src="/features/launch.webp" alt="Go live in minutes">
    </div>
  </div>
</section>
```

```css
.pin-section {
  /* Height = viewport × number of steps */
  height: calc(var(--steps, 3) * 100vh);
  position: relative;
}

.pin-section__sticky {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.pin-section__frame {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.pin-section__frame.is-active {
  opacity: 1;
  transform: translateY(0);
}
```

```javascript
// Simple scroll-based step activation
const section = document.querySelector('.pin-section');
const frames = section.querySelectorAll('.pin-section__frame');
const steps = frames.length;

function updatePinSection() {
  const rect = section.getBoundingClientRect();
  const scrollProgress = Math.max(0, Math.min(1,
    -rect.top / (rect.height - window.innerHeight)
  ));
  const activeStep = Math.min(steps - 1, Math.floor(scrollProgress * steps));

  frames.forEach((frame, i) => {
    frame.classList.toggle('is-active', i === activeStep);
  });
}

window.addEventListener('scroll', updatePinSection, { passive: true });
```

**Performance notes:**
- `position: sticky` is GPU-friendly
- Frame transitions use only `opacity` and `transform`
- Keep to ≤5 steps — more feels like it "traps" the user

---

## 5. Progress Indicator

**Description:** A reading progress bar that fills as the user scrolls through the page. Shows how far they've come and how much remains.

**When to use:** Long sales pages (8+ sections). Signals to the reader that the page has a finite length and they're making progress.

**Psychology:** Commitment & consistency — seeing progress creates momentum to continue. The Zeigarnik effect — incomplete progress bars create a desire to complete.

```html
<div class="progress-bar" role="progressbar" aria-label="Reading progress"
     aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar__fill"></div>
</div>
```

```css
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  z-index: 100;
  background: transparent;
}

/* CSS Scroll-Driven (no JS needed) */
@supports (animation-timeline: scroll()) {
  .progress-bar__fill {
    height: 100%;
    background: var(--accent);
    transform-origin: left;
    animation: progress-fill both linear;
    animation-timeline: scroll();
  }

  @keyframes progress-fill {
    from { transform: scaleX(0); }
    to   { transform: scaleX(1); }
  }
}

/* JS fallback */
.progress-bar__fill {
  height: 100%;
  background: var(--accent);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.1s linear;
}

@media (prefers-reduced-motion: reduce) {
  .progress-bar { display: none; }
}
```

```javascript
// Fallback for non-Chromium
if (!CSS.supports('animation-timeline', 'scroll()')) {
  const fill = document.querySelector('.progress-bar__fill');
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.body.scrollHeight - window.innerHeight;
    const progress = scrollTop / docHeight;
    fill.style.transform = `scaleX(${progress})`;
  }, { passive: true });
}
```

**Performance:** Excellent — `scaleX` is GPU-composited. 3px height is invisible to layout.

---

## 6. Counter Animation

**Description:** Numbers count up from 0 to target value when they scroll into view. Creates visual proof of scale.

**When to use:** Metric sections, social proof counters, any large number that benefits from dramatic reveal.

**Psychology:** Counting animation draws attention and creates a "wow" moment. The final number feels earned because the reader watched it build.

```html
<span class="counter" data-target="14000" data-suffix="+">0</span>
```

```javascript
function animateCounter(element) {
  const target = parseInt(element.dataset.target);
  const suffix = element.dataset.suffix || '';
  const duration = 2000;
  const start = performance.now();

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease-out cubic for natural deceleration
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(eased * target);

    element.textContent = current.toLocaleString() + suffix;

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

// Trigger on scroll into view
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateCounter(entry.target);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.counter').forEach(el => observer.observe(el));
```

```css
.counter {
  font-variant-numeric: tabular-nums;
  /* Prevent layout shift during counting */
  display: inline-block;
  min-width: 4ch;
}

@media (prefers-reduced-motion: reduce) {
  /* Show final value immediately, no animation */
  .counter { /* JS handles this via matchMedia check */ }
}
```

**Performance notes:**
- `requestAnimationFrame` ensures smooth 60fps counting
- `font-variant-numeric: tabular-nums` prevents numbers from shifting width
- Trigger ONCE per page view (use `unobserve` after animation)
- Check `prefers-reduced-motion` in JS before starting animation

---

## Animation Decision Matrix

| Section Type | Recommended Animation | Priority |
|-------------|----------------------|----------|
| Hero | None or subtle parallax | Don't delay LCP |
| Logo bar | None | Speed > flair |
| Features | Stagger reveal | Medium |
| How it works | Pin-and-animate or stagger | High |
| Social proof | Fade-up + counter | Medium |
| Pricing | Fade-up | Low (focus on content) |
| Testimonials | Fade-up | Low |
| Final CTA | None | CTA needs to be instantly visible |
| Full page | Progress indicator | Always on long pages |

## Performance Checklist

- [ ] Only `transform` and `opacity` used (GPU-composited)
- [ ] `prefers-reduced-motion: reduce` respected for ALL animations
- [ ] `@supports` check for `animation-timeline: view()` before using
- [ ] IntersectionObserver fallback for non-Chromium browsers
- [ ] No animation on hero that would delay LCP
- [ ] Total animation JS < 2KB gzipped
- [ ] Animations fire once (not repeated on scroll back)
