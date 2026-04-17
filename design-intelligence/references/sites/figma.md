---
name: Figma
url: https://figma.com
category: [design-tool, saas]
design_style: "Minimal monochrome with signature purple, variable typography, fluid grid system"
last_analyzed: 2026-04-16
---

## Visual Identity

### Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| Primary Background | `#FFFFFF` | Page background (light mode) |
| Dark Background | `#000000` / `#131313` | Dark sections, hero areas, brand pages |
| Primary Text | `#000000` | Headings, body text on light |
| Secondary Text | `rgba(0, 0, 0, 0.65)` | Subheadings, descriptions |
| Tertiary Gray | `#697485` | Metadata, timestamps, labels |
| Accent Purple | `#A259FF` | Legacy brand purple (community, plugins) |
| Accent Blue | `#4D49FC` | Primary interactive accent, CTAs on dark |
| Error Red | `#972121` | Form validation, error states |
| Form Input BG | `rgba(0, 0, 0, 0.08)` | Text input resting state |
| Form Hover BG | `rgba(0, 0, 0, 0.16)` | Text input hover/focus state |
| Badge BG | `rgba(0, 0, 0, 0.08)` | Tags, labels, status pills |
| Border Light | `rgba(0, 0, 0, 0.08)` | Dividers, card borders |
| Dark Mode Text | `#FFFFFF` | Body on dark sections |
| Dark Secondary | `rgba(255, 255, 255, 0.6)` | Muted text on dark |
| Dark Border | `rgba(255, 255, 255, 0.16)` | Borders on dark surfaces |
| Icon BG (dark) | `rgba(255, 255, 255, 0.24)` | Icon containers on dark |

### Expanded Brand Palette (2024 refresh)

Figma expanded from their signature purple to include bold primaries, bright neons, and muted earthy tones. The palette uses variables to dynamically shift across contexts -- reflecting community diversity rather than a single brand color.

### Typography

**Custom Typeface: Figma Sans** -- commissioned from Grilli Type (Switzerland). 60 fonts across 5 families:

| Family | Purpose |
|--------|---------|
| Figma Sans Text | Body copy, UI labels |
| Figma Sans Display | Headlines, hero sections |
| Figma Sans Condensed Text | Compact layouts, tables |
| Figma Sans Condensed Display | Large-format headlines |
| Figma Sans Mono | Code, technical content |

Additional families: **Figma Hand** (by OH no Type) for playful/sketch contexts.

**CSS Font Stacks:**
```css
/* Primary sans-serif */
font-family: 'figmaSans', 'figmaSans Fallback', SF Pro Display, system-ui, helvetica, sans-serif;

/* Display/branding (older pages) */
font-family: 'ABCWhytePlusVariable', Whyte, sans-serif;

/* Monospace */
font-family: 'figmaMono', 'figmaMono Fallback', SF Mono, menlo, monospace;

/* Japanese locale */
font-family: 'Zen Kaku Gothic New', sans-serif;
```

**Type Scale:**

| Level | Size | Weight | Letter-spacing |
|-------|------|--------|----------------|
| Display XL | `5.625rem` (90px) | 400 | `-0.1125rem` |
| Display | `5.375rem` (86px) | 400 | -- |
| H2 | `1.625rem` (26px) | 530 | -- |
| Body | `1.125rem` (18px) | 330 | -- |
| Body Small | `1rem` (16px) | 330 | -- |
| Mono Label | `1rem` (16px) | 400 | uppercase |

**Line-height:** `1.45` (standard across body text)

**Optical sizing:** Enabled (`font-optical-sizing: auto`)

**Unique variable font axis:** Monospace axis allows continuous interpolation from full-mono to proportional.

### Spacing System

| Token | Value | Context |
|-------|-------|---------|
| `--f-gutter` | `24px` | Default gutter (mobile) |
| Gutter (tablet) | `16px` | Below 1024px |
| Gutter (small) | `12px` | Below 375px |
| Block Padding | `5rem` / `7.5rem` / `10rem` | Mobile / 960px+ / 1920px+ |
| Max Content | `1440px` | Standard viewport |
| Max Content XL | `1680px` | 1920px+ viewport |

