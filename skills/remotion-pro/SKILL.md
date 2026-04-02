---
name: remotion-pro
description: Main Remotion Pro orchestrator for GrowthOS — handles first-run onboarding wizard (video-profile.yaml), displays the 8-showcase catalog, routes to the correct showcase skill (product-demo, tech-terminal, before-after, data-story, course-trailer, social-proof, feature-highlight, walkthrough), manages Remotion environment discovery, applies config precedence (briefing > video-profile.yaml > brand-voice.yaml > defaults), and coordinates professional video production output bundles.
---

# Remotion Pro — Orchestrator Skill

Central dispatcher for all GrowthOS video production powered by Remotion. Handles onboarding, showcase selection, environment discovery, and output coordination.

---

## Trigger Conditions

Activate this skill when the user:
- Runs `/grow video` with or without a showcase name
- Mentions "remotion pro", "video showcase", "criar video", "make a video"
- References any of the 8 showcase types by keyword
- Asks for the video catalog or wants to browse showcases

---

## Step 1 — Onboarding Gate

Before doing anything else, check whether `video-profile.yaml` exists in the GrowthOS root directory (`growthOS/video-profile.yaml`).

```
CHECK: does growthOS/video-profile.yaml exist?
  YES → Skip wizard, load profile, proceed to Step 3
  NO  → Run the 6-step onboarding wizard (Step 2)
```

---

## Step 2 — Onboarding Wizard (First-Run Only)

Run this interactive wizard only when `video-profile.yaml` is missing. Present each step clearly, collect input, then generate the YAML file.

### Wizard Header

```
╔══════════════════════════════════════════════════════╗
║         REMOTION PRO — FIRST-RUN SETUP               ║
║   Let's configure your video production profile.     ║
╚══════════════════════════════════════════════════════╝

This takes about 2 minutes. You can edit video-profile.yaml
anytime to update these settings.
```

---

### Step 2.1 — Assets

```
📁 STEP 1/6 — ASSETS
─────────────────────────────────────────────
Where are your brand assets located?

  Logo path (PNG/SVG):
  > [e.g. assets/logo.png or leave blank to skip]

  Screenshots directory:
  > [e.g. assets/screenshots/ — folder with product screenshots]

  App icon path (optional):
  > [e.g. assets/icon.png]
```

Collect: `logo_path`, `screenshots_dir`, `icon_path`

---

### Step 2.2 — Design Tokens

```
🎨 STEP 2/6 — DESIGN TOKENS
─────────────────────────────────────────────
Auto-detecting from brand-voice.yaml...
```

Attempt to read `growthOS/brand-voice.yaml`. Extract:
- `brand.colors.primary` → `primary_color`
- `brand.colors.secondary` → `secondary_color`  
- `brand.colors.accent` → `accent_color`
- `brand.typography.heading_font` → `heading_font`
- `brand.typography.body_font` → `body_font`
- `brand.design.border_radius` → `border_radius`

If auto-detected, display the values and ask for confirmation:

```
  Detected from brand-voice.yaml:
    Primary color:   #[value]   ← confirm or override
    Secondary color: #[value]
    Accent color:    #[value]
    Heading font:    [value]
    Body font:       [value]
    Border radius:   [value]

  Press Enter to confirm or type new values:
  Primary color:   > 
  Secondary color: > 
  Accent color:    > 
  Heading font:    > 
  Body font:       > 
  Border radius:   > 
```

If not auto-detected, ask for each value with defaults:
- `primary_color`: `#7C3AED`
- `secondary_color`: `#1E1E2E`
- `accent_color`: `#F59E0B`
- `heading_font`: `Inter`
- `body_font`: `Inter`
- `border_radius`: `12px`

---

### Step 2.3 — Device Frames

```
🖥️  STEP 3/6 — DEVICE FRAMES
─────────────────────────────────────────────
Which device frames will you use in videos?
(Select all that apply — comma-separated numbers)

  1. Browser frame (Chrome/Safari)
  2. Mobile frame (iPhone)
  3. Desktop frame (MacBook)
  4. Terminal frame

  Selection: > [e.g. 1,2 or "all" or "none"]
```

Map selection to: `device_frames: [browser, mobile, desktop, terminal]`

---

### Step 2.4 — User Journeys

```
🗺️  STEP 4/6 — USER JOURNEYS
─────────────────────────────────────────────
Define named flows for your product walkthroughs.
These are sequences of screens used in demo and walkthrough videos.

  How many journeys do you want to define now?
  (You can add more later in video-profile.yaml)
  > [number, or 0 to skip]
```

For each journey, collect:
```
  Journey [N] name: > [e.g. "Onboarding Flow"]
  
  Screens in this journey (one per line, blank to finish):
    Screen name:       > [e.g. "Landing Page"]
    Screenshot path:   > [e.g. screenshots/landing.png]
    Actions (comma-separated): > [e.g. "click Sign Up, fill email, submit"]
    
    Add another screen? [y/n]
```

