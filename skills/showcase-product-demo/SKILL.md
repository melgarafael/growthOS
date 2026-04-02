---
name: showcase-product-demo
description: Product Demo showcase — full product walkthrough with browser/mobile device frames, animated cursor navigation, scroll and zoom reveals driven by video-profile.yaml journeys, ending with a branded CTA. Produces a 30–60s 16:9 MP4 via the ProductDemo composition.
---

# Showcase: Product Demo

Specialist skill for the **Product Demo** showcase. Activated by the `remotion-pro` orchestrator when the user selects showcase `1` (`demo`, `produto`, `product-demo`). Receives a context object with `video_profile`, `brand_voice`, `remotion`, and `briefing`.

---

## Overview

The Product Demo showcase creates a polished, professional product walkthrough video. It wraps product screenshots in realistic device frames (browser or mobile), animates a cursor navigating through the UI, demonstrates click interactions, smooth scroll reveals, and ends with a branded CTA.

**Best for:** SaaS landing pages, app store previews, investor decks, product launches, feature announcements.

**Composition ID:** `ProductDemo`
**Aspect ratio:** 16:9 (1920×1080)
**FPS:** 30
**Duration range:** 30–60 seconds (900–1800 frames)

---

## Components Used

| Component | File | Purpose in video |
|---|---|---|
| `BrowserFrame` | `components/BrowserFrame.tsx` | Wraps screenshots in Chrome/Safari/Arc chrome with URL bar |
| `MobileFrame` | `components/MobileFrame.tsx` | Wraps screenshots in iPhone/Android device shell |
| `AnimatedCursor` | `components/AnimatedCursor.tsx` | Moves cursor across screen with spring easing and click effects |
| `ScreenScroll` | `components/ScreenScroll.tsx` | Smoothly scrolls a tall screenshot revealing below-fold content |
| `ScreenshotOverlay` | `components/ScreenshotOverlay.tsx` | Displays screenshot with fade/scale/slide-up entry animation |
| `ZoomReveal` | `components/ZoomReveal.tsx` | Zooms into a UI region to highlight a key feature or stat |
| `AnimatedText` | `components/AnimatedText.tsx` | Hook title and CTA text with fade-in / scale-in animations |
| `BackgroundGradient` | `components/BackgroundGradient.tsx` | Dark branded background throughout the video |
| `ProgressBar` | `components/ProgressBar.tsx` | Accent-colored scrub bar at bottom of frame |
| `BrandWatermark` | `components/BrandWatermark.tsx` | Handle overlay at watermark position |

---

## Scene Flow Template

Default sequence for a medium-pacing, browser-frame, 2-screen journey:

```
Scene 1 — Hook           (0s–3s,   frames 0–89)
  AnimatedText: product name + tagline, animation: scale-in
  BackgroundGradient fills frame

Scene 2 — Device Intro   (3s–5s,   frames 90–149)
  BrowserFrame slides in from bottom with spring
  ScreenshotOverlay: first screenshot fades in inside frame
  URL bar shows product domain

Scene 3 — Cursor Navigate (5s–12s, frames 150–359)
  AnimatedCursor follows path from center → target element
  Hotspot: cursor pauses, ripple click effect fires
  ScreenshotOverlay: next screenshot crossfades (screen transition after click)

Scene 4 — Scroll Reveal   (12s–17s, frames 360–509)
  ScreenScroll: page scrolls 600px at ease-in-out speed
  Pause at mid-point 1s to let content read
  Content below fold becomes visible

Scene 5 — Zoom           (17s–20s, frames 510–599)
  ZoomReveal: zooms into key UI element (stat, feature badge, pricing)
  highlightBox: true with accent color border

Scene 6 — CTA            (20s–25s, frames 600–749)
  Device frame fades out / blurs
  AnimatedText: CTA headline bounces in
  URL / app name in accent-colored pill
  BrandWatermark at bottom-right
```

**Pacing multipliers** (applied to all scene durations):
- `fast`: × 0.7
- `medium`: × 1.0 (default)
- `slow`: × 1.4

---

## Storyboard Generation Rules

### Step 1 — Parse the briefing

Extract the following from the user's briefing text:

```
product_name   → explicit mention OR video-profile.yaml → brand.name → "Your Product"
feature        → explicit feature name OR first journey name in video-profile.yaml
device         → "mobile" / "iphone" / "phone" → MobileFrame
                 "browser" / "desktop" / "chrome" → BrowserFrame (default)
journey_name   → match to video-profile.yaml journeys[*].name (fuzzy match)
screenshots    → collect from matched journey screens[*].screenshot
actions        → collect from matched journey screens[*].actions
cta_text       → explicit URL/copy in briefing OR brand-voice.yaml → cta.default
```

### Step 2 — Select journey

```
IF briefing specifies a journey name:
  Find matching journey in video-profile.yaml journeys[] (case-insensitive)
ELSE IF video-profile.yaml has exactly one journey:
  Use that journey
ELSE IF video-profile.yaml has multiple journeys:
  Ask user: "Which journey should the demo follow? [list journey names]"
ELSE:
  Ask user to provide screenshots and action sequence inline
```

