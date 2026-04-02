---
name: showcase-walkthrough
description: App Walkthrough showcase — step-by-step guided tour with animated cursor, Hotspot pulses, Tooltip explanations, scroll transitions, and ZoomReveal on key moments across multiple screens. Journey-driven from video-profile.yaml. Produces a 30–90s 16:9 MP4 via the AppWalkthrough composition.
---

# Showcase: App Walkthrough

Specialist skill for the **App Walkthrough** showcase. Activated by the `remotion-pro` orchestrator when the user selects showcase `8` (`walkthrough`, `tutorial`, `passo-a-passo`, `step-by-step`, `tour`). Receives a context object with `video_profile`, `brand_voice`, `remotion`, and `briefing`.

---

## Overview

The App Walkthrough showcase is the most comprehensive video format — a full guided tour through an entire user journey. An animated cursor navigates the UI step-by-step, `Hotspot` pulses highlight targets before each click, `Tooltip` cards explain each action, `ScreenScroll` transitions move within pages, and `ZoomReveal` emphasizes key outcomes. Multiple screens are woven into one continuous, smooth flow.

**Best for:** product onboarding videos, sales demos, tutorial content, user guides, help center videos, investor walkthroughs, support documentation.

**Composition ID:** `AppWalkthrough`
**Aspect ratio:** 16:9 (1920×1080)
**FPS:** 30
**Duration range:** 30–90 seconds (900–2700 frames)

---

## Components Used

| Component | File | Purpose in video |
|---|---|---|
| `BrowserFrame` | `components/BrowserFrame.tsx` | Wraps each screen in browser chrome with URL bar |
| `MobileFrame` | `components/MobileFrame.tsx` | Wraps screens in iPhone/Android shell (if device=mobile) |
| `AnimatedCursor` | `components/AnimatedCursor.tsx` | Moves cursor from previous position to next target with spring easing |
| `ScreenScroll` | `components/ScreenScroll.tsx` | Scrolls within a tall screenshot between actions |
| `ScreenshotOverlay` | `components/ScreenshotOverlay.tsx` | Crossfades between different app screens on navigation |
| `ZoomReveal` | `components/ZoomReveal.tsx` | Zooms into result or key UI state after important actions |
| `AnimatedText` | `components/AnimatedText.tsx` | Hook title, step labels, and CTA text |
| `BackgroundGradient` | `components/BackgroundGradient.tsx` | Branded background gradient |
| `ProgressBar` | `components/ProgressBar.tsx` | Accent-colored progress bar at bottom |
| `BrandWatermark` | `components/BrandWatermark.tsx` | Handle overlay at watermark position |

### Hotspot (inline component)

`Hotspot` is rendered as an inline animated div inside the `step` scene — a pulsing ring that appears at `cursor_target` coordinates 0.5s before the cursor arrives. Implementation:

```typescript
// Pulsing ring at target position
// Uses interpolate(frame, [0, 15, 30], [0, 1, 0]) for scale pulse
// Color: brand.colors.accent at 60% opacity
// Size: 40×40px, border-radius: 50%, position: absolute
```

### Tooltip (inline component)

`Tooltip` is an animated floating label rendered inside the `step` scene, appearing after the cursor click. Implementation:

```typescript
// Glassmorphic card (blur: 8px, opacity: 0.85) positioned near cursor_target
// Offsets: if target.y > 540 → tooltip above (y - 80), else below (y + 60)
// Contains: action icon + tooltip text (max 60 chars)
// Entry animation: fade-in + slide-up over 12 frames
// Duration: stays visible for remainder of step scene
```

---

## Scene Flow Template

Default sequence for a medium-pacing, 3-screen journey with 2 actions per screen:

