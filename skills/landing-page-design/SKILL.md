---
name: landing-page-design
description: Conversion-optimized landing page design — single-file HTML with embedded CSS, no external dependencies. Hero sections, social proof, CTA placement, A/B variants, responsive design, accessibility, and performance (<100KB). Use when generating landing pages or conversion-focused web content.
---

# Landing Page Design Skill

Generate production-ready, conversion-optimized landing pages as **single self-contained HTML files** with embedded CSS and zero external dependencies.

## Output Constraint: Single-File HTML

Every landing page output MUST be:

- **One `.html` file** — no separate CSS, JS, or image files
- **Embedded CSS** via `<style>` tag in `<head>`
- **No external dependencies** — no CDNs, no Google Fonts links, no external scripts
- **System font stack** — `font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif`
- **Inline SVG only** — for icons and simple graphics
- **Max file size: 100KB** — enforced, no exceptions
- **No JavaScript** unless absolutely required for a specific interaction (accordion, form validation)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="[SEO description]">
  <!-- Open Graph -->
  <meta property="og:title" content="[Title]">
  <meta property="og:description" content="[Description]">
  <meta property="og:type" content="website">
  <title>[Page Title]</title>
  <style>
    /* ALL CSS embedded here */
  </style>
</head>
<body>
  <!-- ALL content here -->
</body>
</html>
```

## Page Structure

Every landing page follows this section order:

### 1. Hero Section (Above the Fold)

The most critical section. Must contain:

- **Headline**: Clear value proposition in <10 words
- **Subheadline**: Supporting detail in 1-2 sentences
- **Primary CTA**: Single button, high contrast, action verb
- **Visual element**: Inline SVG illustration or CSS-only graphic
- **Trust signal**: One proof point (users count, rating, badge)

```html
<section class="hero">
  <h1>[Value proposition — benefit, not feature]</h1>
  <p class="subheadline">[How it works in one sentence]</p>
  <a href="#cta" class="btn-primary">[Action Verb] — [Benefit]</a>
  <p class="trust">[Trust signal: "Used by 10,000+ teams" or "★★★★★ 4.9/5"]</p>
</section>
```

**Hero patterns:**

| Pattern | Best For | Structure |
|---------|----------|-----------|
| Centered | SaaS, apps | Headline + CTA centered, illustration below |
| Split | Products with visuals | Text left, visual right (stacks on mobile) |
| Gradient | Bold brands | Full-width gradient bg, white text |
| Minimal | Premium/luxury | Lots of whitespace, single strong headline |

### 2. Social Proof Section

Position immediately after hero to validate the promise.

```html
<section class="social-proof">
  <!-- Option A: Logo bar -->
  <p class="proof-label">Trusted by</p>
  <div class="logo-bar">[Company names or inline SVG logos]</div>

  <!-- Option B: Testimonials -->
  <div class="testimonials">
    <blockquote>
      <p>"[Specific result achieved]"</p>
      <cite>— [Name], [Title] at [Company]</cite>
    </blockquote>
  </div>

  <!-- Option C: Stats -->
  <div class="stats">
    <div class="stat"><strong>[Number]</strong><span>[Label]</span></div>
  </div>
</section>
```

### 3. Features / Benefits Section

3-4 benefits maximum. Lead with outcomes, not features.

```html
<section class="features">
  <h2>[Section headline — outcome-focused]</h2>
  <div class="feature-grid">
    <div class="feature">
      <div class="feature-icon">[Inline SVG or CSS icon]</div>
      <h3>[Benefit headline]</h3>
      <p>[1-2 sentences explaining the benefit]</p>
    </div>
    <!-- 2-3 more features -->
  </div>
</section>
```

### 4. How It Works (Optional)

3-step process. Reduces cognitive load.

```html
<section class="how-it-works">
  <h2>How it works</h2>
  <ol class="steps">
    <li><strong>[Step 1]</strong><p>[Brief explanation]</p></li>
    <li><strong>[Step 2]</strong><p>[Brief explanation]</p></li>
    <li><strong>[Step 3]</strong><p>[Brief explanation]</p></li>
  </ol>
</section>
```

### 5. CTA Section (Repeat)

Repeat the primary CTA with urgency or additional proof.

```html
<section class="cta-section">
  <h2>[Restate value proposition differently]</h2>
  <p>[Urgency or additional benefit]</p>
  <a href="#" class="btn-primary">[Same CTA text as hero]</a>
  <p class="reassurance">[Risk reversal: "No credit card required" / "Cancel anytime"]</p>
</section>
```

### 6. Footer

Minimal. Don't distract from conversion.

```html
<footer>
  <p>&copy; [Year] [Brand]. [Optional: Privacy | Terms]</p>
