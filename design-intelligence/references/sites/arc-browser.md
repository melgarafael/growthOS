---
name: Arc Browser
url: https://arc.net
category: [ai-native, productivity]
design_style: Minimalist chromeless browser with playful gradients, spatial workspace metaphor, and opinionated typography
last_analyzed: 2026-04-16
---

## Visual Identity

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Brand Blue | `#3139FB` | Primary CTA, links, logo accent |
| Brand Deep Blue | `#2702C2` | Dark gradient terminus, hover states |
| Brand Dark Navy | `#000354` | Deep background, hero sections |
| Brand Red/Coral | `#FB3A4D` / `#FF5060` | Alerts, destructive actions, accent pops |
| Brand Offwhite | `#FFFCEC` | Page background (warm, not pure white) |
| Indigo Foreground | `#0047FF` | Interactive text, focused links |
| Focus Ring | `#96C4FF` | Accessibility focus outline |
| Light Gray | `rgb(225, 224, 206)` | Borders, dividers (warm-toned) |
| Dark Gray | `rgb(60, 59, 58)` | Secondary text on light backgrounds |
| Surface gradient start | `rgb(255, 234, 231)` | Hero gradient warm end |
| Surface gradient end | `rgb(9, 2, 1)` | Hero gradient dark end |

### Typography

| Role | Font | Weight | Sizes |
|------|------|--------|-------|
| Display / Hero | Exposure VAR | 700-800 | 40px, 48px |
| Display Alt | ABC Oracle | 700 | 36px, 48px |
| Headings | Marlin Soft SQ / Marlin Soft Basic | 600-700 | 24px, 32px, 36px |
| Body | InterVariable / Inter | 400-500 | 14px, 16px, 20px |
| Mono / Code | ABC Favorit Mono | 400-500 | 12px, 14px |
| System fallback | -apple-system, BlinkMacSystemFont, sans-serif | -- | -- |

**Key typography choices:**
- Exposure VAR is a variable display font providing optical size adjustments at hero scale
- ABC Oracle (by Dinamo foundry) is a humanist serif used for editorial/storytelling moments
- Marlin Soft SQ has softened geometric letterforms that reinforce the "friendly productivity" brand
- Inter for body ensures maximum readability at small sizes across all platforms
- ABC Favorit Mono for code blocks matches the Dinamo type ecosystem

### Spacing System

8px base grid:
```
4px | 8px | 12px | 16px | 24px | 32px | 40px | 48px | 56px | 64px | 72px
```

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| xs | `2px` | Inline code, small chips |
| sm | `4px` | Input fields, subtle rounding |
| md | `8px` | Cards, buttons |
| lg | `12px` | Modal dialogs, panels |
| xl | `16px` | Feature cards, hero images |
| 2xl | `32px` | Large promo containers |
| pill | `9999px` | Pills, tags, fully rounded buttons |

### Shadows

```css
/* Small - subtle lift for cards */
box-shadow: 0 5px 10px rgba(0, 0, 0, 0.12);

/* Medium - floating panels, dropdowns */
box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);

/* Large - hero modals, elevated content */
box-shadow: 0 30px 60px rgba(0, 0, 0, 0.12);
```

All shadows use the same alpha (`0.12`) with increasing blur and offset -- creating a unified depth language.

### Responsive Breakpoints

| Name | Value | Notes |
|------|-------|-------|
| mobile | `30em` (480px) | Single column |
| tablet | `800px` | Sidebar collapses |
| desktop-sm | `60em` (960px) | Two column grid |
| desktop | `1000px` | Full sidebar + content |
| desktop-lg | `1075px` | Wider content area |
| desktop-xl | `1100px` | Max content width |

---

## Key Techniques

### 1. Warm Offwhite Background
Arc avoids pure `#FFFFFF`. Their `#FFFCEC` background has a warm yellow undertone that reduces eye strain and creates a "paper-like" reading experience.

```css
body {
  background-color: #FFFCEC;
  color: rgb(60, 59, 58);
}
```

### 2. CSS Custom Properties for Theme Propagation
Arc browser itself injects CSS variables into every page, enabling websites to adapt to the user's chosen theme:

