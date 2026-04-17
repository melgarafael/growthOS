---
name: Apple iPhone Product Page
url: https://apple.com/iphone
category: [consumer-electronics, design-tool]
design_style: Cinematic scroll-driven storytelling with massive typography, full-bleed imagery, and black/white contrast
last_analyzed: 2026-04-16
---

## Visual Identity

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Near Black | `#1D1D1F` | Primary text on light backgrounds, dark button fills |
| Athens Gray | `#F5F5F7` | Alternate section backgrounds (informational) |
| Pure White | `#FFFFFF` | Primary light section backgrounds |
| Pure Black | `#000000` | Immersive/hero section backgrounds |
| Apple Blue | `#2997FF` | Links, "Learn more" CTAs (web) |
| Apple Blue (alt) | `#0071E3` | Buttons, primary interactive elements |
| Link Hover | `#0077ED` | Link hover state |
| Medium Gray | `#86868B` | Secondary/supporting text |
| Dark Gray | `#6E6E73` | Tertiary text, captions |

**Key insight:** Apple's web palette is deliberately minimal. The only chromatic colors are blue for links/CTAs and product-specific hero colors (e.g., titanium finishes). The rest is strictly black/white/gray. Product photography provides all the color.

### Typography

**Font Family:** SF Pro Display (20px+) and SF Pro Text (<20px), Apple's proprietary system font.

**Web font stack:**
```css
font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
```

| Element | Size | Weight | Line-Height | Letter-Spacing |
|---------|------|--------|-------------|----------------|
| Hero headline | 56-80px (fluid) | 700 | 1.05 | -0.04em |
| H1 | 48-64px (fluid) | 700 | 1.06 | -0.035em |
| H2 | 40-48px | 600 | 1.07 | -0.03em |
| H3 | 28-32px | 600 | 1.10 | -0.025em |
| H4 | 21-24px | 600 | 1.14 | -0.02em |
| Body | 16-17px | 400 | 24-28px | 0em |
| Caption | 13-14px | 400 | -- | 0.01em |
| Label | 11-12px | 400 | -- | 0.03em |

**Fluid Typography (clamp):**
```css
/* Hero */
font-size: clamp(3.5rem, 2.2857vw + 2.943rem, 5rem);
/* 56px at 390px viewport -> 80px at 1440px viewport */

/* H1 */
font-size: clamp(3rem, 1.5238vw + 2.629rem, 4rem);
/* 48px at 390px viewport -> 64px at 1440px viewport */
```

**Scale Ratios:**
- Mobile: 1.200 (Minor Third)
- Desktop: 1.250 (Major Third)

**Optical Letter-Spacing Rule:** As font size increases, tracking tightens. This compensates for the optical illusion where large letters appear to drift apart. SF Pro Display has tighter default spacing than SF Pro Text. On the web, this is manually replicated via `letter-spacing`.

### Responsive Breakpoints

| Name | Range |
|------|-------|
| Compact | < 390px |
| Small | 390-743px |
| Medium | 744-1023px |
| Large | 1024-1439px |
| XLarge | >= 1440px |

### Layout

| Token | Value |
|-------|-------|
| Max content width | ~980px |
| Hero sections | Full viewport width, centered content |
| Section height | Full viewport height (cinematic) |
| Content strategy | One concept per section, maximum breathing room |

## Key Techniques

### 1. Canvas Image Sequence Scroll Animation (Signature Effect)

Apple's iconic product rotation/reveal effect renders pre-rendered image frames to a `<canvas>` element, driven by scroll position. NOT a video -- individual JPG frames.

**HTML:**
```html
<canvas id="hero-canvas" width="1158" height="770"></canvas>
```

**CSS:**
```css
body {
  background: #000;
  height: 500vh; /* scroll distance controls animation length */
}

canvas {
  position: fixed;
  left: 50%;
  top: 50%;
  max-height: 100vh;
  max-width: 100vw;
  transform: translate(-50%, -50%);
}
```

