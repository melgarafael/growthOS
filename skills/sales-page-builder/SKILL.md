---
name: sales-page-builder
description: >-
  Phase 7 builder for the Sales Page Production System. Converts approved visual design tokens
  (Phase 4) and narrative copy (Phase 5/6) into production-ready single-file HTML with embedded
  CSS and minimal JS. Implements scroll-driven animations, canvas frame sequences, Every Layout
  primitives, fluid typography, and mathematical positioning. Targets <300KB with animations,
  <100KB without. Use when building the final HTML output of a sales page pipeline.
---

# Sales Page Builder Skill

You are the **Build Engine** of the Sales Page Production System (Phase 7). You receive approved design tokens and narrative copy from earlier phases and produce a single, self-contained HTML file that is performant, accessible, SEO-ready, and visually elite.

**You do NOT invent copy or design.** Everything you build traces to Phase 4 (visual design) and Phase 5/6 (narrative/fusion). Your job is engineering excellence.

## Core Principle: Directed Build

```
INPUT:  state.json (Phase 4 design_tokens + Phase 5 sections + Phase 6 fusion)
OUTPUT: Single-file index.html — production-ready, self-contained
```

Every CSS value traces to a design token. Every text node traces to approved copy. Every animation traces to a technique selected in Phase 4.

---

## A. Build Architecture

### Output Constraints

| Rule | Detail |
|------|--------|
| **Single file** | One `.html` file — no separate CSS, JS, or image files |
| **Embedded CSS** | All styles via `<style>` tag in `<head>` |
| **Minimal JS** | Via `<script>` at end of `<body>` — ONLY for animations/interactions that CSS cannot handle |
| **No external deps** | No CDNs, no tracking scripts, no external requests at runtime |
| **Fonts** | System font stack as primary. Optional: single Google Fonts `@import` inline if design requires it |
| **Icons/illustrations** | Inline SVG only — no icon fonts, no external images |
| **File size** | Target <300KB with animations, <100KB without |

### Document Structure

```html
<!DOCTYPE html>
<html lang="{{lang}}">
<head>
  <!-- SEO Meta (Section G) -->
  <style>
    /* 1. CSS Reset */
    /* 2. Custom Properties (Section B) */
    /* 3. Layout Primitives (Section C) */
    /* 4. Component Styles */
    /* 5. Section Styles */
    /* 6. Animation Definitions (Section D) */
    /* 7. Responsive Adjustments */
    /* 8. Reduced Motion */
    /* 9. Print Styles (optional) */
  </style>
</head>
<body>
  <a href="#main" class="skip-link">Skip to content</a>
  <main id="main">
    <!-- Sections from Phase 5/6 narrative -->
  </main>
  <footer><!-- Minimal footer --></footer>
  <script>
    /* Only if canvas frame sequence or complex interactions needed */
  </script>
</body>
</html>
```

### CSS Cascade Order

The `<style>` block follows this exact order to ensure predictable specificity:

1. **Reset** — minimal box-sizing + margin reset
2. **Custom properties** — `:root` tokens from Phase 4
3. **Layout primitives** — composable layout classes (Section C)
4. **Base typography** — body, headings, links, lists
5. **Components** — buttons, badges, cards, accordions
6. **Sections** — hero, features, pricing, etc. (Section E)
7. **Animations** — `@keyframes` + scroll-driven rules (Section D)
8. **Media queries** — responsive overrides, reduced-motion, print

---

## B. CSS Custom Properties System

### Token Mapping

Design tokens from Phase 4's `design_tokens` object map directly to CSS custom properties. The builder reads `state.json` and populates these values.

```css
:root {
  /* ── Colors (from Phase 4 design_tokens.colors) ── */
  --sp-bg: #09090B;
  --sp-fg: #FAFAFA;
  --sp-accent: #3B82F6;
  --sp-accent-2: #8B5CF6;
  --sp-surface: #18181B;
  --sp-muted: #71717A;
  --sp-border: #27272A;

  /* ── Typography — fluid using clamp() ── */
  --sp-text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --sp-text-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --sp-text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --sp-text-lg: clamp(1.125rem, 1rem + 0.625vw, 1.375rem);
  --sp-text-xl: clamp(1.25rem, 1rem + 1.25vw, 1.75rem);
  --sp-text-2xl: clamp(1.5rem, 1rem + 2.5vw, 2.5rem);
  --sp-text-3xl: clamp(2rem, 1rem + 5vw, 4rem);
  --sp-text-hero: clamp(2.5rem, 1rem + 7.5vw, 6rem);

  /* ── Spacing — Utopia-inspired fluid scale ── */
  --sp-space-xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.5rem);
  --sp-space-sm: clamp(0.5rem, 0.4rem + 0.5vw, 1rem);
  --sp-space-md: clamp(1rem, 0.75rem + 1.25vw, 2rem);
  --sp-space-lg: clamp(2rem, 1.5rem + 2.5vw, 4rem);
  --sp-space-xl: clamp(4rem, 3rem + 5vw, 8rem);
  --sp-space-2xl: clamp(6rem, 4rem + 10vw, 12rem);

  /* ── Motion ── */
  --sp-ease: cubic-bezier(0.16, 1, 0.3, 1);
  --sp-ease-out: cubic-bezier(0, 0, 0.3, 1);
  --sp-ease-in: cubic-bezier(0.7, 0, 1, 1);
  --sp-duration-micro: 150ms;
  --sp-duration-fast: 300ms;
  --sp-duration-normal: 500ms;
  --sp-duration-slow: 1000ms;

  /* ── Layout ── */
  --sp-max-width: 1200px;
  --sp-content-width: 720px;
  --sp-gutter: clamp(1rem, 0.5rem + 2.5vw, 2rem);

  /* ── Borders & Effects ── */
  --sp-radius-sm: 4px;
  --sp-radius-md: 8px;
  --sp-radius-lg: 16px;
  --sp-radius-full: 9999px;
  --sp-shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
  --sp-shadow-md: 0 4px 12px rgba(0,0,0,0.4);
  --sp-shadow-lg: 0 12px 40px rgba(0,0,0,0.5);
}
```

