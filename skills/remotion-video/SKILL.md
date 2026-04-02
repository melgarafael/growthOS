---
name: remotion-video
description: Remotion video composition knowledge — 6 template specs, storyboard-to-composition mapping, frame calculations, animation catalog, transition types, platform rules, retention triggers, and anti-patterns for video production
---

# Remotion Video Skill

Specialized knowledge base for mapping creative video concepts to Remotion compositions. Covers template selection, storyboard-to-composition translation, timing and pacing rules, animation and transition catalogs, platform-specific constraints, brand integration, retention psychology, and anti-patterns. This skill is consumed by the video-producer agent and integrates with the copywriting, video-production, and platform-mastery skills.

---

## Trigger Conditions

Use this skill when the user asks to:
- Create a video, reel, short, or explainer
- Produce an animated carousel from existing slide content
- Map a storyboard to a Remotion composition
- Select the right video template for a given topic
- Calculate frame timing for video scenes
- Choose animations or transitions for video content
- Optimize video pacing for retention
- Convert carousel slides into animated video format
- Render a video using Remotion
- Review or improve an existing video storyboard

---

## Template Registry

Six composition templates are available, each with specific constraints and scene flow patterns.

### 1. ReelTips

| Property | Value |
|----------|-------|
| Aspect Ratio | 9:16 (1080x1920) |
| FPS | 30 |
| Duration Range | 15-60 seconds (450-1800 frames) |
| Scene Flow | hook(3s) > points(5s each) > CTA(4s) |
| Background | Dark gradient with accent color from brand |
| Default Animations | fade-in + scale-in for hook, alternating slide-left/right for points, bounce for CTA |
| Best For | Quick tips, lists, how-tos, hacks |

**Props Schema:**
```typescript
{
  template: "ReelTips",
  fps: 30,
  width: 1080,
  height: 1920,
  brand: BrandProps,
  scenes: SceneProps[],  // types: hook, point, cta
  showProgressBar: boolean,
  showWatermark: boolean
}
```

### 2. ReelBeforeAfter

| Property | Value |
|----------|-------|
| Aspect Ratio | 9:16 (1080x1920) |
| FPS | 30 |
| Duration Range | 15-30 seconds (450-900 frames) |
| Scene Flow | hook(3s) > comparisons(6s each) > reveal(4s) > CTA(3s) |
| Background | Split dark/light for before/after contrast |
| Default Animations | wipe transitions for comparisons, slide for reveal |
| Best For | Transformations, comparisons, results, upgrades |

**Props Schema:**
```typescript
{
  template: "ReelBeforeAfter",
  fps: 30,
  width: 1080,
  height: 1920,
  brand: BrandProps,
  scenes: SceneProps[],  // types: hook, comparison, point, cta
  showProgressBar: boolean,
  showWatermark: boolean
}
```

### 3. ReelNumbers

| Property | Value |
|----------|-------|
| Aspect Ratio | 9:16 (1080x1920) |
| FPS | 30 |
| Duration Range | 15-30 seconds (450-900 frames) |
| Scene Flow | hook(3s) > number+context(5s each) > insight(5s) > CTA(3s) |
| Background | Solid dark with accent-colored number highlights |
| Default Animations | counter-up for numbers, fade for context text |
| Best For | Statistics, data points, metrics, growth numbers |

**Props Schema:**
```typescript
{
  template: "ReelNumbers",
  fps: 30,
  width: 1080,
  height: 1920,
  brand: BrandProps,
  scenes: SceneProps[],  // types: hook, number, point, cta
  showProgressBar: boolean,
  showWatermark: boolean
}
```

### 4. ExplainerSteps

| Property | Value |
|----------|-------|
| Aspect Ratio | 16:9 (1920x1080) |
| FPS | 30 |
| Duration Range | 60-180 seconds (1800-5400 frames) |
| Scene Flow | intro(5s) > steps(15s each) > summary grid(10s) > CTA(5s) |
| Background | Clean light or branded gradient |
| Default Animations | slide-up for steps, scale-in for summary |
| Best For | Tutorials, how-to guides, processes, setup guides |

**Props Schema:**
```typescript
{
  template: "ExplainerSteps",
  fps: 30,
  width: 1920,
  height: 1080,
  brand: BrandProps,
  scenes: SceneProps[],  // types: hook, step, point, cta
  showProgressBar: boolean,
  showWatermark: boolean
}
```

### 5. ExplainerDemo

| Property | Value |
|----------|-------|
| Aspect Ratio | 16:9 (1920x1080) |
| FPS | 30 |
| Duration Range | 30-120 seconds (900-3600 frames) |
| Scene Flow | problem(5s) > solution intro(5s) > features(15s each) > social proof(10s) > CTA(5s) |
| Background | Branded gradient or solid |
| Default Animations | fade transitions, scale for features |
| Best For | Product demos, feature showcases, SaaS walkthroughs |

**Props Schema:**
```typescript
{
  template: "ExplainerDemo",
  fps: 30,
  width: 1920,
  height: 1080,
  brand: BrandProps,
  scenes: SceneProps[],  // types: hook, point, demo, cta
  showProgressBar: boolean,
  showWatermark: boolean
}
```

