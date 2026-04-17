---
technique: Glassmorphism
complexity: basic
browser_support: 95%+ global (backdrop-filter); fallbacks for the rest
performance_impact: medium
---

## Overview

Glassmorphism is a UI design style characterised by:
- **Frosted glass translucency** via `backdrop-filter: blur()`
- **Semi-transparent backgrounds** with low alpha
- **Subtle borders** (often 1px white at ~20% opacity)
- **Layered depth** creating a sense of floating panels

Popularised by Apple (macOS Big Sur, iOS), adopted by Microsoft (Fluent Design), Stripe, Linear,
and countless SaaS products.

**When to use:** Cards, modals, navigation bars, dropdowns, sidebars -- any elevated surface
where the background content should remain partially visible.

**When to avoid:** Large body areas, text-heavy content without sufficient contrast,
or when targeting very old browsers without providing fallbacks.

---

## Implementation

### Complete Working Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glassmorphism System</title>
<style>
  /* ==============================================================
     CSS CUSTOM PROPERTIES -- GLASS DESIGN TOKENS
     ============================================================== */
  :root {
    /* ----- Light Mode ----- */
    --glass-bg: rgba(255, 255, 255, 0.25);
    --glass-bg-hover: rgba(255, 255, 255, 0.35);
    --glass-border: rgba(255, 255, 255, 0.3);
    --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    --glass-shadow-elevated: 0 16px 48px rgba(0, 0, 0, 0.18);
    --glass-blur: 16px;
    --glass-blur-heavy: 24px;
    --glass-blur-subtle: 8px;
    --glass-radius: 16px;
    --glass-radius-sm: 8px;
    --glass-text: #1a1a2e;
    --glass-text-muted: rgba(26, 26, 46, 0.7);

    /* ----- Fallback (no backdrop-filter) ----- */
    --glass-fallback-bg: rgba(255, 255, 255, 0.92);

    /* ----- Page Background ----- */
    --page-bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --page-bg-color: #667eea; /* solid fallback */
  }

  /* ----- Dark Mode ----- */
  @media (prefers-color-scheme: dark) {
    :root {
      --glass-bg: rgba(30, 30, 50, 0.4);
      --glass-bg-hover: rgba(30, 30, 50, 0.55);
      --glass-border: rgba(255, 255, 255, 0.12);
      --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
      --glass-shadow-elevated: 0 16px 48px rgba(0, 0, 0, 0.45);
      --glass-text: #f0f0f5;
      --glass-text-muted: rgba(240, 240, 245, 0.65);
      --glass-fallback-bg: rgba(30, 30, 50, 0.95);
      --page-bg-gradient: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      --page-bg-color: #1a1a2e;
    }
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

  /* ==============================================================
     PAGE LAYOUT
     ============================================================== */
  body {
    min-height: 100vh;
    background: var(--page-bg-color);
    background: var(--page-bg-gradient);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: var(--glass-text);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    gap: 2rem;
  }

  /* Decorative background shapes (to show blur effect) */
  body::before,
  body::after {
    content: '';
    position: fixed;
    border-radius: 50%;
    z-index: 0;
    pointer-events: none;
  }

  body::before {
    width: 400px;
    height: 400px;
    background: rgba(255, 107, 107, 0.4);
    top: 10%;
    left: 15%;
    filter: blur(60px);
  }

  body::after {
    width: 300px;
    height: 300px;
    background: rgba(78, 205, 196, 0.4);
    bottom: 15%;
    right: 20%;
    filter: blur(60px);
  }

  /* ==============================================================
     GLASS BASE CLASS
     ============================================================== */
  .glass {
    position: relative;
    z-index: 1;

    /* Core glass effect */
    background: var(--glass-bg);
    -webkit-backdrop-filter: blur(var(--glass-blur));
    backdrop-filter: blur(var(--glass-blur));
    border: 1px solid var(--glass-border);
    border-radius: var(--glass-radius);
    box-shadow: var(--glass-shadow);
    color: var(--glass-text);
  }

  /* Fallback for browsers without backdrop-filter */
  @supports not ((-webkit-backdrop-filter: blur(1px)) or (backdrop-filter: blur(1px))) {
    .glass {
      background: var(--glass-fallback-bg);
    }
  }

  /* Reduced transparency preference */
  @media (prefers-reduced-transparency: reduce) {
    .glass {
      background: var(--glass-fallback-bg);
      -webkit-backdrop-filter: none;
      backdrop-filter: none;
    }
  }

  /* ==============================================================
     GLASS CARD
     ============================================================== */
  .glass-card {
    padding: 2rem;
    max-width: 420px;
    width: 100%;
    transition: background 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
  }

  .glass-card:hover {
    background: var(--glass-bg-hover);
    box-shadow: var(--glass-shadow-elevated);
    transform: translateY(-2px);
  }

  @media (prefers-reduced-motion: reduce) {
    .glass-card:hover {
      transform: none;
    }
  }

  .glass-card h3 {
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
  }

  .glass-card p {
    font-size: 0.9375rem;
    color: var(--glass-text-muted);
    line-height: 1.6;
  }

  /* ==============================================================
     GLASS NAVBAR
     ============================================================== */
  .glass-navbar {
    position: sticky;
    top: 0;
    z-index: 100;
    width: 100%;
    max-width: 900px;
    padding: 0.75rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: var(--glass-radius);
    /* Slightly heavier blur for navbar readability */
    --glass-blur: var(--glass-blur-heavy);
  }

  .glass-navbar__brand {
    font-weight: 700;
    font-size: 1.125rem;
  }

  .glass-navbar__links {
    display: flex;
    gap: 1.25rem;
    list-style: none;
  }

  .glass-navbar__links a {
    color: var(--glass-text);
    text-decoration: none;
    font-size: 0.875rem;
    font-weight: 500;
    opacity: 0.8;
    transition: opacity 0.15s ease;
  }

  .glass-navbar__links a:hover {
    opacity: 1;
  }

  /* ==============================================================
     GLASS INPUT
     ============================================================== */
  .glass-input {
    width: 100%;
    padding: 0.75rem 1rem;
    background: rgba(255, 255, 255, 0.15);
    -webkit-backdrop-filter: blur(var(--glass-blur-subtle));
    backdrop-filter: blur(var(--glass-blur-subtle));
    border: 1px solid var(--glass-border);
    border-radius: var(--glass-radius-sm);
    color: var(--glass-text);
    font-size: 1rem;
    outline: none;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
  }

  .glass-input::placeholder {
    color: var(--glass-text-muted);
  }

  .glass-input:focus {
    border-color: rgba(255, 255, 255, 0.5);
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.15);
  }

  @supports not ((-webkit-backdrop-filter: blur(1px)) or (backdrop-filter: blur(1px))) {
    .glass-input {
      background: rgba(255, 255, 255, 0.85);
    }
  }

  /* ==============================================================
     GLASS BUTTON
     ============================================================== */
  .glass-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.625rem 1.5rem;
    font-size: 0.9375rem;
    font-weight: 600;
    color: var(--glass-text);
    background: rgba(255, 255, 255, 0.2);
    -webkit-backdrop-filter: blur(var(--glass-blur-subtle));
    backdrop-filter: blur(var(--glass-blur-subtle));
    border: 1px solid var(--glass-border);
    border-radius: var(--glass-radius-sm);
    cursor: pointer;
    transition: background 0.15s ease, transform 0.15s ease;
  }

  .glass-button:hover {
    background: rgba(255, 255, 255, 0.35);
    transform: translateY(-1px);
  }

  .glass-button:active {
    transform: translateY(0);
    background: rgba(255, 255, 255, 0.15);
  }

  /* Focus-visible ring */
  .glass-button:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.4);
  }

  @supports not ((-webkit-backdrop-filter: blur(1px)) or (backdrop-filter: blur(1px))) {
    .glass-button {
      background: rgba(255, 255, 255, 0.85);
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .glass-button:hover {
      transform: none;
    }
  }

  /* ==============================================================
     GLASS MODAL
     ============================================================== */
  .glass-modal-backdrop {
    position: fixed;
    inset: 0;
    z-index: 200;
    background: rgba(0, 0, 0, 0.4);
    -webkit-backdrop-filter: blur(4px);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    /* Toggle visibility with JS -- hidden by default */
    display: none;
  }

  .glass-modal-backdrop.active {
    display: flex;
  }

  .glass-modal {
    padding: 2rem;
    max-width: 480px;
    width: 100%;
    --glass-blur: var(--glass-blur-heavy);
  }

  .glass-modal h2 {
    margin-bottom: 1rem;
  }

  .glass-modal p {
    margin-bottom: 1.5rem;
    color: var(--glass-text-muted);
    line-height: 1.6;
  }

  /* ==============================================================
     LAYOUT HELPERS
     ============================================================== */
  .cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(320px, 100%), 1fr));
    gap: 1.5rem;
    width: 100%;
    max-width: 900px;
  }

  .form-stack {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
  }

  h1 {
    font-size: clamp(2rem, 5vw, 3.5rem);
    text-align: center;
    color: var(--glass-text);
    position: relative;
    z-index: 1;
    /* Text shadow for readability over busy backgrounds */
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  .subtitle {
    text-align: center;
    color: var(--glass-text-muted);
    font-size: 1.125rem;
    position: relative;
    z-index: 1;
  }
</style>
</head>
<body>

<h1>Glassmorphism</h1>
<p class="subtitle">Frosted glass UI with proper fallbacks and accessibility</p>

<!-- Glass Navbar -->
<nav class="glass glass-navbar">
  <span class="glass-navbar__brand">Acme</span>
  <ul class="glass-navbar__links">
    <li><a href="#">Products</a></li>
    <li><a href="#">Pricing</a></li>
    <li><a href="#">About</a></li>
  </ul>
</nav>

<!-- Glass Cards -->
<div class="cards-grid">

  <div class="glass glass-card">
    <h3>Performance</h3>
    <p>GPU-accelerated blur compositing keeps the effect smooth at 60fps on modern hardware.</p>
  </div>

  <div class="glass glass-card">
    <h3>Accessibility</h3>
    <p>Sufficient contrast, prefers-reduced-transparency support, and solid fallback backgrounds.</p>
  </div>

  <div class="glass glass-card">
    <h3>Dark Mode</h3>
    <p>Automatic adaptation via prefers-color-scheme with adjusted alpha values and borders.</p>
  </div>

</div>

<!-- Glass Form Card -->
<div class="glass glass-card" style="max-width: 480px;">
  <h3>Contact</h3>
  <div class="form-stack">
    <input class="glass-input" type="text" placeholder="Name" aria-label="Name" />
    <input class="glass-input" type="email" placeholder="Email" aria-label="Email" />
    <button class="glass-button" type="button">Submit</button>
  </div>
</div>

<!-- Modal trigger -->
<button class="glass-button" id="openModal" type="button">Open Modal</button>

<!-- Glass Modal -->
<div class="glass-modal-backdrop" id="modalBackdrop">
  <div class="glass glass-modal">
    <h2>Glass Modal</h2>
    <p>This modal uses backdrop-filter on both the overlay (light blur) and the panel itself (heavy blur).</p>
    <button class="glass-button" id="closeModal" type="button">Close</button>
  </div>
</div>

<script>
  // Simple modal toggle
  const openBtn = document.getElementById('openModal');
  const closeBtn = document.getElementById('closeModal');
  const backdrop = document.getElementById('modalBackdrop');

  openBtn.addEventListener('click', () => backdrop.classList.add('active'));
  closeBtn.addEventListener('click', () => backdrop.classList.remove('active'));
  backdrop.addEventListener('click', (e) => {
    if (e.target === backdrop) backdrop.classList.remove('active');
  });
</script>

</body>
</html>
```

---

## Variants

### Variant A: Frosted Noise Texture

Adds a subtle noise texture over the glass for a more physical feel (like real frosted glass).

```css
.glass-textured::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.04;
  pointer-events: none;
  mix-blend-mode: overlay;
}
```

### Variant B: Neumorphism + Glass Hybrid

Combines the glass blur with inner shadows for a "soft UI" effect.

```css
.glass-neo {
  background: var(--glass-bg);
  -webkit-backdrop-filter: blur(var(--glass-blur));
  backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  box-shadow:
    8px 8px 16px rgba(0, 0, 0, 0.15),
    -8px -8px 16px rgba(255, 255, 255, 0.08),
    inset 1px 1px 0 rgba(255, 255, 255, 0.15);
}
```

### Variant C: Gradient Border Glass

Uses a pseudo-element with a gradient border for a more premium look.

```css
.glass-gradient-border {
  position: relative;
  background: var(--glass-bg);
  -webkit-backdrop-filter: blur(var(--glass-blur));
  backdrop-filter: blur(var(--glass-blur));
  border-radius: var(--glass-radius);
  border: none; /* remove solid border */
  padding: 2rem;
}