```
Scene 1 — Hook              (0s–3s,   frames 0–89)
  AnimatedText: "Here's how [product] works"
  Subtext: journey name or product tagline, animation: fade-in delay 15

Scene 2 — Screen 1 Intro    (3s–5s,   frames 90–149)
  BrowserFrame/MobileFrame slides in from bottom
  ScreenshotOverlay: first screenshot fades in
  AnimatedText: step label appears (e.g., "Step 1: Sign Up")

Scene 3 — Step 1a           (5s–9s,   frames 150–269)
  AnimatedCursor moves from center → target element
  Hotspot pulses at target for 15 frames
  Click effect fires (ripple)
  Tooltip appears: action description
  ScreenshotOverlay crossfades to next state

Scene 4 — Step 1b (scroll)  (9s–12s,  frames 270–359)  [if page is scrollable]
  ScreenScroll: page scrolls down to next interaction target
  Pause at key content for 20 frames

Scene 5 — Transition         (12s–14s, frames 360–419)
  ScreenshotOverlay crossfades to Screen 2
  Step counter increments: "Step 2: [label]"

Scene 6 — Step 2a            (14s–18s, frames 420–539)
  AnimatedCursor: moves from top-left → target element
  Hotspot pulses → click → ripple
  Tooltip: action description
  ScreenshotOverlay: next state loads

Scene 7 — Zoom Reveal        (18s–21s, frames 540–629) [1 zoom per journey]
  ZoomReveal on most important result (confirmation screen, success state, key metric)
  highlightBox: true, highlightColor: brand.colors.accent
  Tooltip: outcome description ("Your dashboard is ready!")

Scene 8 — Screen 3           (21s–27s, frames 630–809) [if 3rd screen exists]
  [Repeat cursor + hotspot + click + tooltip pattern]

Scene 9 — CTA               (27s–31s, frames 810–929)
  Device frame fades out
  AnimatedText: CTA headline bounces in
  Accent pill: product URL / "Start free trial"
  BrandWatermark visible
```

**Pacing multipliers per step type:**
- `fast`: cursor travel = 1.5s, tooltip = 1s, scroll = 2s
- `medium`: cursor travel = 2s, tooltip = 1.5s, scroll = 3s (default)
- `slow`: cursor travel = 3s, tooltip = 2.5s, scroll = 4s

---

## Storyboard Generation Rules

### Step 1 — Parse the briefing

```
product_name   → explicit in briefing OR brand-voice.yaml → brand.name
journey_name   → explicit in briefing OR first journey in video-profile.yaml
device         → "mobile" / "phone" → MobileFrame
               → "browser" / "desktop" / default → BrowserFrame
pacing         → explicit in briefing → video-profile.yaml → style.pacing → "medium"
cta_text       → explicit in briefing → brand-voice.yaml → cta.default
zoom_on        → explicit "zoom on [screen/element]" → auto-select (see Step 4)
```

### Step 2 — Load journey

```
IF briefing specifies journey name:
  Find in video-profile.yaml journeys[] (case-insensitive, fuzzy match)
  IF not found: list available journeys, ask user to select

ELSE IF video-profile.yaml has one journey:
  Use it automatically

ELSE IF video-profile.yaml has multiple journeys:
  Ask: "Which journey should the walkthrough follow? [list names]"

ELSE (no journeys defined):
  Ask user to define steps inline (screen path + action + tooltip)
```

### Step 3 — Build WalkthroughStep list

For each `screen` in the selected journey:

```typescript
// Map each screen to a WalkthroughStep
{
  screenName: screen.name,
  screenshot: screen.screenshot,
  actions: screen.actions.map(action => mapActionToWalkthroughAction(action))
}
```

**Action string → WalkthroughAction mapping:**

| Action string pattern | type | target heuristic | tooltip |
|---|---|---|---|
| `clica [target]` / `click [target]` | `click` | element center heuristic | `"Click [target]"` |
| `clica em [target]` | `click` | element center heuristic | `"Click on [target]"` |
| `scroll até [section]` / `scroll to` | `scroll` | { x: 960, y: 540 } | `"Scroll to [section]"` |
| `digita [text]` / `type [text]` | `type` | input field heuristic | `"Type your [field]"` |
| `preenche [field]` / `fill [field]` | `type` | input field heuristic | `"Fill in [field]"` |
| `navega para [page]` / `navigate to` | `click` | nav link heuristic | `"Go to [page]"` |
| `hover em [element]` / `hover [element]` | `hover` | element center heuristic | `"Hover over [element]"` |
| `submit` / `confirma` / `save` | `click` | submit button heuristic | `"Confirm and continue"` |

**Target coordinate heuristics (1920×1080, browser frame, content area ~1760×900 offset 80,120):**