### 6. CarouselAnimated

| Property | Value |
|----------|-------|
| Aspect Ratio | 4:5 (1080x1350) |
| FPS | 30 |
| Duration Range | 15-60 seconds (450-1800 frames) |
| Scene Flow | cover(4s) > content slides(4s each) > CTA(4s) |
| Background | Inherits from carousel design spec or brand palette |
| Default Animations | slide-left transitions between slides |
| Best For | Animated versions of existing carousel content |

**Props Schema:**
```typescript
{
  template: "CarouselAnimated",
  fps: 30,
  width: 1080,
  height: 1350,
  brand: BrandProps,
  scenes: SceneProps[],  // types: hook, point, cta
  showProgressBar: boolean,
  showWatermark: boolean
}
```

---

## Storyboard-to-Composition Mapping

### Mapping Rules

The storyboard YAML produced by the video-producer agent must be translated into a Remotion composition JSON. Follow these rules exactly.

#### Scene Type Mapping

| Storyboard Scene Type | Remotion SceneProps.type | Typical Animation | Notes |
|----------------------|-------------------------|-------------------|-------|
| `hook` | `"hook"` | fade-in, scale-in | Always first scene. Must fire immediately. |
| `point` | `"point"` | slide-left, slide-right | Content scenes. Alternate directions for pattern interrupt. |
| `comparison` | `"comparison"` | wipe, slide-left | Before/after pairs. Use wipe for dramatic reveal. |
| `number` | `"number"` | counter-up | Numbers animate from 0 to target value. |
| `step` | `"step"` | slide-up, fade-in | Tutorial steps. Numbered prominently. |
| `demo` | `"demo"` | scale-in, fade-in | Product feature highlights. |
| `cta` | `"cta"` | bounce, scale-in | Always last scene. Brand handle visible. |

#### Frame Calculation

```
For each scene in storyboard.scenes:
  scene.durationFrames = scene.duration * storyboard.fps
  scene.startFrame = sum of all previous scenes' durationFrames

Total composition frames:
  totalFrames = sum of all scene durationFrames
```

**Example calculation (30fps):**
```
Scene 1 (hook, 3s):     startFrame=0,    durationFrames=90
Scene 2 (point, 5s):    startFrame=90,   durationFrames=150
Scene 3 (point, 5s):    startFrame=240,  durationFrames=150
Scene 4 (point, 5s):    startFrame=390,  durationFrames=150
Scene 5 (cta, 4s):      startFrame=540,  durationFrames=120
Total:                   totalFrames=660  (22 seconds)
```

#### Brand Injection

Map brand-voice.yaml colors to Remotion BrandProps:

```yaml
# Input: brand-voice.yaml
visual_identity:
  colors:
    primary: "#6c5ce7"
    secondary: "#00cec9"
    background: "#0a0a0a"
    text: "#ffffff"
    accent: "#fd79a8"
  handle: "@myhandle"
  name: "My Brand"

# Output: BrandProps
brand:
  name: "My Brand"
  handle: "@myhandle"
  colors:
    primary: "#6c5ce7"
    secondary: "#00cec9"
    background: "#0a0a0a"
    text: "#ffffff"
    accent: "#fd79a8"
  watermark_position: "bottom-right"
```

#### Composition Assembly

```json
{
  "template": "<from storyboard.template>",
  "fps": 30,
  "width": "<from template spec>",
  "height": "<from template spec>",
  "totalFrames": "<calculated sum>",
  "brand": "<BrandProps from brand-voice.yaml>",
  "scenes": [
    {
      "type": "<mapped scene type>",
      "startFrame": "<calculated>",
      "durationFrames": "<scene.duration * fps>",
      "text": "<from storyboard scene>",
      "subtext": "<from storyboard scene, optional>",
      "icon": "<from storyboard scene, optional>",
      "animation": "<from storyboard scene>",
      "transition": "<from storyboard scene, default crossfade>"
    }
  ],
  "showProgressBar": true,
  "showWatermark": true
}
```

---

## Timing and Pacing

### Duration Rules by Scene Type

| Scene Type | Minimum | Recommended | Maximum | Notes |
|-----------|---------|-------------|---------|-------|
| `hook` | 1.5s | 2-3s | 3s | Must fire immediately. Hook text readable in under 2s. |
| `point` | 3s | 4-6s | 8s | One concept per scene. Text + subtext readable in duration. |
| `comparison` | 4s | 6-8s | 10s | Before/after pair needs time to register contrast. |
| `number` | 3s | 4-5s | 6s | Counter-up animation needs 2-3s, context text needs 2s. |
| `step` | 8s | 12-15s | 20s | Tutorial steps need reading time + comprehension. |
| `demo` | 8s | 12-15s | 20s | Product features need visual demonstration time. |
| `cta` | 2s | 3-4s | 5s | Short, clear, actionable. Don't linger. |

### Pacing by Platform