Structure collected as:
```yaml
journeys:
  - name: "Onboarding Flow"
    screens:
      - name: "Landing Page"
        screenshot: "screenshots/landing.png"
        actions: ["click Sign Up", "fill email", "submit"]
```

---

### Step 2.5 — Maestri Connection

```
🔗 STEP 5/6 — MAESTRI CONNECTION
─────────────────────────────────────────────
Maestri is GrowthOS's AI orchestration layer.
Connect it to enable automated video triggers.

  Enable Maestri integration? [y/n]
  > 

  [If y:]
  Source project path:
  > [path to your Maestri project, or leave blank for auto-detect]

  Protocol: [http/grpc/stdio] (default: stdio)
  > 
```

Collect: `maestri.enabled`, `maestri.source_project`, `maestri.protocol`

---

### Step 2.6 — Style Preferences

```
✨ STEP 6/6 — STYLE PREFERENCES
─────────────────────────────────────────────
Final style settings for your videos.

  Theme:
    1. Dark (recommended for tech/SaaS)
    2. Light
    3. Auto (follows brand-voice.yaml)
  > 

  Pacing:
    1. Fast  (punchy, social-first)
    2. Medium (balanced)
    3. Slow  (detailed, educational)
  > 

  Background music: [y/n] (default: n)
  > 

  Output extras:
    1. Generate thumbnail
    2. Generate caption file (.srt)
    3. Multi-platform renders (9:16, 16:9, 4:5)
    4. All of the above
    5. None
  > 
```

Collect: `style.theme`, `style.pacing`, `style.music`, `style.output_extras`

---

### Wizard Complete — Generate video-profile.yaml

After collecting all inputs, write `growthOS/video-profile.yaml`:

```yaml
# GrowthOS Video Profile
# Generated by Remotion Pro onboarding wizard
# Edit anytime to update settings

version: "1.0"
generated_at: "[ISO timestamp]"

assets:
  logo_path: "[collected value]"
  screenshots_dir: "[collected value]"
  icon_path: "[collected value]"

design_tokens:
  primary_color: "[collected value]"
  secondary_color: "[collected value]"
  accent_color: "[collected value]"
  heading_font: "[collected value]"
  body_font: "[collected value]"
  border_radius: "[collected value]"

device_frames:
  - browser
  - mobile
  # (only selected frames)

journeys:
  # (collected journey data)

maestri:
  enabled: false
  source_project: ""
  protocol: "stdio"

style:
  theme: "dark"
  pacing: "medium"
  music: false
  output_extras:
    thumbnail: false
    captions: false
    multi_platform: false
```

Display confirmation:

```
✅ video-profile.yaml created at growthOS/video-profile.yaml
   Run /grow video anytime to produce a new video.
```

Then continue to Step 3.

---

## Step 3 — Remotion Environment Discovery

Before producing any video, locate and validate the Remotion installation.

### Discovery Protocol

```
1. Find brand-voice.yaml
   → Read growthOS/brand-voice.yaml (or growthOS/brand-voice.example.yaml as fallback)
   → Extract project path hint if present under remotion.project_path

2. Locate Remotion project
   Priority order:
     a. growthOS/remotion/          (default GrowthOS location)
     b. value from brand-voice.yaml remotion.project_path
     c. Search upward from cwd for package.json containing "@remotion/core"

3. Determine entry point
   Look for in this order:
     a. src/index.ts
     b. src/Root.tsx
     c. remotion/index.ts
     d. Value of "remotion" key in package.json scripts

4. Discover CLI
   Try in order:
     a. npx remotion --version
     b. ./node_modules/.bin/remotion --version
     c. bunx remotion --version

5. Validate
   If CLI responds → proceed
   If not → display install instructions:
   
     Remotion not found. Install with:
       npm install @remotion/cli @remotion/core
     Then re-run your video command.
```

Store discovered values:
```
remotion_root: [path]
entry_point:   [file]
cli_command:   [npx remotion | ./node_modules/.bin/remotion]
```

---

## Step 4 — Showcase Catalog

When the user runs `/grow video` without specifying a showcase, display the full catalog:

```
╔══════════════════════════════════════════════════════╗
║              REMOTION PRO — VIDEO CATALOG            ║
╚══════════════════════════════════════════════════════╝

Choose a showcase to create your video:

  🖥️  1. Product Demo        — Full product walkthrough with device frames
  ⌨️  2. Tech Terminal       — Animated CLI/terminal output for devs
  ⚡  3. Before/After UI     — Split-screen comparison reveal
  📊  4. Data Story          — Animated charts and metric counters
  🎓  5. Course Trailer      — Module previews and learning journey
  ⭐  6. Social Proof        — Testimonials, toasts, and counters
  ✨  7. Feature Highlight   — Zoom-in spotlight on one key feature
  👆  8. App Walkthrough     — Step-by-step guided app tour

  Type a number, name, or keyword to select:
  > 
```