### Step 3 — Map actions to scene types

For each action string in journey screen actions, map to a scene type:

| Action pattern | Scene type | Component |
|---|---|---|
| `clica [target]` / `click [target]` | `navigate` | AnimatedCursor → click at target element |
| `scroll até [section]` / `scroll to` | `scroll` | ScreenScroll with pause at section |
| `navega para [page]` / `navigate to` | `navigate` | Cursor click + screen crossfade |
| `zoom em [feature]` / `zoom on` | `zoom` | ZoomReveal centered on feature area |
| `digita [text]` / `type [text]` | `navigate` | Cursor moves to input, AnimatedText typewriter |
| `preenche [field]` / `fill [field]` | `navigate` | Same as digita |

### Step 4 — Estimate cursor coordinates

When screenshots exist: use 960×540 as center (half of 1920×1080 display area).
Use these heuristic coordinates when explicit pixel positions are not provided:

```
Common UI targets (browser frame at 1920×1080, content area ~1760×900):
  "Sign Up" / "Get Started" button   → { x: 960, y: 400 }
  "Login" / "Sign In"                → { x: 960, y: 350 }
  Navigation menu item               → { x: 300, y: 80 }
  Search bar                         → { x: 700, y: 120 }
  Dashboard card                     → { x: 500, y: 500 }
  Settings icon                      → { x: 1700, y: 80 }
  Submit / Save button               → { x: 960, y: 700 }
```

If the user has provided screenshots and named targets: use center-of-named-element estimation based on common UI patterns.

### Step 5 — Calculate scene durations

```
hook_duration      = 3s (always)
device_intro       = 2s (always)
per_navigate_scene = 4s base + 1s per cursor path point
per_scroll_scene   = 3s base + (scrollDistance / 200) seconds
per_zoom_scene     = 2.5s (always)
cta_duration       = 4s (always)

total = sum of all scene durations
IF total < 30: expand navigate scenes by 1.5×
IF total > 60: merge adjacent navigate scenes, reduce scroll to minimum
```

### Step 6 — Output storyboard YAML

```yaml
# storyboard.yaml — Product Demo
showcase: ProductDemo
product: "[product_name]"
device: "[browser|mobile]"
journey: "[journey_name]"
total_duration_s: [calculated]
pacing: "[fast|medium|slow from video-profile.yaml]"

scenes:
  - id: hook
    type: hook
    duration_s: 3
    text: "[product_name]"
    subtext: "[tagline from brand-voice.yaml OR briefing]"
    animation: scale-in

  - id: device-intro
    type: device-intro
    duration_s: 2
    screenshot: "[screens[0].screenshot]"
    device: "[browser|mobile]"
    url: "[product domain]"
    animation: slide-up

  - id: navigate-[N]
    type: navigate
    duration_s: [calculated]
    screenshot: "[screens[N].screenshot]"
    cursor_path:
      - { x: 960, y: 540, action: move }
      - { x: [target_x], y: [target_y], action: click, delay: 20 }
    next_screenshot: "[screens[N+1].screenshot]"
    transition: crossfade

  - id: scroll-[N]
    type: scroll
    duration_s: [calculated]
    screenshot: "[current screenshot]"
    scroll_distance: 600
    pause_points:
      - { position: 300, duration: 30 }

  - id: zoom-[N]
    type: zoom
    duration_s: 2.5
    screenshot: "[current screenshot]"
    zoom_target: { x: 800, y: 400, width: 400, height: 200 }
    zoom_level: 2.5
    highlight_box: true

  - id: cta
    type: cta
    duration_s: 4
    text: "[cta_text]"
    subtext: "[product URL]"
    animation: bounce
```

---

## Composition Mapping

Convert storyboard to Remotion props for the `ProductDemo` composition:

### Frame calculation

```
scene.duration_s × 30 = scene.durationFrames

startFrame for scene[N] = sum of durationFrames for scenes[0..N-1]
```

### Scene type → component mapping