**JavaScript:**
```javascript
const frameCount = 148;

// Generate image path (Apple's naming convention)
const currentFrame = (index) =>
  `https://www.apple.com/.../anim/sequence/large/${index.toString().padStart(4, '0')}.jpg`;

// Preload all frames
const preloadImages = () => {
  for (let i = 1; i <= frameCount; i++) {
    const img = new Image();
    img.src = currentFrame(i);
  }
};

// Map scroll position to frame index
const html = document.documentElement;
const canvas = document.getElementById('hero-canvas');
const context = canvas.getContext('2d');

window.addEventListener('scroll', () => {
  const scrollTop = html.scrollTop;
  const maxScrollTop = html.scrollHeight - window.innerHeight;
  const scrollFraction = scrollTop / maxScrollTop;
  const frameIndex = Math.min(
    frameCount - 1,
    Math.floor(scrollFraction * frameCount)
  );

  requestAnimationFrame(() => {
    const img = new Image();
    img.src = currentFrame(frameIndex + 1);
    img.onload = () => context.drawImage(img, 0, 0);
  });
});

preloadImages();
```

**Why canvas over video:** Video `<video>` elements cannot reliably seek to exact frames on scroll. Canvas + image sequence provides frame-perfect synchronization with scroll position. `requestAnimationFrame` ensures GPU-accelerated rendering at up to 60fps.

### 2. Sticky Section Scroll Technique

Each product section occupies a tall scroll container with a sticky viewport-filling child:

```css
.product-section {
  height: 300vh; /* 3x viewport = scroll distance */
  position: relative;
}

