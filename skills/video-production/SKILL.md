---
name: video-production
description: Video content expertise — scripts (YouTube format), descriptions, thumbnail concepts (text specs for sharp/SVG), storyboarding, video SEO (tags, chapters), hook-first methodology, and retention patterns. Use when producing any video-related content or strategy.
---

# Video Production Skill

Text-based video production expertise for YouTube and social video platforms. All outputs are text — no actual video/image generation.

## Core Methodology: Hook-First

Every video script follows the **hook-first** pattern:

1. **Hook** (0-5s): Pattern interrupt that stops the scroll. Must create curiosity gap or emotional trigger.
2. **Setup** (5-30s): Context + promise of value. State exactly what the viewer will learn/get.
3. **Body** (30s-end): Deliver value in clear segments with retention triggers every 60-90 seconds.
4. **CTA** (final 15s): Single clear action. Never stack multiple CTAs.

### Retention Triggers

Insert one every 60-90 seconds to prevent drop-off:

- **Pattern interrupt**: Change visual pace, topic shift, "but here's where it gets interesting"
- **Open loop**: Tease upcoming content: "I'll show you the exact template in a moment"
- **Social proof**: Quick data point or result
- **Direct address**: "Now you might be thinking..." — acknowledge viewer's mental state
- **B-roll cue**: `[CUT TO: screen recording / example / diagram]`

## Script Writing Format

```markdown
# [VIDEO TITLE — YouTube optimized, <60 chars]

**Target length:** [X] minutes
**Audience:** [specific viewer persona]
**Core promise:** [single sentence — what viewer gets]

---

## HOOK (0:00 - 0:05)

[TALKING HEAD]
"[Pattern interrupt — question, bold statement, or surprising fact]"

## SETUP (0:05 - 0:30)

[TALKING HEAD + B-ROLL]
"[Context. What this video covers. Why it matters NOW.]"

**Retention checkpoint:** [open loop for upcoming content]

## SECTION 1: [Topic] (0:30 - X:XX)

[SCREEN RECORDING / B-ROLL]
"[Teaching content with specific, actionable steps]"

**Key point:** [One-sentence takeaway]

[Repeat sections as needed]

## CTA (X:XX - end)

[TALKING HEAD]
"[Single action: subscribe, link in description, comment]"

---

### SEO Metadata
- **Title:** [<60 chars, front-load keyword]
- **Description:** [see description template below]
- **Tags:** [10-15 relevant tags]
- **Chapters:** [timestamp markers from sections]
```

## YouTube Description Template

```markdown
[Hook sentence — repeat the core promise from the video]

In this video, I [action verb — show/teach/reveal/break down] [specific topic].

🔗 Resources mentioned:
- [Resource 1]: [URL]
- [Resource 2]: [URL]

⏱️ Chapters:
0:00 — [Hook/Intro]
0:30 — [Section 1 title]
X:XX — [Section 2 title]
[...]

📌 Key takeaways:
• [Takeaway 1]
• [Takeaway 2]
• [Takeaway 3]

[CTA paragraph — what to do next, related videos]

#[tag1] #[tag2] #[tag3]
```

## Thumbnail Concept Spec

Thumbnails are described as text specs for sharp/SVG generation. Never attempt to generate actual images.

```yaml
thumbnail:
  layout: [split | centered | thirds | before-after]
  dimensions: "1280x720"
  background:
    type: [solid | gradient | image-blur]
    value: "[color hex or gradient spec]"
  text:
    headline: "[3-5 words MAX — large, readable at mobile size]"
    font_weight: bold
    font_size: "~120px equivalent"
    color: "[high contrast against background]"
    position: [left | center | right]
    stroke: "[optional outline color for readability]"
  face:
    expression: "[emotion: surprise, excitement, curiosity, shock]"
    position: [left | right]
    size: "[head + shoulders, ~40% of frame]"
  accent_elements:
    - type: [arrow | circle | emoji | icon]
      position: "[x, y quadrant]"
      color: "[brand accent color]"
  contrast_score: "[high | medium — must be high for mobile feeds]"
  text_readability: "[mobile-first — readable at 100px thumbnail width]"
```