| Platform | Total Duration Sweet Spot | Scene Pacing | Hook Window |
|----------|--------------------------|-------------|-------------|
| Instagram Reels | 15-30s | Fast (3-5s per scene) | < 1.5s |
| YouTube Shorts | 30-60s | Medium (4-6s per scene) | < 2s |
| TikTok | 15-60s | Fast (3-5s per scene) | < 1s |
| YouTube (long) | 60-180s | Measured (8-15s per scene) | < 3s |

### Pacing Rules

1. **3-5 second visual change rule**: No scene should go more than 5 seconds without a visible change (animation, new text, transition, or motion element).
2. **Descending duration**: Later scenes can be slightly shorter than earlier ones to create acceleration toward the CTA.
3. **Hook compression**: The hook scene should feel urgent. 2-3 seconds maximum. If the hook needs more time, the text is too long.
4. **CTA brevity**: The CTA scene is not for new information. Keep it under 4 seconds. The viewer has already decided to act or not.
5. **Reading speed**: Assume 150 words per minute for on-screen text. A 5-second scene supports approximately 12 words.

---

## Animation Catalog

Ten animation types are available. Each maps to a Remotion animation implementation using `useCurrentFrame()` and `interpolate()`.

| Animation | Description | Best For | Remotion Implementation |
|-----------|-------------|----------|------------------------|
| `fade-in` | Opacity from 0 to 1 over 15 frames | Hook scenes, gentle reveals | `interpolate(frame, [0, 15], [0, 1])` on opacity |
| `fade-out` | Opacity from 1 to 0 over 15 frames | Scene exits, before transitions | `interpolate(frame, [end-15, end], [1, 0])` on opacity |
| `slide-left` | Element enters from right edge, slides to center | Content points (odd positions) | `interpolate(frame, [0, 20], [width, 0])` on translateX |
| `slide-right` | Element enters from left edge, slides to center | Content points (even positions) | `interpolate(frame, [0, 20], [-width, 0])` on translateX |
| `slide-up` | Element enters from bottom, slides to center | Steps, reveals, lists | `interpolate(frame, [0, 20], [height, 0])` on translateY |
| `scale-in` | Element scales from 0.5 to 1.0 with slight bounce | Hooks, reveals, emphasis | `interpolate(frame, [0, 20], [0.5, 1])` on scale with spring config |
| `bounce` | Element enters with elastic bounce effect | CTAs, emphasis, fun reveals | `spring({ frame, fps, config: { damping: 8, stiffness: 100 } })` |
| `typewriter` | Text appears character by character | Quotes, statements, dramatic reveals | Render substring `text.slice(0, charIndex)` per frame |
| `counter-up` | Number counts from 0 to target value | Statistics, metrics, data | `interpolate(frame, [0, durationFrames], [0, targetNumber])` rounded |
| `wipe` | Horizontal wipe reveals new content | Before/after reveals, dramatic transitions | ClipPath animation from `inset(0 100% 0 0)` to `inset(0 0 0 0)` |

### Animation Selection Rules

1. **Hook scenes**: Use `fade-in`, `scale-in`, or `wipe`. Never use `slide-left` or `slide-right` for the first scene — they feel like continuation, not an opening.
2. **Point scenes**: Alternate `slide-left` and `slide-right` for pattern interrupt. Same direction on every scene is monotonous.
3. **Number scenes**: Always use `counter-up` for the number itself. Use `fade-in` for the context text below.
4. **CTA scenes**: Use `bounce` or `scale-in` for emphasis. The CTA must feel like an arrival, not a slide.
5. **Comparison scenes**: Use `wipe` for dramatic before/after reveals. `slide-left`/`slide-right` for less dramatic comparisons.
6. **Step scenes**: Use `slide-up` consistently for all steps. The upward motion creates a sense of building/progressing.
7. **Never use more than 3 different animation types** in a single video. Consistency is more important than variety.

### Animation Timing

| Animation | Default Duration (frames) | At 30fps |
|-----------|--------------------------|----------|
| fade-in | 15 | 0.5s |
| fade-out | 15 | 0.5s |
| slide-left | 20 | 0.67s |
| slide-right | 20 | 0.67s |
| slide-up | 20 | 0.67s |
| scale-in | 20 | 0.67s |
| bounce | 30 | 1.0s |
| typewriter | varies (2 frames/char) | varies |
| counter-up | matches scene duration | varies |
| wipe | 25 | 0.83s |

---

## Transitions

Four transition types connect scenes. Transitions occur between the end of one scene and the start of the next.

| Transition | Frame Duration | At 30fps | Description | Best For |
|-----------|---------------|----------|-------------|----------|
| `crossfade` | 15 frames | 0.5s | Outgoing scene fades out while incoming fades in. Smooth and professional. | Default for most scene changes. Points, steps, generic transitions. |
| `wipe` | 20 frames | 0.67s | Horizontal wipe reveals the new scene from left to right. Dramatic. | Before/after reveals, comparison pairs, dramatic moments. |
| `cut` | 0 frames | 0s | Instant switch. No transition effect. Sharp and immediate. | Hook scene start (always use cut for the first scene), rhythm breaks. |
| `slide` | 15 frames | 0.5s | Outgoing scene slides out while incoming slides in from opposite edge. | Carousel-animated (mimics swipe gesture), sequential content. |