### Reduced Motion Override

```css
@media (prefers-reduced-motion: reduce) {
  :root {
    --sp-duration-micro: 0ms;
    --sp-duration-fast: 0ms;
    --sp-duration-normal: 0ms;
    --sp-duration-slow: 0ms;
  }
}
```

### How to Override Tokens

When Phase 4 provides specific values, replace the defaults above. Example:

```
Phase 4 state: design_tokens.colors.accent_primary = "#B0FF3C"
→ CSS: --sp-accent: #B0FF3C;
```

The builder MUST map every Phase 4 token to its corresponding `--sp-*` variable. Never hardcode colors or sizes outside of custom properties.

---

## C. Layout System (Every Layout-Inspired)

Eight composable layout primitives. Each is a single CSS class with minimal declarations. Combine them to build any section layout without writing custom CSS.

### 1. Stack — Vertical Flow

Consistent vertical spacing between child elements.

```css
.stack {
  display: flex;
  flex-direction: column;
}
.stack > * + * {
  margin-block-start: var(--stack-space, var(--sp-space-md));
}
```

**Usage:** `<div class="stack" style="--stack-space: var(--sp-space-lg)">` to override spacing.

### 2. Center — Content Centering

Horizontally centers content with a max-width and gutters.

```css
.center {
  box-sizing: content-box;
  max-inline-size: var(--center-max, var(--sp-content-width));
  margin-inline: auto;
  padding-inline: var(--sp-gutter);
}
```

### 3. Cluster — Horizontal Wrap

Flexible horizontal grouping with wrapping. For tags, badges, logo bars, social proof.

```css
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--cluster-gap, var(--sp-space-sm));
  align-items: center;
}
```

### 4. Sidebar — Main + Aside

Two-column layout where one side has a fixed width and the other fills remaining space.

```css
.with-sidebar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-space-lg);
}
.with-sidebar > :first-child {
  flex-grow: 999;
  min-inline-size: 65%;
}
.with-sidebar > :last-child {
  flex-basis: var(--sidebar-width, 300px);
  flex-grow: 1;
}
```

### 5. Switcher — Responsive Column Switch

N columns on wide screens, stacks on narrow. Threshold-based, no media queries.

```css
.switcher {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-space-md);
}
.switcher > * {
  flex-grow: 1;
  flex-basis: calc((var(--switcher-threshold, 640px) - 100%) * 999);
}
```

### 6. Grid — Auto-Fit Responsive

Responsive grid that auto-fills columns based on a minimum width.

```css
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(var(--grid-min, 250px), 100%), 1fr));
  gap: var(--sp-space-md);
}
```

### 7. Cover — Full-Viewport Hero

Vertically centers content within a minimum-height container (typically 100vh).

```css
.cover {
  display: flex;
  flex-direction: column;
  min-block-size: var(--cover-min-height, 100vh);
  padding: var(--sp-space-lg);
}
.cover > * {
  margin-block: auto;
}
.cover > :first-child:not(.cover-center) {
  margin-block-start: 0;
}
.cover > :last-child:not(.cover-center) {
  margin-block-end: 0;
}
.cover > .cover-center {
  margin-block: auto;
}
```

### 8. Frame — Aspect-Ratio Container

Maintains aspect ratio for images, videos, and embedded content.

```css
.frame {
  aspect-ratio: var(--frame-ratio, 16/9);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}
.frame > img,
.frame > video {
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
}
```

### Combining Primitives

Primitives compose — nest them to build complex layouts:

```html
<!-- Hero: full-viewport cover with centered content -->
<section class="cover">
  <div class="center cover-center">
    <div class="stack" style="--stack-space: var(--sp-space-lg)">
      <h1>Headline</h1>
      <p>Subheadline</p>
      <a href="#" class="btn-primary">CTA</a>
    </div>
  </div>
</section>

<!-- Features: centered grid -->
<section>
  <div class="center" style="--center-max: var(--sp-max-width)">
    <div class="auto-grid" style="--grid-min: 280px">
      <!-- Feature cards -->
    </div>
  </div>
</section>

<!-- Pricing: sidebar layout -->
<section>
  <div class="center with-sidebar">
    <div class="stack"><!-- Plan details --></div>
    <aside><!-- Price card --></aside>
  </div>
</section>
```

---

## D. Animation Techniques

Four tiers of animation, selected by Phase 4's `animation_strategy` field. Each tier includes the previous.

### Animation Strategy Mapping

| Phase 4 `animation_strategy` | Tiers Included |
|------------------------------|----------------|
| `minimal` | Tier 1 only |
| `moderate` | Tier 1 + Tier 2 + Tier 3 |
| `cinematic` | All 4 tiers |

### Tier 1: Micro-Interactions (Always Included)

Subtle feedback on interactive elements. Pure CSS, no JS, GPU-friendly.

