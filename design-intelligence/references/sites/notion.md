---
name: Notion
url: https://notion.so
category: [productivity, saas]
design_style: "Content-first minimalism, black-and-white primary palette, 10-color constrained system, bento grid marketing"
last_analyzed: 2026-04-16
---

## Visual Identity

### Color Palette -- Brand

| Token | Value | Usage |
|-------|-------|-------|
| Primary Black | `#000000` | Brand mark, primary headings |
| Primary White | `#FFFFFF` | Page background, card surfaces |
| Default Text (Light) | `#373530` | Body text, paragraphs |
| Default Text (Dark) | `#D4D4D4` | Body text in dark mode |
| Default BG (Dark) | `#191919` | Page background in dark mode |

### 10-Color System -- Light Mode

Notion deliberately constrains its palette to exactly 10 colors (plus default). Each color has three tokens: text, background, and icon.

| Color | Text | Background | Icon |
|-------|------|------------|------|
| Default | `#373530` | `#FFFFFF` | `#55534E` |
| Gray | `#787774` | `#F1F1EF` | `#A6A299` |
| Brown | `#976D57` | `#F3EEEE` | `#9F6B53` |
| Orange | `#CC782F` | `#F8ECDF` | `#D87620` |
| Yellow | `#C29343` | `#FAF3DD` | `#CB912F` |
| Green | `#548164` | `#EEF3ED` | `#448361` |
| Blue | `#487CA5` | `#E9F3F7` | `#337EA9` |
| Purple | `#8A67AB` | `#F6F3F8` | `#9065B0` |
| Pink | `#B35488` | `#F9F2F5` | `#C14C8A` |
| Red | `#C4554D` | `#FAECEC` | `#D44C47` |

### 10-Color System -- Dark Mode

| Color | Text | Background | Icon |
|-------|------|------------|------|
| Default | `#D4D4D4` | `#191919` | `#D3D3D3` |
| Gray | `#9B9B9B` | `#252525` | `#7F7F7F` |
| Brown | `#A27763` | `#2E2724` | `#AA755F` |
| Orange | `#CB7B37` | `#36291F` | `#D9730D` |
| Yellow | `#C19138` | `#372E20` | `#CA8E1B` |
| Green | `#4F9768` | `#242B26` | `#2D9964` |
| Blue | `#447ACB` | `#1F282D` | `#2E7CD1` |
| Purple | `#865DBB` | `#2A2430` | `#8D5BC1` |
| Pink | `#BA4A78` | `#2E2328` | `#C94079` |
| Red | `#BE524B` | `#332523` | `#CD4945` |

**Key design decision:** Icon colors are always more saturated and vibrant than text colors of the same hue. This creates visual hierarchy where icons "pop" while text remains readable and restrained.

### Marketing Page Accent Colors

Used on notion.com landing pages for feature sections and bento cards:

| Color | Approximate Value | Usage |
|-------|-------------------|-------|
| Warm Orange | `#FF8A33` | Feature highlights, AI section |
| Vivid Purple | `#AD6DED` | Premium/enterprise features |
| Teal | `#2A9D99` | Collaboration features |
| Coral Red | `#E16259` | Notifications, alerts |
| Soft Blue | `#529CCA` | Data/analytics features |

### Typography

**Primary Font:** Inter (Notion Inter)

| Variant | Weight | Usage |
|---------|--------|-------|
| Inter Regular | 400 | Body text, paragraphs |
| Inter Medium | 500 | Headings (H2-H6), nav labels |
| Inter SemiBold | 600 | Marketing headlines, CTAs |
| Inter Bold | 700 | Display headlines on marketing pages |

**In-App Font Options (3 choices):**

| Option | Font Family | Character |
|--------|-------------|-----------|
| Default | Inter / system sans-serif | Clean, modern, neutral |
| Serif | Georgia / Charter / system serif | Editorial, long-form reading |
| Mono | iA Writer Mono / Consolas / system mono | Technical, note-taking, drafts |

**CSS Font Stack (website):**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 
             Helvetica, Arial, sans-serif;
