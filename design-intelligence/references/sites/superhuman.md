---
name: Superhuman
url: https://superhuman.com
category: [productivity, saas]
design_style: "Speed-focused dark/light duality, deep purple gradients, warm neutrals, keyboard-first ethos"
last_analyzed: 2026-04-16
---

## Visual Identity

### Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| Mysteria Purple | `#1B1938` | Hero gradient background, dark surfaces |
| Lavender Glow | `#CBB7FB` | Primary accent, highlight color |
| Amethyst Link | `#714CB6` | Underlined links, interactive text |
| Charcoal Ink | `#292827` | Primary text on light backgrounds |
| Pure White | `#FFFFFF` | Page background, light surfaces |
| Warm Cream | `#E9E5DD` | Button backgrounds, warm surface areas |
| Parchment Border | `#DCD7D3` | Card borders, dividers, form borders |
| Translucent White 95% | `rgba(255, 255, 255, 0.95)` | Hero text on dark gradient |
| Misted White 80% | `rgba(255, 255, 255, 0.80)` | Secondary text on dark |
| Translucent Border | `rgba(255, 255, 255, 0.20)` | Borders on dark surfaces |
| Error Red | `#C0392B` | Form validation, error states |
| Cod Gray (Dark BG) | `#0B0B0B` | Deepest dark theme surface |
| Picton Blue | `#56C1FF` | Accent blue for interactive elements |

### Dark Theme: Five Shades of Gray

Superhuman's in-app dark theme uses exactly five gray shades, built on the principle that **nearer surfaces are lighter, distant surfaces are darker** (simulating overhead lighting):

| Depth | Approximate Value | Usage |
|-------|-------------------|-------|
| Surface 5 (nearest) | `~#3D3D3D` | Modals, dropdowns, popovers |
| Surface 4 | `~#2D2D2D` | Cards, elevated containers |
| Surface 3 | `~#232323` | Secondary panels, sidebars |
| Surface 2 | `~#1A1A1A` | Main content area |
| Surface 1 (farthest) | `~#121212` | Base background, deepest layer |

**Key rule:** No pure black (`#000000`) or pure white (`#FFFFFF`) in the dark theme. Every element uses tempered values.

### Typography

**Primary Font Family:** Super Sans VF (Variable Font)
- Custom variable font loaded from `superhumanstatic.com`
- Format: WOFF2 with `font-display: swap`
- Weight range: 100-900 (continuous)
- **Non-standard weight stops used:** 460, 540, 600, 700

**Additional Families:**
- **Super Serif VF** -- Variable serif for editorial/marketing content
- **Super Sans Mono VF** -- Variable monospace for keyboard shortcuts, code

**CSS Font Stack (fallback):**
```css
font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Oxygen, Ubuntu, 
             Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
```

**Type Scale:**

| Level | Size | Weight | Line-height | Letter-spacing |
|-------|------|--------|-------------|----------------|
| Display Hero | 64px | 540 | 0.96 | -- |
| Section Display | 48px | 460 | 0.96 | -1.32px |
| H3 | 32px | 540 | 1.10 | -- |
| Body Large | 20px | 460 | 1.50 | -- |
| Body | 16px | 460 | 1.50 | -- |
| Body Small | 14px | 460 | 1.50 | -- |
| Micro Label | 12px | 700 | 1.50 | -- |

### Spacing System

8px base unit. Scale:

```
2  4  6  8  12  16  18  20  24  28  32  36  40  48  56  (px)
```

### Border Radius

| Context | Value |
|---------|-------|
| Buttons, inputs, inline elements | `8px` |
| Cards, containers | `16px` |

### Elevation / Shadows

| Level | Value | Usage |
|-------|-------|-------|
| Flat | `none` | Default, no elevation |
| Border | `1px solid #DCD7D3` | Cards, containers at rest |
| Glow | `0 4px 16px rgba(0, 0, 0, 0.08)` | Hover cards, elevated panels |
| Hover Lift | `translateY(-2px)` + shadow increase | Interactive card hover state |

---

## Key Techniques