### Thumbnail Best Practices

- **3-word rule**: Headline text should be 3-5 words maximum
- **Face + emotion**: Human faces with exaggerated expressions increase CTR 30-40%
- **High contrast**: Must be readable as a 100px-wide thumbnail on mobile
- **No clickbait**: Thumbnail must honestly represent video content
- **Brand consistency**: Use recurring color palette across video series
- **A/B variants**: Always produce 2 thumbnail concepts for testing

## Video SEO

### Tags Strategy

```yaml
tags:
  primary: "[exact target keyword]"
  secondary:
    - "[keyword variation 1]"
    - "[keyword variation 2]"
    - "[related topic 1]"
  long_tail:
    - "[question-format keyword]"
    - "[how-to format keyword]"
  brand:
    - "[channel name]"
    - "[series name if applicable]"
  total: 10-15  # sweet spot for YouTube
```

### Chapter Markers

- First chapter MUST start at `0:00`
- Minimum 3 chapters for YouTube to display them
- Each chapter title: concise, keyword-rich, <40 chars
- Chapters appear in Google search results — optimize for search intent

### YouTube Algorithm Signals

| Signal | Weight | How to Optimize |
|--------|--------|-----------------|
| Click-through rate (CTR) | Very High | Thumbnail + title testing |
| Watch time | Very High | Hook-first + retention triggers |
| Session time | High | End screens + playlists |
| Engagement (likes/comments) | Medium | Ask specific questions in CTA |
| Upload consistency | Medium | Regular schedule |
| Subscriber conversion | Medium | Value-first CTA placement |

## Storyboarding

```yaml
storyboard:
  scene_number: [N]
  timestamp: "[start - end]"
  visual:
    type: [talking-head | screen-recording | b-roll | animation | text-overlay]
    description: "[what viewer sees]"
  audio:
    narration: "[script text for this segment]"
    music: "[mood: upbeat, chill, dramatic, none]"
    sfx: "[sound effect if any]"
  text_overlay: "[on-screen text, lower-thirds, callouts]"
  transition: "[cut | fade | zoom | swipe]"
  retention_device: "[hook | open-loop | proof | direct-address | none]"
  notes: "[production notes, emphasis points]"
```

## Output Types

| Output | Format | Use Case |
|--------|--------|----------|
| Video script | Markdown | Full production script |
| YouTube description | Markdown | Video description + SEO |
| Thumbnail spec | YAML | Spec for sharp/SVG rendering |
| Storyboard | YAML | Scene-by-scene production plan |
| Tags list | YAML | YouTube tag optimization |
| Chapter markers | Markdown | YouTube chapters |

## Anti-Patterns

- Starting with "Hey guys, welcome back" — hook first, intro later
- Stacking multiple CTAs — one CTA per video
- Ignoring mobile thumbnail readability
- Generic tags like "tutorial" or "how to"
- Description with only links, no searchable text
- Chapters without `0:00` start marker
- Scripts without retention triggers in long-form content

---

## Integration with Remotion Rendering

This skill produces **text-based** storyboards and scripts. To convert a storyboard into an actual MP4 video, hand off to the **remotion-video** skill and the **video-producer** agent, which handle:

1. **Storyboard → Composition mapping** (remotion-video skill)
2. **Remotion environment discovery** (auto-detects CLI, entry point, and deps on any machine)
3. **Render to MP4** (video-producer agent Phase 3)

**Handoff flow:**
```
video-production skill (this skill) → generates storyboard YAML
  ↓
remotion-video skill → maps to composition JSON (frame calculations, animations)
  ↓
video-producer agent → discovers Remotion CLI, renders MP4, opens video
```

The storyboard YAML format from this skill is compatible with the remotion-video composition mapping when these fields are present per scene: `type`, `duration` (seconds), `text`, `animation`, `transition`. The remotion-video skill calculates `startFrame` and `durationFrames` automatically.
