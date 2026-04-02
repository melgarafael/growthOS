---
name: showcase-social-proof
description: Social Proof showcase — animated testimonial cards, stacked toast notifications, user counters, and particle celebration effects to build trust and credibility. Routed from remotion-pro orchestrator.
---

# Showcase: Social Proof

**Status: Stub — Full implementation in Wave 4**

This showcase is planned for Wave 4 development. The stub reserves the skill slot, documents the specification, and displays the correct response to users who request it.

---

## Overview

The Social Proof showcase builds trust and desire through a dynamic sequence of real-world validation signals. Toast notifications stack up to simulate live activity, testimonial cards enter with cinematic timing, a counter climbs to a milestone number, and a particle effect punctuates the achievement. Designed to create FOMO and social validation at scale.

Best for: SaaS products, marketplaces, communities, apps with user bases, launch campaigns, testimonial reels.

---

## Components Used

| Component | Purpose |
|---|---|
| `TestimonialCard` | Full testimonial with avatar, name, role, quote, and star rating |
| `ToastNotification` | Stacking "someone just signed up" or "new review" toast banners |
| `CounterUp` | Increments to a milestone number (users, reviews, revenue) |
| `ParticleEffect` | Celebratory particles that burst on milestone achievement |

---

## Scene Flow

```
Hook (2-3s)
  └── "Join thousands of happy users" or equivalent
      Logo or product name fades in

Toasts Stack (4-6s)
  └── ToastNotification slides in from edge — stacks 3-5 notifications
      Each shows a name, avatar, and action
      (e.g., "Maria S. just started a free trial")
      Toasts auto-dismiss to make room for new ones
      
Testimonials Enter (6-10s)
  └── TestimonialCard slides in with spring animation
      Multiple cards sequence (2-4 testimonials)
      Star ratings animate in
      
Counter (3-5s)
  └── CounterUp counts to milestone
      (e.g., "12,000+" users, "4.9 stars", "$2M revenue")
      ParticleEffect bursts on number lock
      
CTA (3-4s)
  └── "Join [counter] others" or social proof CTA
```

**Total Duration:** 20–40 seconds

---

## Required Config

```yaml
# From video-profile.yaml or briefing
hook_text: "Trusted by 12,000+ founders"

toasts:
  - name: "Maria S."
    avatar: "assets/avatars/maria.png"  # optional
    action: "just started a free trial"
    location: "São Paulo, BR"
  - name: "Alex R."
    action: "left a 5-star review"
    location: "New York, US"
  - name: "James K."
    action: "upgraded to Pro"
    location: "London, UK"

testimonials:
  - name: "Sarah Chen"
    role: "Founder, TechFlow"
    avatar: "assets/avatars/sarah.png"  # optional
    quote: "This tool cut our video production time by 80%."
    stars: 5
  - name: "Bruno Dias"
    role: "Marketing Lead, Onda"
    quote: "Melhor ferramenta de vídeo que já usei."
    stars: 5

milestone:
  value: 12000
  label: "happy users"
  prefix: ""
  suffix: "+"

cta_text: "Join them — start free today"
primary_color: "#7C3AED"
```

---

## Stub Response

When a user requests this showcase, display:

```
⭐  SOCIAL PROOF SHOWCASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This showcase is coming in Wave 4 of GrowthOS Remotion Pro.

What it will produce:
  • Live-activity toast notifications stacking up
  • Animated testimonial cards with star ratings
  • Milestone counter with particle celebration
  • Trust-building CTA closing sequence
  • Duration: 20–40 seconds

To be notified when this is ready, check the GrowthOS
changelog or watch the growthOS/remotion/ directory for updates.

In the meantime, you can use the existing remotion-video skill
for general Remotion composition work.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
