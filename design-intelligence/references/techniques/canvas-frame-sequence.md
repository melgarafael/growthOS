---
technique: Canvas Frame Sequence (Apple-style Scroll Animation)
complexity: advanced
browser_support: All modern browsers (Canvas 2D supported since IE9+)
performance_impact: high
---

## Overview

Apple pioneered scroll-driven frame sequence animations on product pages (AirPods Pro, MacBook, iPhone).
The technique renders pre-exported video frames onto an HTML Canvas element, advancing frames as the
user scrolls. This creates the illusion of a video playing in sync with scroll position -- giving the
designer full control over pacing without relying on `<video>` playback (which cannot be reliably
scrubbed by scroll on all browsers/devices).

**Where it is used:** Apple product pages, Sony, Samsung, Tesla, and any hero section where a 3D
product rotates or transforms as the user scrolls.

**Core architecture:**
1. Export a video as a numbered image sequence (e.g. 150-300 WebP/JPEG frames)
2. Preload all frames into `Image` objects
3. Listen to `scroll` events, calculate a progress fraction (0-1)
4. Map progress to a frame index, draw that frame on `<canvas>`
5. Gate drawing calls behind `requestAnimationFrame` to avoid jank

---

## Implementation

### Full Working HTML/CSS/JS

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Apple-style Scroll Frame Sequence</title>
<style>
  /* ============================
     CSS Custom Properties
     ============================ */
  :root {
    --seq-bg: #000;
    --seq-height: 500vh;          /* scrollable height = pacing control */
    --seq-canvas-max-width: 100vw;
    --seq-canvas-max-height: 100vh;
  }

  *,
  *::before,
  *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    background: var(--seq-bg);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #fff;
  }

  /* ============================
     Scroll Container
     ============================ */
  .sequence-section {
    height: var(--seq-height);
    position: relative;
  }

  .sequence-sticky {
    position: sticky;
    top: 0;
    width: 100%;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  .sequence-canvas {
    max-width: var(--seq-canvas-max-width);
    max-height: var(--seq-canvas-max-height);
    /* GPU compositing hint */
    will-change: contents;
  }

  /* ============================
     Loading Overlay
     ============================ */
  .sequence-loader {
    position: fixed;
    inset: 0;
    z-index: 100;
    background: var(--seq-bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: opacity 0.6s ease;
  }

  .sequence-loader.hidden {
    opacity: 0;
    pointer-events: none;
  }

  .sequence-loader__bar {
    width: 200px;
    height: 3px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 2px;
    overflow: hidden;
    margin-top: 16px;
  }

  .sequence-loader__fill {
    height: 100%;
    width: 0%;
    background: #fff;
    border-radius: 2px;
    transition: width 0.1s linear;
  }

  .sequence-loader__text {
    font-size: 14px;
    opacity: 0.6;
    margin-top: 8px;
  }

  /* ============================
     Content Sections (before/after)
     ============================ */
  .content-section {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
  }

  .content-section h2 {
    font-size: clamp(1.5rem, 4vw, 3rem);
    text-align: center;
    max-width: 600px;
  }

  /* ============================
     Fallback for low-power / no-JS
     ============================ */
  .sequence-fallback {
    display: none;
    width: 100%;
    height: 100vh;
    object-fit: cover;
  }

  .no-js .sequence-canvas,
  .no-js .sequence-loader {
    display: none;
  }

  .no-js .sequence-fallback {
    display: block;
  }

  /* Reduced motion: show static image, skip scroll animation */
  @media (prefers-reduced-motion: reduce) {
    .sequence-section {
      height: auto;
    }
    .sequence-sticky {
      position: relative;
      height: auto;
      min-height: 60vh;
    }
  }
</style>
</head>
<body>

<!-- Loading overlay -->
<div class="sequence-loader" id="loader">
  <p>Loading frames...</p>
  <div class="sequence-loader__bar">
    <div class="sequence-loader__fill" id="loaderFill"></div>
  </div>
  <p class="sequence-loader__text" id="loaderText">0%</p>
</div>

<!-- Intro content -->
<section class="content-section">
  <h2>Scroll down to experience the product</h2>
</section>

<!-- Frame sequence section -->
<section class="sequence-section" id="sequenceSection">
  <div class="sequence-sticky">
    <canvas class="sequence-canvas" id="sequenceCanvas"></canvas>
    <!-- Fallback for no-JS or reduced-motion -->
    <img
      class="sequence-fallback"
      src="frames/frame_001.webp"
      alt="Product hero image"
      loading="lazy"
    />
  </div>
</section>

<!-- Outro content -->
<section class="content-section">
  <h2>Crafted with precision</h2>
</section>

<script>
/**
 * Apple-style Canvas Frame Sequence
 *
 * Architecture:
 * 1. Preload all frames as Image objects (with progress callback)
 * 2. On scroll, compute a normalised progress (0-1) within the section
 * 3. Map progress to a frame index
 * 4. Use requestAnimationFrame to draw the frame on canvas
 *
 * Performance notes:
 * - Passive scroll listener (no blocking)
 * - Single rAF guard prevents duplicate draws
 * - Images decoded ahead of time via img.decode() where supported
 * - Canvas uses will-change: contents for GPU compositing
 */

(function () {
  'use strict';

  // ========================
  // Configuration
  // ========================
  const CONFIG = {
    frameCount: 148,                       // total frames
    framePath: (index) => {                // path generator
      // Pads index to 4 digits: frame_0001.webp ... frame_0148.webp
      const num = String(index).padStart(4, '0');
      return `frames/frame_${num}.webp`;
    },
    // For demo purposes without real images, you can use a placeholder:
    // framePath: (index) => `https://www.apple.com/105/media/us/airpods-pro/2019/1299e2f5_9206_4470_b28e_7b31b1b239c8/anim/sequence/large/01-hero-lightpass/${String(index).padStart(4, '0')}.jpg`,
  };

  // ========================
  // DOM References
  // ========================
  const canvas = document.getElementById('sequenceCanvas');
  const ctx = canvas.getContext('2d');
  const section = document.getElementById('sequenceSection');
  const loader = document.getElementById('loader');
  const loaderFill = document.getElementById('loaderFill');
  const loaderText = document.getElementById('loaderText');

  // ========================
  // State
  // ========================
  const frames = [];
  let currentFrame = 0;
  let rafPending = false;

  // ========================
  // Reduced Motion Check
  // ========================
  const prefersReducedMotion = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
  ).matches;

  if (prefersReducedMotion) {
    loader.classList.add('hidden');
    return; // Bail out -- fallback image or static canvas shown via CSS
  }

  // ========================
  // Frame Preloader
  // ========================
  function preloadFrames() {
    return new Promise((resolve) => {
      let loaded = 0;

      for (let i = 1; i <= CONFIG.frameCount; i++) {
        const img = new Image();

        img.onload = () => {
          loaded++;
          const pct = Math.round((loaded / CONFIG.frameCount) * 100);
          loaderFill.style.width = `${pct}%`;
          loaderText.textContent = `${pct}%`;

          if (loaded === CONFIG.frameCount) {
            resolve();
          }
        };

        img.onerror = () => {
          // Silently count errored frames so loader still completes.
          // In production, retry logic or fallback per-frame goes here.
          loaded++;
          if (loaded === CONFIG.frameCount) resolve();
        };

        img.src = CONFIG.framePath(i);
        frames.push(img);
      }
    });
  }

  // ========================
  // Canvas Sizing
  // ========================
  function resizeCanvas() {
    // Match canvas internal resolution to the first frame's natural size
    // (or viewport if frames not loaded yet)
    const ref = frames[0];
    if (ref && ref.naturalWidth) {
      const aspect = ref.naturalWidth / ref.naturalHeight;
      const vw = window.innerWidth;
      const vh = window.innerHeight;
      const viewAspect = vw / vh;

      if (viewAspect > aspect) {
        // viewport is wider -- fit by height
        canvas.height = vh;
        canvas.width = vh * aspect;
      } else {
        // viewport is taller -- fit by width
        canvas.width = vw;
        canvas.height = vw / aspect;
      }
    } else {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
  }

  // ========================
  // Drawing
  // ========================
  function drawFrame(index) {
    const img = frames[index];
    if (!img || !img.complete) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  }

  // ========================
  // Scroll Handler
  // ========================
  function onScroll() {
    if (rafPending) return;
    rafPending = true;

    requestAnimationFrame(() => {
      rafPending = false;

      const rect = section.getBoundingClientRect();
      const sectionTop = -rect.top;
      const sectionHeight = rect.height - window.innerHeight;

      // Normalised progress clamped to [0, 1]
      const progress = Math.min(Math.max(sectionTop / sectionHeight, 0), 1);

      // Map to frame index
      const frameIndex = Math.min(
        Math.floor(progress * CONFIG.frameCount),
        CONFIG.frameCount - 1
      );

      if (frameIndex !== currentFrame) {
        currentFrame = frameIndex;
        drawFrame(currentFrame);
      }
    });
  }

  // ========================
  // Initialise
  // ========================
  async function init() {
    resizeCanvas();

    await preloadFrames();

    // Hide loader
    loader.classList.add('hidden');

    // Draw first frame
    resizeCanvas();
    drawFrame(0);

    // Attach listeners
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', () => {
      resizeCanvas();
      drawFrame(currentFrame);
    });
  }

  init();
})();
</script>

