---
name: Linear
url: https://linear.app
category: [saas, productivity, developer-tool]
design_style: Ultra-minimal dark-first UI with desaturated indigo accent and precision typography
last_analyzed: 2026-04-16
---

## Visual Identity

### Brand Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Brand Indigo | `#5E6AD2` | Primary brand, accent, links |
| Accent Violet | `#7170FF` | Interactive hover states, highlights |
| Accent Hover | `#828FFF` | Hover state on accent elements |
| Mercury White | `#F4F5F8` | Light mode wordmark, light backgrounds |
| Nordic Gray | `#222326` | Dark mode wordmark, dark surface text |

### Dark Theme Palette (Primary -- default experience)

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-page` | `#08090A` | Page background (near-black) |
| `--bg-surface` | `#0F1011` | Card/component surface |
| `--bg-elevated` | `#191A1B` | Elevated panels, dialogs |
| `--bg-hover` | `#28282C` | Hover state backgrounds |
| `--text-primary` | `#F7F8F8` | Primary text |
| `--text-secondary` | `#D0D6E0` | Secondary text |
| `--text-tertiary` | `#8A8F98` | Tertiary/placeholder text |
| `--text-quaternary` | `#62666D` | Disabled/muted text |
| `--border-primary` | `#23252A` | Primary borders |
| `--border-secondary` | `#34343A` | Secondary borders |
| `--border-tertiary` | `#3E3E44` | Tertiary borders |
| `--border-subtle` | `rgba(255,255,255,0.05)` | Subtle dividers |
| `--border-standard` | `rgba(255,255,255,0.08)` | Standard borders |
| Security Lavender | `#7A7FAD` | Security/admin indicators |

### Light Theme Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-page` | `#F7F8F8` | Page background |
| `--bg-surface` | `#FFFFFF` | Card/component surface |
| `--bg-panel` | `#F3F4F5` | Panel backgrounds |
| `--text-primary` | `#1A1A1E` | Primary text |
| `--text-secondary` | `#3C3C43` | Secondary text |
| `--text-tertiary` | `#62666D` | Tertiary text |
| `--text-quaternary` | `#8A8F98` | Muted text |
| `--border-primary` | `#D0D6E0` | Primary borders |
| `--border-subtle` | `#E6E6E6` | Subtle borders |
| `--border-light` | `rgba(0,0,0,0.08)` | Light borders |

### Status Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Success | `#27A644` | Success states |
| Emerald | `#10B981` | Positive indicators |

### Typography

| Element | Font | Size | Weight | Line-Height | Letter-Spacing |
|---------|------|------|--------|-------------|----------------|
| **Sans stack** | `Inter Variable, -apple-system, BlinkMacSystemFont, sans-serif` | -- | -- | -- | -- |
| **Mono stack** | `Berkeley Mono, SF Mono, ui-monospace, monospace` | -- | -- | -- | -- |
| Display | Inter Display | 48px | 510 | 1.00 | -1.056px |
| Heading 1 | Inter Display | 32px | 510 | 1.13 | -0.704px |
| Body Large | Inter | 18px | 400 | 1.60 | -0.165px |
| Body / Small | Inter | 15px | 400 | 1.60 | 0 |
| Label | Inter | 12px | 510 | 1.40 | 0 |
| Mono | Berkeley Mono | 14px | 400 | 1.50 | 0 |

**Note:** Inter Display is used specifically for headings (more expressive), while regular Inter handles body text. The font weight `510` is a variable font value -- slightly heavier than medium (500), providing subtle emphasis without looking bold.

Font loaded from: `https://static.linear.app/fonts/InterVariable.woff2?v=4.1`

### Spacing Scale

| Step | Value |
|------|-------|
| xs | 4px |
| sm | 8px |
| md | 12px |
| base | 16px |
| lg | 20px |
| xl | 24px |
| 2xl | 32px |
| 3xl | 35px |

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| Badge | 2px | Status badges, tags |
| Small | 4px | Small interactive elements |
| Button | 6px | Buttons, inputs |
| Card | 8px | Cards, list items |
| Panel | 12px | Panels, modals |
| Large | 22px | Large containers |
| Pill | 9999px | Pill shapes, toggle switches |

### Shadows

**Dark Theme:**
| Token | Value |
|-------|-------|
| Ring | `rgba(0,0,0,0.2) 0px 0px 0px 1px` |
| Card | `rgba(0,0,0,0.2) 0px 0px 0px 1px, rgba(0,0,0,0.3) 0px 2px 4px` |
| Elevated | `rgba(0,0,0,0.4) 0px 2px 4px, rgba(0,0,0,0.2) 0px 0px 0px 1px` |

