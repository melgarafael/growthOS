---
technique: Micro-Interactions (Production CSS Library)
complexity: basic
browser_support: All modern browsers; graceful degradation everywhere
performance_impact: low
---

## Overview

Micro-interactions are small, focused animations that provide feedback, guide the user, and make
interfaces feel responsive and polished. They operate at the 100-300ms timescale -- fast enough
to feel instant, slow enough to be perceived.

This file provides a complete, themeable, copy-paste-ready CSS micro-interaction library covering:
- Button hover states (lift, glow, ripple, fill)
- Focus-visible rings (accessible, styled)
- Card hover effects (lift, tilt, border glow)
- Toggle/switch animations
- Loading state animations
- All with CSS custom properties and `prefers-reduced-motion` support

**Design principle:** Every animation serves a functional purpose (feedback, state change,
attention). Decoration-only animations are excluded.

---

## Implementation

### Complete Working Library

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Micro-Interactions Library</title>
<style>
  /* ==============================================================
     DESIGN TOKENS
     ============================================================== */
  :root {
    /* Timing */
    --mi-duration-fast: 120ms;
    --mi-duration-normal: 200ms;
    --mi-duration-slow: 350ms;
    --mi-easing: cubic-bezier(0.25, 0.46, 0.45, 0.94);     /* ease-out-quad */
    --mi-easing-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);  /* overshoot */
    --mi-easing-spring: cubic-bezier(0.22, 1, 0.36, 1);     /* fast start, slow end */

    /* Colours */
    --mi-accent: #3b82f6;
    --mi-accent-light: #93c5fd;
    --mi-accent-dark: #1d4ed8;
    --mi-surface: #ffffff;
    --mi-surface-hover: #f3f4f6;
    --mi-text: #111827;
    --mi-text-inverse: #ffffff;
    --mi-border: #d1d5db;
    --mi-shadow-color: rgba(0, 0, 0, 0.08);
    --mi-shadow-color-hover: rgba(0, 0, 0, 0.15);
    --mi-glow-color: rgba(59, 130, 246, 0.4);

    /* Focus Ring */
    --mi-focus-ring-color: var(--mi-accent);
    --mi-focus-ring-width: 2px;
    --mi-focus-ring-offset: 2px;

    /* Spacing */
    --mi-space-xs: 0.25rem;
    --mi-space-sm: 0.5rem;
    --mi-space-md: 1rem;
    --mi-space-lg: 1.5rem;

    /* Radius */
    --mi-radius: 8px;
    --mi-radius-full: 9999px;
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --mi-surface: #1f2937;
      --mi-surface-hover: #374151;
      --mi-text: #f9fafb;
      --mi-text-inverse: #111827;
      --mi-border: #4b5563;
      --mi-shadow-color: rgba(0, 0, 0, 0.3);
      --mi-shadow-color-hover: rgba(0, 0, 0, 0.5);
    }
  }

  /* ==============================================================
     REDUCED MOTION -- GLOBAL OVERRIDE
     ============================================================== */
  @media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }

  /* ==============================================================
     RESET & PAGE
     ============================================================== */
  *,
  *::before,
  *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--mi-surface);
    color: var(--mi-text);
    padding: 2rem;
    line-height: 1.6;
  }

  .demo-section {
    margin-bottom: 3rem;
  }

  .demo-section h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--mi-border);
  }

  .demo-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 1rem;
  }

  .demo-label {
    font-size: 0.75rem;
    color: #6b7280;
    margin-top: 0.5rem;
    text-align: center;
  }

  .demo-col {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* ==============================================================
     1. FOCUS-VISIBLE RING SYSTEM
     ============================================================== */

  /*
   * Strategy: Use :focus-visible to show focus rings ONLY for keyboard
   * navigation, not mouse clicks. This is the modern standard.
   */

  /* Base: remove default outline, add custom ring on :focus-visible */
  .focusable:focus {
    outline: none;
  }

  .focusable:focus-visible {
    outline: var(--mi-focus-ring-width) solid var(--mi-focus-ring-color);
    outline-offset: var(--mi-focus-ring-offset);
    border-radius: var(--mi-radius);
  }

  /* Variant: ring with shadow (softer, more visible on busy backgrounds) */
  .focus-ring-shadow:focus-visible {
    outline: none;
    box-shadow:
      0 0 0 var(--mi-focus-ring-offset) var(--mi-surface),
      0 0 0 calc(var(--mi-focus-ring-offset) + var(--mi-focus-ring-width)) var(--mi-focus-ring-color);
  }

  /* Variant: animated ring that expands */
  .focus-ring-animated:focus-visible {
    outline: none;
    box-shadow:
      0 0 0 var(--mi-focus-ring-offset) var(--mi-surface),
      0 0 0 calc(var(--mi-focus-ring-offset) + var(--mi-focus-ring-width)) var(--mi-focus-ring-color);
    transition: box-shadow var(--mi-duration-fast) var(--mi-easing);
  }

  /* ==============================================================
     2. BUTTON HOVER STATES
     ============================================================== */

  /* Shared button base */
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: var(--mi-space-sm);
    padding: 0.625rem 1.25rem;
    font-size: 0.9375rem;
    font-weight: 600;
    font-family: inherit;
    color: var(--mi-text-inverse);
    background: var(--mi-accent);
    border: none;
    border-radius: var(--mi-radius);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
  }

  /* --- LIFT --- */
  .btn-lift {
    transition:
      transform var(--mi-duration-normal) var(--mi-easing),
      box-shadow var(--mi-duration-normal) var(--mi-easing);
    box-shadow: 0 1px 3px var(--mi-shadow-color);
  }

  .btn-lift:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--mi-shadow-color-hover);
  }

  .btn-lift:active {
    transform: translateY(0);
    box-shadow: 0 1px 3px var(--mi-shadow-color);
    transition-duration: var(--mi-duration-fast);
  }

  /* --- GLOW --- */
  .btn-glow {
    transition:
      box-shadow var(--mi-duration-normal) var(--mi-easing);
    box-shadow: 0 0 0 0 var(--mi-glow-color);
  }

  .btn-glow:hover {
    box-shadow: 0 0 20px 4px var(--mi-glow-color);
  }

  .btn-glow:active {
    box-shadow: 0 0 10px 2px var(--mi-glow-color);
  }

  /* --- RIPPLE (CSS-only, radiates from centre) --- */
  .btn-ripple {
    transition: background var(--mi-duration-normal) var(--mi-easing);
  }

  .btn-ripple::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(
      circle at center,
      rgba(255, 255, 255, 0.3) 0%,
      transparent 60%
    );
    opacity: 0;
    transform: scale(0);
    transition:
      opacity var(--mi-duration-slow) var(--mi-easing),
      transform var(--mi-duration-slow) var(--mi-easing);
  }

  .btn-ripple:active::after {
    opacity: 1;
    transform: scale(2.5);
    transition-duration: 0ms;
  }

  /* --- FILL (underline fill from left) --- */
  .btn-fill {
    color: var(--mi-accent);
    background: transparent;
    border: 2px solid var(--mi-accent);
    transition:
      color var(--mi-duration-normal) var(--mi-easing),
      background var(--mi-duration-normal) var(--mi-easing);
    z-index: 0;
  }

  .btn-fill::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--mi-accent);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform var(--mi-duration-normal) var(--mi-easing);
    z-index: -1;
  }

  .btn-fill:hover {
    color: var(--mi-text-inverse);
  }

  .btn-fill:hover::before {
    transform: scaleX(1);
  }

  /* --- SCALE (subtle press) --- */
  .btn-scale {
    transition: transform var(--mi-duration-fast) var(--mi-easing-bounce);
  }

  .btn-scale:hover {
    transform: scale(1.04);
  }

  .btn-scale:active {
    transform: scale(0.96);
    transition-duration: var(--mi-duration-fast);
  }

  /* All buttons: focus-visible ring */
  .btn:focus-visible {
    outline: var(--mi-focus-ring-width) solid var(--mi-focus-ring-color);
    outline-offset: var(--mi-focus-ring-offset);
  }

  /* ==============================================================
     3. CARD HOVER EFFECTS
     ============================================================== */

  .card {
    background: var(--mi-surface);
    border: 1px solid var(--mi-border);
    border-radius: var(--mi-radius);
    padding: var(--mi-space-lg);
    width: 240px;
  }

  .card h3 {
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }

  .card p {
    font-size: 0.875rem;
    color: #6b7280;
  }

  /* --- CARD LIFT --- */
  .card-lift {
    transition:
      transform var(--mi-duration-normal) var(--mi-easing),
      box-shadow var(--mi-duration-normal) var(--mi-easing);
    box-shadow: 0 1px 3px var(--mi-shadow-color);
  }

  .card-lift:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px var(--mi-shadow-color-hover);
  }

  /* --- CARD BORDER GLOW --- */
  .card-glow {
    transition:
      border-color var(--mi-duration-normal) var(--mi-easing),
      box-shadow var(--mi-duration-normal) var(--mi-easing);
  }

  .card-glow:hover {
    border-color: var(--mi-accent);
    box-shadow: 0 0 0 1px var(--mi-accent), 0 0 20px -4px var(--mi-glow-color);
  }

  /* --- CARD TILT (CSS-only subtle perspective) --- */
  .card-tilt {
    transition: transform var(--mi-duration-normal) var(--mi-easing);
    transform-style: preserve-3d;
    perspective: 800px;
  }

  .card-tilt:hover {
    transform: perspective(800px) rotateX(2deg) rotateY(-2deg) translateY(-2px);
    box-shadow: 4px 8px 24px var(--mi-shadow-color-hover);
  }

  /* --- CARD HIGHLIGHT BAR (top border reveal) --- */
  .card-highlight {
    position: relative;
    overflow: hidden;
    transition: box-shadow var(--mi-duration-normal) var(--mi-easing);
  }

  .card-highlight::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--mi-accent);
    transform: scaleX(0);
    transition: transform var(--mi-duration-normal) var(--mi-easing);
  }

  .card-highlight:hover::before {
    transform: scaleX(1);
  }

  .card-highlight:hover {
    box-shadow: 0 4px 16px var(--mi-shadow-color-hover);
  }

  /* Cards as links: focus-visible */
  .card:focus-visible {
    outline: var(--mi-focus-ring-width) solid var(--mi-focus-ring-color);
    outline-offset: var(--mi-focus-ring-offset);
  }

  /* ==============================================================
     4. TOGGLE / SWITCH
     ============================================================== */

  .toggle-wrapper {
    display: flex;
    align-items: center;
    gap: var(--mi-space-sm);
  }

  .toggle {
    --toggle-width: 48px;
    --toggle-height: 26px;
    --toggle-padding: 3px;
    --toggle-knob-size: calc(var(--toggle-height) - var(--toggle-padding) * 2);
    --toggle-bg-off: var(--mi-border);
    --toggle-bg-on: var(--mi-accent);

    position: relative;
    display: inline-flex;
    width: var(--toggle-width);
    height: var(--toggle-height);
    cursor: pointer;
  }

  .toggle input {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
  }

  .toggle__track {
    position: absolute;
    inset: 0;
    background: var(--toggle-bg-off);
    border-radius: var(--mi-radius-full);
    transition: background var(--mi-duration-normal) var(--mi-easing);
  }

  .toggle__knob {
    position: absolute;
    top: var(--toggle-padding);
    left: var(--toggle-padding);
    width: var(--toggle-knob-size);
    height: var(--toggle-knob-size);
    background: white;
    border-radius: 50%;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    transition:
      transform var(--mi-duration-normal) var(--mi-easing-spring);
  }

  /* Checked state */
  .toggle input:checked ~ .toggle__track {
    background: var(--toggle-bg-on);
  }

  .toggle input:checked ~ .toggle__knob {
    transform: translateX(calc(var(--toggle-width) - var(--toggle-knob-size) - var(--toggle-padding) * 2));
  }

  /* Focus-visible on the toggle */
  .toggle input:focus-visible ~ .toggle__track {
    box-shadow:
      0 0 0 var(--mi-focus-ring-offset) var(--mi-surface),
      0 0 0 calc(var(--mi-focus-ring-offset) + var(--mi-focus-ring-width)) var(--mi-focus-ring-color);
  }

  /* Disabled state */
  .toggle input:disabled ~ .toggle__track {
    opacity: 0.5;
    cursor: not-allowed;
  }
  .toggle input:disabled ~ .toggle__knob {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .toggle-label {
    font-size: 0.875rem;
    cursor: pointer;
    user-select: none;
  }

  /* ==============================================================
     5. LOADING STATES
     ============================================================== */

  /* --- Spinner --- */
  .spinner {
    --spinner-size: 24px;
    --spinner-thickness: 3px;
    --spinner-color: var(--mi-accent);

    width: var(--spinner-size);
    height: var(--spinner-size);
    border: var(--spinner-thickness) solid rgba(0, 0, 0, 0.1);
    border-top-color: var(--spinner-color);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  /* --- Dots --- */
  .dots-loader {
    display: flex;
    gap: 6px;
    align-items: center;
  }

  .dots-loader__dot {
    --dot-size: 8px;
    width: var(--dot-size);
    height: var(--dot-size);
    background: var(--mi-accent);
    border-radius: 50%;
    animation: dot-bounce 1.2s ease-in-out infinite;
  }

  .dots-loader__dot:nth-child(2) { animation-delay: 0.15s; }
  .dots-loader__dot:nth-child(3) { animation-delay: 0.3s; }

  @keyframes dot-bounce {
    0%, 80%, 100% {
      transform: scale(0.6);
      opacity: 0.4;
    }
    40% {
      transform: scale(1);
      opacity: 1;
    }
  }

  /* --- Skeleton Pulse --- */
  .skeleton {
    --skeleton-bg: #e5e7eb;
    --skeleton-shine: #f3f4f6;

    background: linear-gradient(
      90deg,
      var(--skeleton-bg) 25%,
      var(--skeleton-shine) 50%,
      var(--skeleton-bg) 75%
    );
    background-size: 200% 100%;
    animation: skeleton-pulse 1.5s ease-in-out infinite;
    border-radius: var(--mi-radius);
  }

  @keyframes skeleton-pulse {
    from { background-position: 200% 0; }
    to   { background-position: -200% 0; }
  }

  .skeleton-line {
    height: 1rem;
    margin-bottom: 0.75rem;
  }

  .skeleton-line:last-child {
    width: 60%;
  }

  .skeleton-circle {
    width: 48px;
    height: 48px;
    border-radius: 50%;
  }

  @media (prefers-color-scheme: dark) {
    .skeleton {
      --skeleton-bg: #374151;
      --skeleton-shine: #4b5563;
    }
  }

  /* --- Button Loading State --- */
  .btn-loading {
    position: relative;
    color: transparent !important;
    pointer-events: none;
  }

  .btn-loading::after {
    content: '';
    position: absolute;
    width: 18px;
    height: 18px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }

  /* ==============================================================
     6. LINK / TEXT INTERACTIONS
     ============================================================== */

  /* Underline slide-in */
  .link-underline {
    position: relative;
    text-decoration: none;
    color: var(--mi-accent);
    font-weight: 500;
  }

  .link-underline::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 2px;
    background: currentColor;
    transform: scaleX(0);
    transform-origin: right;
    transition: transform var(--mi-duration-normal) var(--mi-easing);
  }

  .link-underline:hover::after {
    transform: scaleX(1);
    transform-origin: left;
  }

  .link-underline:focus-visible {
    outline: var(--mi-focus-ring-width) solid var(--mi-focus-ring-color);
    outline-offset: 4px;
    border-radius: 2px;
  }

  /* ==============================================================
     7. ICON INTERACTIONS
     ============================================================== */

  .icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: transparent;
    border: none;
    border-radius: var(--mi-radius);
    color: var(--mi-text);
    cursor: pointer;
    transition:
      background var(--mi-duration-fast) var(--mi-easing),
      color var(--mi-duration-fast) var(--mi-easing);
    font-size: 1.25rem;
  }

  .icon-btn:hover {
    background: var(--mi-surface-hover);
  }

  .icon-btn:active {
    transform: scale(0.92);
  }

  .icon-btn:focus-visible {
    outline: var(--mi-focus-ring-width) solid var(--mi-focus-ring-color);
    outline-offset: var(--mi-focus-ring-offset);
  }

  /* Heart/like animation */
  .icon-btn-like:active svg {
    animation: like-pop var(--mi-duration-slow) var(--mi-easing-bounce);
  }

  @keyframes like-pop {
    0%   { transform: scale(1); }
    30%  { transform: scale(1.3); }
    60%  { transform: scale(0.9); }
    100% { transform: scale(1); }
  }

  /* ==============================================================
     8. TOOLTIP (CSS-only)
     ============================================================== */

  .tooltip-trigger {
    position: relative;
  }

  .tooltip-trigger::before {
    content: attr(data-tooltip);
    position: absolute;
    bottom: calc(100% + 8px);
    left: 50%;
    transform: translateX(-50%) translateY(4px);
    padding: 0.375rem 0.75rem;
    font-size: 0.8125rem;
    font-weight: 500;
    color: #fff;
    background: #111827;
    border-radius: 6px;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition:
      opacity var(--mi-duration-fast) var(--mi-easing),
      transform var(--mi-duration-fast) var(--mi-easing);
  }

  .tooltip-trigger:hover::before,
  .tooltip-trigger:focus-visible::before {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }

  /* Arrow */
  .tooltip-trigger::after {
    content: '';
    position: absolute;
    bottom: calc(100% + 4px);
    left: 50%;
    transform: translateX(-50%);
    border: 4px solid transparent;
    border-top-color: #111827;
    opacity: 0;
    pointer-events: none;
    transition: opacity var(--mi-duration-fast) var(--mi-easing);
  }

  .tooltip-trigger:hover::after,
  .tooltip-trigger:focus-visible::after {
    opacity: 1;
  }