### Transition Rules

1. **First scene always uses `cut`**: The video must start immediately. No fade-in from black — the hook text must be visible from frame 1.
2. **Default is `crossfade`**: When no transition is specified, use crossfade. It is the safest and most professional option.
3. **Use `wipe` sparingly**: Maximum 2 wipe transitions per video. Overuse makes the video feel gimmicky.
4. **`slide` for CarouselAnimated**: The slide transition mimics the Instagram carousel swipe gesture, making animated carousels feel native.
5. **Transition frames overlap**: Transitions consume frames from both the outgoing and incoming scenes. They do not add to total duration.

---

## Platform Rules

### Instagram Reels

| Parameter | Value | Notes |
|-----------|-------|-------|
| Aspect Ratio | 9:16 (1080x1920) | Mandatory for full-screen Reels |
| Max Duration | 90 seconds | Algorithm favors 15-30s for reach |
| Min Duration | 3 seconds | Below 3s feels like an error |
| Sweet Spot | 15-30 seconds | Highest completion rate and reach |
| Hook Window | < 1.5 seconds | Text must be readable immediately |
| Safe Zones | 250px top, 400px bottom | Avoid UI overlay areas (username, music, buttons) |
| Audio | Optional (motion-only supported) | Add caption overlay for sound-off viewers |

### YouTube Shorts

| Parameter | Value | Notes |
|-----------|-------|-------|
| Aspect Ratio | 9:16 (1080x1920) | Same as Reels |
| Max Duration | 60 seconds | Hard limit enforced by YouTube |
| Min Duration | 15 seconds | Below 15s may not get Shorts shelf |
| Sweet Spot | 30-60 seconds | YouTube Shorts audience tolerates longer content |
| Hook Window | < 2 seconds | Slightly more forgiving than IG |
| Safe Zones | 200px top, 350px bottom | Similar to Reels but slightly different UI |
| Audio | Recommended | YouTube Shorts discovery relies more on audio |

### TikTok

| Parameter | Value | Notes |
|-----------|-------|-------|
| Aspect Ratio | 9:16 (1080x1920) | Standard vertical |
| Max Duration | 3 minutes (180s) | Extended from original 60s |
| Min Duration | 5 seconds | Below 5s may not surface in For You |
| Sweet Spot | 15-60 seconds | Depends on content type |
| Hook Window | < 1 second | TikTok has the shortest attention span |
| Safe Zones | 150px top, 500px bottom | Large bottom safe zone for comments/buttons |
| Audio | Strongly recommended | TikTok is audio-first platform |

### YouTube (Horizontal)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Aspect Ratio | 16:9 (1920x1080) | Standard horizontal |
| Max Duration | No limit | Platform supports any length |
| Min Duration | 30 seconds | Below 30s feels rushed for horizontal |
| Sweet Spot | 60-180 seconds | For explainers and demos |
| Hook Window | < 3 seconds | More patient audience |
| Safe Zones | Minimal | Full-screen video, no UI overlays during playback |
| Audio | Expected | Horizontal YouTube content almost always has narration |

---

## Brand Integration

### Color Mapping from brand-voice.yaml

```yaml
# brand-voice.yaml colors map to video elements:
primary:     # Scene accent colors, progress bar fill, icon highlights
secondary:   # Secondary highlights, subtext emphasis, background accents
background:  # Video background color, gradient base
text:        # All text (headlines, body, subtext)
accent:      # CTA button color, emphasis elements, counter-up numbers
```

### Color Application by Scene Type

| Scene Type | Background | Text | Accent Usage |
|-----------|-----------|------|-------------|
| hook | background color or dark gradient | text color, large | accent on key word or underline |
| point | background color | text color | primary on icon, secondary on subtext |
| comparison | split: muted background / vibrant background | text color | accent on "after" state |
| number | background color | text color for context | accent on the animated number |
| step | background color | text color | primary on step number |
| demo | background color or branded gradient | text color | accent on feature highlights |
| cta | accent color as background or accent border | text color (inverted if needed) | accent dominant |

### Watermark Positioning

The brand watermark (@handle) is rendered by the `BrandWatermark` component:

| Position | Pixel Offset | Best For |
|----------|-------------|----------|
| `bottom-right` | 40px from bottom, 40px from right | Default. Most natural position. |
| `bottom-left` | 40px from bottom, 40px from left | When bottom-right conflicts with platform UI |
| `top-right` | 40px from top, 40px from right | When bottom area is crowded |

**Watermark rules:**
- Fade-in at the start of the first scene, stays visible for entire video
- Opacity: 0.7 (visible but not distracting)
- Font size: 18-22px
- Color: text color from brand at 70% opacity
- Never place over the main text area of any scene

### Progress Bar

The animated progress bar shows video progress (0% to 100% over the full duration):

- **Position**: Top of frame (default) or bottom of frame
- **Height**: 4px
- **Color**: primary color from brand
- **Background**: white at 20% opacity
- **Animation**: Width interpolates from 0% to 100% linearly across totalFrames

