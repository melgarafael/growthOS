---
technique: Fluid Math Positioning (Utopia + Every Layout)
complexity: intermediate
browser_support: CSS clamp() 92%+ global; Flexbox/Grid 97%+
performance_impact: low
---

## Overview

This technique combines two complementary systems:

1. **Utopia (utopia.fyi)** -- fluid type and space scales using CSS `clamp()`. Instead of breakpoint-based
   font sizes and spacing, values interpolate linearly between a minimum viewport (e.g. 320px) and
   maximum viewport (e.g. 1440px). No media queries needed for sizing.

2. **Every Layout (every-layout.dev)** -- intrinsic layout primitives (Stack, Cluster, Sidebar, Switcher,
   Cover, etc.) that use Flexbox properties to create responsive compositions without `@media` queries.

Together they form a complete, breakpoint-free design system for typography, spacing, and layout.

**Where it is used:** Design systems at Clearleft, BBC, Gov.uk, and any project that values
mathematical precision in fluid sizing.

---

## Implementation

### Part 1: Fluid Typography Scale

The `clamp()` formula: `clamp(minSize, preferredSize, maxSize)`

Where `preferredSize` = `yIntercept(rem) + slope * 100vw`

```
slope = (maxSize - minSize) / (maxViewport - minViewport)
yIntercept = minSize - slope * minViewport
```

For a base of 16px at 320px viewport, scaling to 24px at 1440px viewport:

```
slope = (24 - 16) / (1440 - 320) = 8 / 1120 = 0.00714
yIntercept = 16 - (0.00714 * 320) = 16 - 2.286 = 13.714px = 0.857rem
preferred = 0.857rem + 0.714vw
Result: clamp(1rem, 0.857rem + 0.714vw, 1.5rem)
```