**Light Theme:**
| Token | Value |
|-------|-------|
| Ring | `rgba(0,0,0,0.08) 0px 0px 0px 1px` |
| Subtle | `rgba(0,0,0,0.04) 0px 2px 4px 0px` |
| Card | Ring + Subtle combined |
| Elevated | Ring + `rgba(0,0,0,0.06) 0px 4px 12px 0px` |

## Key Techniques

### 1. LCH Color Space Theme Generation

Linear's theme system uses just **3 variables** to generate an entire theme (replacing 98 manually defined variables):

```javascript
// Conceptual model
const theme = generateTheme({
  baseColor: lch(20, 2, 260),    // Near-black with cool undertone
  accentColor: lch(50, 40, 264), // Desaturated indigo
  contrast: 75                    // Range: 30-100, for accessibility
});
```

**Why LCH over HSL:** LCH is perceptually uniform -- a red and yellow at lightness 50 appear equally light to the human eye. HSL does not have this property, causing inconsistent themes when users pick different base hues.

The contrast parameter (30-100) automatically generates high-contrast themes for accessibility without separate theme definitions.

### 2. Surface Elevation System (Dark Mode)

Dark mode uses lighter surfaces at higher elevation, NOT shadows (which disappear against dark backgrounds):

```css
/* Base layer */
.page { background: #08090A; }

/* Surface (elevation 1) */
.card { background: #0F1011; }

/* Elevated (elevation 2) */
.dialog { background: #191A1B; }

/* Hover state (elevation 3) */
.card:hover { background: #28282C; }
```

Each step increases lightness by approximately 4-6% in LCH space, maintaining perceptual uniformity.

### 3. Subtle Border + Ring Shadow Pattern

Instead of traditional box-shadows, Linear uses a `ring` pattern -- a 1px inset outline via box-shadow:

```css
.linear-card {
  background: #0F1011;
  border-radius: 8px;
  box-shadow: rgba(0,0,0,0.2) 0px 0px 0px 1px;
}

.linear-card:hover {
  background: #191A1B;
  box-shadow:
    rgba(0,0,0,0.2) 0px 0px 0px 1px,
    rgba(0,0,0,0.3) 0px 2px 4px;
}
```

### 4. Warm Gray Shift (2025 Redesign)

The 2025 refresh moved from cool blue-gray undertones to warmer, less saturated grays. This reduces eye strain in prolonged dark-mode use while maintaining crispness.

### 5. Reduced Color Philosophy

The 2025 redesign significantly cut color usage -- swapping monochrome blue for monochrome black/white with even fewer accent colors. The indigo `#5E6AD2` is reserved for primary actions only.

## What Makes It Work

### Psychological Principles

1. **Engineer's Aesthetic** -- Dark backgrounds mimic coding environments (VS Code, terminal). Engineers feel immediately at home, reducing cognitive onboarding friction. The founder explicitly designed it to look "professional to engineers."