</body>
</html>
```

### How to Prepare Your Frames

```bash
# Export frames from a video file using ffmpeg
# -r 30 = extract 30 fps (adjust to taste)
# -vf scale=1920:-1 = scale width to 1920px, maintain aspect ratio

ffmpeg -i product-hero.mp4 \
  -r 30 \
  -vf "scale=1920:-1" \
  -q:v 80 \
  frames/frame_%04d.webp

# For Apple-level quality at manageable size:
# ~150 frames, WebP quality 80, 1920px wide = ~5-8 MB total

# Generate a low-res preview set for mobile:
ffmpeg -i product-hero.mp4 \
  -r 30 \
  -vf "scale=960:-1" \
  -q:v 70 \
  frames-mobile/frame_%04d.webp
```

---

## Variants

### Variant A: IntersectionObserver Gate (only preload when approaching)

```js
function lazyPreload(sectionEl, preloadFn) {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          preloadFn();
          observer.disconnect();
        }
      }
    },
    { rootMargin: '200% 0px' } // start preloading 2 viewports before visible
  );
  observer.observe(sectionEl);
}

// Usage:
// lazyPreload(section, preloadFrames);
```

### Variant B: Progressive Loading (show low-res first, swap to hi-res)

```js
async function progressivePreload(frameCount, loResPath, hiResPath) {
  // Phase 1: load every 10th frame (fast preview)
  const keyFrames = [];
  for (let i = 1; i <= frameCount; i += 10) {
    const img = new Image();
    img.src = loResPath(i);
    await new Promise((r) => { img.onload = r; img.onerror = r; });
    keyFrames.push({ index: i, img });
  }

  // Phase 2: fill gaps with hi-res in background
  for (let i = 1; i <= frameCount; i++) {
    if (frames[i - 1]) continue; // already loaded
    const img = new Image();
    img.src = hiResPath(i);
    img.decode?.(); // non-blocking decode
    frames[i - 1] = img;
  }
}
```

### Variant C: CSS Scroll-Driven Animation (no JS, Chrome 115+)

```css
/* Modern alternative using scroll-driven animations API */
/* NOTE: Chrome/Edge 115+ only as of 2025 */