---

## Retention Triggers

### Visual Change Cadence

The single most important retention factor in short-form video is **visual change frequency**. The human brain habituates to static visuals in 3-5 seconds and the viewer's finger moves to scroll.

**Rule: A visible change must occur every 3-5 seconds.**

Types of visible changes (in order of impact):
1. **Scene transition** — new background, new text, new layout (strongest)
2. **Animation start** — text slides in, number counts up, element scales (strong)
3. **Color shift** — background gradient animates, accent color pulses (moderate)
4. **Progress bar movement** — visible progress update (weak but cumulative)

### Retention Trigger Catalog

| Trigger | Implementation | Why It Works |
|---------|---------------|-------------|
| Motion on every scene | All scenes have entrance animations | Static text = scroll away. Motion = visual interest. |
| Counter-up for numbers | Numbers animate from 0 to target | Brain tracks counting, creates micro-anticipation. |
| Alternating slide directions | Odd scenes slide-left, even slide-right | Pattern interrupt prevents visual habituation. |
| Progress bar | Animated bar from 0% to 100% | Creates completion motivation (endowed progress effect). |
| Hook in first 1.5s | Text visible from frame 1, no fade-from-black | First impression determines stay/go. No wasted time. |
| Text in motion | Typewriter, slide, fade — never just "appear" | Motion triggers peripheral vision attention. |
| Color contrast on key words | Accent color on numbers, names, key terms | Draws eye to the most important information. |
| Scene type variety | Mix hooks, points, numbers, comparisons | Different layouts prevent monotony. |

### Retention Anti-Pattern Checklist

Before finalizing any storyboard, verify these are NOT present:

```
Retention Anti-Pattern Checklist:
[ ] No scene exceeds 8 seconds without a visual change
[ ] No two consecutive scenes use the same animation direction
[ ] Hook scene text is visible from frame 1 (no fade-from-black)
[ ] CTA scene is under 5 seconds (viewer has already decided)
[ ] No "intro" scene before the hook (no logos, no "welcome to...")
[ ] Total duration is within platform sweet spot
[ ] Progress bar is enabled (completion motivation)
[ ] At least 1 counter-up animation if content contains numbers
[ ] No scene has more than 20 words of text
```

---

## Anti-Patterns

### Content Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Scene > 8s without visual change | Viewer habituates, scrolls away | Split scene or add mid-scene animation |
| Static text (no animation) | Looks like a screenshot, not a video | Add entrance animation to every text element |
| No CTA at the end | Viewer watches but takes no action | Always end with a clear, single CTA |
| Hook > 3 seconds | Loses viewers before the content starts | Compress hook to 2-3s max. If text is too long, simplify. |
| Intro/logo before hook | Wastes the critical first 1.5s | Hook first, always. Brand watermark handles attribution. |
| Slow pacing (>6s per point scene) | Feels like a slideshow, not a video | Speed up to 4-5s per point. Cut unnecessary subtext. |
| Too many words per scene | Text unreadable in scene duration | Max 20 words per scene. 12 words is ideal for 5s scenes. |
| Same animation on every scene | Monotonous, no pattern interrupts | Alternate directions, mix animation types (max 3 types). |

### Technical Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Duration outside template range | Remotion render may fail or produce bad output | Check template duration constraints before composing |
| Wrong aspect ratio for platform | Video appears letterboxed or cropped | Match template aspect ratio to target platform |
| Transition frames exceeding scene duration | Scene content gets cut by transition overlap | Ensure scene durationFrames > transition frame count |
| Missing brand colors | Video looks generic, no brand recognition | Always load and inject BrandProps from brand-voice.yaml |
| Counter-up without sufficient duration | Number animation too fast to read | Minimum 3s for counter-up scenes |
| Watermark over main text | Blocks content, looks amateur | Position watermark in corner away from text area |

### Strategic Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Using explainer template for reel content | Wrong pacing, wrong audience expectations | Match template to content type and platform |
| 60s reel for a 3-point topic | Padded content feels thin, hurts retention | Shorter content = shorter video. 3 points = 25-30s reel. |
| Animated carousel without original carousel | No source content to adapt | Use reel or explainer template instead. CarouselAnimated is for converting existing content. |
| Ignoring platform safe zones | Text hidden behind platform UI elements | Respect safe zone margins per platform |
| No progress bar on reels | Viewer has no sense of video length | Always enable progress bar for short-form content |

---

## Carousel-to-Video Conversion

### When to Use CarouselAnimated

Convert existing HTML carousel content to animated video when:
- The user explicitly requests an animated version of an existing carousel
- Cross-posting strategy targets video-first platforms (TikTok, YouTube Shorts)
- Carousel performance data suggests video would perform better
- The content is evergreen and worth repurposing

### Conversion Rules

#### Slide-to-Scene Mapping

```
Carousel slide_plan:                    Video storyboard:
  slide 1 (cover)           -->         scene 1 (hook, 4s, fade-in)
  slide 2 (content)         -->         scene 2 (point, 4s, slide-left)
  slide 3 (content)         -->         scene 3 (point, 4s, slide-right)
  ...                                   ...
  slide N (cta)             -->         scene N (cta, 4s, bounce)
```