### Warm Neutral Palette Instead of Cool Grays
```css
/* Superhuman avoids the typical #F5F5F5 cool gray.
   Their neutrals have warm undertones (cream, parchment). */
:root {
  --surface-warm: #E9E5DD;    /* Warm cream -- buttons, tags */
  --border-warm: #DCD7D3;     /* Parchment -- borders, dividers */
  --text-primary: #292827;    /* Charcoal with warm undertone */
  --bg-page: #FFFFFF;
}
```

### Dark Theme Depth via Gray Ramp (No Pure Black)
```css
/* 5-shade system: closer = lighter */
:root[data-theme="dark"] {
  --surface-base: #121212;    /* Farthest from user */
  --surface-main: #1A1A1A;
  --surface-secondary: #232323;
  --surface-card: #2D2D2D;
  --surface-modal: #3D3D3D;   /* Nearest to user */
}
```

### Perceptual Contrast Adjustment
```css
/* Light theme: black at 60% opacity for secondary text */
.contact-details-light {
  color: rgba(0, 0, 0, 0.60);
}

/* Dark theme: white at 65% (not 60%) -- 
   compensates for perceived lower contrast on dark backgrounds */
.contact-details-dark {
  color: rgba(255, 255, 255, 0.65);
}
```

### Variable Font with Non-Standard Weight Stops
```css
@font-face {
  font-family: 'Super Sans VF';
  src: url('https://superhumanstatic.com/fonts/super-sans-vf.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}

/* Non-standard stops create unique typographic feel */
.body { font-weight: 460; }       /* Heavier than regular, lighter than medium */
.heading { font-weight: 540; }    /* Between medium and semi-bold */
.label { font-weight: 700; }      /* Standard bold */
```

### Hero Gradient with Semi-Transparent Overlay
```css
.hero {
  background: linear-gradient(135deg, #1B1938 0%, #2A1B4E 50%, #1B1938 100%);
  position: relative;
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at 50% 0%,
    rgba(203, 183, 251, 0.15) 0%,
    transparent 70%
  );
  pointer-events: none;
}

.hero-text {
  color: rgba(255, 255, 255, 0.95);
}

.hero-subtext {
  color: rgba(255, 255, 255, 0.80);
}
```

---

## What Makes It Work

### Speed as Design Language
Every visual choice reinforces the "fastest email" positioning. Minimal decoration, no gratuitous animation, tight line-heights on headlines (0.96) -- the design communicates efficiency before the user reads a word.

### Warm Neutrals Signal Premium Without Coldness
The `#E9E5DD` cream and `#DCD7D3` parchment tones feel expensive (like thick paper stock) while remaining functional. Cold grays feel "techy"; warm neutrals feel "crafted."

### Dark Theme Done Right: Individual Adjustment
Superhuman rejects the "just invert colors" approach. Each element's contrast is tuned individually -- considering text size, font weight, and line width. Small text gets higher contrast; thick elements can tolerate less. This per-element tuning is why their dark theme feels "designed" rather than "generated."

### Keyboard-First UX Reflected in Typography
The monospaced keyboard shortcut labels (Super Sans Mono VF) and the micro-label style (12px/700) create a visual language that celebrates keyboard mastery. Typography literally teaches the user to be faster.

### Depth via Surface Hierarchy
Five gray shades create clear z-axis layering. Users intuitively understand which elements are interactive (lighter/nearer) vs. background (darker/farther) without relying on shadows.

---

## Patterns to Extract