.glass-gradient-border::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px; /* border thickness */
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.4),
    rgba(255, 255, 255, 0.05)
  );
  -webkit-mask:
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

---

## Performance

### GPU Compositing Behaviour

`backdrop-filter: blur()` triggers a GPU-composited layer. This is efficient for small, isolated
elements but becomes expensive when:

- Many glass elements overlap
- Blur radius is very large (> 24px)
- The element covers a large area of the viewport
- The background behind the glass is frequently animating

### Optimisation Tips

1. **Keep blur between 8-16px** -- diminishing visual returns beyond 20px, but quadratic GPU cost increase.
2. **Limit simultaneous glass layers** -- 3-5 glass elements on screen is fine; 20+ will cause jank on mobile.
3. **Avoid animating the blur value** -- transitioning `backdrop-filter: blur(0) -> blur(16px)` is extremely expensive. Instead, animate `opacity` of the glass element itself.
4. **Use `contain: layout paint`** -- on glass containers to limit compositing scope.
5. **Use `will-change: backdrop-filter`** sparingly -- only on elements that will animate.
6. **Test on low-end Android** -- the weakest link. If it jank there, reduce blur or use fallback.

```css
/* Anti-pattern: DO NOT animate blur directly */
.glass-bad {
  transition: backdrop-filter 0.3s ease; /* EXPENSIVE */
}

/* Better: animate opacity instead */
.glass-reveal {
  opacity: 0;
  transition: opacity 0.3s ease;
}
.glass-reveal.visible {
  opacity: 1;
}
```