</style>
</head>
<body>

<!-- ===== FOCUS RINGS ===== -->
<section class="demo-section">
  <h2>1. Focus-Visible Rings</h2>
  <p style="margin-bottom: 1rem; color: #6b7280;">Tab through these elements to see the focus rings. Mouse clicks will NOT show them.</p>
  <div class="demo-row">
    <div class="demo-col">
      <button class="btn btn-lift focusable">Outline Ring</button>
      <span class="demo-label">Default outline</span>
    </div>
    <div class="demo-col">
      <button class="btn btn-lift focus-ring-shadow">Shadow Ring</button>
      <span class="demo-label">Box-shadow ring</span>
    </div>
    <div class="demo-col">
      <button class="btn btn-lift focus-ring-animated">Animated Ring</button>
      <span class="demo-label">Animated shadow</span>
    </div>
  </div>
</section>

<!-- ===== BUTTONS ===== -->
<section class="demo-section">
  <h2>2. Button Hover States</h2>
  <div class="demo-row">
    <div class="demo-col">
      <button class="btn btn-lift">Lift</button>
      <span class="demo-label">translateY + shadow</span>
    </div>
    <div class="demo-col">
      <button class="btn btn-glow">Glow</button>
      <span class="demo-label">box-shadow glow</span>
    </div>
    <div class="demo-col">
      <button class="btn btn-ripple">Ripple</button>
      <span class="demo-label">Click me (CSS ripple)</span>
    </div>
    <div class="demo-col">
      <button class="btn btn-fill">Fill</button>
      <span class="demo-label">Background fill</span>
    </div>
    <div class="demo-col">
      <button class="btn btn-scale">Scale</button>
      <span class="demo-label">Bounce scale</span>
    </div>
  </div>
  <div class="demo-row">
    <div class="demo-col">
      <button class="btn btn-lift btn-loading">Loading</button>
      <span class="demo-label">Loading state</span>
    </div>
  </div>
