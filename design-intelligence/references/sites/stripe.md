---
name: Stripe
url: https://stripe.com
category: [saas, developer-tool]
design_style: Premium fintech with animated mesh gradients, bold dark navy, and restrained purple accents
last_analyzed: 2026-04-16
---

## Visual Identity

### Brand Colors (Primary)

| Token | Hex | Usage |
|-------|-----|-------|
| Stripe Indigo | `#635BFF` | Primary brand, CTAs, links |
| Downriver | `#0A2540` | Dark backgrounds, headers, hero sections |
| Slate | `#425466` | Secondary text on dark backgrounds |
| Black Squeeze | `#F6F9FC` | Light section backgrounds |
| White | `#FFFFFF` | Cards, content areas |
| Teal Accent | `#00D4AA` | Success states, positive indicators |
| Coral | `#FF7A59` | Warnings, attention elements |

### Extended Palette (Mesh Gradient)

| Hex | Role |
|-----|------|
| `#6ec3f4` | Gradient color 1 (sky blue) |
| `#3a3aff` | Gradient color 2 (deep blue) |
| `#ff61ab` | Gradient color 3 (pink) |
| `#E63946` | Gradient color 4 (red) |

Alternative gradient set used in various sections:
- `#a960ee` (purple)
- `#ff333d` (red)
- `#90e0ff` (cyan)
- `#ffcb57` (gold)

### Typography

| Element | Font | Size | Weight | Line-Height | Letter-Spacing |
|---------|------|------|--------|-------------|----------------|
| **Font stack** | `sohne-var, "Helvetica Neue", Arial, sans-serif` | -- | -- | -- | -- |
| Header 1 | Sohne-var | 38px | 500 | 48px | 0px |
| Header 2 | Sohne-var | 18px | 500 | 28px | 0px |
| Body | Sohne-var | 18px | 300 | 28px | 0px |
| Elements base | Sohne, system-ui, sans-serif | 14px | 500 | -- | -- |

**Note:** Sohne-var is a variable font by Klim Type Foundry (Kris Sowersby, 2019). It replaced Camphor in Stripe's 2020 redesign. Described as "the memory of Akzidenz-Grotesk framed through the reality of Helvetica." Licensed, not freely available -- use `Inter` or `DM Sans` as free alternatives.

### Spacing & Layout

| Token | Value |
|-------|-------|
| Spacing unit | 2px (base) |
| Grid row gap | 15px |
| Section gap | 24px |
| Gradient padding | 120px |
| Gradient title margin | 100px |
| Layout | 4-column grid, left-aligned balance |
| Total page assets | ~26 (mostly HTML elements, not images) |

### Border Radius & Shadows

| Token | Value |
|-------|-------|
| Default border-radius | 4px |
| Card border-radius | 8px |
| Button border-radius (mobile) | 20px |
| Card shadow | `0px 1px 1px rgba(0, 0, 0, 0.03), 0px 3px 6px rgba(18, 42, 66, 0.02)` |

## Key Techniques

### 1. WebGL Animated Mesh Gradient (Signature Effect)

Stripe's hero uses a custom WebGL implementation (~800 lines, ~10KB) called `minigl` with a `Gradient` class. This is NOT a CSS gradient -- it is a full WebGL canvas animation.

**Architecture:**
- Canvas element with WebGL context
- Vertex + fragment shaders for rendering
- Mesh geometry classes for animation state
- Noise functions + sinusoidal UV modulation for liquid surface effect
- `ScrollObserver` to pause when off-viewport

**CSS setup:**
```css
#gradient-canvas {
  width: 100%;
  height: 100%;
  --gradient-color-1: #6ec3f4;
  --gradient-color-2: #3a3aff;
  --gradient-color-3: #ff61ab;
  --gradient-color-4: #E63946;
}
```

**Container transform (the signature diagonal):**
```css
.stripe-gradient-section {
  transform: skewY(-12deg);
  overflow: hidden;
  --section-skew-Y: -12deg;
  --section-angle-sin: 0.212;
  --transform-origin-x: calc(var(--section-gap) * 0.8);
}
```

**Color normalization (JS):**
```javascript
// Converts hex to 0-1 range for WebGL
function normalizeColor(hexCode) {
  return [
    ((hexCode >> 16) & 255) / 255,
    ((hexCode >> 8) & 255) / 255,
    (hexCode & 255) / 255
  ];
}
```

**Why WebGL over CSS animation:** CSS gradient animation causes high CPU/RAM usage due to high-frequency repaints. WebGL offloads to the GPU, achieving smooth 60fps with minimal performance cost.

### 2. Text Layering with Blend Modes

Three text layers create the signature text-over-gradient effect:

```css
.text-above {
  position: relative;
  z-index: 2;
}

.text-under-blended {
  mix-blend-mode: color-burn;
  color: #3a3a3a;
}

.text-under-overlay {
  opacity: 0.2;
}
```

### 3. Accessible Color System

Stripe built a perceptually-uniform color system documented on their blog. Each color ramp maintains WCAG contrast ratios at every step.

### 4. Dark Section Styling