```
"Sign Up" / "Get Started" / "CTA button"  → { x: 960,  y: 500 }
"Login" / "Sign In"                        → { x: 960,  y: 420 }
"Email field"                              → { x: 760,  y: 380 }
"Password field"                           → { x: 760,  y: 460 }
"Submit" / "Continue" / "Next"             → { x: 960,  y: 600 }
"Navigation menu item" (generic)           → { x: 300,  y: 160 }
"Search bar"                               → { x: 760,  y: 180 }
"Profile / Avatar"                         → { x: 1750, y: 160 }
"Settings"                                 → { x: 1700, y: 160 }
"Dashboard / Home card"                    → { x: 480,  y: 520 }
"Sidebar item"                             → { x: 160,  y: 400 }
"Modal close"                              → { x: 1400, y: 300 }
"Dropdown option"                          → { x: 760,  y: 480 }
Fallback (unknown)                         → { x: 960,  y: 540 }
```

### Step 4 — Select zoom target

The walkthrough should have exactly **one** `ZoomReveal` scene. Placement rule:

```
IF briefing specifies "zoom on [screen/element]":
  Use that screen, estimate element coordinates
ELSE:
  Auto-select the screen with the most significant outcome:
    Priority 1: screen labeled "Dashboard", "Success", "Result", "Confirmation"
    Priority 2: last screen in the journey (final state)
    Priority 3: screen with action "zoom em" / "zoom on"

ZoomReveal target: { x: 600, y: 300, width: 720, height: 400 }  (center of content area)
zoomLevel: 2.0
highlightBox: true
highlightColor: brand.colors.accent
```

### Step 5 — Calculate total duration

```
hook_duration         = 3s
screen_intro_duration = 2s (for first screen only)
per_cursor_travel_s   = pacing_cursor[pacing]     (1.5 / 2.0 / 3.0)
per_hotspot_s         = 0.5 (always)
per_click_effect_s    = 0.3 (always)
per_tooltip_s         = pacing_tooltip[pacing]    (1.0 / 1.5 / 2.5)
per_scroll_action_s   = pacing_scroll[pacing]     (2.0 / 3.0 / 4.0)
per_type_action_s     = max(1.5, text.length × 0.08)
transition_s          = 1.5 (between screens)
zoom_reveal_s         = 3s (one per video)
cta_duration          = 4s

per_step_s = cursor_travel + hotspot + click_effect + tooltip (per action)
           + scroll (if action.type === 'scroll')
           + type_time (if action.type === 'type')

screen_section_s = screen_intro (screen 1 only) + sum(per_step_s for all actions)

total_s = hook + sum(screen_section_s) + transitions × (screens - 1) + zoom + cta

IF total_s < 30: extend tooltip durations by 1.5×, add intro text for each screen
IF total_s > 90: reduce tooltip durations to minimum, merge same-screen actions
```

### Step 6 — Output storyboard YAML

```yaml
# storyboard.yaml — App Walkthrough
showcase: AppWalkthrough
product: "[product_name]"
journey: "[journey_name]"
device: "[browser|mobile]"
pacing: "[fast|medium|slow]"
total_duration_s: [calculated]
step_count: [total action count across all screens]

scenes:
  - id: hook
    type: hook
    duration_s: 3
    text: "Here's how [product_name] works"
    subtext: "[journey_name or tagline]"
    animation: scale-in

  - id: screen-1-intro
    type: step
    duration_s: 2
    step:
      screenName: "[screen.name]"
      screenshot: "[screen.screenshot]"
      actions: []
    text: "Step 1: [screen.name]"
    animation: slide-up

  - id: step-1-1
    type: step
    duration_s: [calculated]
    step:
      screenName: "[screen.name]"
      screenshot: "[screen.screenshot]"
      actions:
        - type: "[click|scroll|hover|type]"
          target: { x: [N], y: [N] }
          tooltip: "[tooltip text]"
          duration: [frames]
    # next_screenshot for crossfade after click
    next_screenshot: "[next state screenshot if available]"

  - id: transition-1-2
    type: transition
    duration_s: 1.5
    text: "Step 2: [next screen name]"
    animation: crossfade

  - id: step-2-1
    type: step
    duration_s: [calculated]
    step:
      screenName: "[screen 2 name]"
      screenshot: "[screen 2 screenshot]"
      actions:
        - type: click
          target: { x: [N], y: [N] }
          tooltip: "[tooltip text]"
          duration: [frames]

  - id: zoom-reveal
    type: step
    duration_s: 3
    step:
      screenName: "[result screen name]"
      screenshot: "[result screenshot]"
      actions: []
    zoom:
      target: { x: 600, y: 300, width: 720, height: 400 }
      zoomLevel: 2.0
      highlightBox: true
    text: "[outcome description]"

  - id: cta
    type: cta
    duration_s: 4
    text: "[cta headline]"
    subtext: "[product URL or 'Start free trial']"
    animation: bounce
```