---

## Accessibility

### Contrast Requirements (WCAG 2.1)

| Text Type | Required Ratio | Recommendation |
|-----------|---------------|----------------|
| Normal text (< 18px) | 4.5:1 | Use `rgba(255,255,255,0.25)` minimum bg + text-shadow |
| Large text (>= 18px bold / 24px) | 3:1 | Glass bg alone may suffice |
| UI components (borders, icons) | 3:1 | Use visible border + shadow |

### Ensuring Readability

```css
/* Text shadow improves readability over variable backgrounds */
.glass-readable {
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

/* Or add a stronger background tint */
.glass-high-contrast {
  --glass-bg: rgba(255, 255, 255, 0.45); /* higher alpha = more contrast */
}
```

### prefers-reduced-transparency

Some users enable "Reduce transparency" at the OS level. Respect this:

```css
@media (prefers-reduced-transparency: reduce) {
  .glass {
    background: var(--glass-fallback-bg);
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
  }
}
```

### Screen Reader Considerations

Glass elements are purely visual -- they do not affect semantic HTML or ARIA. Ensure:
- All interactive glass elements have proper focus styles (`:focus-visible`)
- Modal glass overlays trap focus correctly
- Decorative glass backgrounds use `aria-hidden="true"`

---

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge | Samsung | iOS Safari |
|---------|--------|---------|--------|------|---------|------------|
| `backdrop-filter` | 76+ | 103+ | 9+ (-webkit-) | 17+ | 12+ | 9+ |
| `@supports` query | 28+ | 22+ | 9+ | 12+ | 4+ | 9+ |
| `prefers-color-scheme` | 76+ | 67+ | 12.1+ | 79+ | 13+ | 13+ |
| `prefers-reduced-transparency` | 118+ | No | 16.4+ | 118+ | No | 16.4+ |