```css
/* Button hover + active */
.btn-primary {
  transition: transform var(--sp-duration-micro) var(--sp-ease),
              box-shadow var(--sp-duration-micro) var(--sp-ease);
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.btn-primary:active {
  transform: translateY(0);
  box-shadow: var(--sp-shadow-sm);
}

/* Focus outlines */
:focus-visible {
  outline: 2px solid var(--sp-accent);
  outline-offset: 3px;
}

/* Link underline transition */
a:not(.btn-primary) {
  text-decoration-color: transparent;
  text-underline-offset: 3px;
  transition: text-decoration-color var(--sp-duration-micro) var(--sp-ease);
}
a:not(.btn-primary):hover {
  text-decoration-color: currentColor;
}

/* Card hover lift */
.card {
  transition: transform var(--sp-duration-fast) var(--sp-ease),
              box-shadow var(--sp-duration-fast) var(--sp-ease);
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--sp-shadow-lg);
}
```

### Tier 2: Reveal-on-Scroll (CSS Scroll-Driven Animations)

Elements fade/slide into view as they enter the viewport. Uses the modern CSS `animation-timeline: view()` API with a fallback.

```css
/* Progressive enhancement — only applies if browser supports scroll-driven */
@supports (animation-timeline: view()) {
  .reveal {
    animation: reveal-up linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 35%;
  }

  .reveal-left {
    animation: reveal-left linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 35%;
  }

  .reveal-scale {
    animation: reveal-scale linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 40%;
  }

  /* Stagger children — apply to parent, children get delayed reveals */
  .reveal-stagger > * {
    animation: reveal-up linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 40%;
  }
  .reveal-stagger > :nth-child(2) { animation-delay: 80ms; }
  .reveal-stagger > :nth-child(3) { animation-delay: 160ms; }
  .reveal-stagger > :nth-child(4) { animation-delay: 240ms; }
  .reveal-stagger > :nth-child(5) { animation-delay: 320ms; }
  .reveal-stagger > :nth-child(6) { animation-delay: 400ms; }
}

@keyframes reveal-up {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes reveal-left {
  from { opacity: 0; transform: translateX(-30px); }
  to   { opacity: 1; transform: translateX(0); }
}

@keyframes reveal-scale {
  from { opacity: 0; transform: scale(0.95); }
  to   { opacity: 1; transform: scale(1); }
}
```

**Fallback for unsupported browsers:** Elements render at full opacity (no animation = no loss of content).

### Tier 3: Parallax Effects (CSS Scroll-Driven)

Depth illusion through differential scroll speeds. Pure CSS, no JS.

```css
@supports (animation-timeline: scroll()) {
  .parallax-slow {
    animation: parallax-down linear;
    animation-timeline: scroll();
  }

  .parallax-fast {
    animation: parallax-up linear;
    animation-timeline: scroll();
  }

  /* Hero background image parallax */
  .hero-parallax-bg {
    animation: parallax-hero linear;
    animation-timeline: scroll();
    will-change: transform;
  }
}

@keyframes parallax-down {
  from { transform: translateY(0); }
  to   { transform: translateY(-10%); }
}

@keyframes parallax-up {
  from { transform: translateY(0); }
  to   { transform: translateY(-20%); }
}

@keyframes parallax-hero {
  from { transform: translateY(0) scale(1.1); }
  to   { transform: translateY(-15%) scale(1.1); }
}
```

**Usage:** Add `.parallax-slow` to background decorative elements, `.parallax-fast` to foreground decorative elements. Never apply parallax to text or interactive content.

### Tier 4: Canvas Frame Sequence (Apple-Style, JS Required)

Video-to-frames scroll animation. The user scrolls through a product reveal like Apple's product pages.

**When to use:** Only when `scroll_technique` = `canvas-frame-sequence` in Phase 4.

#### Frame Preparation (pre-build step)

```
1. Extract frames from video: ffmpeg -i input.mp4 -vf "fps=30,scale=1280:-1" frame_%04d.webp
2. Optimize: cwebp -q 75 frame_XXXX.webp -o frame_XXXX.webp
3. Target: 60-120 frames, ~5-15KB each
4. Encode as base64 data URIs or load via preloader
```

For self-contained builds, frames are embedded as base64 data URIs in a JS array. For external builds, they load from a `/frames/` directory.

#### Implementation

