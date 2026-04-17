# Visual Hierarchy — Eye Movement & Layout for Conversion

> **Purpose:** Every layout decision in a sales page must align with how humans actually scan and process visual information.
> **Key Insight:** Users don't read pages — they scan. Visual hierarchy determines what gets seen, in what order, and what gets ignored.

---

## Eye-Tracking Patterns

### F-Pattern

**Source:** Jakob Nielsen, Nielsen Norman Group, 2006 (replicated across 200+ studies through 2025).

Users scan text-heavy pages in an F-shape:

```
████████████████████████████        ← First horizontal scan (top)
████████████████████████████
████████████████                    ← Second horizontal scan (shorter)
████████████████
████                                ← Vertical scan down left side
████
████
████
████
```

**When it applies:**
- Text-heavy pages (blog posts, documentation, about pages)
- Pages with uniform visual weight (no strong focal points)
- Content pages without clear visual hierarchy

**Implications for sales pages:**
- Place the most important information in the first two lines
- Left-align key headlines and CTAs
- Use subheadings to create new "F-scan starting points"
- The F-pattern is a FAILURE state — good visual hierarchy prevents it

### Z-Pattern

**Source:** Gutenberg diagram studies + confirmed by eye-tracking for structured pages.

Users scan simple, image-focused pages in a Z-shape:

```
1 ─────────────────────→ 2          ← Top left → Top right (logo → CTA)
                        ╱
                      ╱
                    ╱                ← Diagonal scan
                  ╱
                ╱
3 ─────────────────────→ 4          ← Bottom left → Bottom right (content → CTA)
```

**When it applies:**
- Landing pages with clear visual structure
- Pages with hero + content + CTA layout
- Pages designed with deliberate visual hierarchy

**Implications for sales pages:**
- **Position 1 (top-left):** Logo or brand identifier
- **Position 2 (top-right):** Primary navigation or secondary CTA
- **Diagonal:** Core message — headline, key visual, value proposition
- **Position 3 (bottom-left):** Supporting content, features
- **Position 4 (bottom-right):** Primary CTA — the terminal fixation point

### Gutenberg Diagram

For balanced, evenly-weighted layouts:

```
┌──────────────────┬──────────────────┐
│                  │                  │
│  PRIMARY         │  STRONG          │
│  OPTICAL AREA    │  FALLOW AREA     │
│  (high attention)│  (some attention)│
│                  │                  │
├──────────────────┼──────────────────┤
│                  │                  │
│  WEAK            │  TERMINAL        │
│  FALLOW AREA     │  AREA            │
│  (low attention) │  (CTA goes here) │
│                  │                  │
└──────────────────┴──────────────────┘
```

**Implication:** The bottom-right is where the eye naturally comes to rest. Place your CTA there.

---

## Gestalt Principles Applied to Sales Pages

Gestalt psychology explains how the brain organizes visual information into meaningful groups. These principles are not optional — they're how human vision works.

### 1. Proximity

**Principle:** Elements placed close together are perceived as related.

**Sales page application:**
```
┌────────────────────────────┐
│  Feature Icon + Title      │ ← These are grouped because
│  Feature Description       │   they're close together
│                            │
│                            │ ← Gap separates from next feature
│                            │
│  Feature Icon + Title      │ ← New group
│  Feature Description       │
└────────────────────────────┘
```

**Rules:**
- Group related elements with ≤8px spacing
- Separate unrelated groups with ≥24px spacing
- The ratio between intra-group and inter-group spacing should be at least 1:3
- Feature cards, pricing tiers, testimonial blocks all use proximity

### 2. Similarity

**Principle:** Elements that look similar are perceived as part of the same group or system.

**Sales page application:**
- All CTA buttons have the same color, size, and style → user learns "that color = click"
- All feature icons have the same style → user perceives them as a coherent set
- All testimonial cards have the same layout → user recognizes the pattern

**Anti-pattern:** If your primary CTA is orange rounded, your secondary CTA should NOT be orange rounded in a different size. Use a ghost/outline variant.

### 3. Continuity

**Principle:** The eye follows smooth lines, curves, and implied directions.

**Sales page application:**
- Vertical scroll flow should guide the eye naturally from section to section
- Diagonal lines or gradients can guide the eye toward the CTA
- Progress indicators create a sense of movement through the page
- Section transitions should flow, not jump