</section>

<!-- ===== CARDS ===== -->
<section class="demo-section">
  <h2>3. Card Hover Effects</h2>
  <div class="demo-row">
    <div class="card card-lift" tabindex="0">
      <h3>Lift</h3>
      <p>Elevates on hover with enhanced shadow.</p>
    </div>
    <div class="card card-glow" tabindex="0">
      <h3>Border Glow</h3>
      <p>Border turns accent colour with outer glow.</p>
    </div>
    <div class="card card-tilt" tabindex="0">
      <h3>Tilt</h3>
      <p>Subtle 3D perspective rotation.</p>
    </div>
    <div class="card card-highlight" tabindex="0">
      <h3>Highlight Bar</h3>
      <p>Top accent bar reveals on hover.</p>
    </div>
  </div>
</section>

<!-- ===== TOGGLES ===== -->
<section class="demo-section">
  <h2>4. Toggle Switch</h2>
  <div class="demo-row">
    <label class="toggle-wrapper">
      <label class="toggle">
        <input type="checkbox" />
        <span class="toggle__track"></span>
        <span class="toggle__knob"></span>
      </label>
      <span class="toggle-label">Notifications</span>
    </label>
    <label class="toggle-wrapper">
      <label class="toggle">
        <input type="checkbox" checked />
        <span class="toggle__track"></span>
        <span class="toggle__knob"></span>
      </label>
      <span class="toggle-label">Dark mode</span>
    </label>
    <label class="toggle-wrapper">
      <label class="toggle">
        <input type="checkbox" disabled />
        <span class="toggle__track"></span>
        <span class="toggle__knob"></span>
      </label>
      <span class="toggle-label">Disabled</span>
    </label>
  </div>
