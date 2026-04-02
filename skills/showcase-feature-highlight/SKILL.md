---
name: showcase-feature-highlight
description: Feature Highlight showcase — zoom-in spotlight on a single key feature using hotspot pulses, glassmorphism cards, tooltips, and particle accents. Routed from remotion-pro orchestrator.
---

# Showcase: Feature Highlight

**Status: Stub — Full implementation in Wave 3**

This showcase is planned for Wave 3 development. The stub reserves the skill slot, documents the specification, and displays the correct response to users who request it.

---

## Overview

The Feature Highlight showcase creates a focused, cinematic spotlight on a single product feature. The full UI appears, a hotspot pulses to draw attention, the camera zooms into the feature area, a tooltip explains it, and the particle effect celebrates the reveal. Designed for feature release announcements, changelog updates, and "did you know?" content.

Best for: feature announcements, changelog videos, product updates, onboarding highlights, "tip of the week" content.

---

## Components Used

| Component | Purpose |
|---|---|
| `GlassmorphismCard` | Frames the feature name and description overlay |
| `ZoomReveal` | Cinematic zoom into the feature region |
| `Hotspot` | Pulsing ring/dot that draws attention to a UI element |
| `BrowserFrame` | Wraps the product screenshot in a browser chrome |
| `ParticleEffect` | Accent particles on the zoom reveal moment |
| `Tooltip` | Floating label explaining what the feature does |

---

## Scene Flow

```
Hook (2-3s)
  └── "Introducing [Feature Name]" headline
      GlassmorphismCard fades in with feature name
      
Screen Appears (2s)
  └── BrowserFrame slides in with full product screenshot
      Feature is visible but not yet highlighted
      
Hotspot Pulses (2-3s)
  └── Hotspot ring animates over the target UI element
      Pulsing draws viewer's eye to the exact location
      
Zoom (2-3s)
  └── ZoomReveal magnifies into the feature area
      ParticleEffect accents the zoom moment
      
Tooltip (3-4s)
  └── Tooltip floats in explaining the feature
      Key benefit statement in clear language
      
CTA (3-4s)
  └── Zoom out, GlassmorphismCard with CTA appears
      "Try it now" or "Available in [plan]"
```

**Total Duration:** 20–45 seconds

---

## Required Config

```yaml
# From video-profile.yaml or briefing
feature:
  name: "Smart Scheduling"
  tagline: "Book meetings without the back-and-forth"
  benefit: "Saves 3+ hours per week"

screenshot: "assets/screenshots/dashboard.png"
hotspot:
  x: 420          # pixel x from left
  y: 280          # pixel y from top
  radius: 40
  
zoom:
  target_x: 420
  target_y: 280
  zoom_factor: 2.5

tooltip_text: "Click to auto-schedule based on availability"

device_frame: browser | none
cta_text: "Available on all plans — try free"
primary_color: "#7C3AED"
accent_color: "#F59E0B"
```

---

## Stub Response

When a user requests this showcase, display:

```
✨  FEATURE HIGHLIGHT SHOWCASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This showcase is coming in Wave 3 of GrowthOS Remotion Pro.

What it will produce:
  • Full UI screenshot with browser frame
  • Pulsing hotspot drawing attention to the feature
  • Cinematic zoom-in with particle accent
  • Tooltip explanation of the feature benefit
  • Branded CTA closing sequence
  • Duration: 20–45 seconds

To be notified when this is ready, check the GrowthOS
changelog or watch the growthOS/remotion/ directory for updates.

In the meantime, you can use the existing remotion-video skill
for general Remotion composition work.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