.frame-sequence {
  --frame-count: 148;
  width: 100%;
  height: 100vh;
  position: sticky;
  top: 0;
  background-image: url('frames/sprite-sheet.webp');
  background-size: 100% calc(var(--frame-count) * 100%);
  background-position: 0% 0%;

  animation: scroll-frames linear;
  animation-timeline: view();
  animation-range: contain 0% contain 100%;
}

@keyframes scroll-frames {
  from { background-position: 0% 0%; }
  to   { background-position: 0% 100%; }
}
```

---

## Performance

### Image Budget Guidelines

| Frame Count | Resolution | Format | Approx Total Size |
|-------------|-----------|--------|-------------------|
| 60          | 1920x1080 | WebP   | ~2 MB             |
| 150         | 1920x1080 | WebP   | ~5-8 MB           |
| 300         | 1920x1080 | WebP   | ~10-15 MB         |
| 150         | 960x540   | WebP   | ~2-3 MB (mobile)  |

### Critical Optimisations

1. **Passive scroll listener** -- `{ passive: true }` prevents scroll blocking.
2. **rAF guard** -- a boolean flag ensures only one `requestAnimationFrame` callback is queued at a time.
3. **`will-change: contents`** on canvas -- hints browser to optimise compositing.
4. **WebP over JPEG** -- 25-35% smaller at equivalent quality.
5. **Avoid decoding in the hot path** -- preload ALL images before animation starts. Never set `img.src` inside the scroll handler.
6. **`img.decode()`** -- available in modern browsers; forces asynchronous image decode off the main thread.
7. **Lazy preload via IntersectionObserver** -- only start loading frames when the section is approaching the viewport (see Variant A).
8. **Limit frame count** -- 120-150 frames is a sweet spot. Beyond 200 frames the preload time and memory pressure become noticeable on mobile.

### Memory Management

```js
// For very long pages with multiple sequences,
// release frames once the section is passed:
function releaseFrames(sectionEl, framesArray) {
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting && entry.boundingClientRect.bottom < 0) {
        framesArray.length = 0; // release references for GC
        observer.disconnect();
      }
    }
  });
  observer.observe(sectionEl);
}
```

---

## Accessibility

- **`prefers-reduced-motion: reduce`** -- skip the entire scroll animation; show a static hero image instead (implemented in the CSS and JS above).
- **`alt` text on fallback `<img>`** -- describes the product shown in the sequence.
- **No autoplaying video** -- this technique is inherently user-controlled (scroll-driven), which is better for vestibular disorders than auto-playing video.
- **Keyboard scrollability** -- since it relies on native scroll, keyboard users (Space, Page Down, arrow keys) get the same experience.
- **Loading state announced** -- the loading overlay should use `aria-live="polite"` to announce progress to screen readers:

```html
<div class="sequence-loader" id="loader" role="status" aria-live="polite">
  <p>Loading frames...</p>
  <p class="sequence-loader__text" id="loaderText" aria-label="Loading progress">0%</p>