2. **Calm Authority** -- The desaturated indigo (#5E6AD2) conveys authority without urgency. Unlike bright blues or reds, it does not trigger stress responses. This matches the product's promise: bringing calm to chaotic project management.

3. **Information Density Without Clutter** -- Linear achieves high data density through precise spacing (4px grid), subtle borders (rgba at 0.05-0.08 opacity), and typographic hierarchy (weight 510 vs 400). No decorative elements compete for attention.

4. **Monochrome Focus** -- By removing almost all color except the indigo accent, every colored element carries meaning. Color is signal, not decoration.

5. **Battery & Eye Strain** -- Dark mode saves battery on OLED screens and reduces eye fatigue. For a productivity tool used 8+ hours daily, this is a functional advantage, not just aesthetic.

## Patterns to Extract

### Reusable Pattern 1: Dark Minimal Card
- Near-black background with subtle 1px ring shadow
- Hover elevates background color (not shadow)
- 8px border-radius, 16px padding
- Single accent color for interactive elements

### Reusable Pattern 2: Semantic Elevation Stack
- Page -> Surface -> Elevated -> Hover
- Each level is a background-color change, not a shadow change
- In dark mode: `#08090A` -> `#0F1011` -> `#191A1B` -> `#28282C`
- In light mode: `#F7F8F8` -> `#FFFFFF` -> `#F3F4F5`

### Reusable Pattern 3: LCH-Based Theme System
- 3 variables (base, accent, contrast) generate full theme
- LCH ensures perceptual uniformity
- Contrast param enables automatic accessibility support

### Reusable Pattern 4: Typography with Variable Weight
- Display: 510 weight, tight negative tracking (-1.056px at 48px)
- Body: 400 weight, relaxed line-height (1.60)
- Label: 510 weight at small size (12px) for micro-hierarchy

### Reusable Pattern 5: Border-as-Ring
- Use `box-shadow: 0 0 0 1px` instead of CSS `border`
- Avoids border affecting box model
- Cleaner rendering at subpixel levels

## Code Snippets

### Linear Dark Card

```css
.linear-card {
  background: #0F1011;
  border-radius: 8px;
  padding: 16px;
  box-shadow: rgba(0,0,0,0.2) 0px 0px 0px 1px;
  color: #F7F8F8;
  font-family: "Inter Variable", -apple-system, BlinkMacSystemFont, sans-serif;
  transition: background 0.15s ease;
}

.linear-card:hover {
  background: #191A1B;
}

.linear-card h3 {
  font-size: 15px;
  font-weight: 510;
  line-height: 1.40;
  color: #F7F8F8;
  margin: 0 0 4px;
}

.linear-card p {
  font-size: 14px;
  font-weight: 400;
  line-height: 1.60;
  color: #8A8F98;
  margin: 0;
}
```

### Linear Page Layout

```css
:root {
  --bg-page: #08090A;
  --bg-surface: #0F1011;
  --bg-elevated: #191A1B;
  --text-primary: #F7F8F8;
  --text-secondary: #D0D6E0;
  --text-tertiary: #8A8F98;
  --accent: #5E6AD2;
  --accent-hover: #7170FF;
  --border: rgba(255,255,255,0.08);
  --radius-card: 8px;
  --radius-button: 6px;
}

body {
  background: var(--bg-page);
  color: var(--text-primary);
  font-family: "Inter Variable", -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 15px;
  line-height: 1.60;
  -webkit-font-smoothing: antialiased;
}

.sidebar {
  background: var(--bg-surface);
  border-right: 1px solid var(--border);
  width: 240px;
}

.main-content {
  padding: 24px;
}
```

### Linear Button

```css
.linear-button {
  background: #5E6AD2;
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 510;
  line-height: 1.40;
  cursor: pointer;
  transition: background 0.15s ease;
}

.linear-button:hover {
  background: #7170FF;
}

.linear-button--secondary {
  background: rgba(255,255,255,0.08);
  color: #D0D6E0;
}

.linear-button--secondary:hover {
  background: rgba(255,255,255,0.12);
}
```

### Linear Display Heading

```css
.linear-display {
  font-family: "Inter Display", "Inter Variable", sans-serif;
  font-size: 48px;
  font-weight: 510;
  line-height: 1.00;
  letter-spacing: -1.056px;
  color: #F7F8F8;
}

.linear-h1 {
  font-family: "Inter Display", "Inter Variable", sans-serif;
  font-size: 32px;
  font-weight: 510;
  line-height: 1.13;
  letter-spacing: -0.704px;
  color: #F7F8F8;
}
```

## Anti-Patterns to Avoid

1. **Do NOT use pure black (`#000000`) as background.** Linear uses `#08090A` -- a slightly warm near-black. Pure black creates harsh contrast with text and causes eye strain. The slight warmth matters.

2. **Do NOT add color to "make it pop."** Linear's power comes from color absence. The indigo accent works BECAUSE almost everything else is monochrome. Adding decorative colors defeats the design philosophy.

3. **Do NOT use HSL for theme generation.** Linear switched from HSL to LCH specifically because HSL produces perceptually non-uniform results. A "50% lightness" red looks dramatically different from a "50% lightness" yellow in HSL.

4. **Do NOT use heavy shadows in dark mode.** Shadows are invisible against dark backgrounds. Linear uses background elevation changes and subtle ring shadows instead. If you add `box-shadow: 0 4px 12px rgba(0,0,0,0.5)` to a dark card, it looks like nothing.

5. **Do NOT use regular `border` for card outlines.** Linear uses `box-shadow: 0 0 0 1px` (ring pattern) instead. This avoids border affecting the box model and renders more cleanly at fractional pixel values.

6. **Do NOT skip `-webkit-font-smoothing: antialiased` on dark backgrounds.** Without it, light text on dark backgrounds appears heavier/bolder than intended. This is critical for Inter at weight 400.

7. **Do NOT use Inter Display below 24px.** It is optimized for headlines. At body sizes, its wider spacing and looser curves reduce readability vs regular Inter.