### Grid System

Fluid column grid that scales responsively:

| Breakpoint | Columns |
|------------|---------|
| < 560px | 1 column |
| 560px+ | 12 columns |
| 768px+ | 24 columns |
| 960px+ | 48 columns |

Column width is calculated dynamically: `var(--f-col-width)` with gutter `calc(var(--f-col-width) * 2)`.

### Component Details

**Buttons:**
- Border-radius: `8px`
- Padding: `0.75rem 1.3125rem` (12px 21px)
- Primary: `background: #000000; color: #FFFFFF`
- Secondary: `box-shadow: inset 0 0 0 1px var(--f-text-color)` (ghost with inset border)
- Hover transition: `160ms ease-out`

**Cards:**
- Border-radius: `0.5rem` (8px)
- Shadow: `0 1.5rem 4.375rem 0 rgba(0, 0, 0, 0.10)`
- Background: `#FFFFFF` with subtle gradients

**Navigation:**
- Fixed header height: `81px`
- Bottom border: `box-shadow: 0 1px 0 rgba(0, 0, 0, 0.08)`

**Focus States:**
- Dashed `2px` outline with `4px` offset

---

## Key Techniques

### Fluid Column Grid with CSS Custom Properties
```css
:root {
  --f-max-content-width: 1440px;
  --f-columns: 12;
  --f-gutter: 24px;
  --f-col-width: calc(
    (min(100vw, var(--f-max-content-width)) - var(--f-gutter) * 2) 
    / var(--f-columns)
  );
}

@media (min-width: 768px) {
  :root { --f-columns: 24; }
}

@media (min-width: 960px) {
  :root { --f-columns: 48; }
}

@media (min-width: 1920px) {
  :root { --f-max-content-width: 1680px; }
}
```

### Variable Font Weight Interpolation
```css
/* Figma Sans uses non-standard weight stops */
.heading { font-weight: 530; }
.body { font-weight: 330; }
.display { font-weight: 540; }

/* Monospace axis interpolation */
.mono-full { font-variation-settings: 'MONO' 1; }
.mono-half { font-variation-settings: 'MONO' 0.5; }
.mono-off { font-variation-settings: 'MONO' 0; }
```

### Ghost Button with Inset Box-Shadow (no border)
```css
.btn-secondary {
  background: transparent;
  box-shadow: inset 0 0 0 1px currentColor;
  border-radius: 8px;
  padding: 0.75rem 1.3125rem;
  transition: all 160ms ease-out;
}

.btn-secondary:hover {
  background: rgba(0, 0, 0, 0.08);
}
```

### Opacity-Based Color Tokens (single source color)
```css
/* Instead of defining N gray shades, Figma uses opacity on black */
--text-primary: #000000;
--text-secondary: rgba(0, 0, 0, 0.65);
--border: rgba(0, 0, 0, 0.08);
--surface-hover: rgba(0, 0, 0, 0.16);
--badge-bg: rgba(0, 0, 0, 0.08);

/* Dark mode inverts to white with opacity */
--text-primary-dark: #FFFFFF;
--text-secondary-dark: rgba(255, 255, 255, 0.6);
--border-dark: rgba(255, 255, 255, 0.16);
```

---

## What Makes It Work

### Cognitive Simplicity Through Monochrome
The black/white base with a single accent color reduces decision fatigue. Users focus on content, not chrome. The lack of color noise makes the purple accent (when used) feel premium and intentional.

### Variable Typography as Brand Differentiator
Custom variable font with a monospace axis is unprecedented -- it signals "we build tools for designers" without saying it. The non-standard weights (330, 530) avoid the generic feel of 400/700 pairings.

### Progressive Disclosure via Grid Density
The 48-column grid at large viewports allows incredibly precise layout control without visible complexity. Content appears spacious on small screens and dense-but-organized on large ones.