```html
<section class="frame-sequence-section" style="height: 300vh;">
  <div class="frame-sequence-sticky">
    <canvas id="frame-canvas" width="1280" height="720"></canvas>
  </div>
</section>

<style>
  .frame-sequence-section {
    position: relative;
  }
  .frame-sequence-sticky {
    position: sticky;
    top: 0;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }
  .frame-sequence-sticky canvas {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
</style>

<script>
(function() {
  'use strict';

  // Configuration
  const TOTAL_FRAMES = 90;
  const CANVAS = document.getElementById('frame-canvas');
  if (!CANVAS) return;
  const CTX = CANVAS.getContext('2d');
  const SECTION = CANVAS.closest('.frame-sequence-section');

  // Respect reduced motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Show middle frame as static image, skip animation
    loadFrame(Math.floor(TOTAL_FRAMES / 2)).then(img => {
      CTX.drawImage(img, 0, 0, CANVAS.width, CANVAS.height);
    });
    return;
  }

  // Frame cache
  const frames = new Array(TOTAL_FRAMES);
  let loaded = 0;

  function frameSrc(i) {
    // For base64-embedded: return FRAME_DATA[i];
    // For external: return `frames/frame_${String(i).padStart(4,'0')}.webp`;
    return `frames/frame_${String(i + 1).padStart(4, '0')}.webp`;
  }

  function loadFrame(i) {
    return new Promise((resolve) => {
      if (frames[i]) { resolve(frames[i]); return; }
      const img = new Image();
      img.onload = () => { frames[i] = img; loaded++; resolve(img); };
      img.onerror = () => resolve(null);
      img.src = frameSrc(i);
    });
  }

  // Preload strategy: first, last, then fill
  async function preload() {
    // Priority: first + last frames
    await Promise.all([loadFrame(0), loadFrame(TOTAL_FRAMES - 1)]);
    // Draw first frame immediately
    if (frames[0]) CTX.drawImage(frames[0], 0, 0, CANVAS.width, CANVAS.height);
    // Fill remaining
    const remaining = [];
    for (let i = 1; i < TOTAL_FRAMES - 1; i++) remaining.push(loadFrame(i));
    await Promise.all(remaining);
  }

  // Scroll handler with RAF debounce
  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const rect = SECTION.getBoundingClientRect();
      const scrollableHeight = SECTION.offsetHeight - window.innerHeight;
      const progress = Math.max(0, Math.min(1, -rect.top / scrollableHeight));
      const frameIndex = Math.min(TOTAL_FRAMES - 1, Math.floor(progress * TOTAL_FRAMES));
      if (frames[frameIndex]) {
        CTX.clearRect(0, 0, CANVAS.width, CANVAS.height);
        CTX.drawImage(frames[frameIndex], 0, 0, CANVAS.width, CANVAS.height);
      }
      ticking = false;
    });
  }

  preload();
  window.addEventListener('scroll', onScroll, { passive: true });
})();
</script>
```

#### Fallback Strategy

| Condition | Behavior |
|-----------|----------|
| `prefers-reduced-motion` | Show single static frame (middle) |
| Slow connection (`navigator.connection.effectiveType === '2g'`) | Show static frame + skip preload |
| Canvas not supported | Hide canvas, show `<noscript>` fallback image |
| Frames fail to load | Show first successfully loaded frame |

### Tier 5: Mesh Gradient Background (CSS + Optional JS)

Stripe-style animated gradient. CSS-only version for most cases; JS version for interactive mouse-follow.

#### CSS-Only Version

```css
.mesh-gradient {
  position: fixed;
  inset: 0;
  z-index: -1;
  background:
    radial-gradient(ellipse at 20% 50%, var(--sp-accent) 0px, transparent 50%),
    radial-gradient(ellipse at 80% 20%, var(--sp-accent-2) 0px, transparent 50%),
    radial-gradient(ellipse at 50% 80%, var(--sp-accent) 0px, transparent 40%);
  opacity: 0.15;
  filter: blur(80px);
  animation: mesh-shift 20s var(--sp-ease) infinite alternate;
}

@keyframes mesh-shift {
  0%   { transform: translateX(0) translateY(0) rotate(0deg); }
  33%  { transform: translateX(3%) translateY(-3%) rotate(1deg); }
  66%  { transform: translateX(-2%) translateY(2%) rotate(-1deg); }
  100% { transform: translateX(1%) translateY(-1%) rotate(0.5deg); }
}
```

#### JS Interactive Version (mouse-follow)

```javascript
// Only add if animation_strategy === 'cinematic'
(function() {
  const el = document.querySelector('.mesh-gradient');
  if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  let mouseX = 0.5, mouseY = 0.5;
  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX / window.innerWidth;
    mouseY = e.clientY / window.innerHeight;
  }, { passive: true });

  function animate() {
    el.style.background = `
      radial-gradient(ellipse at ${20 + mouseX * 20}% ${50 + mouseY * 10}%, var(--sp-accent) 0px, transparent 50%),
      radial-gradient(ellipse at ${80 - mouseX * 15}% ${20 + mouseY * 15}%, var(--sp-accent-2) 0px, transparent 50%),
      radial-gradient(ellipse at ${50 + mouseX * 10}% ${80 - mouseY * 10}%, var(--sp-accent) 0px, transparent 40%)
    `;
    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);
})();
```

---

## E. Section Templates

Each section type has a semantic HTML structure and associated CSS. These are the building blocks — the builder selects and orders them based on Phase 5's `sections` array.

### hero — Variant: gradient

Full-viewport gradient hero with centered content.

```html
<section class="sp-hero cover" aria-labelledby="hero-heading">
  <div class="mesh-gradient" aria-hidden="true"></div>
  <div class="center cover-center">
    <div class="stack" style="--stack-space: var(--sp-space-lg)">
      <p class="sp-eyebrow">{{eyebrow}}</p>
      <h1 id="hero-heading" class="sp-hero-title">{{headline}}</h1>
      <p class="sp-hero-subtitle">{{subheadline}}</p>
      <div class="cluster" style="--cluster-gap: var(--sp-space-sm)">
        <a href="{{cta_action}}" class="btn-primary">{{cta_text}}</a>
        <a href="{{secondary_action}}" class="btn-ghost">{{secondary_text}}</a>
      </div>
      <p class="sp-trust">{{social_proof_element}}</p>
    </div>
  </div>
</section>
```

```css
.sp-hero {
  --cover-min-height: 100vh;
  --cover-min-height: 100dvh;
  position: relative;
  overflow: hidden;
  background: var(--sp-bg);
  color: var(--sp-fg);
}
.sp-eyebrow {
  font-size: var(--sp-text-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--sp-accent);
}
.sp-hero-title {
  font-size: var(--sp-text-hero);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.05;
  max-inline-size: 16ch;
}
.sp-hero-subtitle {
  font-size: var(--sp-text-xl);
  color: var(--sp-muted);
  max-inline-size: 48ch;
  line-height: 1.5;
}
.sp-trust {
  font-size: var(--sp-text-sm);
  color: var(--sp-muted);
}
```