```

**Type Scale (estimated from website):**

| Level | Size | Weight | Line-height |
|-------|------|--------|-------------|
| Display | 56-64px | 700 | 1.1 |
| H1 | 40-48px | 700 | 1.15 |
| H2 | 32px | 600 | 1.25 |
| H3 | 24px | 600 | 1.3 |
| Body Large | 20px | 400 | 1.6 |
| Body | 16px | 400 | 1.6 |
| Small / Caption | 14px | 400 | 1.5 |

### Spacing

Notion uses an 8px base grid with generous whitespace:

| Token | Value | Usage |
|-------|-------|-------|
| Page margin (desktop) | 96px | Side margins on content pages |
| Page margin (mobile) | 16-24px | Compact mobile margins |
| Section gap | 64-80px | Between major content sections |
| Card gap (bento) | 16px | Between bento grid cards |
| Content max-width | 720px | In-app page content width |
| Marketing max-width | 1200px | Marketing page content |
| Full-width max | 1440px | Edge-to-edge hero sections |

### Border Radius

| Context | Value |
|---------|-------|
| Buttons | `8px` |
| Cards (bento) | `12-16px` |
| Input fields | `6px` |
| Avatars | `50%` (circle) |
| Page previews | `8px` |
| Modal/dialog | `12px` |

### Shadows

| Level | Value | Usage |
|-------|-------|-------|
| Subtle | `0 1px 2px rgba(0, 0, 0, 0.04)` | Cards at rest |
| Card | `0 4px 12px rgba(0, 0, 0, 0.08)` | Elevated cards |
| Modal | `0 8px 32px rgba(0, 0, 0, 0.12)` | Dialogs, popovers |
| Dropdown | `0 4px 16px rgba(0, 0, 0, 0.10)` | Menus, dropdowns |

---

## Key Techniques

### Bento Grid Layout for Feature Communication
```css
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

.bento-item { border-radius: 16px; overflow: hidden; padding: 32px; }
.bento-large { grid-column: span 2; grid-row: span 2; }
.bento-wide { grid-column: span 2; }
.bento-tall { grid-row: span 2; }

@media (max-width: 768px) {
  .bento-grid { grid-template-columns: repeat(2, 1fr); }
  .bento-large { grid-column: span 2; grid-row: span 1; }
}

@media (max-width: 480px) {
  .bento-grid { grid-template-columns: 1fr; }
  .bento-large, .bento-wide { grid-column: span 1; }
}
```

### Three-Token-Per-Color System
```css
/* Each of 10 colors has text, background, and icon variants */
:root {
  --blue-text: #487CA5;
  --blue-bg: #E9F3F7;
  --blue-icon: #337EA9;   /* More saturated than text */
  
  --green-text: #548164;
  --green-bg: #EEF3ED;
  --green-icon: #448361;
}

/* Dark mode overrides */
[data-theme="dark"] {
  --blue-text: #447ACB;
  --blue-bg: #1F282D;
  --blue-icon: #2E7CD1;
}

/* Usage pattern */
.tag-blue {
  color: var(--blue-text);
  background: var(--blue-bg);
}