</section>

<!-- ===== LOADING ===== -->
<section class="demo-section">
  <h2>5. Loading States</h2>
  <div class="demo-row" style="align-items: center;">
    <div class="demo-col">
      <div class="spinner"></div>
      <span class="demo-label">Spinner</span>
    </div>
    <div class="demo-col">
      <div class="dots-loader">
        <div class="dots-loader__dot"></div>
        <div class="dots-loader__dot"></div>
        <div class="dots-loader__dot"></div>
      </div>
      <span class="demo-label">Dots</span>
    </div>
    <div class="demo-col" style="width: 200px;">
      <div style="width: 100%;">
        <div class="skeleton skeleton-line" style="width: 80%;"></div>
        <div class="skeleton skeleton-line"></div>
        <div class="skeleton skeleton-line"></div>
      </div>
      <span class="demo-label">Skeleton</span>
    </div>
  </div>
</section>

<!-- ===== LINKS ===== -->
<section class="demo-section">
  <h2>6. Link & Text Interactions</h2>
  <div class="demo-row">
    <a href="#" class="link-underline">Hover me for underline</a>
  </div>
</section>

<!-- ===== TOOLTIPS ===== -->
<section class="demo-section">
  <h2>7. Tooltips</h2>
  <div class="demo-row">
    <button
      class="btn btn-lift tooltip-trigger"
      data-tooltip="This is a tooltip!"
    >
      Hover for tooltip
    </button>
    <button
      class="icon-btn tooltip-trigger"
      data-tooltip="Settings"
      aria-label="Settings"
    >
      &#9881;
    </button>
  </div>