### Complete Fluid Design System (copy-paste ready)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fluid Math Positioning System</title>
<style>
  /* ==============================================================
     FLUID TYPE & SPACE SCALE
     Based on Utopia methodology
     Min viewport: 320px | Max viewport: 1440px
     Base size: 16px (1rem) -> 20px (1.25rem)
     Type scale: 1.2 (minor third) at min, 1.25 (major third) at max
     ============================================================== */

  :root {
    /* ----- FLUID TYPE SCALE ----- */
    /* Step -2: 11.11px -> 12.80px */
    --font-size--2: clamp(0.6944rem, 0.6622rem + 0.1613vw, 0.8rem);

    /* Step -1: 13.33px -> 16.00px */
    --font-size--1: clamp(0.8331rem, 0.7831rem + 0.25vw, 1rem);

    /* Step 0 (base): 16px -> 20px */
    --font-size-0: clamp(1rem, 0.9286rem + 0.3571vw, 1.25rem);

    /* Step 1: 19.20px -> 25.00px */
    --font-size-1: clamp(1.2rem, 1.0964rem + 0.5179vw, 1.5625rem);

    /* Step 2: 23.04px -> 31.25px */
    --font-size-2: clamp(1.44rem, 1.2929rem + 0.7357vw, 1.9531rem);

    /* Step 3: 27.65px -> 39.06px */
    --font-size-3: clamp(1.7281rem, 1.5225rem + 1.0282vw, 2.4413rem);

    /* Step 4: 33.18px -> 48.83px */
    --font-size-4: clamp(2.0736rem, 1.7905rem + 1.4155vw, 3.0519rem);

    /* Step 5: 39.81px -> 61.04px */
    --font-size-5: clamp(2.4883rem, 2.1028rem + 1.9277vw, 3.815rem);

    /* ----- FLUID SPACE SCALE ----- */
    /* T-shirt sizes derived from base step 0 */

    /* 3XS: 4px -> 5px */
    --space-3xs: clamp(0.25rem, 0.2321rem + 0.0893vw, 0.3125rem);

    /* 2XS: 8px -> 10px */
    --space-2xs: clamp(0.5rem, 0.4643rem + 0.1786vw, 0.625rem);

    /* XS: 12px -> 15px */
    --space-xs: clamp(0.75rem, 0.6964rem + 0.2679vw, 0.9375rem);

    /* S: 16px -> 20px */
    --space-s: clamp(1rem, 0.9286rem + 0.3571vw, 1.25rem);

    /* M: 24px -> 30px */
    --space-m: clamp(1.5rem, 1.3929rem + 0.5357vw, 1.875rem);

    /* L: 32px -> 40px */
    --space-l: clamp(2rem, 1.8571rem + 0.7143vw, 2.5rem);

    /* XL: 48px -> 60px */
    --space-xl: clamp(3rem, 2.7857rem + 1.0714vw, 3.75rem);

    /* 2XL: 64px -> 80px */
    --space-2xl: clamp(4rem, 3.7143rem + 1.4286vw, 5rem);

    /* 3XL: 96px -> 120px */
    --space-3xl: clamp(6rem, 5.5714rem + 2.1429vw, 7.5rem);

    /* ----- ONE-UP PAIRS (min of one step, max of the next) ----- */
    /* Useful for responsive spacing that "jumps" a size */
    --space-s-m: clamp(1rem, 0.7857rem + 1.0714vw, 1.875rem);
    --space-m-l: clamp(1.5rem, 1.25rem + 1.25vw, 2.5rem);
    --space-l-xl: clamp(2rem, 1.5714rem + 2.1429vw, 3.75rem);
    --space-xl-2xl: clamp(3rem, 2.5rem + 2.5vw, 5rem);

    /* ----- LAYOUT ----- */
    --measure: 65ch;                /* max line width */
    --gutter: var(--space-s-m);     /* responsive gutter */
    --border-radius: 0.25rem;

    /* ----- COLORS (neutral example) ----- */
    --color-text: #1a1a2e;
    --color-bg: #ffffff;
    --color-muted: #6b7280;
    --color-accent: #3b82f6;
    --color-border: #e5e7eb;
  }

  /* ==============================================================
     RESET
     ============================================================== */
  *,
  *::before,
  *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  html {
    font-size: 100%; /* 16px base */
    -webkit-text-size-adjust: 100%;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, sans-serif;
    font-size: var(--font-size-0);
    line-height: 1.6;
    color: var(--color-text);
    background: var(--color-bg);
  }

  /* ==============================================================
     TYPOGRAPHY UTILITIES
     ============================================================== */
  .text--2 { font-size: var(--font-size--2); }
  .text--1 { font-size: var(--font-size--1); }
  .text-0  { font-size: var(--font-size-0); }
  .text-1  { font-size: var(--font-size-1); }
  .text-2  { font-size: var(--font-size-2); }
  .text-3  { font-size: var(--font-size-3); }
  .text-4  { font-size: var(--font-size-4); }
  .text-5  { font-size: var(--font-size-5); }

  h1 { font-size: var(--font-size-5); line-height: 1.1; letter-spacing: -0.02em; }
  h2 { font-size: var(--font-size-4); line-height: 1.15; letter-spacing: -0.015em; }
  h3 { font-size: var(--font-size-3); line-height: 1.2; }
  h4 { font-size: var(--font-size-2); line-height: 1.3; }
  h5 { font-size: var(--font-size-1); line-height: 1.4; }
  h6 { font-size: var(--font-size-0); line-height: 1.5; font-weight: 600; }

  p { max-width: var(--measure); }

  /* ==============================================================
     EVERY LAYOUT PRIMITIVES
     ============================================================== */

  /* ----- THE STACK ----- */
  /* Vertical spacing between child elements */
  .stack {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  .stack > * {
    margin-block: 0; /* reset */
  }

  .stack > * + * {
    margin-block-start: var(--stack-space, var(--space-s));
  }

  /* Modifier: larger spacing for sections */
  .stack[data-space="l"] { --stack-space: var(--space-l); }
  .stack[data-space="xl"] { --stack-space: var(--space-xl); }
  .stack[data-space="2xl"] { --stack-space: var(--space-2xl); }

  /* ----- THE CLUSTER ----- */
  /* Horizontal wrapping group with consistent gaps */
  .cluster {
    display: flex;
    flex-wrap: wrap;
    gap: var(--cluster-space, var(--space-s));
    justify-content: var(--cluster-justify, flex-start);
    align-items: var(--cluster-align, center);
  }

  /* ----- THE SIDEBAR ----- */
  /* Main + sidebar layout without media queries */
  .sidebar {
    display: flex;
    flex-wrap: wrap;
    gap: var(--gutter);
  }

  .sidebar > :first-child {
    /* Sidebar element */
    flex-basis: var(--sidebar-width, 20rem);
    flex-grow: 1;
  }

  .sidebar > :last-child {
    /* Main content element */
    flex-basis: 0;
    flex-grow: 999;
    min-inline-size: var(--sidebar-threshold, 50%);
  }

  /* ----- THE SWITCHER ----- */
  /* Switches from horizontal to vertical when space is tight */
  .switcher {
    display: flex;
    flex-wrap: wrap;
    gap: var(--gutter);
  }

  .switcher > * {
    /*
      When container < threshold, each child gets full width.
      When container >= threshold, children share space equally.
      The calc() trick:
        (threshold - 100%) * 999 produces a very large positive number
        when the container is narrower than threshold (forcing wrap),
        or a very large negative number when wider (clamped to 0 by max()).
    */
    flex-grow: 1;
    flex-basis: calc((var(--switcher-threshold, 30rem) - 100%) * 999);
  }

  /* Limit children (e.g. max 4 per row) */
  .switcher[data-limit="4"] > :nth-last-child(n+5),
  .switcher[data-limit="4"] > :nth-last-child(n+5) ~ * {
    flex-basis: 100%;
  }

  /* ----- THE COVER ----- */
  /* Full-height section with vertically centred principal element */
  .cover {
    display: flex;
    flex-direction: column;
    min-block-size: var(--cover-min-height, 100vh);
    padding: var(--space-l);
  }

  .cover > * {
    margin-block: var(--space-s);
  }

  .cover > :first-child:not(.cover__principal) {
    margin-block-start: 0;
  }

  .cover > :last-child:not(.cover__principal) {
    margin-block-end: 0;
  }

  .cover > .cover__principal {
    margin-block: auto; /* centres vertically */
  }

  /* ----- THE CENTER ----- */
  /* Horizontally centred column with max-width */
  .center {
    box-sizing: content-box;
    max-inline-size: var(--measure);
    margin-inline: auto;
    padding-inline: var(--gutter);
  }

  /* ----- THE BOX ----- */
  /* Padded container */
  .box {
    padding: var(--box-padding, var(--space-s));
    border: var(--box-border, 1px solid var(--color-border));
    border-radius: var(--border-radius);
    background: var(--box-bg, transparent);
  }

  /* ----- THE GRID ----- */
  /* Auto-fill grid with minimum column width */
  .grid {
    display: grid;
    gap: var(--gutter);
    grid-template-columns: repeat(
      auto-fill,
      minmax(min(var(--grid-min, 15rem), 100%), 1fr)
    );
  }

  /* ----- THE FRAME ----- */
  /* Fixed aspect ratio container */
  .frame {
    aspect-ratio: var(--frame-ratio, 16 / 9);
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

  /* ----- THE REEL ----- */
  /* Horizontal scrolling strip */
  .reel {
    display: flex;
    gap: var(--gutter);
    overflow-x: auto;
    overflow-y: hidden;
    scrollbar-color: var(--color-border) transparent;
    -webkit-overflow-scrolling: touch;
  }

  .reel > * {
    flex: 0 0 auto;
  }

  /* ==============================================================
     WRAPPER / PAGE CONTAINER
     ============================================================== */
  .wrapper {
    max-inline-size: 1440px;
    margin-inline: auto;
    padding-inline: var(--gutter);
  }

  /* ==============================================================
     DEMO STYLES
     ============================================================== */
  .demo-card {
    padding: var(--space-m);
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius);
  }

  .demo-section {
    padding-block: var(--space-xl);
    border-block-end: 1px solid var(--color-border);
  }

  .demo-swatch {
    width: 100%;
    height: 3rem;
    border-radius: var(--border-radius);
    background: var(--color-accent);
    opacity: 0.15;
  }

  .tag {
    display: inline-block;
    padding: var(--space-3xs) var(--space-xs);
    font-size: var(--font-size--1);
    background: var(--color-border);
    border-radius: 999px;
  }
</style>
</head>
<body>

<div class="wrapper">

  <!-- ===== TYPOGRAPHY DEMO ===== -->
  <section class="demo-section stack" data-space="l">
    <h1>Fluid Typography</h1>
    <p>Resize the browser. Every size interpolates smoothly between 320px and 1440px -- no breakpoints.</p>

    <div class="stack">
      <p class="text-5">Step 5 -- Display</p>
      <p class="text-4">Step 4 -- H1</p>
      <p class="text-3">Step 3 -- H2</p>
      <p class="text-2">Step 2 -- H3</p>
      <p class="text-1">Step 1 -- H4</p>
      <p class="text-0">Step 0 -- Body (base)</p>
      <p class="text--1">Step -1 -- Small</p>
      <p class="text--2">Step -2 -- Caption</p>
    </div>
  </section>

  <!-- ===== STACK DEMO ===== -->
  <section class="demo-section stack" data-space="l">
    <h2>The Stack</h2>
    <p>Vertical rhythm between siblings via <code>margin-block-start</code>.</p>
    <div class="stack box">
      <div class="demo-swatch"></div>
      <div class="demo-swatch"></div>
      <div class="demo-swatch"></div>
    </div>
  </section>

  <!-- ===== CLUSTER DEMO ===== -->
  <section class="demo-section stack" data-space="l">
    <h2>The Cluster</h2>
    <p>Horizontal wrapping group -- great for tags, nav items, button groups.</p>
    <div class="cluster">
      <span class="tag">Design</span>
      <span class="tag">Typography</span>
      <span class="tag">Fluid</span>
      <span class="tag">Layout</span>
      <span class="tag">CSS</span>
      <span class="tag">Every Layout</span>
      <span class="tag">Utopia</span>
    </div>
  </section>

  <!-- ===== SIDEBAR DEMO ===== -->
  <section class="demo-section stack" data-space="l">
    <h2>The Sidebar</h2>
    <p>Sidebar + main content. Wraps to stacked when space is insufficient.</p>
    <div class="sidebar">
      <nav class="box">
        <p><strong>Sidebar</strong></p>
        <p>Navigation or filters go here.</p>
      </nav>
      <main class="box">
        <p><strong>Main content</strong></p>
        <p>This area takes up the remaining space and the sidebar
           collapses below when the viewport is narrow.</p>
      </main>
    </div>
  </section>

  <!-- ===== SWITCHER DEMO ===== -->
  <section class="demo-section stack" data-space="l">
    <h2>The Switcher</h2>
    <p>Horizontal when there is room, vertical when there is not. No media query.</p>
    <div class="switcher">
      <div class="demo-card"><strong>Card 1</strong><p>Content here</p></div>
      <div class="demo-card"><strong>Card 2</strong><p>Content here</p></div>
      <div class="demo-card"><strong>Card 3</strong><p>Content here</p></div>
    </div>
  </section>

  <!-- ===== COVER DEMO ===== -->
  <section class="demo-section">
    <h2>The Cover</h2>
    <div class="cover box" style="--cover-min-height: 50vh;">
      <p>Header area</p>
      <h3 class="cover__principal">I am vertically centred</h3>
      <p>Footer area</p>
    </div>
  </section>

  <!-- ===== GRID DEMO ===== -->
  <section class="demo-section stack" data-space="l">
    <h2>The Grid</h2>
    <p>Auto-fill columns with a minimum width. Columns appear and disappear as viewport changes.</p>
    <div class="grid">
      <div class="demo-card">Item 1</div>
      <div class="demo-card">Item 2</div>
      <div class="demo-card">Item 3</div>
      <div class="demo-card">Item 4</div>
      <div class="demo-card">Item 5</div>
      <div class="demo-card">Item 6</div>
    </div>
  </section>

</div>

</body>
</html>
```

---

## Variants

### Custom Clamp Generator (JS utility)

```js
/**
 * Generate a CSS clamp() value for fluid sizing.
 *
 * @param {number} minSize  - Minimum size in px
 * @param {number} maxSize  - Maximum size in px
 * @param {number} minVw    - Minimum viewport width in px (default: 320)
 * @param {number} maxVw    - Maximum viewport width in px (default: 1440)
 * @returns {string} CSS clamp() value in rem + vw
 */
function fluidClamp(minSize, maxSize, minVw = 320, maxVw = 1440) {
  const slope = (maxSize - minSize) / (maxVw - minVw);
  const yIntercept = minSize - slope * minVw;

  const minRem = (minSize / 16).toFixed(4);
  const maxRem = (maxSize / 16).toFixed(4);
  const interceptRem = (yIntercept / 16).toFixed(4);
  const slopeVw = (slope * 100).toFixed(4);

  return `clamp(${minRem}rem, ${interceptRem}rem + ${slopeVw}vw, ${maxRem}rem)`;
}

// Usage:
console.log(fluidClamp(16, 24));
// => "clamp(1.0000rem, 0.8571rem + 0.7143vw, 1.5000rem)"

console.log(fluidClamp(32, 64));
// => "clamp(2.0000rem, 1.1429rem + 2.8571vw, 4.0000rem)"
```

### Generating a Full Type Scale

```js
/**
 * Generate a fluid type scale.
 *
 * @param {number} baseMin     - Base size at min viewport (px)
 * @param {number} baseMax     - Base size at max viewport (px)
 * @param {number} ratioMin    - Scale ratio at min viewport (e.g. 1.2)
 * @param {number} ratioMax    - Scale ratio at max viewport (e.g. 1.25)
 * @param {number} stepsUp     - Number of steps above base
 * @param {number} stepsDown   - Number of steps below base
 */
function generateTypeScale(
  baseMin = 16, baseMax = 20,
  ratioMin = 1.2, ratioMax = 1.25,
  stepsUp = 5, stepsDown = 2
) {
  const scale = {};

  for (let step = -stepsDown; step <= stepsUp; step++) {
    const minSize = baseMin * Math.pow(ratioMin, step);
    const maxSize = baseMax * Math.pow(ratioMax, step);
    const name = step === 0 ? '0' : step > 0 ? String(step) : String(step);
    scale[`--font-size-${name}`] = fluidClamp(minSize, maxSize);
  }

  return scale;
}

// Print as CSS custom properties
const scale = generateTypeScale();
const css = Object.entries(scale)
  .map(([k, v]) => `  ${k}: ${v};`)
  .join('\n');

console.log(`:root {\n${css}\n}`);
```

### Tailwind CSS Integration

```js
// tailwind.config.js
const { fluidClamp } = require('./utils/fluid');

module.exports = {
  theme: {
    fontSize: {
      '-2': [fluidClamp(11.11, 12.8), { lineHeight: '1.5' }],
      '-1': [fluidClamp(13.33, 16), { lineHeight: '1.5' }],
      '0':  [fluidClamp(16, 20), { lineHeight: '1.6' }],
      '1':  [fluidClamp(19.2, 25), { lineHeight: '1.4' }],
      '2':  [fluidClamp(23.04, 31.25), { lineHeight: '1.3' }],
      '3':  [fluidClamp(27.65, 39.06), { lineHeight: '1.2' }],
      '4':  [fluidClamp(33.18, 48.83), { lineHeight: '1.15' }],
      '5':  [fluidClamp(39.81, 61.04), { lineHeight: '1.1' }],
    },
    spacing: {
      '3xs': fluidClamp(4, 5),
      '2xs': fluidClamp(8, 10),
      'xs':  fluidClamp(12, 15),
      's':   fluidClamp(16, 20),
      'm':   fluidClamp(24, 30),
      'l':   fluidClamp(32, 40),
      'xl':  fluidClamp(48, 60),
      '2xl': fluidClamp(64, 80),
      '3xl': fluidClamp(96, 120),
    },
  },
};
```

---

## Performance

- **Zero runtime cost** -- all `clamp()` values are computed by the CSS engine natively. No JavaScript needed at render time.
- **No media queries** -- fewer CSS rules to evaluate, smaller stylesheet.
- **Custom properties** -- modern browsers resolve these efficiently. Using them for spacing/typography has negligible overhead.
- **Layout primitives** -- Flexbox `flex-grow`/`flex-basis` tricks in Switcher and Sidebar are resolved in a single layout pass. No JS resize observers needed.

### Gotchas

1. **`clamp()` + `calc()` rounding** -- browsers may round sub-pixel values differently. Visually negligible, but test if pixel-perfect alignment matters.
2. **`ch` unit for `--measure`** -- depends on the font's `0` glyph width. Different fonts produce different `65ch` widths, which is usually fine but worth knowing.
3. **Nested flex contexts** -- combining multiple Every Layout primitives (e.g. Switcher inside Sidebar) works well, but deeply nested flex containers can occasionally produce unexpected shrinking. Use `min-width: 0` on flex children if content overflows.

---

## Accessibility

- **Fluid type respects zoom** -- because sizes are in `rem` + `vw`, browser zoom (Ctrl/Cmd +) increases the `rem` component. Text remains scalable.
- **`--measure: 65ch`** -- keeps lines readable (45-75 characters per line is the recommended range for body text).
- **No content hiding** -- Every Layout primitives reflow content rather than hiding it. Nothing disappears at small viewports.
- **Focus visibility** -- layout primitives do not affect focus styles. Combine with your focus-visible system (see micro-interactions.md).

---

## Browser Support

| Feature              | Chrome | Firefox | Safari | Edge  |
|----------------------|--------|---------|--------|-------|
| `clamp()`            | 79+    | 75+     | 13.1+  | 79+   |
| CSS Custom Properties| 49+    | 31+     | 9.1+   | 15+   |
| `flex-wrap`          | 29+    | 28+     | 9+     | 12+   |
| `gap` (flexbox)      | 84+    | 63+     | 14.1+  | 84+   |
| `aspect-ratio`       | 88+    | 89+     | 15+    | 88+   |
| CSS Grid `auto-fill` | 57+    | 52+     | 10.1+  | 16+   |

For the rare browser without `clamp()` support (< 2% global), provide a static fallback:

```css
/* Fallback then enhancement */
font-size: 1rem;
font-size: clamp(1rem, 0.9286rem + 0.3571vw, 1.25rem);
```

---

## Sources

- [Utopia: Fluid Type Scale Calculator](https://utopia.fyi/type/calculator/)
- [Utopia: Fluid Space Calculator](https://utopia.fyi/space/calculator/)
- [Utopia: Clamp Explained](https://utopia.fyi/blog/clamp/)
- [Smashing Magazine: Designing and Building with Fluid Type and Space Scales](https://www.smashingmagazine.com/2021/04/designing-developing-fluid-type-space-scales/)
- [Every Layout: Layouts](https://every-layout.dev/layouts/)
- [Every Layout: The Stack](https://every-layout.dev/layouts/stack/)
- [Every Layout: The Sidebar](https://every-layout.dev/layouts/sidebar/)
- [Aleksandr Hovhannisyan: Creating a Fluid Type Scale with CSS Clamp](https://www.aleksandrhovhannisyan.com/blog/fluid-type-scale-with-css-clamp/)
- [LogRocket: Fluid vs Responsive Typography with CSS clamp](https://blog.logrocket.com/fluid-vs-responsive-typography-css-clamp/)
- [Fluid Type Scale Calculator (fluid-type-scale.com)](https://www.fluid-type-scale.com/)