### hero — Variant: video-bg

Dark overlay on a background video or canvas.

```html
<section class="sp-hero sp-hero--video cover" aria-labelledby="hero-heading">
  <div class="sp-hero-media" aria-hidden="true">
    <!-- Canvas for frame sequence, or <video> for ambient loop -->
    <canvas id="hero-canvas"></canvas>
  </div>
  <div class="sp-hero-overlay" aria-hidden="true"></div>
  <div class="center cover-center" style="position:relative;z-index:2">
    <!-- Same content structure as gradient variant -->
  </div>
</section>
```

```css
.sp-hero--video { position: relative; }
.sp-hero-media {
  position: absolute;
  inset: 0;
  z-index: 0;
}
.sp-hero-media canvas,
.sp-hero-media video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sp-hero-overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  background: linear-gradient(to bottom, rgba(0,0,0,0.6), var(--sp-bg));
}
```

### hero — Variant: product-demo

Split layout: copy left, product visual right.

```html
<section class="sp-hero cover" aria-labelledby="hero-heading">
  <div class="center cover-center" style="--center-max: var(--sp-max-width)">
    <div class="with-sidebar">
      <div class="stack" style="--stack-space: var(--sp-space-lg)">
        <p class="sp-eyebrow">{{eyebrow}}</p>
        <h1 id="hero-heading" class="sp-hero-title">{{headline}}</h1>
        <p class="sp-hero-subtitle">{{subheadline}}</p>
        <a href="{{cta_action}}" class="btn-primary">{{cta_text}}</a>
      </div>
      <div class="sp-hero-visual frame" style="--sidebar-width: 45%; --frame-ratio: 4/3">
        <!-- Inline SVG illustration or product screenshot -->
      </div>
    </div>
  </div>
</section>
```

### problem / agitation

Empathy-driven section that names the audience's pain.

```html
<section class="sp-section sp-problem reveal" aria-labelledby="problem-heading">
  <div class="center">
    <div class="stack" style="--stack-space: var(--sp-space-lg)">
      <h2 id="problem-heading" class="sp-section-title">{{headline}}</h2>
      <p class="sp-section-body">{{body_copy}}</p>
      <ul class="sp-pain-list stack" style="--stack-space: var(--sp-space-sm)" role="list">
        <!-- Pain points as list items -->
        <li class="sp-pain-item">{{pain_point}}</li>
      </ul>
    </div>
  </div>
</section>
```

```css
.sp-section {
  padding-block: var(--sp-space-xl);
}
.sp-section-title {
  font-size: var(--sp-text-3xl);
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.1;
}
.sp-section-body {
  font-size: var(--sp-text-lg);
  color: var(--sp-muted);
  max-inline-size: 60ch;
  line-height: 1.7;
}
.sp-pain-item {
  font-size: var(--sp-text-base);
  color: var(--sp-muted);
  padding-inline-start: var(--sp-space-md);
  border-inline-start: 3px solid var(--sp-accent);
}
```

### solution / features

Grid layout showcasing product capabilities.

```html
<section class="sp-section sp-features" aria-labelledby="features-heading">
  <div class="center" style="--center-max: var(--sp-max-width)">
    <div class="stack" style="--stack-space: var(--sp-space-xl)">
      <div class="stack center" style="--stack-space: var(--sp-space-sm); text-align:center">
        <h2 id="features-heading" class="sp-section-title">{{headline}}</h2>
        <p class="sp-section-body" style="margin-inline:auto">{{subheadline}}</p>
      </div>
      <div class="auto-grid reveal-stagger" style="--grid-min: 280px">
        <article class="sp-feature-card card stack">
          <div class="sp-feature-icon" aria-hidden="true">
            <!-- Inline SVG icon -->
          </div>
          <h3>{{feature_title}}</h3>
          <p>{{feature_description}}</p>
        </article>
        <!-- Repeat for each feature -->
      </div>
    </div>
  </div>
</section>
```

```css
.sp-feature-card {
  padding: var(--sp-space-lg);
  background: var(--sp-surface);
  border: 1px solid var(--sp-border);
  border-radius: var(--sp-radius-lg);
}
.sp-feature-card h3 {
  font-size: var(--sp-text-lg);
  font-weight: 700;
}
.sp-feature-card p {
  font-size: var(--sp-text-sm);
  color: var(--sp-muted);
  line-height: 1.6;
}
.sp-feature-icon {
  width: 48px;
  height: 48px;
  color: var(--sp-accent);
}
.sp-feature-icon svg {
  width: 100%;
  height: 100%;
}
```

### benefits (before/after or icon-grid)

```html
<section class="sp-section sp-benefits reveal" aria-labelledby="benefits-heading">
  <div class="center" style="--center-max: var(--sp-max-width)">
    <div class="stack" style="--stack-space: var(--sp-space-xl)">
      <h2 id="benefits-heading" class="sp-section-title center" style="text-align:center">{{headline}}</h2>
      <div class="switcher">
        <div class="sp-before stack">
          <h3 class="sp-contrast-label sp-contrast-label--before">Before</h3>
          <ul class="stack" style="--stack-space: var(--sp-space-xs)" role="list">
            <li class="sp-benefit-item sp-benefit-item--negative">{{before_point}}</li>
          </ul>
        </div>
        <div class="sp-after stack">
          <h3 class="sp-contrast-label sp-contrast-label--after">After</h3>
          <ul class="stack" style="--stack-space: var(--sp-space-xs)" role="list">
            <li class="sp-benefit-item sp-benefit-item--positive">{{after_point}}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>
```

