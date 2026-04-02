# GrowthOS Output Contracts

Unified schema reference for every output type across all 9 GrowthOS skills. Agents MUST conform to these contracts to ensure outputs are parseable, consistent, and pipeline-compatible.

## Contract Index

| Skill | Output Type | Format | Schema Section |
|-------|------------|--------|----------------|
| marketing-strategy | Marketing plan | Markdown | [Strategy Outputs](#strategy-outputs) |
| marketing-strategy | Campaign brief | YAML | [Strategy Outputs](#strategy-outputs) |
| copywriting | Headlines | Markdown | [Copy Outputs](#copy-outputs) |
| copywriting | Email sequence | Markdown | [Copy Outputs](#copy-outputs) |
| copywriting | Ad copy variants | Markdown | [Copy Outputs](#copy-outputs) |
| content-creation | Blog post | Markdown | [Content Outputs](#content-outputs) |
| content-creation | Newsletter | Markdown | [Content Outputs](#content-outputs) |
| content-creation | Content calendar | YAML | [Content Outputs](#content-outputs) |
| seo-growth | Keyword research | YAML | [SEO Outputs](#seo-outputs) |
| seo-growth | SEO audit | Markdown | [SEO Outputs](#seo-outputs) |
| social-media-management | Social posts | Markdown | [Social Outputs](#social-outputs) |
| social-media-management | Posting schedule | YAML | [Social Outputs](#social-outputs) |
| competitive-intelligence | Competitor report | Markdown | [Intelligence Outputs](#intelligence-outputs) |
| competitive-intelligence | SWOT analysis | YAML | [Intelligence Outputs](#intelligence-outputs) |
| video-production | Video script | Markdown | [Video Outputs](#video-outputs) |
| video-production | Thumbnail spec | YAML | [Video Outputs](#video-outputs) |
| video-production | YouTube description | Markdown | [Video Outputs](#video-outputs) |
| video-production | Storyboard | YAML | [Video Outputs](#video-outputs) |
| landing-page-design | Landing page | HTML | [Landing Page Outputs](#landing-page-outputs) |
| landing-page-design | A/B variant spec | YAML | [Landing Page Outputs](#landing-page-outputs) |
| landing-page-design | A/B test plan | YAML + HTML | [Landing Page Outputs](#landing-page-outputs) |
| landing-page-design | Tracking plan | YAML | [Landing Page Outputs](#landing-page-outputs) |
| landing-page-design | CRO report | YAML + MD | [Landing Page Outputs](#landing-page-outputs) |
| platform-mastery | Platform brief | Markdown | [Platform Outputs](#platform-outputs) |
| platform-mastery | Cross-platform plan | YAML | [Platform Outputs](#platform-outputs) |

---

## Strategy Outputs

### Marketing Plan

```yaml
contract:
  format: markdown
  required_sections:
    - executive_summary
    - target_audience
    - positioning
    - channels
    - campaign_timeline
    - kpis
    - budget_allocation
  frontmatter:
    brand: "[from brand-voice.yaml]"
    date: "[ISO 8601]"
    version: "[semver]"
    status: "[draft | review | approved]"
```

### Campaign Brief

```yaml
contract:
  format: yaml
  schema:
    campaign:
      name: string
      objective: string
      audience:
        primary: string
        secondary: string
      channels: string[]
      timeline:
        start: date
        end: date
        milestones: {date: string}[]
      budget: number
      kpis:
        - metric: string
          target: number
          unit: string
      messaging:
        headline: string
        value_prop: string
        cta: string
      assets_needed: string[]
```

---

## Copy Outputs

### Headlines

```yaml
contract:
  format: markdown
  structure: |
    ## Headlines for [Context]

    ### Primary (recommended)
    [Headline]

    ### Variants
    1. [Benefit-led variant]
    2. [Curiosity-led variant]
    3. [Social-proof-led variant]
    4. [Urgency-led variant]

    ### Rationale
    [Why primary was chosen]
  constraints:
    max_length: 70 chars
    anti_slop: "enforced from brand-voice.yaml"
```

### Email Sequence

```yaml
contract:
  format: markdown
  structure_per_email:
    subject_line: "string, <50 chars"
    preview_text: "string, <90 chars"
    body: "markdown"
    cta: "single CTA per email"
    send_timing: "delay from trigger or previous email"
  sequence_metadata:
    trigger: "event that starts the sequence"
    goal: "conversion action"
    total_emails: number
    cadence: "timing between emails"
```

### Ad Copy Variants

```yaml
contract:
  format: markdown
  per_variant:
    platform: "[google | meta | linkedin | twitter]"
    headline: "string, platform char limit"
    description: "string, platform char limit"
    cta: "string"
    display_url: "string"
    audience_note: "who this targets"
  minimum_variants: 3
  constraints:
    google_headline: "<30 chars"
    google_description: "<90 chars"
    meta_primary_text: "<125 chars (recommended)"
    meta_headline: "<40 chars"
    linkedin_intro: "<150 chars"
```

---

## Content Outputs

### Blog Post

```yaml
contract:
  format: markdown
  frontmatter:
    title: string
    slug: string
    meta_description: "string, <160 chars"
    keywords: string[]
    author: string
    date: date
    category: string
    reading_time: "N min"
  required_sections:
    - introduction (hook + thesis)
    - body (H2 sections with H3 subsections)
    - conclusion (summary + CTA)
  constraints:
    word_count: "800-2500 words"
    heading_hierarchy: "H1 > H2 > H3 only"
    internal_links: "2-5 suggested"
    images_alt_text: "specified for each image placeholder"
```

### Content Calendar

```yaml
contract:
  format: yaml
  schema:
    calendar:
      period: "YYYY-MM"
      entries:
        - date: date
          platform: string
          content_type: string
          topic: string
          status: "[planned | drafted | scheduled | published]"
          owner: string
          notes: string
      themes:
        - week: number
          theme: string
```

---

## SEO Outputs

### Keyword Research

```yaml
contract:
  format: yaml
  schema:
    research:
      seed_topic: string
      keywords:
        - keyword: string
          search_volume: "[estimated range: low|medium|high]"
          difficulty: "[low|medium|high]"
          intent: "[informational|navigational|transactional|commercial]"
          priority: "[P0|P1|P2]"
          content_type: "[blog|landing|product|comparison]"
      clusters:
        - name: string
          primary_keyword: string
          supporting_keywords: string[]
          content_gap: string
```

### SEO Audit

```yaml
contract:
  format: markdown
  required_sections:
    - executive_summary
    - technical_issues (with severity)
    - on_page_analysis
    - content_gaps
    - recommendations (prioritized)
  issue_format:
    severity: "[critical|high|medium|low]"
    description: string
    impact: string
    fix: string
```

---

## Social Outputs

### Social Posts

```yaml
contract:
  format: markdown
  per_post:
    platform: string
    content: "string, within platform char limit"
    hashtags: "string[], platform-appropriate count"
    media: "description of image/video needed"
    cta: string
    posting_time: "suggested time"
    notes: "platform-specific optimization notes"
  constraints:
    twitter_length: "<=280 chars"
    linkedin_length: "<=3000 chars"
    instagram_caption: "<=2200 chars"
    threads_length: "<=500 chars"
    anti_slop: "enforced from brand-voice.yaml"
```

### Posting Schedule

```yaml
contract:
  format: yaml
  schema:
    schedule:
      period: "YYYY-MM-DD to YYYY-MM-DD"
      entries:
        - datetime: "ISO 8601"
          platform: string
          content_ref: "reference to social post"
          status: "[scheduled|posted|skipped]"
          engagement_target: string
```

---

## Intelligence Outputs

### Competitor Report

```yaml
contract:
  format: markdown
  required_sections:
    - overview (competitor landscape)
    - per_competitor:
        - name
        - positioning
        - strengths
        - weaknesses
        - content_strategy
        - channels
        - key_metrics (if available)
    - opportunities
    - threats
    - recommendations
```

### SWOT Analysis

```yaml
contract:
  format: yaml
  schema:
    swot:
      subject: string
      strengths:
        - point: string
          evidence: string
      weaknesses:
        - point: string
          evidence: string
      opportunities:
        - point: string
          evidence: string
      threats:
        - point: string
          evidence: string
      priority_actions: string[]
```

---

## Video Outputs

### Video Script

```yaml
contract:
  format: markdown
  frontmatter:
    title: "string, <60 chars"
    target_length: "N minutes"
    audience: string
    core_promise: string
  required_sections:
    - hook (0-5s)
    - setup (5-30s)
    - body (sectioned with timestamps)
    - cta (final segment)
  seo_metadata:
    title: "string, <60 chars"
    description: "see YouTube description contract"
    tags: "string[], 10-15"
    chapters: "timestamp + title pairs"
```

### Thumbnail Spec

```yaml
contract:
  format: yaml
  schema:
    thumbnail:
      layout: "[split|centered|thirds|before-after]"
      dimensions: "1280x720"
      background:
        type: "[solid|gradient|image-blur]"
        value: string
      text:
        headline: "string, 3-5 words max"
        font_weight: bold
        color: string
        position: string
      face:
        expression: string
        position: "[left|right]"
      accent_elements:
        - type: string
          position: string
          color: string
      variants: 2  # always produce 2 for A/B testing
```

### YouTube Description

```yaml
contract:
  format: markdown
  structure:
    - hook_sentence
    - summary_paragraph
    - resources_links
    - chapters (timestamps)
    - key_takeaways (bullets)
    - cta_paragraph
    - hashtags (3-5)
  constraints:
    first_150_chars: "critical — shown in search results"
    chapters_start: "0:00"
    min_chapters: 3
```

### Storyboard

```yaml
contract:
  format: yaml
  schema:
    storyboard:
      scenes:
        - scene_number: number
          timestamp: string
          visual:
            type: "[talking-head|screen-recording|b-roll|animation|text-overlay]"
            description: string
          audio:
            narration: string
            music: string
            sfx: string
          text_overlay: string
          transition: "[cut|fade|zoom|swipe]"
          retention_device: "[hook|open-loop|proof|direct-address|none]"
```

---

## Landing Page Outputs

### Landing Page

```yaml
contract:
  format: html
  type: single-file
  constraints:
    no_external_dependencies: true
    embedded_css: true
    system_font_stack: true
    max_file_size: "100KB"
    no_javascript: "unless strictly required"
    responsive: true
    accessible: "WCAG 2.1 AA"
  required_sections:
    - meta_tags (SEO + Open Graph)
    - hero_section (headline + CTA above fold)
    - social_proof
    - features_benefits
    - cta_repeat
    - footer
  required_elements:
    - skip_link
    - semantic_html
    - alt_text_on_all_visuals
    - focus_states
    - lang_attribute
```

### A/B Variant Spec (Simple)

```yaml
contract:
  format: yaml
  schema:
    ab_variants:
      - element: string
        control: string
        variant: string
        hypothesis: string
        metric: "[ctr|conversion|bounce_rate|scroll_depth]"
    minimum_variants: 2
```

### A/B Test Plan (Advanced)

```yaml
contract:
  format: yaml + html
  template: "templates/reports/ab-test-template.md"
  schema:
    ab_test_plan:
      test_name: string
      status: "[draft | running | completed | archived]"
      hypothesis:
        observation: string
        change: string
        expected_outcome: string
        reasoning: string
        primary_metric: string
        secondary_metrics: string[]
        minimum_detectable_effect: string
      control:
        id: "control"
        file: string  # separate HTML file
        description: string
      variants:
        - id: string
          change: string
          file: string  # separate HTML file per variant
          hypothesis: string
          expected_impact: string
      traffic_split:
        method: "[equal | weighted]"
        allocation: { variant_id: number }
      duration:
        minimum_days: number
        minimum_conversions_per_variant: number
        confidence_level: number
      success_criteria:
        primary_metric: string
        minimum_improvement: string
        statistical_significance: number
  constraints:
    min_variants: 1
    max_variants: 4
    each_variant_separate_html: true
    hypothesis_required: true
```

### Analytics Tracking Plan

```yaml
contract:
  format: yaml
  template: "templates/reports/tracking-plan-template.md"
  schema:
    tracking_plan:
      project: string
      version: string
      last_updated: date
      analytics_tool: "[GA4 | Plausible | Umami]"
      events:
        - name: string  # snake_case
          description: string
          trigger: string
          category: "[engagement | conversion | navigation | error]"
          properties:
            - name: string
              type: "[string | number | boolean]"
              description: string
              required: boolean
              example: string
          kpi_contribution: string
      properties:
        global:
          - name: string
            type: string
            description: string
        user:
          - name: string
            type: string
            description: string
      kpis:
        - name: string
          definition: string
          target: string
          events_used: string[]
          dashboard_location: string
      implementation_snippets:
        GA4: string
        Plausible: string
        Umami: string
  constraints:
    events_must_have_kpis: true
    snake_case_event_names: true
    implementation_snippet_required: true
    no_pii_in_properties: true
```

### CRO Report

```yaml
contract:
  format: yaml + markdown
  template: "templates/reports/cro-report-template.md"
  schema:
    funnel_analysis:
      funnel_name: string
      analysis_date: date
      total_entry_traffic: number
      stages:
        - name: string
          traffic: number
          conversion_to_next: string  # percentage
          drop_off_rate: string  # percentage
      drop_offs:
        - stage_transition: string
          drop_off_rate: string
          severity: "[critical | high | medium | low]"
          identified_causes:
            - cause: string
              evidence: string
              affected_segment: string
      recommendations:
        - id: string  # REC-NNN
          title: string
          stage: string
          drop_off_cause: string
          change_description: string
          ice_score:
            impact: number   # 1-10
            confidence: number  # 1-10
            ease: number   # 1-10
            total: number  # I x C x E (max 1000)
          expected_improvement: string
          implementation_effort: string
          test_plan: string
  constraints:
    ice_scored: true
    recommendations_sorted_by_ice_desc: true
    max_priority_recommendations: 5
    severity_thresholds:
      critical: ">80% drop-off"
      high: "60-80%"
      medium: "40-60%"
      low: "<40%"
```

---

## Platform Outputs

### Platform Brief

```yaml
contract:
  format: markdown
  required_sections:
    - platform_name
    - algorithm_summary
    - content_rules
    - optimal_format
    - anti_patterns
    - posting_schedule
```

### Cross-Platform Plan

```yaml
contract:
  format: yaml
  schema:
    cross_platform:
      source_content: string
      adaptations:
        - platform: string
          format: string
          tone_adjustment: string
          length: string
          cta: string
          posting_time: string
          hashtag_strategy: string
```

---

## Global Constraints

All outputs MUST respect:

1. **brand-voice.yaml**: Tone, banned phrases, anti-slop rules
2. **Autonomy level**: Respect `manual | semi | auto` from config
3. **Preview before publish**: When `require_preview: true`
4. **Dry run default**: When `dry_run_default: true`, output preview only
5. **Format consistency**: Use exact structure defined in contracts
6. **No hallucinated data**: Metrics, stats, and quotes must be sourced or clearly marked as examples

---

## Carousel Outputs

### Carousel HTML

```yaml
contract:
  skill: instagram-carousel
  format: html
  type: "1 file per slide + 1 preview file"
  constraints:
    max_slides: 10
    min_slides: 3
    max_words_per_slide: 50
    headline_max_words:
      cover: 7
      content: 10
    file_size: "<15KB per slide"
    dimensions: "1080x1350 (default, portrait 4:5)"
  required_elements:
    - cover_slide (headline + hook)
    - content_slides (body with visual hierarchy)
    - cta_slide (call to action + handle)
  structure_per_slide:
    file: "slide-{N}.html"
    embedded_css: true
    no_external_dependencies: true
    system_font_stack: true
    responsive: false  # fixed dimensions for Instagram
  preview:
    file: "preview.html"
    description: "Single-page preview showing all slides in sequence for review"
  metadata:
    topic: string
    style: string
    type: "[educational | storytelling | tips | listicle | case-study]"
    slide_count: number
    brand: "[from brand-voice.yaml]"
    dimensions: "WxH"
```

---

## Video Outputs

### Video MP4

```yaml
contract:
  skill: remotion-video
  format: "MP4 H.264"
  max_duration: "180s"
  max_file_size: "50MB"
  fps: 30
  aspect_ratios:
    - "9:16"
    - "16:9"
    - "4:5"
  output_directory: ".growthOS/output/videos/{timestamp}/"
  constraints:
    codec: "H.264"
    container: "MP4"
    audio: "none (motion graphics only)"
    progressive_download: true
```

### Storyboard YAML

```yaml
contract:
  skill: remotion-video
  format: yaml
  max_scenes: 20
  required_fields:
    - format
    - duration_seconds
    - scenes
  schema:
    storyboard:
      format: "reel | explainer | carousel-animated"
      duration_seconds: number
      aspect_ratio: "9:16 | 16:9 | 4:5"
      template: string
      scenes:
        - scene: number
          type: "hook | point | comparison | number | step | demo | cta"
          duration: number
          text: string
          subtext: string
          icon: string
          animation: string
          transition: string
```

### Composition JSON

```yaml
contract:
  skill: remotion-video
  format: json
  required_fields:
    - template
    - fps
    - width
    - height
    - durationInFrames
    - props
  schema:
    composition:
      template: string
      fps: 30
      width: number
      height: number
      durationInFrames: number
      props:
        brand:
          name: string
          handle: string
          colors:
            primary: string
            secondary: string
            background: string
            text: string
            accent: string
          watermark_position: "bottom-right | bottom-left | top-right"
        scenes: "SceneProps[]"
        showProgressBar: boolean
        showWatermark: boolean
```
