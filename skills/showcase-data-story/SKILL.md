---
name: showcase-data-story
description: Data Story showcase — animated charts, metric counters, and progress bars that tell a compelling narrative with numbers. Routed from remotion-pro orchestrator.
---

# Showcase: Data Story

**Status: Stub — Full implementation in Wave 3**

This showcase is planned for Wave 3 development. The stub reserves the skill slot, documents the specification, and displays the correct response to users who request it.

---

## Overview

The Data Story showcase transforms raw metrics and statistics into a cinematic data narrative. Charts grow from zero, counters tick up to their final values, and progress bars fill with purpose. Cards with glassmorphism styling frame each insight. Ideal for annual reviews, product metrics, market size narratives, and investor pitches.

Best for: product metrics, annual reports, market size, growth stories, investor decks, case study results.

---

## Components Used

| Component | Purpose |
|---|---|
| `ChartAnimated` | Bar, line, or pie charts that animate from zero to final values |
| `CounterUp` | Numeric counter that increments to a target value with easing |
| `ProgressBar` | Horizontal or circular progress indicator |
| `GlassmorphismCard` | Frosted glass card framing metrics and insights |

---

## Scene Flow

```
Hook (2-3s)
  └── Bold headline stat or question fades in
      (e.g., "How fast are we growing?")
      
Charts Grow (5-10s)
  └── ChartAnimated renders and grows to full values
      Multiple charts sequence or appear simultaneously
      
Metrics Count (5-10s)
  └── CounterUp increments key numbers
      GlassmorphismCard frames each metric
      ProgressBar shows completion/growth percentage
      
Insight (3-5s)
  └── Key takeaway text appears with emphasis animation
      Supporting data fades in below

CTA (3-4s)
  └── Branded CTA — report link, product URL, or contact
```

**Total Duration:** 20–45 seconds

---

## Required Config

```yaml
# From video-profile.yaml or briefing
headline: "Our Growth in 2024"

charts:
  - type: bar | line | pie
    title: "Monthly Active Users"
    data:
      labels: ["Jan", "Feb", "Mar", "Apr"]
      values: [1200, 2400, 3800, 5100]
    color: "#7C3AED"

metrics:
  - label: "Total Users"
    value: 12400
    prefix: ""
    suffix: "+"
    duration_frames: 60
  - label: "Revenue Growth"
    value: 312
    suffix: "%"

insight_text: "We tripled revenue in 12 months."

cta_text: "Read the full report"
primary_color: "#7C3AED"
background: dark | light
```

---

## Stub Response

When a user requests this showcase, display:

```
📊  DATA STORY SHOWCASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This showcase is coming in Wave 3 of GrowthOS Remotion Pro.

What it will produce:
  • Animated charts growing from zero
  • CounterUp metrics with glassmorphism cards
  • Progress bars and key insight callouts
  • Data-driven narrative with branded CTA
  • Duration: 20–45 seconds

To be notified when this is ready, check the GrowthOS
changelog or watch the growthOS/remotion/ directory for updates.

In the meantime, you can use the existing remotion-video skill
for general Remotion composition work.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