.icon-blue {
  color: var(--blue-icon);
}
```

### Color-Coded Feature Sections
```css
/* Notion uses tinted backgrounds to group related features */
.feature-analytics { background: #E9F3F7; }  /* Blue tint */
.feature-collab { background: #EEF3ED; }      /* Green tint */
.feature-ai { background: #F8ECDF; }          /* Orange tint */
.feature-docs { background: #F6F3F8; }        /* Purple tint */
```

### Content-Width Constraint for Readability
```css
/* Notion in-app: strict 720px content width for readability */
.page-content {
  max-width: 720px;
  margin: 0 auto;
  padding: 0 96px;
  font-size: 16px;
  line-height: 1.6;
}

/* Full-width toggle expands to fill viewport */
.page-content.full-width {
  max-width: 100%;
  padding: 0 96px;
}

@media (max-width: 768px) {
  .page-content { padding: 0 24px; }
}
```

---

## What Makes It Work

### Deliberate Constraint Creates Coherence
CEO Ivan Zhao is known for being extremely selective about color. The 10-color system is not a limitation -- it is a deliberate constraint that forces consistency. When every page, every tag, every highlight uses the same 10 colors, the entire product feels unified.

### Three Tokens Per Color Solve the Saturation Problem
By giving each color a distinct text, background, and icon variant, Notion avoids the common pitfall of a single color value that looks good as text but washed-out as a background (or vice versa). Icon colors are pushed toward higher saturation to remain visible at small sizes.

### Black-and-White as Default Reduces Visual Noise
The primary palette is literally `#000000` and `#FFFFFF`. Color is reserved for user-applied semantics (tags, highlights, callouts). This means the UI recedes and the user's content takes center stage -- a textbook content-first approach.

### Bento Grid Sizes Match Content Importance
On Notion's marketing pages, card sizes in the bento grid directly correspond to feature importance. A feature that benefits from a large screenshot gets a 2x2 card; simpler capabilities get 1x1. Size IS the hierarchy signal.

### Typography Scale Optimized for Long-Form Reading
The 16px/1.6 body text with 720px max-width hits the research-backed sweet spot: 65-75 characters per line, sufficient line-height to avoid re-reading. The "Small text" toggle reduces this for dense reference content.

### Warm Muted Backgrounds Instead of Saturated Blocks
Background colors like `#F1F1EF` (gray), `#F8ECDF` (orange), `#E9F3F7` (blue) are extremely desaturated. They tint the surface without competing with content. This is the opposite of using saturated background blocks.

---

## Patterns to Extract

1. **10-color constrained palette** -- With three tokens per color (text/bg/icon), covering all semantic needs
2. **Bento grid with semantic sizing** -- Card size communicates importance (2x2 = hero, 1x1 = secondary)
3. **720px content width** -- Optimal reading width for long-form content, with full-width toggle
4. **Muted backgrounds for categorization** -- Desaturated tints to group features without visual noise
5. **Icon saturation offset** -- Icons get more saturated values than text in the same hue family
6. **Black/white primary + color as semantic layer** -- Color applied by users, not by the product chrome
7. **Small text toggle** -- Simple density control for power users
8. **Light/dark mode with per-token overrides** -- Every color token has explicit light AND dark values

---

## Code Snippets

### Notion-Style Page Layout
```css
.notion-page {
  max-width: 720px;
  margin: 0 auto;
  padding: 80px 96px 120px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: #373530;
}

.notion-page.full-width {
  max-width: 100%;
}

.notion-page h1 {
  font-size: 40px;
  font-weight: 700;
  line-height: 1.15;
  margin-top: 32px;
  margin-bottom: 4px;
}

.notion-page h2 {
  font-size: 30px;
  font-weight: 600;
  line-height: 1.25;
  margin-top: 28px;
}

.notion-page h3 {
  font-size: 24px;
  font-weight: 600;
  line-height: 1.3;
  margin-top: 24px;
}
```

### Notion Color Tag System
```css
.tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.5;
}

.tag-gray { color: #787774; background: #F1F1EF; }
.tag-brown { color: #976D57; background: #F3EEEE; }
.tag-orange { color: #CC782F; background: #F8ECDF; }
.tag-yellow { color: #C29343; background: #FAF3DD; }
.tag-green { color: #548164; background: #EEF3ED; }
.tag-blue { color: #487CA5; background: #E9F3F7; }
.tag-purple { color: #8A67AB; background: #F6F3F8; }
.tag-pink { color: #B35488; background: #F9F2F5; }
.tag-red { color: #C4554D; background: #FAECEC; }
```

### Notion-Style Callout Block
```css
.callout {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 6px;
  background: #F1F1EF;
  font-size: 16px;
  line-height: 1.6;
}

.callout-icon {
  flex-shrink: 0;
  font-size: 20px;
  line-height: 1.6;
}

.callout-content {
  flex: 1;
  min-width: 0;
}

/* Color variants */
.callout-blue { background: #E9F3F7; }
.callout-yellow { background: #FAF3DD; }
.callout-red { background: #FAECEC; }
.callout-green { background: #EEF3ED; }
```

### Bento Marketing Grid
```css
.marketing-bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  max-width: 1200px;
  margin: 80px auto;
  padding: 0 24px;
}

.bento-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 32px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  transition: box-shadow 200ms ease;
}

.bento-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Tinted feature cards */
.bento-card[data-feature="ai"] { background: #F8ECDF; }
.bento-card[data-feature="docs"] { background: #F6F3F8; }
.bento-card[data-feature="collab"] { background: #EEF3ED; }
.bento-card[data-feature="data"] { background: #E9F3F7; }

.bento-card-hero {
  grid-column: span 2;
  grid-row: span 2;
}

.bento-card-wide {
  grid-column: span 2;
}

@media (max-width: 768px) {
  .marketing-bento { grid-template-columns: repeat(2, 1fr); }
  .bento-card-hero { grid-column: span 2; grid-row: span 1; }
}

@media (max-width: 480px) {
  .marketing-bento { grid-template-columns: 1fr; }
  .bento-card-hero, .bento-card-wide { grid-column: span 1; }
}
```

### Dark Mode Override System
```css
[data-theme="dark"] {
  --page-bg: #191919;
  --text-default: #D4D4D4;
  --icon-default: #D3D3D3;
  
  --gray-text: #9B9B9B;
  --gray-bg: #252525;
  --gray-icon: #7F7F7F;
  
  --blue-text: #447ACB;
  --blue-bg: #1F282D;
  --blue-icon: #2E7CD1;
  
  --green-text: #4F9768;
  --green-bg: #242B26;
  --green-icon: #2D9964;
  
  --orange-text: #CB7B37;
  --orange-bg: #36291F;
  --orange-icon: #D9730D;
  
  --red-text: #BE524B;
  --red-bg: #332523;
  --red-icon: #CD4945;
  
  --purple-text: #865DBB;
  --purple-bg: #2A2430;
  --purple-icon: #8D5BC1;
  
  --pink-text: #BA4A78;
  --pink-bg: #2E2328;
  --pink-icon: #C94079;
  
  --yellow-text: #C19138;
  --yellow-bg: #372E20;
  --yellow-icon: #CA8E1B;
  
  --brown-text: #A27763;
  --brown-bg: #2E2724;
  --brown-icon: #AA755F;
}
```

---

## Anti-Patterns to Avoid

1. **Do NOT add more than 10 semantic colors** -- Notion's constraint is the source of its coherence. Adding an 11th color for "special" use breaks the system. If you need differentiation, use the existing colors with context (labels, positioning).

2. **Do NOT use saturated backgrounds** -- Notion's background values are extremely muted (`#F1F1EF`, `#E9F3F7`). Using fully saturated backgrounds (`#0000FF`) destroys readability and clashes with content. Keep background saturation below 15%.

3. **Do NOT set content width above 720px for reading** -- Research (and Notion's practice) confirms 65-75 characters per line is optimal. Wider content areas increase cognitive load and reduce comprehension.

4. **Do NOT use the same color value for text and icons** -- Notion deliberately separates these. Icons at text color appear dull; text at icon saturation becomes fatiguing. Always create separate tokens.

5. **Do NOT add decorative elements** -- Notion's power comes from absence. No gradients, no illustrations in the chrome, no decorative borders. Every visual element serves a functional purpose.

6. **Do NOT ignore dark mode token mapping** -- Each light-mode color needs a specifically designed dark-mode counterpart. Auto-inverting colors (e.g., inverting `#487CA5` to get a dark mode blue) produces incorrect, untested results.

7. **Do NOT use bento grid without size-based hierarchy** -- Bento layouts without intentional size differentiation (large = important, small = secondary) devolve into random-looking Pinterest boards. Every card size must be a conscious editorial decision.

8. **Do NOT override Notion's font choices with trendy alternatives** -- Inter was selected for extreme readability at all sizes. Replacing it with a display font or a narrower typeface degrades the content-first experience.