```css
.dark-section {
  background-color: #0A2540;
  color: #adbdcc;
}

.dark-section h2 {
  color: #ffffff;
}

.dark-section .highlight {
  color: #635BFF;
}
```

## What Makes It Work

### Psychological Principles

1. **Premium Perception via Restraint** -- The dark navy (#0A2540) paired with a single vibrant accent (#635BFF) signals institutional trust and premium quality. Fintech users equate visual restraint with financial seriousness.

2. **Motion as Trust Signal** -- The mesh gradient is organic, slow, and continuous. It communicates "alive and working" without being distracting. Subconsciously conveys uptime and reliability.

3. **Progressive Disclosure** -- Content reveals through scroll, with each section introducing ONE concept. Cognitive load stays minimal despite high information density.

4. **Diagonal Geometry** -- The `skewY(-12deg)` transform breaks horizontal monotony and creates forward momentum. The angle suggests progress and movement.

5. **Dark-to-Light Narrative** -- Hero sections use dark backgrounds (immersion, focus) while feature sections use light backgrounds (clarity, detail). This alternation maintains visual engagement.

## Patterns to Extract

### Reusable Pattern 1: Gradient Hero with Diagonal Cut
- Full-bleed WebGL/CSS gradient background
- Container with `skewY()` transform and overflow hidden
- Content counter-rotated to stay horizontal
- Text layered with blend modes

### Reusable Pattern 2: Feature Section Card Grid
- 4-column grid on desktop, stacking to 1 on mobile
- Cards with subtle shadow: `0px 1px 1px rgba(0,0,0,0.03), 0px 3px 6px rgba(18,42,66,0.02)`
- 8px border-radius
- White background on light gray (#F6F9FC) section

### Reusable Pattern 3: Dark Code Editor Block
- Syntax-highlighted code block with dark background
- Animated typing effect or tabbed language switching
- Demonstrates product capability inline

### Reusable Pattern 4: Alternating Light/Dark Sections
- Dark (#0A2540) for immersive hero/demo moments
- Light (#F6F9FC) for informational/feature moments
- White (#FFFFFF) for cards and interactive elements

## Code Snippets

### Minimal Stripe-Style Gradient (CSS fallback)

```css
.stripe-gradient-fallback {
  background: linear-gradient(
    135deg,
    #635BFF 0%,
    #0A2540 50%,
    #00D4AA 100%
  );
  animation: gradientShift 8s ease infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
```

### Stripe Dark Section

```css
.stripe-dark {
  background: #0A2540;
  color: #adbdcc;
  padding: 120px 0;
  font-family: sohne-var, "Helvetica Neue", Arial, sans-serif;
}

.stripe-dark h1 {
  font-size: 38px;
  font-weight: 500;
  line-height: 48px;
  color: #ffffff;
}

.stripe-dark p {
  font-size: 18px;
  font-weight: 300;
  line-height: 28px;
  color: #adbdcc;
}

.stripe-dark .cta {
  background: #635BFF;
  color: #ffffff;
  border-radius: 20px;
  padding: 12px 24px;
  font-weight: 500;
  border: none;
  transition: background 0.15s ease;
}

.stripe-dark .cta:hover {
  background: #7A73FF;
}
```

### Diagonal Section Container

```css
.diagonal-section {
  transform: skewY(-12deg);
  overflow: hidden;
  padding: 120px 0;
}

.diagonal-section__content {
  transform: skewY(12deg); /* counter-rotate */
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 24px;
}
```

### Card with Stripe Shadow

```css
.stripe-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 24px;
  box-shadow:
    0px 1px 1px rgba(0, 0, 0, 0.03),
    0px 3px 6px rgba(18, 42, 66, 0.02);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.stripe-card:hover {
  box-shadow:
    0px 2px 4px rgba(0, 0, 0, 0.04),
    0px 8px 16px rgba(18, 42, 66, 0.04);
  transform: translateY(-2px);
}
```

## Anti-Patterns to Avoid

1. **Do NOT use CSS `background: linear-gradient` with animation for the mesh effect.** It causes repaints on every frame, destroys performance on mobile. Stripe uses WebGL for a reason -- use canvas/WebGL or a static gradient fallback.

2. **Do NOT overuse the diagonal skew.** Stripe uses it exactly once (hero). Repeating it throughout a page creates visual chaos and makes text hard to read.

3. **Do NOT copy the 73-color palette.** Stripe's homepage uses 73 colors because each element is hand-crafted HTML. For most projects, stick to 5-7 colors maximum from their system.

4. **Do NOT set body text to `font-weight: 300` without a high-quality variable font.** Sohne-var renders beautifully at 300; most system fonts become illegible. Use 400 weight with Inter/DM Sans as alternatives.

5. **Do NOT mix the purple (#635BFF) with bright competing colors.** Stripe's palette works because the purple is the ONLY vibrant accent against muted navy/gray. Adding bright reds, oranges, or greens alongside it destroys the restraint that makes it premium.

6. **Do NOT use the `mix-blend-mode: color-burn` text technique on variable backgrounds.** It only works reliably when the background gradient is controlled. On user-generated or dynamic content, it produces illegible results.