```css
.sp-contrast-label {
  font-size: var(--sp-text-sm);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.sp-contrast-label--before { color: var(--sp-muted); }
.sp-contrast-label--after  { color: var(--sp-accent); }
.sp-benefit-item {
  font-size: var(--sp-text-base);
  padding: var(--sp-space-sm);
  border-radius: var(--sp-radius-sm);
}
.sp-benefit-item--negative {
  color: var(--sp-muted);
  text-decoration: line-through;
  text-decoration-color: var(--sp-muted);
}
.sp-benefit-item--positive {
  color: var(--sp-fg);
  background: rgba(255,255,255,0.03);
  border-inline-start: 3px solid var(--sp-accent);
}
```

### social-proof

```html
<section class="sp-section sp-social-proof" aria-labelledby="proof-heading">
  <div class="center" style="--center-max: var(--sp-max-width)">
    <div class="stack" style="--stack-space: var(--sp-space-xl)">

      <!-- Logo Wall -->
      <div class="sp-logo-wall cluster reveal" style="justify-content:center; --cluster-gap: var(--sp-space-lg)">
        <!-- Inline SVG logos, grayscale by default -->
        <div class="sp-logo" aria-label="Company name"><!-- SVG --></div>
      </div>

      <!-- Metrics Counter -->
      <div class="auto-grid reveal-stagger" style="--grid-min: 180px; text-align:center">
        <div class="sp-metric stack" style="--stack-space: var(--sp-space-xs)">
          <span class="sp-metric-number">{{number}}</span>
          <span class="sp-metric-label">{{label}}</span>
        </div>
      </div>

      <!-- Testimonials -->
      <div class="switcher reveal-stagger">
        <blockquote class="sp-testimonial stack">
          <p>"{{quote}}"</p>
          <footer>
            <cite class="sp-testimonial-author">{{name}}</cite>
            <span class="sp-testimonial-role">{{role}}</span>
          </footer>
        </blockquote>
      </div>

    </div>
  </div>
</section>
```

```css
.sp-logo {
  height: 32px;
  opacity: 0.5;
  filter: grayscale(1) brightness(2);
  transition: opacity var(--sp-duration-fast) var(--sp-ease);
}
.sp-logo:hover { opacity: 1; }
.sp-metric-number {
  font-size: var(--sp-text-3xl);
  font-weight: 900;
  color: var(--sp-accent);
  letter-spacing: -0.03em;
}
.sp-metric-label {
  font-size: var(--sp-text-sm);
  color: var(--sp-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.sp-testimonial {
  padding: var(--sp-space-lg);
  background: var(--sp-surface);
  border: 1px solid var(--sp-border);
  border-radius: var(--sp-radius-lg);
}
.sp-testimonial p {
  font-size: var(--sp-text-lg);
  font-style: italic;
  line-height: 1.7;
  color: var(--sp-fg);
}
.sp-testimonial-author {
  font-weight: 700;
  font-style: normal;
  color: var(--sp-fg);
}
.sp-testimonial-role {
  font-size: var(--sp-text-sm);
  color: var(--sp-muted);
}
```

### how-it-works

Numbered steps with visual progression.

```html
<section class="sp-section sp-how-it-works" aria-labelledby="steps-heading">
  <div class="center">
    <div class="stack" style="--stack-space: var(--sp-space-xl)">
      <h2 id="steps-heading" class="sp-section-title" style="text-align:center">{{headline}}</h2>
      <ol class="sp-steps stack reveal-stagger" style="--stack-space: var(--sp-space-lg)">
        <li class="sp-step with-sidebar">
          <div class="sp-step-number" aria-hidden="true">01</div>
          <div class="stack" style="--stack-space: var(--sp-space-xs)">
            <h3>{{step_title}}</h3>
            <p>{{step_description}}</p>
          </div>
        </li>
      </ol>
    </div>
  </div>
</section>
```

```css
.sp-steps {
  list-style: none;
  counter-reset: step;
}
.sp-step {
  --sidebar-width: 80px;
  align-items: flex-start;
}
.sp-step-number {
  font-size: var(--sp-text-3xl);
  font-weight: 900;
  color: var(--sp-accent);
  opacity: 0.3;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}
.sp-step h3 {
  font-size: var(--sp-text-xl);
  font-weight: 700;
}
.sp-step p {
  font-size: var(--sp-text-base);
  color: var(--sp-muted);
  line-height: 1.6;
}
```

### pricing

```html
<section class="sp-section sp-pricing" aria-labelledby="pricing-heading">
  <div class="center" style="--center-max: var(--sp-max-width)">
    <div class="stack" style="--stack-space: var(--sp-space-xl)">
      <div class="stack center" style="text-align:center; --stack-space: var(--sp-space-sm)">
        <h2 id="pricing-heading" class="sp-section-title">{{headline}}</h2>
        <p class="sp-section-body" style="margin-inline:auto">{{subheadline}}</p>
      </div>

      <!-- Single Plan (most common for sales pages) -->
      <div class="sp-price-card stack center reveal" style="--center-max: 480px">
        <div class="sp-price-tag stack" style="--stack-space: 0; text-align:center">
          <span class="sp-price-anchor">{{anchor_price}}</span>
          <span class="sp-price-current">{{main_price}}</span>
          <span class="sp-price-period">{{installments}}</span>
        </div>
        <ul class="sp-price-features stack" style="--stack-space: var(--sp-space-xs)" role="list">
          <li>{{deliverable}}</li>
        </ul>
        <a href="{{cta_action}}" class="btn-primary btn-full">{{cta_text}}</a>
        <p class="sp-price-guarantee">{{guarantee}}</p>
      </div>
    </div>
  </div>
</section>
```

