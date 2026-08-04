---
name: raw-footage-editing
description: Technical methodology for turning real raw video (phone/camera recordings, screen captures, podcast clips) into a captioned vertical cut ready to post — silence-cut, semantic trim, word-synced burned-in captions. Use when the user has an actual video FILE to edit, not when they need a video generated from a text brief (that's remotion-video / video-producer).
---

# Raw Footage Editing

Turns a raw recording into a 50-90 second vertical cut with burned-in captions. Three layers, always in this order: **mechanical cut**, **semantic cut**, **captions**. Skipping straight to captions on unedited footage produces a technically-correct but boring video — cuts are what make it watchable.

This skill is the technical counterpart to `platform-mastery` (format/duration rules) and `copywriting` (hook/CTA wording). It does not write scripts — it edits footage that already exists.

## Required tools

Discover these on `PATH` before doing anything. Never assume a fixed install location — different machines running GrowthOS will have them in different places.

```bash
command -v ffmpeg      # video/audio processing — required
command -v auto-editor  # silence-based mechanical cut — required
command -v whisper-cli  # word-timestamped transcription — required for captions
```

If any is missing, tell the user which one and stop — do not attempt to compile or install dependencies yourself as part of a content-creation task. Point them to the `editor-de-video` skill/installer (github.com/bernardreacher/editor-de-video-claude) which documents the full setup, including the whisper model download.

Also locate a whisper model (`ggml-small.bin` or larger — `base` mis-transcribes foreign/brand words too often for pt-BR). Check, in order: `$WHISPER_MODEL_PATH`, `~/.local/share/whisper-models/`, the working directory. Ask the user for the path if none is found.

## Before cutting (mandatory order)

1. **Watch it first.** Extract a handful of frames and actually look, don't cut from the transcript alone — a transcript hides bad framing, flubbed delivery, and energy drops that a silence detector will happily preserve.
2. **A raw take over 5 minutes is almost never one video.** Transcribe, map the content, and check whether it's really two clips glued together with different hooks and goals. Split before cutting. Each split becomes its own 60-90s cut, hook in the first 3 seconds, typically ~75% fat trimmed.
3. **Never re-cut an already-rendered export.** Re-encoding mangles the caption sync at the splice points. Always rebuild from the raw source.

## Layer 1 — mechanical cut

Normalize to vertical 1080x1920 @ 30fps (use `platform-mastery` for the target aspect ratio if the destination isn't Instagram Reels — 9:16 for reels/stories/shorts, 4:5 for feed/portrait, 1:1 for classic feed). Concatenate multi-part raws in order first, then cut silence:

```bash
auto-editor RAW.mp4 --edit audio:threshold=5% --margin 0.12s -b:v 12M -o CUT.mp4
```

The `0.12s` margin exists so the cut doesn't eat the start of words. Without it the result sounds choppy.

## Layer 2 — semantic cut (what the machine can't do)

`auto-editor` removes silence; it does not remove a bad take, a repeated sentence, or a dead lead-in. Read the word-level transcript and decide those cuts by hand:

- Cut the dead lead-in — start on the line that matters.
- Remove flubs and repeated sentences.
- Order as hook → development → CTA.
- Never leave an orphan sentence — one whose meaning depends on context that got cut.

**Golden rule: every cut edge must land on a real silence gap.** Cutting mid-speech leaves a fragment of a word, which is what makes a cut sound amateur. Find the gaps:

```bash
ffmpeg -i RAW.mp4 -af silencedetect=noise=-32dB:d=0.15 -f null - 2>&1 | grep silence
```

Only cut where a gap exists.

### Filler words

Isolated hesitation ("uh", "um") and verbal tics can be auto-removed, but **only when there's a real ≥120ms pause before the tic**. Without a pause, the cut eats the neighboring word and produces an audible click. When tics are glued to speech with no pause at all, automation cannot fix it — the honest options are: cut whole sentences at their natural end-pauses, do a manual trim, or re-record with pauses. Never deliver it as clean when it isn't.

## Layer 3 — captions

Transcribe with word-level timestamps:

```bash
ffmpeg -i CUT.mp4 -ar 16000 -ac 1 audio.wav
whisper-cli -m "$WHISPER_MODEL" -l pt -ml 1 -sow -f audio.wav -osrt -of words
```

`-ml 1 -sow` are what make whisper return one word per line with an exact timestamp each — without them captions drift out of sync.

Maintain a small correction dictionary for terms whisper reliably mangles in this brand's niche (product names, industry jargon) — fixing the same mis-transcription by hand every time is wasted effort. Store it as `.growthOS/video-corrections.yaml` (word → correction pairs) next to `brand-voice.yaml`; create it on first use if it doesn't exist yet, and check it before any manual fix.

**Burning the captions in:** if a `legendador`-style Remotion caption project is available (check, in order: a path recorded in `.growthOS/video-corrections.yaml`, a `legendador/` directory next to the raw footage, a sibling checkout of `editor-de-video-claude/legendador`), use it — it renders word-synced captions with emphasis sizing and the zoom-punch described below. Discover and drive it the same way `video-producer` discovers its Remotion project (never hardcode the path; verify `package.json`/`node_modules` before invoking `npx remotion render`).

If no such project is available, fall back to a plain burned-in caption via ffmpeg's `drawtext` from the SRT (lower fidelity — fixed size, no emphasis/zoom, but readable and always available since it only needs ffmpeg):

```bash
ffmpeg -i CUT.mp4 -vf "subtitles=words.srt:force_style='FontName=Arial,FontSize=14,PrimaryColour=&HFFFFFF,Outline=1,Alignment=2'" -c:a copy CAPTIONED.mp4
```

Style that reads well at arm's length on a phone: pure white, heavy weight, ~56px at 1080px width, centered, thin outline, one to three words visible at a time, natural casing. No colored highlight.

Run the burned caption text through the brand's `anti_slop.banned_phrases` / `avoid` list from `brand-voice.yaml` before finalizing — a banned phrase slipping through because it came from spoken audio instead of written copy is still a brand-voice miss.

## What makes an edit look expensive

Three things, all automatable, all optional depending on the legendador/Remotion path being available (the ffmpeg-only fallback can't do these):

**Variable size.** A word with a number, or a brand-vocabulary term, renders larger and heavier than the rest. This one detail moves perceived quality the most.

**Zoom-punch.** An ~8% zoom punch, ~11 frames, eased, every time a number appears in the caption. The frame pushes into the data point.

**Corner support image.** Read the transcript, find terms that render well as an image (countries, brands, concepts), and place a rounded card in the corner while that word is spoken. Two hard rules: never during the hook, and a minimum gap between cards so they don't stack.

## Color grading

Do not apply by default. Automatic grading tends to lighten skin and shift the person's real skin tone. Only apply if explicitly requested, and approve by looking at a frame before rendering the full export.

## Verification (never skip)

Always extract frames from the result and look. Repeat until clean. Running the pipeline and delivering without watching is the video equivalent of committing without running the test.

## Platform sizing

Defer to the `platform-mastery` skill for the destination's aspect ratio, duration ceiling, and file-size expectations before layer 1 — re-cropping after captions are burned in means re-doing layer 3.

## The rule that saves the most time

Ask the person being filmed to leave a clear pause between takes. A clean take lets the pipeline get the cut right on its own. A stumbled, run-on take needs manual cutting and no amount of automation saves it — say so plainly instead of delivering a rough cut as if it were finished.
