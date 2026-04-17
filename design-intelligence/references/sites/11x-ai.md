---
name: 11x.ai
url: https://11x.ai
category: [ai-native, saas]
design_style: Ultra-minimal light-mode with restrained black-and-white palette, system-native typography, and cinematic astronaut imagery conveying AI frontier exploration
last_analyzed: 2026-04-17
---

## Visual Identity

### Brand Colors

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Black (Primary) | `#000000` | 0, 0, 0 | Logo, headings, primary text |
| White (Background) | `#FFFFFF` | 255, 255, 255 | Page background, reverse text |
| Focus Blue | `#4D65FF` | 77, 101, 255 | Keyboard focus outlines, accessibility states |
| Near-Black | `#1A1A1A` | 26, 26, 26 | Body text, secondary headings |
| Light Gray | `#F5F5F5` | 245, 245, 245 | Section backgrounds, subtle dividers |
| Medium Gray | `#6B7280` | 107, 114, 128 | Secondary text, captions |
| Warm Beige | `#F3EDE4` | 243, 237, 228 | Hero background accents, warmth layer |

### Gradients

Minimal explicit gradients. The site relies on photography and whitespace rather than CSS gradients for visual interest. Any subtle depth comes from opacity layering on hero imagery.

### Typography

**Font Strategy: System-Native + Antialiased**

11x.ai uses the operating system's native font stack with aggressive antialiasing, creating a "native app" feel in the browser.

| Property | Value |
|----------|-------|
| Font Stack | System default (no custom web fonts loaded) |
| Smoothing | `-webkit-font-smoothing: antialiased` |
| Smoothing (Firefox) | `-moz-osx-font-smoothing: grayscale` |
| Smoothing (Opera) | `-o-font-smoothing: antialiased` |

**Effective Font Resolution by OS:**

| OS | Resolved Font |
|----|---------------|
| macOS/iOS | SF Pro Display / SF Pro Text |
| Windows | Segoe UI |
| Android | Roboto |
| Linux | system-ui |

**Fluid Typography (viewport-responsive):**

| Breakpoint | Calculation |
|-----------|-------------|
| Base (>1440px) | `1rem` (16px) |
| Desktop (<=1440px) | `calc(0.8127rem + 0.2081vw)` |
| Mobile (<=479px) | `calc(0.7497rem + 0.4184vw)` |

This fluid approach means text scales continuously between breakpoints rather than jumping at fixed sizes.

**Heading Hierarchy:**

The site uses a restrained hierarchy. Headlines are large but not enormous, typically 32-48px range, with generous letter-spacing for the tagline "Digital workers, Human results."

### Spacing

| Utility | Value |
|---------|-------|
| Margin/Padding Reset | `0rem` (utility classes) |
| Container Centered | `margin-left: auto; margin-right: auto` |
| Section Padding | Generous vertical whitespace (80-120px typical) |

**Responsive Breakpoints:**

| Name | Width |
|------|-------|
| Mobile | <= 479px |
| Mobile Landscape | 480px - 767px |
| Tablet | 768px - 991px |
| Desktop | 992px - 1439px |
| Large Desktop | >= 1440px |
| Ultra-wide | >= 1920px |

### Border Radius

| Context | Value |
|---------|-------|
| Focus Outline | `0.125rem` (2px) |
| Focus Offset | `0.125rem` (2px) |
| Buttons | Minimal, consistent with system defaults |

### Shadows

The site uses virtually no box-shadows. The flat aesthetic relies on whitespace and contrast for hierarchy rather than elevation.

## Key Techniques

### Ultra-Light Visual Weight

```css
/* 11x achieves weightlessness through absence */
body {
  margin: 0;
  min-height: 100%;
  background-color: #FFFFFF;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* No custom fonts = faster load, native feel */
/* No shadows = flat, modern, confident */
/* No gradients = content-first hierarchy */
```

### Fluid Typography System