</footer>
```

## Conversion Optimization (CRO) Principles

### CTA Rules

- **One primary CTA** per page — never compete with yourself
- **Above the fold** — first CTA visible without scrolling
- **Repeated** — CTA appears 2-3 times (hero, mid-page, bottom)
- **Action verb + benefit**: "Start Free Trial" not "Submit"
- **High contrast**: CTA button must have ≥4.5:1 contrast ratio
- **Size**: Minimum 44x44px touch target (mobile accessibility)

### Copy Hierarchy

1. **Headline**: Benefit-first, <10 words
2. **Subheadline**: Supporting detail, 1-2 sentences
3. **Body**: Scannable, bullet points preferred
4. **CTA**: Action verb, 2-5 words

### Psychological Triggers

| Trigger | Implementation |
|---------|---------------|
| Social proof | Numbers, testimonials, logos |
| Scarcity | "Limited spots" (only if true) |
| Authority | Certifications, press mentions |
| Risk reversal | "Money-back guarantee", "No CC required" |
| Reciprocity | Free resource, calculator, tool |

## Responsive Design

All pages must work across breakpoints:

```css
/* Mobile-first approach */
/* Base: mobile (320px+) */
.feature-grid { display: grid; grid-template-columns: 1fr; gap: 2rem; }

/* Tablet (768px+) */
@media (min-width: 768px) {
  .feature-grid { grid-template-columns: repeat(2, 1fr); }
  .hero { padding: 4rem 2rem; }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .feature-grid { grid-template-columns: repeat(3, 1fr); }
  .hero { padding: 6rem 4rem; }
  body { max-width: 1200px; margin: 0 auto; }
}
```

### Mobile Priorities

- CTA button full-width on mobile
- Font size minimum 16px (prevents iOS zoom)
- Touch targets minimum 44x44px
- Stack columns vertically
- Reduce padding, keep content density

## Accessibility Requirements

- Semantic HTML: `<header>`, `<main>`, `<section>`, `<footer>`
- All images/SVGs: `alt` text or `aria-label`
- Color contrast: ≥4.5:1 for text, ≥3:1 for large text
- Focus states: Visible outline on all interactive elements
- Skip link: Hidden "Skip to content" link
- Form labels: Every input has associated `<label>`
- `lang` attribute on `<html>` tag

```html
<html lang="en">
<body>
  <a href="#main" class="skip-link">Skip to content</a>
  <header role="banner">...</header>
  <main id="main" role="main">...</main>
  <footer role="contentinfo">...</footer>
</body>
```

## Performance Budget

| Metric | Target |
|--------|--------|
| Total file size | <100KB |
| First Contentful Paint | <1.0s |
| CSS size | <15KB |
| No external requests | 0 |
| Inline SVG total | <20KB |

### Performance Techniques

- CSS custom properties for theming (reduces duplication)
- `prefers-reduced-motion` media query for animations
- `prefers-color-scheme` for dark mode variant (optional)
- Minimal CSS — no unused selectors
- System font stack — zero font loading time

## A/B Testing Variants

When generating a landing page, always produce a primary version and specify testable variants:

```yaml
ab_variants:
  - element: headline
    control: "[Original headline]"
    variant: "[Alternative headline]"
    hypothesis: "[Why this might convert better]"
  - element: cta_text
    control: "[Original CTA]"
    variant: "[Alternative CTA]"
    hypothesis: "[Why this might convert better]"
  - element: hero_layout
    control: "[centered | split]"
    variant: "[opposite layout]"
    hypothesis: "[Layout impact on conversion]"
```

## CSS Design System (Embedded)

```css
:root {
  /* Typography */
  --font-stack: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --font-mono: ui-monospace, 'Cascadia Code', 'Fira Code', monospace;
  --text-base: 1rem;
  --text-lg: 1.25rem;
  --text-xl: 1.5rem;
  --text-2xl: 2rem;
  --text-3xl: 2.5rem;
  --text-4xl: 3.5rem;

  /* Spacing (8px grid) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 1rem;
  --space-4: 1.5rem;
  --space-5: 2rem;
  --space-6: 3rem;
  --space-7: 4rem;
  --space-8: 6rem;

  /* Colors — override per brand */
  --color-primary: #2563eb;
  --color-primary-dark: #1d4ed8;
  --color-text: #1a1a2e;
  --color-text-muted: #64748b;
  --color-bg: #ffffff;
  --color-bg-alt: #f8fafc;
  --color-border: #e2e8f0;
  --color-success: #059669;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;
}

/* Button base */
.btn-primary {
  display: inline-block;
  padding: var(--space-3) var(--space-5);
  background: var(--color-primary);
  color: #fff;
  font-size: var(--text-lg);
  font-weight: 600;
  text-decoration: none;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-primary:hover { background: var(--color-primary-dark); }
.btn-primary:focus { outline: 3px solid var(--color-primary); outline-offset: 2px; }
```

## Anti-Patterns

- External font loading (Google Fonts CDN)
- JavaScript frameworks for static content
- Multiple competing CTAs
- Feature lists without benefit framing
- Stock photo placeholders (use SVG or CSS)
- Hamburger menus on landing pages (no nav needed)
- Footer with 20+ links (landing page ≠ website)
- Auto-playing video/audio
- Pop-ups or modals on load