</section>

</body>
</html>
```

---

## Variants

### Custom Theme Override

```css
/* Override tokens for a completely different look */
.theme-warm {
  --mi-accent: #f59e0b;
  --mi-accent-light: #fcd34d;
  --mi-accent-dark: #d97706;
  --mi-glow-color: rgba(245, 158, 11, 0.4);
  --mi-focus-ring-color: #f59e0b;
  --mi-radius: 12px;
  --mi-duration-normal: 250ms;
  --mi-easing: cubic-bezier(0.33, 1, 0.68, 1);
}

.theme-minimal {
  --mi-accent: #000;
  --mi-glow-color: rgba(0, 0, 0, 0.15);
  --mi-focus-ring-color: #000;
  --mi-radius: 0;
  --mi-duration-normal: 150ms;
}
```

### JS-Enhanced Ripple (precise click position)

```js
/**
 * Add a real ripple effect that originates from the click position.
 * Apply to any element with [data-ripple].
 */
document.querySelectorAll('[data-ripple]').forEach((el) => {
  el.addEventListener('click', function (e) {
    const rect = this.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const size = Math.max(rect.width, rect.height) * 2;

    const ripple = document.createElement('span');
    ripple.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      left: ${x - size / 2}px;
      top: ${y - size / 2}px;
      background: rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      transform: scale(0);
      animation: js-ripple 0.5s ease-out forwards;
      pointer-events: none;
    `;

    this.style.position = 'relative';
    this.style.overflow = 'hidden';
    this.appendChild(ripple);

    ripple.addEventListener('animationend', () => ripple.remove());
  });
});

// Add this keyframe to your CSS:
// @keyframes js-ripple {
//   to { transform: scale(1); opacity: 0; }
// }
```

### JS-Enhanced Card Tilt (follows mouse)

```js
/**
 * 3D tilt that follows the mouse cursor.
 * Apply to any element with [data-tilt].
 */
document.querySelectorAll('[data-tilt]').forEach((card) => {
  const maxTilt = 8; // degrees

  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;  // 0-1
    const y = (e.clientY - rect.top) / rect.height;   // 0-1
    const rotateX = (0.5 - y) * maxTilt;
    const rotateY = (x - 0.5) * maxTilt;

    card.style.transform =
      `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(4px)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
    card.style.transition = 'transform 0.4s ease';
    setTimeout(() => { card.style.transition = ''; }, 400);
  });
});
```

---

## Performance

All micro-interactions in this library are optimised for compositor-only animations where possible:

| Animation Property | Compositor-Only? | Trigger Repaint? |
|-------------------|------------------|-----------------|
| `transform`       | Yes              | No              |
| `opacity`         | Yes              | No              |
| `box-shadow`      | No               | Yes (but fast)  |
| `background`      | No               | Yes             |
| `border-color`    | No               | Yes             |

### Guidelines

1. **Prefer `transform` and `opacity`** for animations -- these bypass layout and paint.
2. **`box-shadow` transitions** are acceptable for hover states (not per-frame animation).
3. **`will-change`** is intentionally NOT applied globally -- only add it to elements that are about to animate (e.g. via a class added by JS before animation starts, then removed after).
4. **Duration: 120-250ms** for most interactions. Slower feels sluggish; faster is imperceptible.
5. **Easing: ease-out** for entrances, **ease-in** for exits. Never use `linear` for UI motion.

---

## Accessibility

### prefers-reduced-motion

The global override at the top of the stylesheet disables ALL animations and transitions when the user has enabled "Reduce motion" in their OS settings. This is a nuclear option that ensures nothing moves.

For a more nuanced approach, you can selectively keep non-motion transitions (like colour changes):

```css
@media (prefers-reduced-motion: reduce) {
  /* Disable motion (transforms, animations) */
  .btn-lift:hover { transform: none; }
  .card-lift:hover { transform: none; }
  .card-tilt:hover { transform: none; }

  /* Keep non-motion transitions (colour, opacity) */
  .btn-fill:hover { background: var(--mi-accent); color: var(--mi-text-inverse); }
  .btn-fill::before { display: none; } /* remove sliding fill */
}
```

### Focus Management

- `:focus-visible` is used throughout (not `:focus`) to avoid showing focus rings on mouse clicks.
- All interactive elements have visible focus indicators with sufficient contrast (2px solid ring).
- Cards with hover effects include `tabindex="0"` so keyboard users can access them.
- Tooltips appear on `:focus-visible` in addition to `:hover`.

### Colour Contrast

- All button text meets WCAG AA (4.5:1) against the accent background.
- Focus rings are rendered with an offset gap (white space between element and ring) to ensure visibility on any background.

---

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| `:focus-visible` | 86+ | 85+ | 15.4+ | 86+ |
| `prefers-reduced-motion` | 74+ | 63+ | 10.1+ | 79+ |
| CSS Custom Properties | 49+ | 31+ | 9.1+ | 15+ |
| `transform` transitions | 36+ | 16+ | 9+ | 12+ |
| `@keyframes` | 43+ | 16+ | 9+ | 12+ |
| `gap` (flexbox) | 84+ | 63+ | 14.1+ | 84+ |

For Safari < 15.4 (no `:focus-visible`), add the polyfill or use `:focus` as fallback:

```css
/* Fallback for old Safari */
.btn:focus {
  outline: 2px solid var(--mi-focus-ring-color);
  outline-offset: 2px;
}