### Opacity-Based Theming
Using a single base color with opacity variations (instead of named gray shades) ensures perfect harmony across light/dark modes and reduces token count while maintaining visual consistency.

### Perceived Speed
- `scroll-behavior: smooth` for navigation
- 160ms button transitions (below the 200ms "instant" threshold)
- `font-display: swap` prevents layout shift

---

## Patterns to Extract

1. **Opacity token system** -- Single-color + opacity approach for creating consistent light/dark theming with minimal tokens
2. **Fluid 48-column grid** -- CSS custom property-based grid that scales from 1 to 48 columns
3. **Ghost button via inset box-shadow** -- No `border` property needed, cleaner hover states
4. **Variable font weight ramp** -- Non-standard weight stops (330, 530) for typographic subtlety
5. **Monochrome + single accent** -- Extreme reduction in color palette forces hierarchy through typography and spacing
6. **Fixed nav with 1px shadow-border** -- `box-shadow: 0 1px 0` instead of `border-bottom` for crisp rendering at any DPI
7. **Block padding scale** -- Responsive vertical rhythm (`5rem` / `7.5rem` / `10rem`) that breathes at larger viewports

---

## Code Snippets

### Responsive Block Padding
```css
.section {
  padding-block: 5rem;
}

@media (min-width: 960px) {
  .section { padding-block: 7.5rem; }
}

@media (min-width: 1920px) {
  .section { padding-block: 10rem; }
}
```

### Card Component
```css
.card {
  background: #FFFFFF;
  border-radius: 0.5rem;
  box-shadow: 0 1.5rem 4.375rem 0 rgba(0, 0, 0, 0.10);
  overflow: hidden;
}
```

### Primary CTA Button
```css
.btn-primary {
  background: var(--f-primary-btn-bg-color, #000000);
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.3125rem;
  font-family: 'figmaSans', system-ui, sans-serif;
  font-weight: 530;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 160ms ease-out;
}

.btn-primary:hover {
  opacity: 0.85;
}
```

### Figma's Motion Easing
```css
/* Primary easing curve */
--ease-figma: cubic-bezier(0.8, 0, 0.2, 1);

/* Transition durations by intent */
--duration-micro: 160ms;   /* Button hover, toggles */
--duration-standard: 250ms; /* Panel transitions */
--duration-emphasis: 400ms;  /* Modal open/close */

.animated {
  transition: transform var(--duration-standard) var(--ease-figma),
              opacity var(--duration-standard) var(--ease-figma);
}
```

### Infinite Carousel (used on homepage)
```css
@keyframes carousel-scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.carousel-track {
  display: flex;
  animation: carousel-scroll 60s linear infinite;
  width: max-content;
}

/* Duplicate items to create seamless loop */
```

---

## Anti-Patterns to Avoid

1. **Do NOT copy the 48-column grid for simple sites** -- It introduces unnecessary complexity unless you genuinely need sub-column precision. 12 columns is sufficient for 95% of layouts.

2. **Do NOT use opacity-only theming without fallbacks** -- `rgba(0,0,0,0.08)` on a non-white background produces unexpected results. Always validate against actual background colors.

3. **Do NOT use weight 330 with system fonts** -- The non-standard weight only works with Figma Sans variable font. System fonts will snap to 300 or 400, producing inconsistent results.

4. **Do NOT overuse monochrome** -- Figma can pull it off because they are a design tool and the content is inherently colorful (screenshots, illustrations). For text-heavy marketing sites, pure monochrome creates a flat, uninviting hierarchy.

5. **Do NOT skip focus states** -- Figma uses dashed outlines which look intentional. If you remove their focus ring pattern, replace it with something equally visible (not just `outline: none`).

6. **Do NOT set gutter to 12px globally** -- Figma only uses 12px gutter below 375px. On mobile, 24px gutter is still the default. Premature gutter reduction kills readability.