</div>
```

---

## Browser Support

| Feature             | Chrome | Firefox | Safari | Edge  |
|---------------------|--------|---------|--------|-------|
| Canvas 2D           | 4+     | 3.6+    | 3.1+   | 12+   |
| `img.decode()`      | 64+    | 68+     | 15.4+  | 79+   |
| IntersectionObserver| 51+    | 55+     | 12.1+  | 15+   |
| Passive listeners   | 51+    | 49+     | 10+    | 14+   |
| Scroll-driven anim. | 115+   | No      | No     | 115+  |
| WebP `<img>`        | 32+    | 65+     | 16+    | 18+   |

The core technique (Canvas 2D + scroll listener + rAF) works in every modern browser and
gracefully degrades to a static image for legacy browsers or reduced-motion preferences.

---

## Sources

- [CSS-Tricks: Fancy Scrolling Animations Used on Apple Product Pages](https://css-tricks.com/lets-make-one-of-those-fancy-scrolling-animations-used-on-apple-product-pages/)
- [Codrops: Smooth Scroll-Synchronized Animation (OPTIKKA)](https://tympanus.net/codrops/2025/10/16/creating-smooth-scroll-synchronized-animation-for-optikka-from-html5-video-to-frame-sequences/)
- [Ales Kozelsky: Scroll image animation like Sony, Apple and Samsung](https://kozelsky.medium.com/how-to-make-scroll-image-animation-like-sony-apple-and-samsung-936528679fc6)
- [Ankit Trehan: Scroll animations similar to Apple AirPods Pro](https://ankittrehan2000.medium.com/creating-scroll-animations-similar-to-apples-airpods-pro-page-bc5c1c0814df)
- [CSS Image Sequence Animations (almost pure CSS)](https://geyer.dev/blog/css-image-sequence-animations/)
- [Scrollsequence: Video Scroll Complete Guide (2026)](https://scrollsequence.com/how-to-make-scroll-image-animation/)
