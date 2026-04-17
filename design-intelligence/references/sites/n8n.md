---
name: n8n
url: https://n8n.io
category: [saas, developer-tool, productivity]
design_style: Dark-mode-first technical aesthetic with warm orange/coral accents on deep navy backgrounds, node-based visual language
last_analyzed: 2026-04-17
---

## Visual Identity

### Brand Colors

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Primary Orange | `#EE4F27` | 238, 79, 39 | Main CTA, primary accent |
| Secondary Orange | `#FF9B26` | 255, 155, 38 | Gradient start, highlights |
| Brand Pink (legacy) | `#EA4B71` | 234, 75, 113 | Brand mark, logo accent |
| Purple Accent | `#6B21EF` | 107, 33, 239 | Secondary interactive elements |
| Base Red | `#FF492C` | 255, 73, 44 | Error states, alerts |
| Midnight Navy (bg) | `#0E0918` | 14, 9, 24 | Primary dark background |
| Deep Navy | `#1F192A` | 31, 25, 42 | Card backgrounds |
| Dark Navy | `#1B1728` | 27, 23, 40 | Elevated surfaces |
| Hard Gray | `#464646` | 70, 70, 70 | Secondary text |
| Soft Gray | `#E4E4E4` | 228, 228, 228 | Borders, dividers |
| Darker Gray | `#7A7A7A` | 122, 122, 122 | Muted text |
| White | `#FFFFFF` | 255, 255, 255 | Primary text on dark |

### Gradients

| Name | Definition | Usage |
|------|-----------|-------|
| Flame | `linear-gradient(90deg, #FF9B26 29.28%, #EE4F27 67.8%)` | CTA buttons, hero accents |
| Navy Radial | `radial-gradient(266.47% 215.14% at 10.15% 142.35%, #d97e4b38 0, #fff0 37%)` | Background glow effects |

### Design System Color Architecture (CSS Variables, HSL-based)

The product design system uses HSL components for theme flexibility:

| Token | Light Mode | Dark Mode |
|-------|-----------|-----------|
| `--color-primary` | HSL(6.9, 100%, 67.6%) | HSL(7, 100%, 68%) |
| `--color-primary-tint-1` | HSL(6.9, 100%, 88%) | HSL(7, 100%, 18%) |
| `--color-primary-tint-2` | HSL(6.9, 100%, 94.5%) | HSL(7, 100%, 9%) |
| `--color-primary-tint-3` | HSL(6.9, 100%, 96.9%) | HSL(7, 100%, 3%) |
| `--color-primary-shade-1` | HSL(6.9, 100%, 23%) | HSL(7, 100%, 89%) |
| `--color-secondary` | HSL(247.4, 100%, 65.1%) | HSL(247, 100%, 35%) |
| `--color-text-dark` | HSL(0, 0%, 33.3%) | HSL(0, 0%, 100%) |
| `--color-text-base` | HSL(240, 4%, 51%) | HSL(240, 4%, 49%) |
| `--color-text-light` | HSL(220, 4.2%, 58.2%) | HSL(220, 4%, 42%) |
| `--color-text-lighter` | HSL(220, 10.5%, 77.6%) | HSL(222, 17%, 12%) |

### Typography

**Website (Landing Page):**

| Property | Value |
|----------|-------|
| Primary Font | `geomanist` (weights: 300, 400, 500, 700) |
| Secondary Font | `geomanist-book` (weight: 400) |
| Monospace | `ui-monospace, SFMono-Regular, Menlo, Monaco` |

| Element | Size | Line Height |
|---------|------|-------------|
| Headline Large | 54px | 100% |
| Headline Medium | 48px | 100% |
| Headline Small | 38px | 100% |
| Headline XS | 32px | 100% |
| Body Large | 18px | 150% |
| Body Medium | 16px | 150% |
| Body Small | 14px | 150% |
| Nav Links | 15px | 100% |

**Product (Design System):**

| Property | Value |
|----------|-------|
| Font Family | `'Open Sans', sans-serif` |

| Token | Size | Pixel Eq. |
|-------|------|-----------|
| `--font-size-2xs` | 0.75rem | 12px |
| `--font-size-xs` | 0.8125rem | 13px |
| `--font-size-s` | 0.875rem | 14px |
| `--font-size-m` | 1rem | 16px |
| `--font-size-l` | 1.125rem | 18px |
| `--font-size-xl` | 1.25rem | 20px |
| `--font-size-2xl` | 1.75rem | 28px |