---

## Composition Mapping

Convert storyboard to Remotion props for the `AppWalkthrough` composition:

### Frame calculation

```
scene.duration_s × 30 = scene.durationFrames
startFrame[N] = sum of durationFrames[0..N-1]
```

### Props object structure

```typescript
// AppWalkthroughProps (from types.ts)
{
  brand: {
    name: "[product_name]",
    handle: brand_voice.brand.handle,
    colors: {
      primary:    design_tokens.primary_color,
      secondary:  design_tokens.secondary_color,
      background: "#0F0F1A",
      text:       "#FFFFFF",
      accent:     design_tokens.accent_color,
    },
    watermark_position: "bottom-right",
  },
  deviceType: "[browser|mobile]",
  deviceConfig: {
    browser: "chrome",
    device: "iphone15",
    darkMode: true,
  },
  showProgressBar: true,
  showWatermark: true,
  scenes: [
    // hook
    {
      type: "hook",
      startFrame: 0,
      durationFrames: 90,
      text: "Here's how [product] works",
      subtext: "[journey name or tagline]",
      animation: "scale-in",
    },
    // step scenes (one per action, or grouped by screen)
    {
      type: "step",
      startFrame: [N],
      durationFrames: [N],
      text: "Step [N]: [screen name]",
      step: {
        screenName: "[screen name]",
        screenshot: "[path/to/screenshot.png]",
        actions: [
          {
            type: "click",
            target: { x: 960, y: 500 },
            tooltip: "Click 'Get Started' to begin",
            duration: 60,   // frames for this action
          },
        ],
      },
    },
    // transition
    {
      type: "transition",
      startFrame: [N],
      durationFrames: 45,
      text: "Step [N]: [next screen name]",
      animation: "wipe",
    },
    // zoom (one per video)
    {
      type: "step",
      startFrame: [N],
      durationFrames: 90,
      text: "[outcome description]",
      step: {
        screenName: "[result screen]",
        screenshot: "[result screenshot path]",
        actions: [],   // no cursor for zoom scene
      },
    },
    // cta
    {
      type: "cta",
      startFrame: [N],
      durationFrames: 120,
      text: "[cta headline]",
      subtext: "[URL or trial text]",
      animation: "bounce",
    },
  ],
}
```

### Cursor path interpolation between steps

When building `AnimatedCursorProps.path` for each action, the cursor's starting position is the previous action's `target`. For the first action, start from screen center `{ x: 960, y: 540 }`.

```
path[0] = previous_target  (or {x: 960, y: 540} for first action)
path[1] = current action.target with action: "move"  (intermediate point if needed)
path[2] = current action.target with action: "click" / "hover"
```

Add intermediate path points for long diagonal travel (distance > 400px):
```
midpoint = { x: (start.x + end.x) / 2, y: start.y, action: "move", delay: 5 }
```

---

## Config Reading

### From video-profile.yaml

| Field | Used for |
|---|---|
| `design_tokens.primary_color` | `brand.colors.primary`, BrowserFrame bar |
| `design_tokens.accent_color` | Hotspot color, ProgressBar, CTA pill, ZoomReveal highlight |
| `design_tokens.heading_font` | step label font-family |
| `assets.screenshots_dir` | prepended to all screenshot paths |
| `assets.logo_path` | hook scene overlay if present |
| `device_frames[]` | validate device choice |
| `journeys[*]` | source of all screens, screenshots, actions |
| `style.pacing` | cursor/tooltip/scroll duration multipliers |
| `style.theme` | background and frame color strategy |