```typescript
// ProductDemoProps (from types.ts)
{
  brand: {
    name: video_profile.assets → brand-voice.yaml → "Product",
    handle: brand-voice.yaml.brand.handle,
    colors: {
      primary:    design_tokens.primary_color,
      secondary:  design_tokens.secondary_color,
      background: "#0F0F1A",         // dark default
      text:       "#FFFFFF",
      accent:     design_tokens.accent_color,
    },
    watermark_position: "bottom-right",
  },
  deviceType: "[browser|mobile]",
  deviceConfig: {
    browser: "chrome",               // or "safari", "arc"
    device:  "iphone15",             // if mobile
    darkMode: true,
  },
  showProgressBar: true,
  showWatermark: true,
  scenes: [
    // hook scene
    { type: "hook", duration: 3, text: "...", subtext: "...", animation: "scale-in",
      startFrame: 0, durationFrames: 90 },

    // device-intro scene
    { type: "device-intro", duration: 2, screenshot: "path/to/screen.png",
      device: "browser", startFrame: 90, durationFrames: 60 },

    // navigate scene
    { type: "navigate", duration: 5, screenshot: "path/to/screen.png",
      cursorPath: [
        { x: 960, y: 540, action: "move" },
        { x: 800, y: 350, action: "click", delay: 20 },
      ],
      startFrame: 150, durationFrames: 150 },

    // scroll scene
    { type: "scroll", duration: 4, screenshot: "path/to/long-screen.png",
      scrollDistance: 600, startFrame: 300, durationFrames: 120 },

    // zoom scene
    { type: "zoom", duration: 2.5,
      zoomTarget: { x: 800, y: 400, width: 400, height: 200 },
      startFrame: 420, durationFrames: 75 },

    // cta scene
    { type: "cta", duration: 4, text: "Try it free", subtext: "product.com",
      animation: "bounce", startFrame: 495, durationFrames: 120 },
  ],
}
```

### Props JSON for render command

Serialize the full props object to JSON and pass via `--props`. Screenshot paths must be relative to the Remotion project `public/` directory or absolute.

---

## Config Reading

### From video-profile.yaml

| Field | Used for |
|---|---|
| `design_tokens.primary_color` | `brand.colors.primary` |
| `design_tokens.secondary_color` | `brand.colors.secondary` |
| `design_tokens.accent_color` | `brand.colors.accent` |
| `design_tokens.heading_font` | font-family in title scenes |
| `assets.screenshots_dir` | prepended to all screenshot paths |
| `assets.logo_path` | shown in hook scene if present |
| `device_frames[]` | validate requested device is in allowed list |
| `journeys[*]` | source of screens, screenshots, and actions |
| `style.pacing` | pacing multiplier (fast/medium/slow) |
| `style.theme` | background color strategy |

### From brand-voice.yaml

| Field | Used for |
|---|---|
| `brand.name` | product_name fallback |
| `brand.handle` | `brand.handle` in watermark |
| `brand.colors.primary` | design token fallback |
| `brand.colors.accent` | accent color fallback |
| `brand.tagline` | hook scene subtext fallback |
| `cta.default` | CTA text fallback |
| `automation.autonomy` | output bundle level (manual/semi/auto) |

### Briefing overrides (highest priority)

Any explicit value in the user's briefing text takes precedence over both YAML files.

---

## Render Command

After generating the composition props, return to the orchestrator with:

```yaml
composition_id: ProductDemo
props: { ...full props object... }
```

The orchestrator renders using the discovered Remotion CLI:

```bash
cd "${REMOTION_PROJECT}" && npx remotion render src/index.ts ProductDemo "${OUTPUT_DIR}/video.mp4" \
  --props='{"brand":{...},"scenes":[...]}' \
  --fps=30
```

For multi-platform (auto autonomy mode), the orchestrator adds additional renders:
```bash
# 9:16 social variant
npx remotion render src/index.ts ProductDemo "${OUTPUT_DIR}/video-9x16.mp4" \
  --width=1080 --height=1920 --props='...' --fps=30
```

---

## Briefing Collection UI

When the orchestrator routes here, display this briefing prompt to the user:

```
PRODUCT DEMO SHOWCASE
─────────────────────────────────────────────────────────
I'll create a product walkthrough video with animated
cursor navigation and device frames.

  Product / feature to demo:
  > [e.g. "GrowthOS onboarding flow" or "checkout feature"]

  Device frame: [browser / mobile]  (default: browser)
  > 

  Journey to use (from video-profile.yaml):
  [list available journeys or "custom"]
  > 

  CTA text (optional — uses brand-voice.yaml default):
  > [e.g. "Try free at growthOS.app"]

  Pacing: [fast / medium / slow]  (default: medium)
  > 
─────────────────────────────────────────────────────────
```

If `video-profile.yaml` has a `style.pacing` value, pre-fill that default. If `journeys` list is empty, skip the journey question and ask for inline screenshots.

---

## Error Handling

| Error condition | Response |
|---|---|
| Journey not found in video-profile.yaml | List available journeys, ask user to select or define inline |
| Screenshot file not found at path | Warn, list missing paths, use gray placeholder frame, continue |
| No journeys defined | Ask user to provide at least 2 screenshot paths with action descriptions |
| Total duration < 15s | Expand cursor paths and add a second scroll scene |
| Total duration > 65s | Ask user which screens to cut or merge adjacent navigate scenes |
| device not in device_frames list | Warn "device X not in your profile's device_frames list", proceed anyway |

---

## Output

Return to orchestrator:

```yaml
status: ready
composition_id: ProductDemo
storyboard_path: "[OUTPUT_DIR]/storyboard.md"
props: { ...ProductDemoProps JSON... }
estimated_duration_s: [N]
scene_count: [N]
```

The orchestrator handles the render call, thumbnail, captions, and output bundle.