#### Content Adaptation

| Carousel Element | Video Adaptation |
|-----------------|-----------------|
| Slide headline | Scene text (keep as-is, already optimized) |
| Slide body text | Scene subtext (may need trimming for reading speed) |
| Slide bullets | Convert to sequential text reveals within scene |
| Slide icon/emoji | Scene icon (keep as-is) |
| Progress dots | Replace with animated progress bar |
| Brand watermark | Map to BrandWatermark component |

#### Timing Calculation

```
Carousel with N slides:
  Each slide becomes a 4-second scene
  Total duration = N * 4 seconds

  Example: 7-slide carousel = 28-second video

  If total > 60s: reduce per-scene duration to 3s
  If total < 15s: increase per-scene duration to 5s
```

#### Transition for Carousel-Animated

Always use `slide` transition for CarouselAnimated. This mimics the Instagram carousel swipe gesture and makes the animated version feel like a natural extension of the carousel format.

#### Design Spec Inheritance

When converting from an existing carousel, the CarouselAnimated template inherits:
- Color palette from the carousel's `design_spec.palette`
- Brand handle from the carousel's `design_spec.brand.handle`
- Typography style from the carousel's `design_spec.typography`

Do not re-derive these from brand-voice.yaml — use the carousel's existing design decisions for visual consistency between the static and animated versions.

---

## Shared Components Reference

Six Remotion React components are available for all templates:

| Component | Purpose | Props |
|-----------|---------|-------|
| `AnimatedText` | Renders text with specified animation type and delay | `text`, `animation`, `delay`, `style` |
| `ProgressBar` | Animated bar showing video progress (0-100%) | `position` ("top" or "bottom"), `color`, `height` |
| `BrandWatermark` | Brand handle overlay in corner, fades in on first scene | `handle`, `position`, `color`, `opacity` |
| `TransitionWipe` | Renders transition effect between scenes | `type` ("crossfade", "wipe", "cut", "slide"), `durationFrames` |
| `BackgroundGradient` | Animated gradient background with subtle color shift | `colors` (array), `direction`, `animationSpeed` |
| `CounterUp` | Counts from 0 to target number with easing | `target`, `durationFrames`, `style`, `easing` |

---

## Output Contract

```yaml
output_contract:
  skill: remotion-video
  format: composition_json
  required_fields:
    template: string       # Must match a registered template name
    fps: integer           # Always 30
    width: integer         # From template spec
    height: integer        # From template spec
    totalFrames: integer   # Calculated sum of all scene durationFrames
    brand: BrandProps      # From brand-voice.yaml
    scenes: SceneProps[]   # Mapped from storyboard
    showProgressBar: boolean
    showWatermark: boolean
  scene_required_fields:
    type: string           # hook | point | comparison | number | step | demo | cta
    startFrame: integer    # Calculated cumulative position
    durationFrames: integer # scene.duration * fps
    text: string           # Scene headline text
    animation: string      # From animation catalog
  scene_optional_fields:
    subtext: string
    icon: string
    transition: string     # Default: crossfade
  validation:
    total_frames_within_template_range: true
    all_animations_in_catalog: true
    all_transitions_in_catalog: true
    frame_calculations_correct: true
    brand_colors_present: true
    no_scene_exceeds_max_duration: true
```

---

## Remotion Environment Discovery & Rendering

### CRITICAL: Run this discovery routine BEFORE any render attempt.

The Remotion CLI may be installed differently on each user's machine. Never assume a fixed path or command. Follow this discovery sequence exactly.

### Step 1: Locate the GrowthOS Remotion Project

The Remotion project lives inside the GrowthOS plugin directory. Discover its path dynamically:

```bash
# Strategy 1: Relative to the growthOS plugin root
GROWTHOS_ROOT="$(find . -maxdepth 4 -name 'brand-voice.yaml' -exec dirname {} \; 2>/dev/null | head -1)"
REMOTION_PROJECT="${GROWTHOS_ROOT}/remotion"

# Strategy 2: If brand-voice.yaml not found, search for remotion/src/Root.tsx
REMOTION_PROJECT="$(find . -maxdepth 5 -path '*/growthOS/remotion' -type d 2>/dev/null | head -1)"

# Strategy 3: Check common Claude Code plugin locations
PLUGIN_LOCATIONS=(
  "${HOME}/.claude/plugins"
  "${HOME}/Downloads"
  "$(pwd)"
)
for loc in "${PLUGIN_LOCATIONS[@]}"; do
  if [ -f "${loc}/growthOS/remotion/src/Root.tsx" ] || [ -f "${loc}/growthOS/remotion/index.ts" ]; then
    REMOTION_PROJECT="${loc}/growthOS/remotion"
    break
  fi
done
```

**Validation:** After locating, confirm the project is valid:
```bash
# Must have at least one of these entry points
[ -f "${REMOTION_PROJECT}/index.ts" ] || [ -f "${REMOTION_PROJECT}/src/Root.tsx" ]
```

### Step 2: Determine the Entry Point

