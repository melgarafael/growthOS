# Design Intelligence Base — Master Index

> **Status:** Active — Growing with every project
> **Purpose:** Every design decision in the Sales Page System traces to a reference in this base.
> **Rule:** Read DESIGN-DOCTRINE.md before making any visual decision. No exceptions.

---

## Core Documents (MANDATORY reads)

| Document | Path | Purpose |
|----------|------|---------|
| **DESIGN-DOCTRINE** | `DESIGN-DOCTRINE.md` | Master visual rules, 7 archetypes, tokens |
| **AI-SLOP** | `anti-patterns/AI-SLOP.md` | What NEVER to do (3-tier system) |
| **STYLE-PROFILE** | `approved/STYLE-PROFILE.md` | User visual preferences (RLHF) |
| **APPROVED** | `approved/APPROVED-DESIGNS.md` | Designs with positive reinforcement |
| **REJECTED** | `anti-patterns/REJECTED-DESIGNS.md` | Designs with negative reinforcement |

---

## Reference Sites

Detailed analysis of elite landing pages. Each file documents: visual identity, key techniques, what makes it work, patterns to extract, code snippets, anti-patterns to avoid.

| Site | File | Category | Key Technique |
|------|------|----------|---------------|
| Stripe | `references/sites/stripe.md` | SaaS | Mesh gradient WebGL, CSS 3D, diagonal layout |
| Linear | `references/sites/linear.md` | SaaS | Dark-mode, glassmorphism, 8px scale |
| Apple iPhone | `references/sites/apple-iphone.md` | Consumer | Canvas frame sequence, pinned scroll |
| CodeWiki Google | `references/sites/codewiki-google.md` | Developer | Material Design 3, radial gradients |
| Arc Browser | `references/sites/arc-browser.md` | Productivity | Emotional LP, video loops, poetic copy |
| Figma | `references/sites/figma.md` | Design Tool | Interactive product demo in-page |
| Superhuman | `references/sites/superhuman.md` | Productivity | Elitist positioning, speed-as-brand |
| Notion | `references/sites/notion.md` | Productivity | Custom illustrations, friendly tone |
| n8n | `references/sites/n8n.md` | Developer | Workflow visualization, open-source |
| 11x.ai | `references/sites/11x-ai.md` | AI | AI-native positioning, agent narrative |
| Cal.com | `references/sites/cal-com.md` | Developer | Open-source clean, strong social proof |

---

## Design Patterns

Reusable patterns cataloged with when-to-use rules, CSS snippets, and reference site examples.

| Pattern | File | Sections Covered |
|---------|------|-----------------|
| Hero Sections | `references/patterns/hero-sections.md` | 6+ hero variants |
| Social Proof | `references/patterns/social-proof-layouts.md` | Logo walls, testimonials, metrics |
| CTA Patterns | `references/patterns/cta-patterns.md` | Button styles, placement, urgency |
| Pricing Sections | `references/patterns/pricing-sections.md` | Tables, toggles, enterprise CTA |
| Scroll Animations | `references/patterns/scroll-animations.md` | CSS scroll-driven, canvas, parallax |
| Objection Handling | `references/patterns/objection-handling.md` | FAQ, guarantee, comparison |

---

## Implementation Techniques

Detailed implementation guides with working code.

| Technique | File | Complexity |
|-----------|------|-----------|
| Canvas Frame Sequence | `references/techniques/canvas-frame-sequence.md` | High — Apple-style scroll video |
| Mesh Gradient | `references/techniques/mesh-gradient-webgl.md` | High — Stripe-style animated gradient |
| Fluid Math Positioning | `references/techniques/fluid-math-positioning.md` | Medium — Utopia + Every Layout |
| Glassmorphism | `references/techniques/glassmorphism.md` | Low — backdrop-filter + borders |
| Micro-interactions | `references/techniques/micro-interactions.md` | Low — hover, focus, transitions |

---

## Theory (Psychological Foundations)

Research-backed principles that justify design decisions.

| Theory | File | Application |
|--------|------|-------------|
| Ogilvy Principles | `theory/ogilvy-principles.md` | Layout order, headline rules, copy length |
| Conversion Psychology | `theory/conversion-psychology.md` | Cialdini, cognitive biases, anchoring |
| Color Psychology | `theory/color-psychology.md` | Color → emotion → purchase behavior |
| Typography & Emotion | `theory/typography-emotion.md` | Font → brand perception mapping |
| Visual Hierarchy | `theory/visual-hierarchy.md` | F/Z-pattern, Gestalt, eye direction |

---

## How to Add New References

1. Create a file following the schema in the relevant directory
2. Add an entry to this INDEX.md
3. Reference it in your design decisions with a traceable citation

## Statistics

- Total reference sites: 11
- Total patterns: 6
- Total techniques: 5
- Total theory files: 5
- Total files in base: 32+