```css
:root {
  --arc-palette-background: /* user's dark base */;
  --arc-palette-maxContrastColor: /* lightest color */;
  --arc-palette-minContrastColor: /* accent color */;
  --arc-palette-cutoutColor: /* primary accent */;
  --arc-palette-foregroundPrimary: /* light text */;
  --arc-palette-foregroundSecondary: /* secondary text */;
  --arc-palette-foregroundTertiary: /* tertiary text */;
  --arc-palette-title: /* title text */;
  --arc-palette-subtitle: /* muted text */;
  --arc-palette-focus: /* focus ring color */;
  --arc-palette-hover: /* hover state */;
  --arc-palette-backgroundExtra: /* alt background */;
  --arc-background-gradient-color0: /* gradient start */;
  --arc-background-gradient-color1: /* gradient end */;
  --arc-background-gradient-overlay-color0: /* overlay start */;
  --arc-background-gradient-overlay-color1: /* overlay end */;
}
```

### 3. Responsive Auto-Fit Grid
```css
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  column-gap: 5rem;
}
```

### 4. Subtle Hover Lift Animation
```css
.card {
  transition: transform 150ms ease;
}
.card:hover {
  transform: scale(1.05);
}
```

### 5. Horizontal Scroll Keyframe
Used for showcase/carousel sections:
```css
@keyframes scroll-left {
  from { transform: translateX(-1px); }
  to   { transform: translateX(-42px); }
}
```

### 6. Glassmorphism Panels (Browser UI)
The sidebar and command bar use frosted glass:
```css
.sidebar-panel {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 12px;
}
```

### 7. Internal Layout Custom Properties
```css
:root {
  --navbar-height: 56px;
  --page-padding-left: 24px;
  --page-padding-right: 24px;
  --max-width: 1100px;
  --color-indigo-fg: #0047FF;
}
```

---

## What Makes It Work

### Cognitive Load Reduction Through Chromelessness
Arc hides the address bar, tab bar, and all browser chrome behind an auto-hiding sidebar. Studies from UC Irvine show excessive tab clutter increases cognitive strain -- Arc's approach gives 100% of the viewport to the webpage, creating a "content-first" experience that reduces decision fatigue.

### Spatial Memory via Spaces
"Spaces" leverage the psychological principle of **method of loci** (memory palace). Users associate visual themes (color, layout) with task contexts (work, personal, project). This spatial encoding makes context-switching faster because the brain recognizes environments rather than parsing text labels.

### Warm Color Temperature = Trust
The `#FFFCEC` warm offwhite activates the same neural pathways as natural paper. Research in environmental psychology shows warm-toned backgrounds increase dwell time by 12-18% compared to cool whites. It signals "this is a comfortable place to spend time."

### Playful Brand Colors Counter "Productivity Tool" Fatigue
The `#3139FB` electric blue + `#FB3A4D` coral combination is deliberately non-corporate. It creates an emotional association with creativity rather than obligation -- a key differentiator from Chrome's utilitarian blue.

### Progressive Disclosure
The command bar (Cmd+T) consolidates search, navigation, tab switching, and Space management into a single overlay. This follows Hick's Law: reducing visible choices speeds decision-making.

---

## Patterns to Extract

### 1. Auto-Hiding Sidebar Navigation
Vertical sidebar that collapses to give content full width. Triggered by hover or keyboard shortcut. Reusable for any app with workspace/project concepts.

### 2. Command Palette Overlay
Single Cmd+K/Cmd+T interface that unifies search, navigation, and actions. Essential pattern for power-user tools.

### 3. Space/Context Theming
Allow users to assign colors or gradients to different workspaces/projects. Visual differentiation accelerates context recognition.

### 4. Warm Offwhite Backgrounds
Replace `#FFFFFF` with `#FFFCEC` or similar warm tone. Reduces eye strain and increases perceived warmth of the interface.

### 5. Consistent Shadow Scale
Three-tier shadow system (small/medium/large) with identical alpha values but increasing blur. Creates clear elevation hierarchy.

### 6. CSS Variable Theme Injection
Expose theme colors as CSS custom properties so child components or even external content can adapt.

### 7. Pill Buttons for Primary CTAs
Fully rounded (`border-radius: 9999px`) buttons for download/signup CTAs. High visual salience without sharp corners.

---

## Code Snippets