GrowthOS has two Remotion entry point structures. Detect which one is active:

```bash
# Preferred: Full project with 6 compositions (src/ structure)
if [ -f "${REMOTION_PROJECT}/src/Root.tsx" ] && [ -f "${REMOTION_PROJECT}/src/compositions/index.ts" ]; then
  ENTRY_POINT="${REMOTION_PROJECT}/src/index.ts"
  ENTRY_TYPE="full"
  # Available compositions: ReelTips, ReelBeforeAfter, ReelNumbers, ExplainerSteps, ExplainerDemo, CarouselAnimated

# Fallback: Simplified structure (root-level)
elif [ -f "${REMOTION_PROJECT}/index.ts" ]; then
  ENTRY_POINT="${REMOTION_PROJECT}/index.ts"
  ENTRY_TYPE="simple"
  # Available compositions: ReelTips only (others must be added)
fi
```

**Entry point decision table:**

| Structure | Entry Point | Compositions | When to Use |
|-----------|-------------|-------------|-------------|
| `src/` (full) | `remotion/src/index.ts` | All 6 templates | Default — use this when available |
| Root-level (simple) | `remotion/index.ts` | ReelTips only | Fallback if src/ not present |

### Step 3: Discover the Remotion CLI

Remotion CLI can be installed in multiple ways. Check in order of preference:

```bash
# Method 1: Local npx (most reliable — uses project's node_modules)
cd "${REMOTION_PROJECT}" && npx remotion --version 2>/dev/null
REMOTION_CMD="npx remotion"

# Method 2: Project-level node_modules binary
if [ -x "${REMOTION_PROJECT}/node_modules/.bin/remotion" ]; then
  REMOTION_CMD="${REMOTION_PROJECT}/node_modules/.bin/remotion"
fi

# Method 3: GrowthOS parent node_modules (if deps installed at growthOS level)
GROWTHOS_BIN="${GROWTHOS_ROOT}/node_modules/.bin/remotion"
if [ -x "${GROWTHOS_BIN}" ]; then
  REMOTION_CMD="${GROWTHOS_BIN}"
fi

# Method 4: Global install
if command -v remotion &>/dev/null; then
  REMOTION_CMD="remotion"
fi

# Method 5: Not found — install needed
if [ -z "${REMOTION_CMD}" ]; then
  echo "Remotion not found. Installing..."
  cd "${REMOTION_PROJECT}" && npm install
  REMOTION_CMD="npx remotion"
fi
```

**Discovery result table:**

| Method | Command | Reliability | Notes |
|--------|---------|-------------|-------|
| `npx remotion` | High | Uses local node_modules, auto-resolves version | **Preferred** |
| `./node_modules/.bin/remotion` | High | Direct binary, no npx overhead | Fast alternative |
| Global `remotion` | Medium | May version-mismatch with project deps | Check version compatibility |
| Not found | — | — | Run `npm install` in remotion project dir |

### Step 4: Verify Dependencies

Before rendering, confirm all dependencies are installed:

```bash
cd "${REMOTION_PROJECT}"

# Check if node_modules exists and has remotion
if [ ! -d "node_modules/remotion" ]; then
  echo "Installing Remotion dependencies..."
  npm install
fi

# Verify Chrome Headless Shell (Remotion downloads this automatically on first render)
# No manual action needed — Remotion handles this. But if it fails:
# npx remotion browser ensure
```

### Step 5: Render Commands

Use the discovered `REMOTION_CMD` and `ENTRY_POINT` to execute renders:

```bash
# Ensure output directory exists
mkdir -p "${GROWTHOS_ROOT}/.growthOS/output/videos/$(date +%Y-%m-%d-%H%M%S)"
OUTPUT_DIR="${GROWTHOS_ROOT}/.growthOS/output/videos/$(date +%Y-%m-%d-%H%M%S)"

# List available compositions (verify before render)
cd "${REMOTION_PROJECT}" && ${REMOTION_CMD} compositions "${ENTRY_POINT}"

# Render MP4 video
cd "${REMOTION_PROJECT}" && ${REMOTION_CMD} render "${ENTRY_POINT}" <CompositionId> "${OUTPUT_DIR}/video.mp4"

# Render a still frame (preview/thumbnail)
cd "${REMOTION_PROJECT}" && ${REMOTION_CMD} still "${ENTRY_POINT}" <CompositionId> "${OUTPUT_DIR}/preview.png" --frame=45

# Open Remotion Studio (interactive preview in browser)
cd "${REMOTION_PROJECT}" && ${REMOTION_CMD} studio "${ENTRY_POINT}"
```

**Passing dynamic props (from composition.json):**

```bash
# Pass scene data from the storyboard via --props flag
cd "${REMOTION_PROJECT}" && ${REMOTION_CMD} render "${ENTRY_POINT}" ReelTips "${OUTPUT_DIR}/video.mp4" \
  --props="${OUTPUT_DIR}/composition.json"
```

### Step 6: Cross-Platform Considerations