---

## Step 5 — Showcase Routing

Match user input to the correct showcase skill. Use keyword matching (case-insensitive, handles Portuguese and English):

| Input Keywords | Showcase Skill |
|---|---|
| `product-demo`, `demo`, `produto`, `product`, `1` | `showcase-product-demo` |
| `terminal`, `cli`, `tech`, `código`, `code`, `2` | `showcase-tech-terminal` |
| `before-after`, `antes-depois`, `comparação`, `comparison`, `before`, `after`, `3` | `showcase-before-after` |
| `data`, `dados`, `métricas`, `metrics`, `números`, `numbers`, `chart`, `4` | `showcase-data-story` |
| `course`, `curso`, `aula`, `módulo`, `module`, `trailer`, `5` | `showcase-course-trailer` |
| `proof`, `depoimento`, `testimonial`, `social proof`, `review`, `6` | `showcase-social-proof` |
| `feature`, `funcionalidade`, `destaque`, `highlight`, `spotlight`, `7` | `showcase-feature-highlight` |
| `walkthrough`, `tutorial`, `passo-a-passo`, `step-by-step`, `tour`, `8` | `showcase-walkthrough` |

When a match is found, activate the corresponding showcase skill and pass the following context:

```yaml
context:
  video_profile: [loaded video-profile.yaml data]
  brand_voice: [loaded brand-voice.yaml data]
  remotion:
    root: [remotion_root]
    entry_point: [entry_point]
    cli: [cli_command]
  briefing: [any user-provided description or requirements]
```

---

## Step 6 — Config Precedence

When populating showcase parameters, apply values in this priority order (highest to lowest):

```
1. BRIEFING        — Explicit values provided by the user in this session
2. video-profile.yaml — Saved user preferences from onboarding/edits
3. brand-voice.yaml   — Global brand settings (colors, fonts, tone)
4. DEFAULTS        — Showcase-specific hardcoded fallbacks
```

Example resolution for `primary_color`:
```
briefing["primary_color"]  → use if present
video-profile.yaml["design_tokens"]["primary_color"] → use if present
brand-voice.yaml["brand"]["colors"]["primary"] → use if present
"#7C3AED"  → default fallback
```

---

## Step 7 — Output Bundle

After the showcase skill produces the composition, assemble the output bundle based on the autonomy level from `brand-voice.yaml`:

### Read autonomy level:
```yaml
# From brand-voice.yaml
automation:
  autonomy: manual | semi | auto
```

### Bundle by autonomy level:

| Level | Outputs |
|---|---|
| `manual` | MP4 render + storyboard.md + Remotion composition file |
| `semi` | Everything in manual + thumbnail PNG + caption file (.srt) |
| `auto` | Everything in semi + multi-platform renders (9:16, 16:9, 4:5) |

### Output directory:
```
growthOS/out/videos/[showcase-name]-[YYYYMMDD-HHmm]/
  ├── video.mp4                  (always)
  ├── storyboard.md              (always)
  ├── composition.tsx            (always)
  ├── thumbnail.png              (semi + auto)
  ├── captions.srt               (semi + auto)
  ├── video-9x16.mp4             (auto only)
  ├── video-16x9.mp4             (auto only)
  └── video-4x5.mp4              (auto only)
```

### Render command:
```bash
[cli_command] render [entry_point] [CompositionId] out/videos/[folder]/video.mp4 \
  --props='[JSON props]' \
  --fps=30
```

For multi-platform (auto mode), run three renders with width/height overrides.

---

## Error Handling

| Error | Response |
|---|---|
| `video-profile.yaml` write fails | Show values, ask user to create manually |
| Remotion CLI not found | Show install instructions, do not proceed |
| brand-voice.yaml not found | Use all defaults, warn user |
| Showcase skill not found | Display catalog, ask user to select again |
| Render fails | Show Remotion error output, suggest fixes |
| Screenshot path not found | Warn and use placeholder, list missing paths |

---

## Quick Reference — Command Examples

```bash
/grow video                          # Show catalog
/grow video demo                     # Product Demo showcase
/grow video terminal                 # Tech Terminal showcase
/grow video before-after             # Before/After UI showcase
/grow video data                     # Data Story showcase
/grow video curso                    # Course Trailer (Portuguese)
/grow video depoimento               # Social Proof (Portuguese)
/grow video feature                  # Feature Highlight showcase
/grow video walkthrough              # App Walkthrough showcase
```

---

## Notes for Showcase Skills

Each showcase skill (`showcase-*`) receives the full context object from this orchestrator. They are responsible for:
1. Collecting showcase-specific briefing from the user
2. Building the Remotion props object
3. Writing the composition file (or instructing code generation)
4. Returning the composition ID and props to this orchestrator for rendering
5. Generating the storyboard.md

This orchestrator handles rendering and output bundling after the showcase skill completes.