### 4. Closure

**Principle:** The brain completes incomplete shapes and patterns.

**Sales page application:**
- Partially visible sections at the bottom of the viewport invite scrolling ("there's more below")
- Card layouts with subtle overflow suggest continuation
- Cropped images create curiosity

### 5. Figure-Ground

**Principle:** The brain separates elements into foreground (focus) and background (context).

**Sales page application:**
- Hero text MUST have sufficient contrast against the background image/video
- CTA buttons must visually "pop" from their surroundings
- Glassmorphism (blur + transparency) creates clear foreground/background separation
- Dark overlays on hero images ensure text readability

**Critical rule:** If your hero has a background image, use a dark overlay (70-90% opacity) or a solid background section for text. Text floating over complex imagery fails figure-ground separation.

### 6. Common Region

**Principle:** Elements within a shared boundary are perceived as grouped.

**Sales page application:**
- Cards, containers, and bordered sections create visual groups
- Pricing tiers in separate cards are compared as distinct options
- Testimonials in cards are perceived as individual stories
- Feature groups in bordered sections are perceived as categories

---

## Fitts's Law

**Principle:** The time to reach a target is a function of the distance to and size of the target.

```
T = a + b × log₂(1 + D/W)
Where: D = distance to target, W = width of target
```

### Implications for CTAs

| Factor | Rule | Minimum |
|--------|------|---------|
| Button height | Taller = easier to click | 44px (mobile), 36px (desktop) |
| Button width | Wider = easier to click | 120px or full-width on mobile |
| Touch target | Total tappable area including padding | 48×48px minimum (Google/Apple) |
| Distance from cursor | Closer to expected cursor position = faster | Place CTA in natural reading flow |

### Practical CTA Sizing

```css
.cta-primary {
  min-height: 48px;
  padding: 12px 32px;
  font-size: 16px;

  /* Mobile: full width for easy thumb reach */
  @media (max-width: 768px) {
    width: 100%;
    min-height: 52px;
    font-size: 18px;
  }
}
```

---

## Hick's Law

**Principle:** Decision time increases logarithmically with the number of choices.

```
T = b × log₂(n + 1)
Where: n = number of choices
```

### Implications for Sales Pages

| Element | Maximum Choices | Why |
|---------|----------------|-----|
| Pricing tiers | 3 (max 4 with enterprise) | 3 options can be compared quickly |
| CTAs per section | 1 primary + 1 secondary max | More = paralysis |
| Navigation links | 5-7 visible items | Beyond 7, scanning replaces reading |
| Feature categories | 3-4 groups | More groups = cognitive overload |
| Form fields | Minimum viable | Every field reduces completion rate by ~7% |

**Key rule for sales pages:** The page should present ONE primary action. Every section supports that one action. The reader should never wonder "what should I do here?"

---

## The Above-the-Fold Question

### The Myth

"Everything important must be above the fold."

### The Reality (Eye-Tracking Data)

- **People DO scroll.** ClickTale analysis (5M+ sessions): 76% of pages are scrolled some, 22% are scrolled to the bottom.
- **Attention doesn't end at the fold.** NNGroup: content just below the fold gets 84% of the attention of above-fold content.
- **BUT the hero matters most.** Users form their first impression in 50ms (Lindgaard et al., 2006). If the hero fails, they leave before scrolling.

### What Goes Above the Fold

| Element | Required | Why |
|---------|----------|-----|
| Headline | Yes | First impression. Must communicate core promise. |
| Subheadline | Yes | Expands on how the promise is delivered. |
| Primary CTA | Yes | For most-aware visitors who are ready to act. |
| Key visual | Strongly recommended | Product screenshot, hero image, or video. |
| Trust signal | Recommended | Logo bar or metric counter for instant credibility. |

### What Goes Below the Fold

Everything else — features, testimonials, objection handling, pricing, FAQ, guarantee. These sections are for visitors who need more convincing before they act.

**The scroll invitation:** Design the bottom of the viewport to show a partial next section — continuity (Gestalt) invites scrolling.

---

## Whitespace as Conversion Tool

### The Paradox