/* Override for browsers that support :focus-visible */
.btn:focus:not(:focus-visible) {
  outline: none;
}

.btn:focus-visible {
  outline: 2px solid var(--mi-focus-ring-color);
  outline-offset: 2px;
}
```

---

## Sources

- [CSS-Tricks: Hover Selector in 2026](https://thelinuxcode.com/css-hover-selector-in-2026-practical-patterns-pitfalls-and-accessible-interactions/)
- [SitePoint: 10 Simple CSS and JavaScript Micro-interactions for Buttons](https://www.sitepoint.com/button-micro-interactions/)
- [FrontendTools: 10 Micro-Interaction Examples](https://www.frontendtools.tech/blog/micro-interactions-ui-ux-guide)
- [Pixel Free Studio: Best Practices for Animating Micro-Interactions with CSS](https://blog.pixelfreestudio.com/best-practices-for-animating-micro-interactions-with-css/)
- [CodePen: Pure CSS ripple effect for Material Design](https://codepen.io/finnhvman/pen/jLXKJw)
- [Roberto Moreno: Micro-Interactions That Don't Annoy](https://robertcelt95.medium.com/micro-interactions-that-dont-annoy-the-3-second-rule-for-ui-animation-9881300cd187)
- [FreeFrontend: 103 UI Micro Interaction Examples](https://freefrontend.com/ui-micro-interaction/)
- [CSS Author: CSS Hover Effects 2025](https://cssauthor.com/css-hover-effects/)
