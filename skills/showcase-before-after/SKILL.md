---
name: showcase-before-after
description: Before/After UI showcase — split-screen wipe reveal comparing two product states, UI redesigns, or workflow improvements. Routed from remotion-pro orchestrator.
---

# Showcase: Before/After UI

**Status: Stub — Full implementation in Wave 3**

This showcase is planned for Wave 3 development. The stub reserves the skill slot, documents the specification, and displays the correct response to users who request it.

---

## Overview

The Before/After UI showcase creates a compelling comparison video that reveals a transformation using a split-screen wipe effect. Shows two states side-by-side or sequentially — old vs new, manual vs automated, before vs after your product. Ideal for redesigns, productivity gains, and transformation narratives.

Best for: UI redesigns, workflow comparisons, productivity improvements, A/B test results, product transformations.

---

## Components Used

| Component | Purpose |
|---|---|
| `SplitScreenWipe` | Animated wipe that reveals the "after" state from the "before" |
| `ScreenshotOverlay` | Layers and transitions between the two screen states |
| `BrowserFrame` | Optionally wraps both screens in browser frames |
| `AnimatedText` | Labels ("Before", "After"), stats, and result callouts |

---

## Scene Flow

```
Hook (2-3s)
  └── Problem statement or "before" label fades in

Before Screen (3-5s)
  └── "Before" screenshot appears in BrowserFrame
      AnimatedText labels it clearly
      
Wipe Reveal (2-3s)
  └── SplitScreenWipe sweeps across (left-to-right or center-out)
      Both states briefly visible simultaneously

After Screen (3-5s)
  └── "After" state revealed
      AnimatedText highlights key improvements
      
Result (2-3s)
  └── Stat or outcome callout (e.g., "60% faster")

CTA (3-4s)
  └── Branded CTA with product name or URL
```

**Total Duration:** 15–30 seconds

---

## Required Config

```yaml
# From video-profile.yaml or briefing
before:
  screenshot: "assets/screenshots/before.png"
  label: "Before"
  caption: "Manual process — 2 hours"

after:
  screenshot: "assets/screenshots/after.png"
  label: "After"
  caption: "With our tool — 5 minutes"

wipe_direction: left-to-right | right-to-left | center-out
result_stat: "95% time saved"
device_frame: browser | none
cta_text: "Start your free trial"
primary_color: "#7C3AED"
```

---

## Stub Response

When a user requests this showcase, display:

```
⚡  BEFORE/AFTER UI SHOWCASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This showcase is coming in Wave 3 of GrowthOS Remotion Pro.

What it will produce:
  • Split-screen wipe reveal comparison
  • Before and after screenshots with device frames
  • Result stat callout (e.g., "95% faster")
  • Branded CTA closing sequence
  • Duration: 15–30 seconds

To be notified when this is ready, check the GrowthOS
changelog or watch the growthOS/remotion/ directory for updates.

In the meantime, you can use the existing remotion-video skill
for general Remotion composition work.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