| Platform | Working Dir Separator | Shell | NPX Available | Notes |
|----------|----------------------|-------|---------------|-------|
| **macOS** | `/` | zsh/bash | Yes (with Node) | Default dev platform. `open file.mp4` to play. |
| **Linux** | `/` | bash | Yes (with Node) | `xdg-open file.mp4` to play. May need `apt install chromium` for headless. |
| **Windows (native)** | `\` | PowerShell/cmd | Yes (with Node) | Use `start file.mp4` to play. Paths need backslash or quotes. |
| **Windows (WSL)** | `/` | bash | Yes (with Node) | Render inside WSL, output accessible at `/mnt/c/...`. `explorer.exe file.mp4` to play. |

**macOS-specific:**
```bash
# Render and open
cd "${REMOTION_PROJECT}" && ${REMOTION_CMD} render "${ENTRY_POINT}" ReelTips out/video.mp4 && open out/video.mp4
```

**Linux-specific:**
```bash
# Ensure headless Chrome dependencies
sudo apt-get install -y chromium-browser 2>/dev/null || true
cd "${REMOTION_PROJECT}" && ${REMOTION_CMD} render "${ENTRY_POINT}" ReelTips out/video.mp4 && xdg-open out/video.mp4
```

**WSL-specific:**
```bash
# Render in WSL, open in Windows
cd "${REMOTION_PROJECT}" && ${REMOTION_CMD} render "${ENTRY_POINT}" ReelTips out/video.mp4
explorer.exe "$(wslpath -w out/video.mp4)"
```

### Step 7: Performance Tuning

```bash
# Default concurrency (auto-detected from CPU cores)
${REMOTION_CMD} render "${ENTRY_POINT}" ReelTips out/video.mp4

# Explicit concurrency (use 50-75% of available cores)
${REMOTION_CMD} render "${ENTRY_POINT}" ReelTips out/video.mp4 --concurrency=8

# Lower quality for fast preview
${REMOTION_CMD} render "${ENTRY_POINT}" ReelTips out/preview.mp4 --jpeg-quality=60 --scale=0.5

# High quality for publication
${REMOTION_CMD} render "${ENTRY_POINT}" ReelTips out/video.mp4 --jpeg-quality=90 --crf=18
```

### Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `remotion: command not found` | CLI not installed | `cd ${REMOTION_PROJECT} && npm install` then use `npx remotion` |
| `Cannot find module 'remotion'` | Dependencies not installed | `cd ${REMOTION_PROJECT} && npm install` |
| `Could not find composition` | Wrong entry point or composition ID | Run `${REMOTION_CMD} compositions ${ENTRY_POINT}` to list available |
| `Chrome Headless Shell not found` | First render, downloading | Wait for auto-download, or run `npx remotion browser ensure` |
| `ENOMEM` / out of memory | Video too long or high concurrency | Reduce `--concurrency` or add `--scale=0.5` |
| `ENOSPC` / disk space | Not enough disk for render frames | Free 500MB+ before rendering |
| `Timed out` | Render exceeds 5min | Reduce duration, lower quality, or increase `--timeout` |
| `JSX element type 'X' does not have any construct` | TypeScript/React version mismatch | Check `tsconfig.json` has `"jsx": "react-jsx"` |
| `Module not found: @remotion/cli/config` | Old remotion.config.ts API | Update to `import { Config } from "@remotion/cli/config"` |

### Complete Discovery Script (copy-paste ready)

```bash
#!/bin/bash
# GrowthOS Remotion Discovery — run from project root
set -e

# 1. Find GrowthOS root
GROWTHOS_ROOT="$(find . -maxdepth 4 -name 'brand-voice.yaml' -exec dirname {} \; 2>/dev/null | head -1)"
if [ -z "$GROWTHOS_ROOT" ]; then
  echo "ERROR: brand-voice.yaml not found. Run /grow setup first."
  exit 1
fi

# 2. Find Remotion project
REMOTION_PROJECT="${GROWTHOS_ROOT}/remotion"
if [ ! -d "$REMOTION_PROJECT" ]; then
  echo "ERROR: Remotion project not found at ${REMOTION_PROJECT}"
  exit 1
fi

# 3. Determine entry point
if [ -f "${REMOTION_PROJECT}/src/compositions/index.ts" ]; then
  ENTRY_POINT="src/index.ts"
  echo "Entry: full (6 compositions)"
else
  ENTRY_POINT="index.ts"
  echo "Entry: simple (ReelTips only)"
fi

# 4. Ensure dependencies
if [ ! -d "${REMOTION_PROJECT}/node_modules/remotion" ]; then
  echo "Installing dependencies..."
  cd "$REMOTION_PROJECT" && npm install
fi

# 5. Verify
cd "$REMOTION_PROJECT" && npx remotion compositions "$ENTRY_POINT"

echo ""
echo "Remotion ready!"
echo "  Project: ${REMOTION_PROJECT}"
echo "  Entry:   ${ENTRY_POINT}"
echo "  Render:  cd ${REMOTION_PROJECT} && npx remotion render ${ENTRY_POINT} <CompositionId> out/video.mp4"
echo "  Studio:  cd ${REMOTION_PROJECT} && npx remotion studio ${ENTRY_POINT}"
```