```css
/* Desktop fluid scaling */
@media screen and (max-width: 1440px) {
  html {
    font-size: calc(0.8126951092611863rem + 0.20811654526534862vw);
  }
}

/* Mobile fluid scaling */
@media screen and (max-width: 479px) {
  html {
    font-size: calc(0.7497384937238494rem + 0.41841004184100417vw);
  }
}
```

### Pulse Animation (AI Activity Indicator)

```css
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: scale(5);
    opacity: 0;
  }
}

.pulse-ring {
  animation: pulse 3s infinite;
}

.pulse-ring:nth-child(2) {
  animation-delay: 1000ms;
}

.pulse-ring:nth-child(3) {
  animation-delay: 2000ms;
}
```

### Audio Wire Animation (Voice AI Indicator)

```css
@keyframes animateUpDown {
  0% { height: 30%; }
  100% { height: 90%; }
}

.audio-wire {
  animation: animateUpDown 0.4s infinite alternate;
}

/* Toggle play state for interactive control */
.audio-wire.paused {
  animation-play-state: paused;
}

.audio-wire.playing {
  animation-play-state: running;
}
```

### Text Truncation (Content Cards)

```css
.text-clamp-2 {
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.text-clamp-3 {
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
```

### Accessible Focus States

```css
*:focus-visible {
  outline: 0.125rem solid #4D65FF;
  outline-offset: 0.125rem;
}
```

### 3D Card Flip Effect

```css
.card-3d {
  transform: rotateY(-180deg);
  transform-style: preserve-3d;
  transition: transform 0.6s ease;
}

.card-3d:hover {
  transform: rotateY(0deg);
}
```

## What Makes It Work

### Psychological Principles

1. **Confident minimalism signals premium.** By stripping away decoration, 11x.ai communicates that the product is sophisticated enough to sell itself. This mirrors luxury brand strategy -- the less you decorate, the more confidence you project.

2. **Black-and-white creates authority.** The near-monochrome palette triggers associations with newspapers, legal documents, and executive communications. For an enterprise AI product, this builds trust with B2B buyers who associate color with "consumer" and simplicity with "serious."

3. **System fonts = native trust.** Using the OS font stack means the text "feels like" a system application, not a marketing site. This subtly signals reliability and deep integration -- the product feels like it belongs on your machine.

4. **Astronaut imagery as frontier metaphor.** The photorealistic astronaut-on-barren-landscape visuals position AI digital workers as pioneers. The vast, empty landscapes suggest unexplored potential while the spacesuit-clad figures humanize the technology.

5. **Whitespace as a luxury signal.** Excessive padding between sections communicates that the company does not need to cram information to convince you. It mirrors the "we have nothing to prove" confidence of Stripe, Linear, and Apple.

6. **Pulsing rings = alive, working.** The 3-second pulse animation on key elements suggests continuous background activity -- the AI is always working. The staggered delays create an organic, breathing rhythm rather than mechanical repetition.

7. **"Digital workers, Human results" resolves cognitive dissonance.** The tagline directly addresses the fear that AI = inhuman. By pairing "digital" with "human results," it frames the product as augmentation, not replacement.

## Patterns to Extract

### 1. Zero-Decoration Hero

Clean headline + subtext + single CTA on white background. No gradients, no illustrations, no background patterns. The text IS the design. Works for any product confident enough to lead with its value proposition.

### 2. Fluid Typography Without Custom Fonts

System font stack with calc()-based scaling creates a lightweight, native-feeling experience. No FOUT (Flash of Unstyled Text), no font loading delay. Ideal for performance-first sites.

### 3. Staggered Pulse Animation

Three concentric rings pulsing at 1-second offsets. Creates "breathing" AI activity indicator. Reusable for any "something is happening" state.

### 4. Audio Wire Equalizer

Simple height-oscillating bars that indicate active voice/audio processing. Toggle between paused/playing states for interactive feedback.

### 5. Photorealistic Concept Imagery