**Key notes:**
- Firefox added `backdrop-filter` support in v103 (2022). Before that, it required a flag.
- Safari requires `-webkit-backdrop-filter` prefix (stable since Safari 9).
- The `@supports` fallback handles the remaining ~5% of browsers gracefully.

---

## Sources

- [Glassmorphism Design Trend: Complete Implementation Guide (2025)](https://playground.halfaccessible.com/blog/glassmorphism-design-trend-implementation-guide)
- [Glassmorphism CSS Generator: Complete Design Guide (2026)](https://www.codeformatter.in/blog-glassmorphism-generator.html)
- [Intellure: The Ultimate Guide to Glassmorphism in Modern Web Design (2026)](https://intellure.co/blog/glassmorphism-guide)
- [OpenReplay: How to Create Glassmorphic UI Effects with Pure CSS](https://blog.openreplay.com/create-glassmorphic-ui-css/)
- [Neel Networks: Glassmorphism Web Design Guide 2026](https://www.neelnetworks.com/blog/glassmorphism-web-design-guide-2026/)
- [CSS Backdrop-Filter Complete Guide (CodeLucky)](https://codelucky.com/css-backdrop-filter/)
- [WPDean: 44 CSS Glassmorphism Examples](https://wpdean.com/css-glassmorphism/)
