---
technique: Mesh Gradient (Stripe-style Animated Background)
complexity: intermediate
browser_support: CSS version all modern browsers; WebGL version 97%+ global coverage
performance_impact: medium
---

## Overview

Stripe popularised the animated mesh gradient on their homepage -- a flowing, organic blend of colours
that shifts like liquid paint. The effect is achieved through WebGL shaders that use Simplex noise and
Fractal Brownian Motion to animate colour fields on a canvas.

There are two practical approaches:
1. **Pure CSS** -- uses layered `conic-gradient` or `radial-gradient` with a large `blur()` filter. Simpler, lower fidelity, higher CPU cost at large sizes.
2. **WebGL / Canvas** -- uses fragment shaders for GPU-accelerated, buttery-smooth animation. Higher fidelity, lower CPU cost, requires a bit more code.

**Where it is used:** Stripe, Linear, Vercel, Raycast, and countless SaaS landing pages.

---

## Implementation

### Approach 1: Pure CSS Mesh Gradient

This technique layers multiple radial gradients and applies a heavy blur, then animates their positions.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CSS Mesh Gradient</title>
<style>
  :root {
    /* Colour palette -- easy to customise */
    --mg-color-1: #ff6b6b;
    --mg-color-2: #4ecdc4;
    --mg-color-3: #45b7d1;
    --mg-color-4: #f7dc6f;
    --mg-color-5: #bb8fce;
    --mg-bg: #0a0a0a;
    --mg-blur: 120px;
    --mg-speed: 20s;
  }

  *,
  *::before,
  *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    min-height: 100vh;
    background: var(--mg-bg);
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }

  .mesh-gradient-css {
    position: fixed;
    inset: 0;
    overflow: hidden;
    z-index: 0;
  }

  /* Each blob is an absolutely-positioned circle with a radial gradient */
  .mesh-gradient-css__blob {
    position: absolute;
    width: 60vmax;
    height: 60vmax;
    border-radius: 50%;
    filter: blur(var(--mg-blur));
    opacity: 0.8;
    mix-blend-mode: screen;
    will-change: transform;
  }

  .mesh-gradient-css__blob:nth-child(1) {
    background: radial-gradient(circle, var(--mg-color-1) 0%, transparent 70%);
    top: -20%;
    left: -10%;
    animation: blob-drift-1 var(--mg-speed) ease-in-out infinite alternate;
  }

  .mesh-gradient-css__blob:nth-child(2) {
    background: radial-gradient(circle, var(--mg-color-2) 0%, transparent 70%);
    top: 30%;
    right: -15%;
    animation: blob-drift-2 calc(var(--mg-speed) * 1.2) ease-in-out infinite alternate;
  }

  .mesh-gradient-css__blob:nth-child(3) {
    background: radial-gradient(circle, var(--mg-color-3) 0%, transparent 70%);
    bottom: -25%;
    left: 20%;
    animation: blob-drift-3 calc(var(--mg-speed) * 0.8) ease-in-out infinite alternate;
  }

  .mesh-gradient-css__blob:nth-child(4) {
    background: radial-gradient(circle, var(--mg-color-4) 0%, transparent 70%);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation: blob-drift-4 calc(var(--mg-speed) * 1.5) ease-in-out infinite alternate;
  }

  .mesh-gradient-css__blob:nth-child(5) {
    background: radial-gradient(circle, var(--mg-color-5) 0%, transparent 70%);
    bottom: 10%;
    right: 10%;
    animation: blob-drift-5 calc(var(--mg-speed) * 0.9) ease-in-out infinite alternate;
  }

  @keyframes blob-drift-1 {
    to { transform: translate(30vw, 20vh) scale(1.1); }
  }
  @keyframes blob-drift-2 {
    to { transform: translate(-25vw, 15vh) scale(0.9); }
  }
  @keyframes blob-drift-3 {
    to { transform: translate(20vw, -30vh) scale(1.2); }
  }
  @keyframes blob-drift-4 {
    to { transform: translate(-15vw, -10vh) scale(0.85); }
  }
  @keyframes blob-drift-5 {
    to { transform: translate(-20vw, 20vh) scale(1.15); }
  }

  /* Content overlay */
  .content {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    color: #fff;
    text-align: center;
    padding: 2rem;
  }

  .content h1 {
    font-size: clamp(2rem, 6vw, 5rem);
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  /* Reduced motion: stop animation, show static gradient */
  @media (prefers-reduced-motion: reduce) {
    .mesh-gradient-css__blob {
      animation: none !important;
    }
  }
</style>
</head>
<body>

<div class="mesh-gradient-css">
  <div class="mesh-gradient-css__blob"></div>
  <div class="mesh-gradient-css__blob"></div>
  <div class="mesh-gradient-css__blob"></div>
  <div class="mesh-gradient-css__blob"></div>
  <div class="mesh-gradient-css__blob"></div>
</div>

<div class="content">
  <h1>Mesh Gradient</h1>
</div>

</body>
</html>
```

---

### Approach 2: WebGL Animated Mesh Gradient (Stripe-style)

This is the high-fidelity approach. A fragment shader uses Simplex noise to blend colours smoothly
on the GPU. Based on the MiniGL pattern Stripe uses internally.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WebGL Mesh Gradient</title>
<style>
  :root {
    --mg-canvas-opacity: 1;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    min-height: 100vh;
    background: #000;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }

  #gradient-canvas {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    opacity: var(--mg-canvas-opacity);
    /* Render at lower resolution for performance */
  }

  .content {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    color: #fff;
    text-align: center;
  }

  .content h1 {
    font-size: clamp(2rem, 6vw, 5rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
  }

  @media (prefers-reduced-motion: reduce) {
    #gradient-canvas {
      /* Shader will detect this and stop animating */
    }
  }
</style>
</head>
<body>

<canvas id="gradient-canvas"></canvas>

<div class="content">
  <h1>WebGL Mesh Gradient</h1>
</div>

<script>
/**
 * WebGL Mesh Gradient
 *
 * Renders a Stripe-inspired animated mesh gradient using:
 * - Simplex 3D noise in GLSL (for organic movement)
 * - Fractal Brownian Motion (FBM) for layered detail
 * - Configurable colour palette via JS
 * - GPU-accelerated, runs at 60fps on most devices
 */
(function () {
  'use strict';

  // ========================
  // Configuration
  // ========================
  const COLORS = [
    [0.43, 0.28, 0.92],   // #6E47EB -- purple
    [0.94, 0.30, 0.44],   // #F04D70 -- coral
    [0.20, 0.76, 0.80],   // #33C2CC -- teal
    [1.00, 0.76, 0.24],   // #FFC23D -- amber
  ];

  const SPEED = 0.0003;             // animation speed
  const NOISE_SCALE = 1.5;          // noise frequency
  const PIXEL_RATIO_CAP = 1.5;      // limit resolution for perf

  // ========================
  // Shaders
  // ========================
  const VERTEX_SHADER = `
    attribute vec2 a_position;
    void main() {
      gl_Position = vec4(a_position, 0.0, 1.0);
    }
  `;

  const FRAGMENT_SHADER = `
    precision mediump float;

    uniform float u_time;
    uniform vec2 u_resolution;
    uniform vec3 u_colors[4];
    uniform float u_noiseScale;

    // Simplex 3D noise (Ashima Arts)
    vec4 permute(vec4 x) { return mod(((x*34.0)+1.0)*x, 289.0); }
    vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

    float snoise(vec3 v) {
      const vec2 C = vec2(1.0/6.0, 1.0/3.0);
      const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
      vec3 i = floor(v + dot(v, C.yyy));
      vec3 x0 = v - i + dot(i, C.xxx);
      vec3 g = step(x0.yzx, x0.xyz);
      vec3 l = 1.0 - g;
      vec3 i1 = min(g.xyz, l.zxy);
      vec3 i2 = max(g.xyz, l.zxy);
      vec3 x1 = x0 - i1 + C.xxx;
      vec3 x2 = x0 - i2 + C.yyy;
      vec3 x3 = x0 - D.yyy;
      i = mod(i, 289.0);
      vec4 p = permute(permute(permute(
                i.z + vec4(0.0, i1.z, i2.z, 1.0))
              + i.y + vec4(0.0, i1.y, i2.y, 1.0))
              + i.x + vec4(0.0, i1.x, i2.x, 1.0));
      float n_ = 1.0/7.0;
      vec3 ns = n_ * D.wyz - D.xzx;
      vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
      vec4 x_ = floor(j * ns.z);
      vec4 y_ = floor(j - 7.0 * x_);
      vec4 x = x_ * ns.x + ns.yyyy;
      vec4 y = y_ * ns.x + ns.yyyy;
      vec4 h = 1.0 - abs(x) - abs(y);
      vec4 b0 = vec4(x.xy, y.xy);
      vec4 b1 = vec4(x.zw, y.zw);
      vec4 s0 = floor(b0) * 2.0 + 1.0;
      vec4 s1 = floor(b1) * 2.0 + 1.0;
      vec4 sh = -step(h, vec4(0.0));
      vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
      vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;
      vec3 p0 = vec3(a0.xy, h.x);
      vec3 p1 = vec3(a0.zw, h.y);
      vec3 p2 = vec3(a1.xy, h.z);
      vec3 p3 = vec3(a1.zw, h.w);
      vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
      p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
      vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
      m = m * m;
      return 42.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
    }

    // Fractal Brownian Motion
    float fbm(vec3 p) {
      float value = 0.0;
      float amplitude = 0.5;
      float frequency = 1.0;
      for (int i = 0; i < 4; i++) {
        value += amplitude * snoise(p * frequency);
        frequency *= 2.0;
        amplitude *= 0.5;
      }
      return value;
    }

    void main() {
      vec2 uv = gl_FragCoord.xy / u_resolution;

      // Warp UV with sinusoidal mesh (liquid fabric look)
      float t = u_time;
      vec2 warpedUV = uv;
      warpedUV.x += sin(uv.y * 3.0 + t * 0.5) * 0.05;
      warpedUV.y += cos(uv.x * 3.0 + t * 0.4) * 0.05;

      // Noise fields for colour mixing
      float n1 = fbm(vec3(warpedUV * u_noiseScale, t * 0.3));
      float n2 = fbm(vec3(warpedUV * u_noiseScale + 5.0, t * 0.25));
      float n3 = fbm(vec3(warpedUV * u_noiseScale + 10.0, t * 0.35));

      // Remap noise from [-1,1] to [0,1]
      n1 = n1 * 0.5 + 0.5;
      n2 = n2 * 0.5 + 0.5;
      n3 = n3 * 0.5 + 0.5;

      // Blend four colours using noise fields
      vec3 color = mix(u_colors[0], u_colors[1], n1);
      color = mix(color, u_colors[2], n2);
      color = mix(color, u_colors[3], n3 * 0.6);

      // Subtle vignette
      float vignette = 1.0 - 0.3 * length(uv - 0.5);
      color *= vignette;

      gl_FragColor = vec4(color, 1.0);
    }
  `;

  // ========================
  // WebGL Setup
  // ========================
  const canvas = document.getElementById('gradient-canvas');
  const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

  if (!gl) {
    console.warn('WebGL not supported, falling back to CSS gradient');
    document.body.style.background =
      'linear-gradient(135deg, #6E47EB 0%, #F04D70 50%, #33C2CC 100%)';
    canvas.style.display = 'none';
    return;
  }

  function compileShader(source, type) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.error('Shader error:', gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  }

  const vertShader = compileShader(VERTEX_SHADER, gl.VERTEX_SHADER);
  const fragShader = compileShader(FRAGMENT_SHADER, gl.FRAGMENT_SHADER);

  const program = gl.createProgram();
  gl.attachShader(program, vertShader);
  gl.attachShader(program, fragShader);
  gl.linkProgram(program);
  gl.useProgram(program);

  // Full-screen quad
  const vertices = new Float32Array([
    -1, -1,  1, -1,  -1, 1,
    -1,  1,  1, -1,   1, 1,
  ]);

  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

  const posLoc = gl.getAttribLocation(program, 'a_position');
  gl.enableVertexAttribArray(posLoc);
  gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

  // Uniforms
  const uTime = gl.getUniformLocation(program, 'u_time');
  const uResolution = gl.getUniformLocation(program, 'u_resolution');
  const uNoiseScale = gl.getUniformLocation(program, 'u_noiseScale');

  // Set colour uniforms
  for (let i = 0; i < COLORS.length; i++) {
    const loc = gl.getUniformLocation(program, `u_colors[${i}]`);
    gl.uniform3fv(loc, COLORS[i]);
  }
  gl.uniform1f(uNoiseScale, NOISE_SCALE);

  // ========================
  // Resize
  // ========================
  function resize() {
    const dpr = Math.min(window.devicePixelRatio, PIXEL_RATIO_CAP);
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * dpr;
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(uResolution, canvas.width, canvas.height);
  }

  window.addEventListener('resize', resize);
  resize();

  // ========================
  // Animation Loop
  // ========================
  const prefersReducedMotion = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
  ).matches;

  let startTime = performance.now();
  let animationId;

  function render(now) {
    const elapsed = (now - startTime) * SPEED;
    gl.uniform1f(uTime, elapsed);
    gl.drawArrays(gl.TRIANGLES, 0, 6);

    if (!prefersReducedMotion) {
      animationId = requestAnimationFrame(render);
    }
  }

  // If reduced motion, render one frame and stop
  if (prefersReducedMotion) {
    render(performance.now());
  } else {
    animationId = requestAnimationFrame(render);
  }

  // Cleanup on page hide (save battery)
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      cancelAnimationFrame(animationId);
    } else if (!prefersReducedMotion) {
      startTime = performance.now();
      animationId = requestAnimationFrame(render);
    }
  });
})();
</script>

</body>
</html>
```

---

## Variants

### Colour Palette Presets

```js
// Stripe (original)
const STRIPE = [
  [0.43, 0.28, 0.92],  // purple
  [0.94, 0.30, 0.44],  // coral
  [0.20, 0.76, 0.80],  // teal
  [1.00, 0.76, 0.24],  // amber
];

// Ocean
const OCEAN = [
  [0.00, 0.20, 0.40],  // deep navy
  [0.10, 0.50, 0.70],  // cerulean
  [0.30, 0.80, 0.75],  // seafoam
  [0.60, 0.90, 0.95],  // pale aqua
];

// Sunset
const SUNSET = [
  [0.95, 0.25, 0.20],  // red
  [1.00, 0.55, 0.20],  // orange
  [1.00, 0.80, 0.30],  // gold
  [0.55, 0.20, 0.55],  // plum
];

// Aurora (dark mode)
const AURORA = [
  [0.10, 0.90, 0.50],  // green
  [0.20, 0.60, 0.95],  // blue
  [0.60, 0.20, 0.80],  // violet
  [0.05, 0.40, 0.30],  // dark teal
];

// Monochrome (elegant)
const MONO = [
  [0.15, 0.15, 0.20],  // charcoal
  [0.30, 0.30, 0.38],  // slate
  [0.50, 0.50, 0.55],  // grey
  [0.75, 0.75, 0.80],  // silver
];
```

### Runtime Colour Update

```js
function updateColors(newColors) {
  for (let i = 0; i < newColors.length; i++) {
    const loc = gl.getUniformLocation(program, `u_colors[${i}]`);
    gl.uniform3fv(loc, newColors[i]);
  }
}

// Smooth transition between palettes
function transitionPalette(from, to, duration = 2000) {
  const start = performance.now();
  function step(now) {
    const t = Math.min((now - start) / duration, 1);
    const eased = t * t * (3 - 2 * t); // smoothstep
    const blended = from.map((c, i) =>
      c.map((v, j) => v + (to[i][j] - v) * eased)
    );
    updateColors(blended);
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
```

---

## Performance

| Approach | CPU Usage | GPU Usage | Mobile Safe | Battery Impact |
|----------|-----------|-----------|-------------|----------------|
| CSS blobs + blur | Medium-High | Low | Caution at large sizes | Medium |
| WebGL shader | Low | Medium | Yes (with DPR cap) | Low-Medium |

### Key Optimisations

1. **Cap pixel ratio** -- `Math.min(devicePixelRatio, 1.5)` prevents 3x rendering on high-DPI mobile.
2. **Pause when hidden** -- `visibilitychange` listener stops the animation loop when the tab is backgrounded.
3. **Fewer FBM octaves** -- reducing from 4 to 2 octaves in the shader halves fragment shader cost (at the expense of detail).
4. **CSS approach: `will-change: transform`** on blobs enables compositor-only animation (no repaint).
5. **CSS approach: reduce blob count** -- 3 blobs is often enough for a convincing effect.

---

## Accessibility

- **`prefers-reduced-motion`** -- the WebGL version renders a single static frame; the CSS version freezes all animations.
- **Content overlay** -- always place text content ABOVE the gradient in z-index with sufficient contrast. Use `text-shadow` or a semi-transparent overlay if needed.
- **Not purely decorative?** -- if the gradient conveys brand identity but no information, mark the canvas with `role="presentation"` and `aria-hidden="true"`.
- **Seizure safety** -- the animation speed is intentionally slow (full cycle ~20s). Rapid colour flashing is avoided by design.

```html
<canvas id="gradient-canvas" role="presentation" aria-hidden="true"></canvas>
```

---

## Browser Support

| Feature       | Chrome | Firefox | Safari | Edge  |
|---------------|--------|---------|--------|-------|
| WebGL 1.0     | 9+     | 4+      | 5.1+   | 12+   |
| CSS filter blur| 18+   | 35+     | 6+     | 12+   |
| mix-blend-mode| 41+    | 32+     | 8+     | 79+   |
| will-change   | 36+    | 36+     | 9.1+   | 79+   |

**Fallback chain:** WebGL shader -> CSS blobs -> static `linear-gradient`.

---

## Sources

- [Kevin Hufnagl: How To Create the Stripe Website Gradient Effect](https://kevinhufnagl.com/how-to-stripe-website-gradient-effect/)
- [Bram.us: How To Create the Stripe Website Gradient Effect](https://www.bram.us/2021/10/13/how-to-create-the-stripe-website-gradient-effect/)
- [Stripe Mesh Gradient WebGL Gist](https://gist.github.com/jordienr/64bcf75f8b08641f205bd6a1a0d4ce1d)
- [exzenter/gradient-stripe (GitHub)](https://github.com/exzenter/gradient-stripe)
- [Alex Harri: A flowing WebGL gradient, deconstructed](https://alexharri.com/blog/webgl-gradients)
- [Codrops: How to Recreate Stripe's Lava Lamp Gradient with Three.js](https://tympanus.net/codrops/2022/09/26/how-to-recreate-stripes-lava-lamp-gradient-with-three-js/)
- [Stripe MiniGL CodePen by Bramus](https://codepen.io/bramus/pen/ExvKVzo)