More whitespace = fewer elements visible = higher perceived quality = higher conversion.

### Research

| Study | Finding |
|-------|---------|
| Wichita State University (2004) | Increased margins around text improved comprehension by 20% |
| Crazy Egg (2019) | Pages with 40%+ whitespace had 20% higher engagement |
| Google Material Design | Minimum 16px padding between interactive elements |

### Types of Whitespace in Sales Pages

| Type | Purpose | Minimum |
|------|---------|---------|
| **Micro** (within components) | Readability, breathing room | 8-16px |
| **Meso** (between components) | Grouping, separation | 24-48px |
| **Macro** (between sections) | Pacing, premium feel | 64-120px |

### Whitespace Rules for Sales Pages

1. **Section padding:** Minimum 80px vertical padding per section (120px+ for premium).
2. **Content max-width:** 1200px container. Never fill the full viewport width.
3. **Text block max-width:** 65ch for body copy. Wider = harder to read.
4. **CTA breathing room:** Minimum 48px clear space around primary CTA buttons.
5. **Premium perception:** Whitespace signals "we don't need to fill every pixel to prove our value."

```css
/* Generous section spacing for premium feel */
.section {
  padding-block: clamp(4rem, 8vw, 8rem);  /* 64-128px */
}

/* Content containment */
.container {
  max-width: 1200px;
  margin-inline: auto;
  padding-inline: clamp(1rem, 4vw, 2rem); /* 16-32px */
}

/* Text measure */
.prose {
  max-width: 65ch;
}
```

---

## Scroll Depth and Section Placement

### Average Scroll Depth by Page Type

| Page Type | Average Scroll Depth | Implication |
|-----------|---------------------|-------------|
| Landing page (short) | 65-80% | Most visitors see pricing |
| Sales page (long) | 50-65% | Place primary CTA by 50% |
| Blog post | 40-55% | Place CTA early |
| Product page | 55-70% | Visual products get more scrolling |

### Section Placement Strategy

```
0%    ┌─ Hero: Promise + CTA ────────────────┐
      │  (must convert most-aware visitors)   │
10%   ├─ Logo bar / Trust ───────────────────┤
      │                                       │
20%   ├─ Problem / Features ─────────────────┤
      │  (build the case)                     │
35%   ├─ How it works / Solution ────────────┤
      │                                       │
45%   ├─ Social proof ───────────────────────┤
      │  (validate the case)                  │
55%   ├─ Second CTA ─────────────────────────┤  ← Critical placement
      │  (catch the 50% dropout zone)         │
65%   ├─ Objection handling ─────────────────┤
      │                                       │
75%   ├─ Pricing ────────────────────────────┤
      │                                       │
85%   ├─ Guarantee + FAQ ────────────────────┤
      │                                       │
95%   ├─ Final CTA ──────────────────────────┤
100%  └─ Footer ─────────────────────────────┘
```

**Rule:** Never place more than 2 full scroll-lengths (2 viewports) between CTAs. If a visitor is ready to buy at 35%, they shouldn't have to scroll to 75% to find the button.

---

## Sources

- Nielsen, Jakob. [F-Shaped Pattern for Reading Web Content](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/). NNGroup, 2006.
- 99designs: [Using F and Z patterns to create visual hierarchy](https://99designs.com/blog/tips/visual-hierarchy-landing-page-designs/)
- IxDF: [Visual Hierarchy: Organizing content to follow natural eye movement patterns](https://ixdf.org/literature/article/visual-hierarchy-organizing-content-to-follow-natural-eye-movement-patterns)
- Ramotion: [Visual Hierarchy: Principles & How to Design](https://www.ramotion.com/blog/visual-hierarchy/)
- Parallel HQ: [Improving Visual Hierarchy: Techniques Guide (2026)](https://www.parallelhq.com/blog/what-can-be-used-to-improve-visual-hierarchy)
- MasterClass: [Visual Hierarchy in Design: 9 Principles (2026)](https://www.masterclass.com/articles/visual-hierarchy)
- Lindgaard, G., et al. "Attention web designers: You have 50 milliseconds to make a good first impression!" *Behaviour & Information Technology*, 2006.
- Fitts, Paul M. "The information capacity of the human motor system." *Journal of Experimental Psychology*, 1954.