1. **Warm neutral token set** -- Replace cool grays (#F5F5F5) with warm tones (#E9E5DD, #DCD7D3) for premium feel
2. **5-shade dark theme** -- Systematic gray ramp from #121212 to #3D3D3D based on proximity principle
3. **Perceptual contrast offset** -- Different opacity values for light vs dark themes (60% vs 65%) to maintain perceived contrast
4. **Non-standard font weights** -- 460/540 weight stops for typographic distinction without custom fonts
5. **Border-only elevation** -- `1px solid` as default, shadow only on hover interaction
6. **Hero gradient + radial glow** -- Deep purple base with subtle radial Lavender highlight from top-center
7. **Micro label style** -- 12px/700 uppercase for keyboard shortcuts and metadata
8. **Hover lift pattern** -- `translateY(-2px)` + shadow expansion for interactive cards

---

## Code Snippets

### Warm Button System
```css
.btn-primary-warm {
  background: #E9E5DD;
  color: #292827;
  border: none;
  border-radius: 8px;
  padding: 14px 24px;
  font-weight: 540;
  font-size: 16px;
  cursor: pointer;
  transition: background 200ms ease;
}

.btn-primary-warm:hover {
  background: #DCD7D3;
}

.btn-dark {
  background: #292827;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  padding: 14px 24px;
  font-weight: 540;
}

.btn-outline {
  background: transparent;
  color: #292827;
  border: 1px solid #DCD7D3;
  border-radius: 8px;
  padding: 14px 24px;
}

.btn-ghost {
  background: none;
  border: none;
  color: #714CB6;
  text-decoration: underline;
  font-weight: 460;
}
```

### Card with Hover Lift
```css
.card {
  background: #FFFFFF;
  border: 1px solid #DCD7D3;
  border-radius: 16px;
  padding: 24px;
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}
```

### Dark Surface Card
```css
.card-dark {
  background: #292827;
  border: 1px solid #292827;
  border-radius: 16px;
  padding: 24px;
  color: rgba(255, 255, 255, 0.95);
}
```

### Hero Section with Gradient Glow
```css
.hero-section {
  background: #1B1938;
  background-image: 
    radial-gradient(ellipse at 50% 0%, rgba(203, 183, 251, 0.15) 0%, transparent 60%),
    linear-gradient(135deg, #1B1938 0%, #2A1B4E 40%, #1B1938 100%);
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.hero-title {
  font-size: 64px;
  font-weight: 540;
  line-height: 0.96;
  color: rgba(255, 255, 255, 0.95);
  max-width: 800px;
}

.hero-subtitle {
  font-size: 20px;
  font-weight: 460;
  line-height: 1.50;
  color: rgba(255, 255, 255, 0.80);
  margin-top: 24px;
}
```

### Form Input (Warm Style)
```css
.input-warm {
  background: #FFFFFF;
  border: 1px solid #DCD7D3;
  border-radius: 8px;
  padding: 12px;
  font-size: 16px;
  font-weight: 460;
  color: #292827;
  transition: border-color 200ms ease;
}

.input-warm:focus {
  border-color: #292827;
  outline: none;
}

.input-warm.error {
  border-color: #C0392B;
}
```

### Keyboard Shortcut Label
```css
.kbd-label {
  font-family: 'Super Sans Mono VF', 'SF Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.5;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: rgba(0, 0, 0, 0.65);
  background: rgba(0, 0, 0, 0.06);
  padding: 2px 6px;
  border-radius: 4px;
}
```

---

## Anti-Patterns to Avoid

1. **Do NOT use pure black (#000000) in dark themes** -- Superhuman explicitly avoids this. Use `#121212` as the darkest value. Pure black against gray surfaces creates harsh, jarring contrast.

2. **Do NOT apply a single opacity value to all text** -- Superhuman adjusts contrast per-element based on text size and weight. Small text needs higher contrast than large headings. A blanket `opacity: 0.7` produces inconsistent readability.

3. **Do NOT replicate the warm neutrals with cool brand colors** -- The cream/parchment tones only work because Superhuman's accent (purple) has warm undertones. Pairing warm neutrals with a cold blue accent creates visual dissonance.

4. **Do NOT overuse the hover lift** -- `translateY(-2px)` on every interactive element creates a "bouncy" feeling that undermines the speed aesthetic. Reserve it for cards and primary actions only.

5. **Do NOT copy the 5-shade system without testing** -- The gray values depend on your specific color temperature. Test each shade against actual content (text, images, icons) in both light conditions. Monitor vs. phone screens render dark grays very differently.

6. **Do NOT use variable font weight stops (460, 540) without the actual variable font** -- Standard fonts will snap to 400/500/600, producing unintended results. Either use Super Sans VF or stick to standard weight stops.

7. **Do NOT add gradients for decoration** -- Superhuman's purple gradient serves a functional purpose (hero hierarchy). Random gradients on cards or sections dilute the premium feel.