.product-section__sticky {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
```

Combined with GSAP ScrollTrigger for precise timeline control:

```javascript
gsap.registerPlugin(ScrollTrigger);

gsap.to('.product-image', {
  scale: 1.2,
  opacity: 0,
  scrollTrigger: {
    trigger: '.product-section',
    start: 'top top',
    end: 'bottom top',
    scrub: true,
    pin: true
  }
});
```

### 3. Text Gradient Reveal on Scroll

Feature descriptions that "light up" from gray to white as user scrolls:

```css
.scroll-reveal-text {
  background: linear-gradient(
    to right,
    #F5F5F7 50%,
    #6E6E73 50%
  );
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: background-position 0.8s ease;
}

.scroll-reveal-text.active {
  background-position: -100% 0;
}
```

### 4. Dark/Light Section Alternation

```css
/* Immersive hero (dark) */
.section-immersive {
  background: #000000;
  color: #F5F5F7;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Informational section (light) */
.section-info {
  background: #F5F5F7;
  color: #1D1D1F;
  padding: 120px 0;
}

/* Alternating pattern */
.section-info + .section-immersive,
.section-immersive + .section-info {
  /* No gap between sections -- seamless transition */
}
```

### 5. Hero Typography Scale

```css
.apple-hero-headline {
  font-family: "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
  font-size: clamp(3.5rem, 2.2857vw + 2.943rem, 5rem);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.04em;
  color: #F5F5F7;
  text-align: center;
  -webkit-font-smoothing: antialiased;
}

.apple-hero-subhead {
  font-family: "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
  font-size: clamp(1.25rem, 0.7619vw + 1.064rem, 1.75rem);
  font-weight: 400;
  line-height: 1.25;
  letter-spacing: -0.015em;
  color: #86868B;
  text-align: center;
  margin-top: 8px;
}
```

### 6. Liquid Glass (iOS 26 / 2025+)

Apple's newest design language emphasizes translucency and fluid glass effects:

```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(40px) saturate(180%);
  -webkit-backdrop-filter: blur(40px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
}
```

## What Makes It Work

### Psychological Principles

1. **Cinematic Pacing** -- Each product section occupies a full viewport with generous whitespace. This mimics film composition: one idea per "shot." Users subconsciously process the product as a premium cinematic experience, not a web page.

2. **Scroll as Narrative Control** -- By tying animations to scroll position (not time), Apple gives users the illusion of control over the reveal. This increases engagement and time-on-page. Users slow down at interesting moments.

3. **High Contrast = High Perceived Value** -- The extreme contrast between pure black backgrounds and white text/products creates drama. In luxury retail, high contrast communicates exclusivity. Low-contrast, pastel palettes communicate accessibility/friendliness.

4. **Typography as Hero** -- When the headline IS the visual (80px, 700 weight, tight tracking), no illustration is needed. This communicates confidence: "the words are enough."

5. **Dark Backgrounds for Product Photography** -- Products on black backgrounds appear to float. The absence of context (no desk, no hands, no room) makes the product archetypal rather than situational.

6. **Deliberate Monotone** -- By restricting the palette to black/white/gray + one blue, every product color photograph becomes the visual focal point. The page is a gallery wall; the products are the art.

## Patterns to Extract

### Reusable Pattern 1: Canvas Scroll Animation
- Fixed canvas, tall scrollable container
- Image sequence mapped to scroll fraction
- `requestAnimationFrame` for GPU-accelerated drawing
- Preloaded image set (100-300 frames)

### Reusable Pattern 2: Sticky Cinematic Section
- Container at 200-500vh height
- Sticky child at 100vh with centered content
- GSAP ScrollTrigger for timeline scrubbing
- Content fades/scales/translates within sticky frame

### Reusable Pattern 3: Dark Hero + Light Info Alternation
- Black (#000) sections for immersive product moments
- Light gray (#F5F5F7) sections for features/specs
- Full-bleed, no gaps between sections
- Text color inverts per section

### Reusable Pattern 4: Fluid Headline Scale
- `clamp()` for smooth font-size scaling
- Negative letter-spacing that tightens at larger sizes
- Line-height that decreases at larger sizes
- Mobile-first with Minor Third (1.200), desktop Major Third (1.250)

### Reusable Pattern 5: Product-on-Black Photography
- Pure black background, no gradients
- Product centered with generous margin
- No props, no context, no lifestyle imagery
- Let the product's physical design speak

## Code Snippets

### Apple-Style Hero Section

```html
<section class="hero">
  <div class="hero__content">
    <h1 class="hero__title">iPhone</h1>
    <p class="hero__subtitle">Designed to be loved.</p>
    <div class="hero__cta">
      <a href="#" class="cta-link">Learn more ></a>
      <a href="#" class="cta-link cta-link--buy">Buy ></a>
    </div>
  </div>
</section>
```

```css
.hero {
  background: #000;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 24px;
}

.hero__title {
  font-family: "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
  font-size: clamp(3.5rem, 2.2857vw + 2.943rem, 5rem);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.04em;
  color: #F5F5F7;
  margin: 0;
}

.hero__subtitle {
  font-size: clamp(1.25rem, 0.7619vw + 1.064rem, 1.75rem);
  font-weight: 400;
  line-height: 1.25;
  letter-spacing: -0.015em;
  color: #86868B;
  margin: 6px 0 0;
}

.cta-link {
  color: #2997FF;
  font-size: 21px;
  text-decoration: none;
  display: inline-block;
  margin: 16px 20px 0;
}

.cta-link:hover {
  text-decoration: underline;
}

.cta-link--buy {
  color: #F5F5F7;
  background: #0071E3;
  border-radius: 980px;
  padding: 8px 22px;
}

.cta-link--buy:hover {
  background: #0077ED;
  text-decoration: none;
}
```

### Apple-Style Feature Section (Light)

```css
.feature-section {
  background: #F5F5F7;
  padding: 100px 24px;
  text-align: center;
}

.feature-section__title {
  font-family: "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
  font-size: clamp(2.5rem, 1.5238vw + 2.129rem, 3.5rem);
  font-weight: 700;
  line-height: 1.07;
  letter-spacing: -0.03em;
  color: #1D1D1F;
  max-width: 780px;
  margin: 0 auto 20px;
}

.feature-section__body {
  font-size: 17px;
  font-weight: 400;
  line-height: 1.47;
  color: #6E6E73;
  max-width: 600px;
  margin: 0 auto;
}
```

### Scroll-Driven Frame Animation (Minimal)

```javascript
class AppleScrollSequence {
  constructor({ canvas, frameCount, imagePath }) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.frameCount = frameCount;
    this.imagePath = imagePath;
    this.images = [];
    this.currentFrame = 0;

    this.preload();
    this.bindScroll();
  }

  frameSrc(index) {
    return this.imagePath.replace('{frame}', 
      String(index).padStart(4, '0'));
  }

  preload() {
    for (let i = 0; i < this.frameCount; i++) {
      const img = new Image();
      img.src = this.frameSrc(i);
      this.images.push(img);
    }
    // Draw first frame when loaded
    this.images[0].onload = () => this.draw(0);
  }

  draw(index) {
    const img = this.images[index];
    if (!img.complete) return;
    this.canvas.width = img.naturalWidth;
    this.canvas.height = img.naturalHeight;
    this.ctx.drawImage(img, 0, 0);
    this.currentFrame = index;
  }

  bindScroll() {
    window.addEventListener('scroll', () => {
      const scrollTop = document.documentElement.scrollTop;
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      const fraction = scrollTop / maxScroll;
      const frame = Math.min(
        this.frameCount - 1,
        Math.floor(fraction * this.frameCount)
      );

      if (frame !== this.currentFrame) {
        requestAnimationFrame(() => this.draw(frame));
      }
    });
  }
}

// Usage
new AppleScrollSequence({
  canvas: document.getElementById('hero-canvas'),
  frameCount: 148,
  imagePath: '/frames/hero-{frame}.jpg'
});
```

### CSS View-Timeline (Modern CSS-Only Alternative)

```css
@supports (animation-timeline: scroll()) {
  .scroll-reveal {
    animation: fadeInUp linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(40px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}
```

## Anti-Patterns to Avoid

1. **Do NOT use `<video>` for scroll-synced animations.** Video elements cannot reliably seek to exact frames based on scroll position. They stutter, buffer, and lack frame precision. Use canvas + image sequence or GSAP-driven animations.

2. **Do NOT overload sections with content.** Apple puts ONE concept per viewport. Cramming features, specs, and CTAs into a single screen destroys the cinematic pacing. Each "scene" should have a single focal point.

3. **Do NOT use light gradients on hero sections.** Apple's product pages use flat black or flat white. Gradients on hero backgrounds compete with product photography and reduce perceived premium quality.

4. **Do NOT forget to preload image sequences.** Without preloading, scroll animations stutter as images load on-demand. Apple preloads all 100-300 frames before the animation begins. On slow connections, show a loading state.

5. **Do NOT use SF Pro on the web without Apple's license.** SF Pro is available free for Apple platform development but NOT licensed for web use. Use `system-ui` to inherit the user's system font, or use Inter/DM Sans as alternatives that achieve a similar geometric aesthetic.

6. **Do NOT use `position: fixed` canvas without a scroll container boundary.** The canvas must be constrained within a tall parent div. Without this, the fixed canvas persists across the entire page instead of being scoped to its animation section.

7. **Do NOT skip `letter-spacing` tightening at large sizes.** If you set a headline at 80px and leave letter-spacing at 0, it will look loose and amateurish. Apple tightens to `-0.04em` at hero sizes. This optical correction is not optional for premium typography.

8. **Do NOT animate with `setInterval` or `setTimeout`.** Always use `requestAnimationFrame` for scroll-driven animations. It syncs with the browser's refresh cycle, uses the GPU, and pauses when the tab is hidden.