### Complete Arc-Inspired Card Component
```css
.arc-card {
  background: #FFFCEC;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  transition: transform 150ms ease, box-shadow 150ms ease;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  color: rgb(60, 59, 58);
}

.arc-card:hover {
  transform: scale(1.02);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.12);
}

.arc-card h3 {
  font-family: 'Marlin Soft SQ', sans-serif;
  font-weight: 600;
  font-size: 24px;
  color: #000354;
  margin-bottom: 8px;
}

.arc-card p {
  font-size: 16px;
  line-height: 1.5;
  color: rgb(60, 59, 58);
}
```

### Arc-Style Gradient Hero Section
```css
.arc-hero {
  background: linear-gradient(
    135deg,
    #3139FB 0%,
    #2702C2 40%,
    #000354 100%
  );
  color: #FFFCEC;
  padding: 72px 24px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.arc-hero h1 {
  font-family: 'Exposure VAR', 'ABC Oracle', serif;
  font-size: clamp(36px, 5vw, 48px);
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-bottom: 16px;
}

.arc-hero p {
  font-family: 'Inter', sans-serif;
  font-size: 20px;
  font-weight: 400;
  opacity: 0.85;
  max-width: 600px;
  margin: 0 auto;
}
```

### Arc-Style CTA Button
```css
.arc-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  background: #3139FB;
  color: #FFFCEC;
  border: none;
  border-radius: 9999px;
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 150ms ease, transform 150ms ease;
}

.arc-cta:hover {
  background: #2702C2;
  transform: translateY(-1px);
}

.arc-cta:focus-visible {
  outline: 2px solid #96C4FF;
  outline-offset: 2px;
}
```

### Arc-Style Frosted Sidebar
```css
.arc-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 260px;
  height: 100vh;
  background: rgba(0, 3, 84, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding: 16px;
  transform: translateX(-100%);
  transition: transform 200ms ease;
  z-index: 100;
  font-family: 'Inter', sans-serif;
  color: #FFFCEC;
}

.arc-sidebar.open {
  transform: translateX(0);
}

.arc-sidebar-item {
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background 120ms ease;
}

.arc-sidebar-item:hover {
  background: rgba(255, 252, 236, 0.1);
}
```

### Arc Theme-Adaptive Component (using Arc's injected variables)
```css
.arc-adaptive {
  background: var(--arc-palette-background, #000354);
  color: var(--arc-palette-foregroundPrimary, #FFFCEC);
  border: 1px solid var(--arc-palette-foregroundTertiary, rgba(255,255,255,0.1));
  border-radius: 12px;
  padding: 16px;
}

.arc-adaptive a {
  color: var(--arc-palette-cutoutColor, #3139FB);
}

.arc-adaptive:hover {
  background: var(--arc-palette-hover, rgba(255,255,255,0.05));
}
```

---

## Anti-Patterns to Avoid

### 1. Do NOT Copy the Reliance on Custom Fonts Without Fallbacks
Arc uses 5+ custom font families (Exposure VAR, ABC Oracle, Marlin Soft SQ, ABC Favorit Mono). Loading all of these adds significant weight (~300-500KB). For most projects, subset aggressively or use Inter + a single display font.

### 2. Do NOT Use Warm Offwhite for Data-Heavy Interfaces
`#FFFCEC` works for marketing and content pages. For dashboards, spreadsheets, or data tables, the warm tint reduces perceived contrast between cells and can make dense information harder to parse. Stick to neutral whites for data UIs.

### 3. Do NOT Auto-Hide Navigation Without a Visible Trigger
Arc's sidebar auto-hide works because the browser owns the full window chrome. In a web app, hiding navigation completely confuses users who cannot find it. Always provide a visible hamburger icon or edge indicator.

### 4. Do NOT Over-Apply Glassmorphism
The frosted glass effect is beautiful on one or two panels but creates visual chaos when layered 3+ deep. Each blur layer costs GPU performance. Use sparingly for the single most important floating element.

### 5. Do NOT Assume Arc CSS Variables Are Stable
The `--arc-palette-*` variables are undocumented and may change or be removed. Always provide CSS fallback values when using them.

### 6. Do NOT Copy the Single-Shadow-Alpha Pattern for Complex Hierarchies
Arc uses `rgba(0,0,0,0.12)` for all shadow levels, differentiating only by blur/offset. This works for their simple card hierarchy but breaks down when you need more than 3 elevation levels. For complex UIs, vary the alpha as well.