| Weight Token | Value |
|-------------|-------|
| `--font-weight-regular` | 400 |
| `--font-weight-semi-bold` | 500 |
| `--font-weight-bold` | 600 |

| Line Height Token | Value |
|------------------|-------|
| `--font-line-height-compact` | 1.25 |
| `--font-line-height-regular` | 1.3 |
| `--font-line-height-loose` | 1.35 |
| `--font-line-height-xloose` | 1.5 |

### Spacing System

13-point scale from the design system:

| Token | Value |
|-------|-------|
| 5xs | 0.125rem (2px) |
| 4xs | 0.25rem (4px) |
| 3xs | 0.375rem (6px) |
| 2xs | 0.5rem (8px) |
| xs | 0.75rem (12px) |
| s | 1rem (16px) |
| m | 1.5rem (24px) |
| l | 2rem (32px) |
| xl | 3rem (48px) |
| 2xl | 4rem (64px) |
| 3xl | 8rem (128px) |
| 4xl | 12rem (192px) |
| 5xl | 16rem (256px) |

**Landing Page Sections:**

| Token | Value |
|-------|-------|
| Section Y Gap | 48px |
| Section Y Gap Small | 32px |
| Section X Gap | 16px |
| Hero Y Gap | 96px |

### Border Radius

| Token | Value |
|-------|-------|
| Default | 24px |
| Large (2xl) | 16px |
| Medium (lg) | 6px |
| Full (pill) | 9999px |
| Small (sm) | 2px |

### Shadows

| Name | Value |
|------|-------|
| Card Top Glow | `inset 0 0 0 1px hsla(0,0%,100%,.1), inset 0 1px 0 0 rgba(255,142,93,.3)` |
| Soft Shadow | `4px 4px 14px #080f340a, 1px 1px 1px #170f490a` |
| Deep Shadow | `0px 0px 8px 0px rgba(0,0,0,.26)` |

## Key Techniques

### Dark Mode Hero with Gradient Glow

```css
.hero-section {
  background-color: #0E0918;
  position: relative;
  padding-top: 96px;
}

.hero-section::before {
  content: '';
  position: absolute;
  background: radial-gradient(
    266.47% 215.14% at 10.15% 142.35%,
    #d97e4b38 0,
    #fff0 37%
  );
  inset: 0;
  pointer-events: none;
}
```

### Flame Gradient CTA Button

```css
.cta-button {
  background: linear-gradient(90deg, #FF9B26 29.28%, #EE4F27 67.8%);
  border-radius: 9999px;
  color: #FFFFFF;
  font-family: 'geomanist', sans-serif;
  font-weight: 500;
  font-size: 16px;
  padding: 12px 24px;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}

.cta-button:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}
```

### Card with Inset Glow Border (Glassmorphism-adjacent)

```css
.feature-card {
  background: #1F192A;
  border-radius: 24px;
  padding: 32px;
  box-shadow:
    inset 0 0 0 1px hsla(0, 0%, 100%, 0.1),
    inset 0 1px 0 0 rgba(255, 142, 93, 0.3);
  backdrop-filter: blur(22px);
}
```

### Dot Pattern Background

```css
.dot-pattern {
  background-image: radial-gradient(
    hsla(0, 0%, 100%, 0.1) 1px,
    transparent 0
  );
  background-size: 15px 15px;
}
```

### HSL-Based Theming Architecture

```css
:root {
  --color-primary-h: 6.9;
  --color-primary-s: 100%;
  --color-primary-l: 67.6%;
  --color-primary: hsl(
    var(--color-primary-h),
    var(--color-primary-s),
    var(--color-primary-l)
  );
}

.theme-dark {
  --color-primary-l: 68%;
  --color-text-dark-l: 100%;
  --color-background-base-l: 8%;
}
```

### Smooth Transitions

```css
* {
  transition-duration: 0.15s;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

.extended-transition {
  transition-duration: 0.3s;
}
```

## What Makes It Work

### Psychological Principles

1. **Warm-on-dark contrast** -- The orange/coral on deep navy creates high visual contrast that draws the eye to CTAs without the coldness of blue-on-dark schemes. The warmth conveys approachability for a technical product.

2. **Controlled complexity** -- The node-based workflow canvas is inherently complex. The dark background reduces visual noise, letting the colorful node connections become the hero element. Users focus on their work, not the UI chrome.