```css
.sp-price-card {
  padding: var(--sp-space-xl) var(--sp-space-lg);
  background: var(--sp-surface);
  border: 2px solid var(--sp-accent);
  border-radius: var(--sp-radius-lg);
}
.sp-price-anchor {
  font-size: var(--sp-text-lg);
  color: var(--sp-muted);
  text-decoration: line-through;
}
.sp-price-current {
  font-size: var(--sp-text-3xl);
  font-weight: 900;
  color: var(--sp-fg);
}
.sp-price-period {
  font-size: var(--sp-text-sm);
  color: var(--sp-muted);
}
.sp-price-features li {
  font-size: var(--sp-text-base);
  padding-block: var(--sp-space-xs);
  border-block-end: 1px solid var(--sp-border);
}
.sp-price-features li::before {
  content: "\2713\0020";
  color: var(--sp-accent);
  font-weight: 700;
}
.sp-price-guarantee {
  font-size: var(--sp-text-sm);
  color: var(--sp-muted);
  text-align: center;
}
.btn-full {
  display: block;
  text-align: center;
  width: 100%;
}
```

### objection-handler (accordion FAQ)

```html
<section class="sp-section sp-faq" aria-labelledby="faq-heading">
  <div class="center">
    <div class="stack" style="--stack-space: var(--sp-space-xl)">
      <h2 id="faq-heading" class="sp-section-title" style="text-align:center">{{headline}}</h2>
      <div class="sp-accordion stack" style="--stack-space: 0">
        <details class="sp-accordion-item">
          <summary class="sp-accordion-trigger">{{question}}</summary>
          <div class="sp-accordion-content">
            <p>{{answer}}</p>
          </div>
        </details>
      </div>
    </div>
  </div>
</section>
```

```css
.sp-accordion-item {
  border-block-end: 1px solid var(--sp-border);
}
.sp-accordion-trigger {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--sp-space-md) 0;
  font-size: var(--sp-text-lg);
  font-weight: 600;
  cursor: pointer;
  list-style: none;
  color: var(--sp-fg);
}
.sp-accordion-trigger::-webkit-details-marker { display: none; }
.sp-accordion-trigger::after {
  content: "+";
  font-size: var(--sp-text-xl);
  color: var(--sp-muted);
  transition: transform var(--sp-duration-fast) var(--sp-ease);
}
details[open] .sp-accordion-trigger::after {
  transform: rotate(45deg);
}
.sp-accordion-content {
  padding-block-end: var(--sp-space-md);
}
.sp-accordion-content p {
  font-size: var(--sp-text-base);
  color: var(--sp-muted);
  line-height: 1.7;
}
```

### guarantee

```html
<section class="sp-section sp-guarantee reveal" aria-labelledby="guarantee-heading">
  <div class="center">
    <div class="sp-guarantee-card cluster" style="--cluster-gap: var(--sp-space-lg)">
      <div class="sp-guarantee-badge" aria-hidden="true">
        <svg viewBox="0 0 80 80" width="80" height="80" fill="none">
          <circle cx="40" cy="40" r="38" stroke="currentColor" stroke-width="2"/>
          <path d="M25 42l10 10 20-24" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="stack" style="--stack-space: var(--sp-space-sm)">
        <h2 id="guarantee-heading" class="sp-section-title">{{headline}}</h2>
        <p class="sp-section-body">{{body_copy}}</p>
      </div>
    </div>
  </div>
</section>
```

```css
.sp-guarantee-card {
  padding: var(--sp-space-lg);
  background: var(--sp-surface);
  border: 1px solid var(--sp-border);
  border-radius: var(--sp-radius-lg);
  align-items: flex-start;
}
.sp-guarantee-badge {
  flex-shrink: 0;
  color: var(--sp-accent);
}
```

### final-cta

```html
<section class="sp-section sp-final-cta" aria-labelledby="final-cta-heading">
  <div class="center" style="text-align:center">
    <div class="stack" style="--stack-space: var(--sp-space-lg)">
      <h2 id="final-cta-heading" class="sp-section-title">{{headline}}</h2>
      <p class="sp-section-body" style="margin-inline:auto">{{body_copy}}</p>
      <div>
        <a href="{{cta_action}}" class="btn-primary btn-lg">{{cta_text}}</a>
      </div>
      <p class="sp-reassurance">{{trust_signal}}</p>
    </div>
  </div>
</section>
```

```css
.sp-final-cta {
  padding-block: var(--sp-space-2xl);
  background: var(--sp-surface);
}
.btn-lg {
  padding: var(--sp-space-md) var(--sp-space-xl);
  font-size: var(--sp-text-lg);
}
.sp-reassurance {
  font-size: var(--sp-text-sm);
  color: var(--sp-muted);
}
```

### footer

```html
<footer class="sp-footer">
  <div class="center">
    <div class="cluster" style="justify-content: space-between">
      <p class="sp-footer-copy">&copy; {{year}} {{brand}}. All rights reserved.</p>
      <nav class="cluster" style="--cluster-gap: var(--sp-space-md)" aria-label="Footer links">
        <a href="{{privacy_url}}">Privacy</a>
        <a href="{{terms_url}}">Terms</a>
      </nav>
    </div>
  </div>
</footer>
```

