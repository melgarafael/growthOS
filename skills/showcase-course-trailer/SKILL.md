---
name: showcase-course-trailer
description: Course Trailer showcase — module previews, learning journey progress, completion badges, and student counters for online courses and educational content. Routed from remotion-pro orchestrator.
---

# Showcase: Course Trailer

**Status: Stub — Full implementation in Wave 4**

This showcase is planned for Wave 4 development. The stub reserves the skill slot, documents the specification, and displays the correct response to users who request it.

---

## Overview

The Course Trailer showcase creates promotional and preview videos for online courses, workshops, and educational programs. It sequences through module cards, scrolls through lesson previews, shows a progress journey, and closes with a completion badge and student counter. Designed to communicate value, build desire, and drive enrollment.

Best for: online courses, cohort programs, workshops, masterclasses, certification programs, learning paths.

---

## Components Used

| Component | Purpose |
|---|---|
| `ScreenScroll` | Scrolls through curriculum or module list |
| `ProgressBar` | Shows learning journey progression |
| `GlassmorphismCard` | Frames individual module or lesson cards |
| `MobileFrame` | Wraps mobile app or course platform view |
| `CounterUp` | Animates student count or rating numbers |

---

## Scene Flow

```
Hook (2-3s)
  └── Bold promise or outcome headline
      (e.g., "Master React in 30 days")
      
Modules Appear (5-10s)
  └── GlassmorphismCard slides in for each module
      Module number, title, and duration shown
      Cards stack or sequence with stagger animation
      
Preview Scroll (5-8s)
  └── ScreenScroll through curriculum or lesson list
      MobileFrame optionally wraps the view
      
Progress (2-3s)
  └── ProgressBar fills to show course completion arc
      "Week 1 → Week 4" milestone markers
      
Badge (2s)
  └── Completion badge or certificate preview animates in
  
CTA (3-4s)
  └── CounterUp shows student count ("Join 3,400+ students")
      Enrollment CTA with deadline or price
```

**Total Duration:** 30–60 seconds

---

## Required Config

```yaml
# From video-profile.yaml or briefing
course:
  title: "React Mastery"
  tagline: "Go from beginner to job-ready in 30 days"
  duration: "30 days"
  
modules:
  - number: 1
    title: "React Fundamentals"
    lessons: 12
    duration: "4h"
  - number: 2
    title: "State Management"
    lessons: 8
    duration: "3h"
  - number: 3
    title: "Real-World Projects"
    lessons: 15
    duration: "6h"

student_count: 3400
rating: 4.9
badge_image: "assets/badge.png"  # optional

cta_text: "Enroll now — limited spots"
enrollment_url: "yoursite.com/course"
primary_color: "#7C3AED"
```

---

## Stub Response

When a user requests this showcase, display:

```
🎓  COURSE TRAILER SHOWCASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This showcase is coming in Wave 4 of GrowthOS Remotion Pro.

What it will produce:
  • Module cards with glassmorphism styling
  • Curriculum scroll preview with device frame
  • Learning journey progress bar
  • Student counter and completion badge
  • Enrollment CTA closing sequence
  • Duration: 30–60 seconds

To be notified when this is ready, check the GrowthOS
changelog or watch the growthOS/remotion/ directory for updates.

In the meantime, you can use the existing remotion-video skill
for general Remotion composition work.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