### From brand-voice.yaml

| Field | Used for |
|---|---|
| `brand.name` | product_name fallback, hook text |
| `brand.handle` | `brand.handle` in watermark |
| `brand.tagline` | hook subtext fallback |
| `cta.default` | CTA text fallback |
| `automation.autonomy` | output bundle level (manual/semi/auto) |

### Briefing overrides (highest priority)

Any explicit value in the user's briefing (journey name, device, pacing, CTA text, zoom target, specific step tooltip text) takes precedence over both YAML files.

---

## Render Command

After generating the composition props, return to the orchestrator with:

```yaml
composition_id: AppWalkthrough
props: { ...AppWalkthroughProps JSON... }
```

The orchestrator renders using the discovered Remotion CLI:

```bash
cd "${REMOTION_PROJECT}" && npx remotion render src/index.ts AppWalkthrough "${OUTPUT_DIR}/video.mp4" \
  --props='{"brand":{...},"scenes":[...],"deviceType":"browser"}' \
  --fps=30
```

For multi-platform (auto autonomy), the orchestrator also runs a 9:16 variant for social:
```bash
npx remotion render src/index.ts AppWalkthrough "${OUTPUT_DIR}/video-9x16.mp4" \
  --width=1080 --height=1920 --props='...' --fps=30
```

---

## Briefing Collection UI

When the orchestrator routes here, display this briefing prompt:

```
APP WALKTHROUGH SHOWCASE
─────────────────────────────────────────────────────────
I'll create a step-by-step guided tour of your product
with cursor navigation, hotspot pulses, and tooltip labels.

  Product name:
  > [e.g. "GrowthOS" or leave blank to use brand-voice.yaml]

  Journey to walk through (from video-profile.yaml):
  [list available journey names]
  > [select by name or number, or type "custom" to define steps]

  Device frame: [browser / mobile]  (default: browser)
  >

  CTA text (optional):
  > [e.g. "Start free at growthOS.app"]

  Pacing: [fast / medium / slow]  (default: medium)
  >

  Zoom focus (optional — which screen to zoom into):
  > [e.g. "dashboard" or "confirmation screen" or leave blank for auto]
─────────────────────────────────────────────────────────
```

If user selects "custom", collect steps inline:

```
CUSTOM STEPS — Define your walkthrough

  Step 1:
    Screenshot path: > [e.g. assets/screenshots/home.png]
    Screen name:     > [e.g. "Landing Page"]
    Actions (one per line, blank to finish):
      > [e.g. "click Sign Up" or "scroll to pricing"]
      > [e.g. "click Get Started"]
      >

  Add another screen? [y/n] >
```

Repeat until user types `n`. Minimum 2 screens required for a walkthrough (otherwise recommend `showcase-product-demo` instead).

---

## Error Handling

| Error condition | Response |
|---|---|
| Journey not found in video-profile.yaml | List available journeys, offer to define inline |
| Journey has only 1 screen | Warn: "Walkthroughs work best with 2+ screens. Use Product Demo for single-screen videos?" |
| Screenshot file missing | Warn with path, use gray placeholder, list all missing paths at end |
| No actions defined for a screen | Add a default "scroll to bottom" action for that screen |
| Total duration < 25s | Extend tooltip durations, add step-label intro for each screen |
| Total duration > 95s | Ask user which screens to cut, or merge actions into fewer steps |
| More than 8 screens | Warn "8+ screens may make the video too long", suggest splitting into 2 videos |
| Cursor coordinates out of frame | Clamp to (80–1840, 120–1020) content area bounds |
| device not in video-profile.yaml device_frames | Warn, proceed with requested device |

---

## Output

Return to orchestrator:

```yaml
status: ready
composition_id: AppWalkthrough
storyboard_path: "[OUTPUT_DIR]/storyboard.md"
props: { ...AppWalkthroughProps JSON... }
estimated_duration_s: [N]
screen_count: [N]
step_count: [total actions]
zoom_screen: "[name of zoomed screen]"
```

The orchestrator handles the render call, thumbnail, captions, and output bundle.