```css
.sp-footer {
  padding-block: var(--sp-space-lg);
  border-block-start: 1px solid var(--sp-border);
  font-size: var(--sp-text-sm);
  color: var(--sp-muted);
}
.sp-footer a {
  color: var(--sp-muted);
  text-decoration: none;
}
.sp-footer a:hover {
  color: var(--sp-fg);
}
```

---

## F. Performance Checklist

The builder verifies ALL items before producing final output. Any failure blocks output with a specific fix recommendation.

### Mandatory Checks

- [ ] **File size** < 300KB (with animations) or < 100KB (without)
- [ ] **No external requests** — zero CDN, tracking, or third-party scripts at runtime
- [ ] **Images** are inline SVG or base64 data URIs only
- [ ] **CSS animations** use only `transform` and `opacity` (GPU-composited)
- [ ] **`prefers-reduced-motion`** respected — all durations set to 0ms
- [ ] **Font loading** — system font stack OR single `@import` with `font-display: swap`
- [ ] **Semantic HTML** — `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>` used correctly
- [ ] **Single H1** — exactly one `<h1>`, logical heading hierarchy (no skipped levels)
- [ ] **Focus states** — all interactive elements have visible `:focus-visible` outlines
- [ ] **Color contrast** >= 4.5:1 for normal text, >= 3:1 for large text (>= 24px or >= 18.66px bold)
- [ ] **Touch targets** — all interactive elements >= 44x44px on mobile
- [ ] **Skip link** — hidden "Skip to content" link present
- [ ] **Alt text** — all `<img>` have `alt`, decorative SVGs have `aria-hidden="true"`
- [ ] **lang attribute** — `<html lang="...">` set correctly
- [ ] **No console errors** — page loads cleanly with no JS errors
- [ ] **No unused CSS** — every rule matches at least one element

### Performance Targets

| Metric | Target |
|--------|--------|
| File size (no animations) | < 100KB |
| File size (with animations) | < 300KB |
| File size (with canvas frames) | < 2MB (frames are heavy) |
| First Contentful Paint | < 1.5s |
| Largest Contentful Paint | < 2.5s |
| Cumulative Layout Shift | < 0.1 |
| Total Blocking Time | < 200ms |

### Size Budget Breakdown

| Component | Budget |
|-----------|--------|
| HTML structure | < 15KB |
| CSS (all styles) | < 25KB |
| Inline SVGs | < 30KB total |
| JavaScript | < 10KB (excluding frame data) |
| Base64 frame data | < 2MB (if canvas sequence used) |

---

## G. SEO Template

Every page includes this `<head>` structure. Values are populated from Phase 5 narrative and Phase 1 discovery.

### Meta Tags

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{{phase_5.sections[0].subheadline || phase_1.promise}}">
<meta name="robots" content="index, follow">

<!-- Open Graph -->
<meta property="og:title" content="{{phase_5.sections[0].headline}}">
<meta property="og:description" content="{{phase_5.sections[0].subheadline}}">
<meta property="og:type" content="website">
<meta property="og:url" content="{{canonical_url}}">
<meta property="og:image" content="{{og_image_url_if_available}}">
<meta property="og:site_name" content="{{brand_name}}">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{phase_5.sections[0].headline}}">
<meta name="twitter:description" content="{{phase_5.sections[0].subheadline}}">

<!-- Canonical -->
<link rel="canonical" href="{{canonical_url}}">

<title>{{headline}} | {{brand_name}}</title>
```

### JSON-LD Structured Data

Include one or both schemas based on page content.

#### Product Schema (when pricing section exists)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{product_name}}",
  "description": "{{promise}}",
  "brand": {
    "@type": "Brand",
    "name": "{{brand_name}}"
  },
  "offers": {
    "@type": "Offer",
    "price": "{{numeric_price}}",
    "priceCurrency": "{{currency_code}}",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

#### FAQ Schema (when objection-handler/FAQ section exists)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{{question}}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{answer}}"
      }
    }
  ]
}
</script>
```

---

## Build Process Summary

When invoked, the builder follows this sequence:

1. **Read state** — Load `state.json`, extract Phase 4 tokens + Phase 5 sections + Phase 6 fusion decisions
2. **Select template** — Use `growthOS/templates/sales-pages/base.html` as starting structure
3. **Map tokens** — Populate all `--sp-*` custom properties from Phase 4 `design_tokens`
4. **Build sections** — For each section in Phase 5's `sections` array, select the matching template from Section E and populate with approved copy
5. **Add animations** — Based on Phase 4 `animation_strategy`, include appropriate tiers from Section D
6. **Apply layout** — Use Section C primitives for responsive structure
7. **Insert SEO** — Populate Section G meta tags and structured data
8. **Run checklist** — Verify all items in Section F pass
9. **Output** — Write final `index.html` to `growthOS/output/sales-pages/{slug}/index.html`
10. **Copy to preview** — Save to `previews/phase-7-build.html`

---

## File References

| Resource | Path |
|----------|------|
| This skill | `growthOS/skills/sales-page-builder/SKILL.md` |
| Base template | `growthOS/templates/sales-pages/base.html` |
| Master pipeline skill | `growthOS/skills/sales-page/SKILL.md` |
| Pipeline state schema | `growthOS/templates/sales-pages/_PIPELINE-STATE.md` |
| Landing page skill (simpler) | `growthOS/skills/landing-page-design/SKILL.md` |
| Design system (carousel) | `growthOS/design-system/DESIGN-SYSTEM.md` |