Full-bleed photographic imagery (astronauts, landscapes) used as metaphorical storytelling rather than product screenshots. Creates emotional resonance where product UIs create rational evaluation.

### 6. Enterprise Logo Carousel (Swiper)

Horizontal auto-scrolling logo strip using Swiper.js. Establishes credibility without dedicating vertical space. Standard pattern but 11x executes with generous spacing between logos.

### 7. Accessible Focus Ring Pattern

2px solid blue outline with 2px offset -- visible, clear, and non-intrusive. The `#4D65FF` blue is distinct enough to be noticed but not garish.

## Code Snippets

### Complete Minimal Hero Section

```css
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 120px 24px 80px;
  background: #FFFFFF;
}

.hero-headline {
  font-size: clamp(32px, 5vw, 56px);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: #000000;
  margin-bottom: 16px;
  max-width: 800px;
}

.hero-subtext {
  font-size: clamp(16px, 2vw, 20px);
  font-weight: 400;
  line-height: 1.5;
  color: #6B7280;
  margin-bottom: 32px;
  max-width: 560px;
}

.hero-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #000000;
  color: #FFFFFF;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.hero-cta:hover {
  opacity: 0.85;
}

.hero-cta svg {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}

.hero-cta:hover svg {
  transform: translateX(4px);
}
```

### Responsive Container System

```css
.container-large {
  max-width: 1280px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 24px;
  padding-right: 24px;
}

.container-medium {
  max-width: 960px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 24px;
  padding-right: 24px;
}

.container-small {
  max-width: 640px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 24px;
  padding-right: 24px;
}
```

### AI Activity Pulse Ring

```html
<div class="pulse-container" style="position: relative; width: 80px; height: 80px;">
  <div class="pulse-ring" style="
    position: absolute; inset: 0;
    border: 2px solid #000000;
    border-radius: 50%;
    animation: pulse 3s infinite;
  "></div>
  <div class="pulse-ring" style="
    position: absolute; inset: 0;
    border: 2px solid #000000;
    border-radius: 50%;
    animation: pulse 3s infinite;
    animation-delay: 1000ms;
  "></div>
  <div class="pulse-ring" style="
    position: absolute; inset: 0;
    border: 2px solid #000000;
    border-radius: 50%;
    animation: pulse 3s infinite;
    animation-delay: 2000ms;
  "></div>
  <div style="
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 12px; height: 12px;
    background: #000000;
    border-radius: 50%;
  "></div>
</div>
```

## Anti-Patterns to Avoid

1. **Do not mistake minimalism for emptiness.** 11x.ai's restraint works because every element serves a clear purpose. Copying the whitespace without the information density creates a site that feels incomplete, not confident.

2. **Avoid system fonts without antialiasing.** The native font stack only looks premium with `-webkit-font-smoothing: antialiased`. Without it, system fonts render with heavier strokes that look dated, especially on Windows.

3. **Do not use black-and-white for products that need emotional warmth.** This palette works for enterprise B2B sales tools. For consumer products, wellness apps, or creative tools, it reads as cold and unapproachable.

4. **Avoid the astronaut imagery metaphor for non-frontier products.** The "exploring new territory" visual language works for AI/tech pioneers. Using it for a CRM or accounting tool creates a tonal disconnect.

5. **Do not scale the pulse animation to more than 3 rings.** The staggered timing creates a natural breathing effect at 3 layers. More than 3 becomes distracting and reads as a loading spinner rather than an activity indicator.

6. **Avoid zero-font-loading strategy on text-heavy pages.** System fonts are ideal for marketing sites with sparse copy. For documentation, blogs, or data-dense UIs, a custom font (Inter, etc.) provides better readability at small sizes.

7. **Do not combine this minimal aesthetic with complex navigation.** 11x.ai's simple nav (5-6 items) matches the minimal visual language. A mega-menu or multi-level dropdown would create a jarring contrast.