3. **Progressive disclosure** -- The landing page reveals complexity gradually: simple headline, then product screenshots, then feature cards. Each layer adds detail without overwhelming first-time visitors.

4. **Technical credibility signaling** -- Dark mode defaults, monospace fonts in code snippets, and the gradient-glow aesthetic signal "developer tool" without being hostile to non-developers. The geomanist font's geometric quality reinforces precision.

5. **Flame gradient as action catalyst** -- The orange gradient CTA stands out dramatically against the navy/purple palette. It creates urgency through color temperature contrast (warm action vs. cool environment).

6. **Social proof architecture** -- Integration logos and workflow counts establish ecosystem scale. The "400+ integrations" claim is reinforced visually by the sheer density of connection logos.

## Patterns to Extract

### 1. Dark Hero with Radial Glow

Full-width dark section with subtle radial gradient emanating from bottom-left. Creates depth without illustration. Reusable for any technical product hero.

### 2. Flame Gradient CTA

Orange-to-coral gradient pill button that creates maximum contrast on dark backgrounds. Pairs with white text. Include hover brightness boost.

### 3. Inset Border Glow Cards

Cards that use `inset box-shadow` to create a subtle light border effect on dark backgrounds. More elegant than solid borders on dark themes.

### 4. HSL-Based Token System

Decompose colors into H/S/L components as CSS variables. Enables tint/shade generation by only adjusting lightness. Superior to hex tokens for theme flexibility.

### 5. Node/Workflow Visual Language

Connected dots and lines as decorative elements that reinforce the product metaphor. Dot grid patterns serve as subtle backgrounds.

### 6. Integration Logo Grid

Dense grid of partner/integration logos with consistent sizing and grayscale treatment. Establishes ecosystem credibility at a glance.

### 7. Section Gap Rhythm

Consistent 48px vertical gap between sections, 96px for hero, 32px for tighter groupings. Creates predictable visual rhythm.

## Code Snippets

### Complete Dark Landing Page Section

```css
.section-dark {
  background: #0E0918;
  color: #FFFFFF;
  padding: 48px 16px;
  position: relative;
  overflow: hidden;
}

.section-dark .heading {
  font-family: 'geomanist', sans-serif;
  font-weight: 700;
  font-size: 54px;
  line-height: 100%;
  letter-spacing: -0.02em;
  margin-bottom: 24px;
}

.section-dark .body-text {
  font-family: 'geomanist-book', sans-serif;
  font-size: 18px;
  line-height: 150%;
  color: rgb(209, 206, 206);
  max-width: 600px;
}

.section-dark .body-text strong {
  color: #FFFFFF;
}
```

### Backdrop Blur Navigation

```css
.nav {
  min-height: 56px;
  padding: 0 8px;
  backdrop-filter: blur(22px);
  background: rgba(14, 9, 24, 0.7);
  position: sticky;
  top: 0;
  z-index: 50;
}

.nav-link {
  font-size: 15px;
  line-height: 100%;
  color: rgba(255, 255, 255, 0.7);
  transition: color 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-link:hover {
  color: #FFFFFF;
}
```

### Skeleton Loading Animation

```css
@keyframes skeleton-pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

.skeleton {
  background: linear-gradient(90deg, #1F192A 25%, #2a2236 50%, #1F192A 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.75s linear infinite;
  border-radius: 6px;
}
```

## Anti-Patterns to Avoid

1. **Do not copy the full dark palette for non-technical products.** The deep navy + warm accents aesthetic signals "developer tool." Using it for consumer apps or creative tools creates a tonal mismatch.

2. **Avoid the dot pattern at high density.** The 15px grid works at low opacity (0.1). At higher opacity or smaller spacing, it creates visual noise and can trigger pattern-recognition fatigue.

3. **Do not use inset glow borders on light backgrounds.** The card glow technique relies on contrast with dark surfaces. On light backgrounds, it reads as a rendering artifact.

4. **Avoid mixing geomanist with other geometric sans-serifs.** The font has distinctive character widths. Pairing it with Inter or DM Sans creates subtle rhythm clashes.

5. **Do not over-apply the flame gradient.** One or two gradient CTAs per viewport is the maximum. More than that diminishes the pattern's attention-grabbing power and creates visual competition.

6. **Avoid pure black (#000000) backgrounds.** n8n uses #0E0918 (slightly purple-tinted navy), not true black. Pure black creates excessive contrast with text and feels flat.
