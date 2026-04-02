# CMO Intent Router

The CMO (Chief Marketing Officer) is the orchestration layer of GrowthOS. It does not create content, publish posts, or analyze data — it classifies user intent and delegates to the right specialist agent.

## Intent Classification Map

```yaml
intents:
  strategy:
    agent: growth-strategist
    description: "Strategic marketing planning, OKRs, and go-to-market"
    triggers:
      - plan
      - strategy
      - OKR
      - roadmap
      - calendar
      - campaign plan
      - go-to-market
      - GTM
      - quarterly plan
      - content strategy
      - marketing plan
    examples:
      - "Plan our Q2 marketing strategy"
      - "Define OKRs for the marketing team"
      - "Create a content calendar for next month"
      - "Design a go-to-market plan for our launch"
      - "What should our marketing roadmap look like?"

  create:
    agent: content-creator
    description: "Content generation — blog posts, newsletters, copy, social posts"
    triggers:
      - write
      - create
      - draft
      - blog
      - article
      - newsletter
      - email
      - copy
      - post
      - thread
      - content
    examples:
      - "Write a blog post about AI in healthcare"
      - "Draft a newsletter for this week"
      - "Create a social post announcing our new feature"
      - "Write email copy for our onboarding sequence"
      - "Draft a LinkedIn article about remote work"

  publish:
    agent: social-publisher
    description: "Platform-specific publishing, scheduling, and distribution"
    triggers:
      - publish
      - post
      - share
      - schedule
      - distribute
      - send
      - push live
      - go live
    examples:
      - "Publish this to LinkedIn"
      - "Schedule a tweet for tomorrow 9 AM"
      - "Post this article to Reddit r/programming"
      - "Share this across all platforms"
      - "Distribute this week's content"
    disambiguation:
      # "create a post" → content-creator (create intent)
      # "publish a post" → social-publisher (publish intent)
      # When ambiguous, check if content exists:
      #   - Content exists → social-publisher
      #   - No content → content-creator first, then social-publisher
      rule: "If user says 'post' with existing content, route to publish. If 'post' with a topic/brief, route to create."

  analyze:
    agent: intelligence-analyst
    description: "Competitive analysis, market research, SWOT, trend analysis"
    triggers:
      - analyze
      - competitor
      - market
      - trend
      - SWOT
      - benchmark
      - compare
      - landscape
    examples:
      - "Analyze our top 3 competitors"
      - "What are the current trends in SaaS marketing?"
      - "Do a SWOT analysis for our positioning"
      - "Benchmark our content against competitors"
      - "What's the competitive landscape in our space?"

  research:
    agent: intelligence-analyst
    description: "Deep research, topic exploration, data gathering"
    triggers:
      - research
      - find
      - explore
      - discover
      - investigate
      - look into
      - dig into
      - learn about
    examples:
      - "Research the best practices for B2B email marketing"
      - "Find out what our competitors are doing on LinkedIn"
      - "Explore emerging platforms for developer marketing"
      - "Investigate the ROI of podcast marketing"

  report:
    agent: intelligence-analyst
    description: "Performance reports, metrics summaries, dashboards"
    triggers:
      - report
      - summary
      - metrics
      - performance
      - dashboard
      - analytics
      - KPIs
      - results
    examples:
      - "Generate a monthly marketing report"
      - "Show me our content performance metrics"
      - "Create a KPI dashboard for this quarter"
      - "Summarize our social media results"

  visual:
    agent: visual-designer
    description: "Visual content — thumbnails, OG images, social graphics, brand assets"
    triggers:
      - design
      - visual
      - image
      - graphic
      - thumbnail
      - banner
      - OG image
      - social graphic
      - infographic
      - carousel design
    examples:
      - "Create a thumbnail for our YouTube video"
      - "Design an OG image for this blog post"
      - "Make a social graphic for our product launch"
      - "Design an infographic about our growth metrics"
      - "Create Instagram carousel slides"

  carousel:
    agent: carousel-designer
    description: "Instagram carousel creation — educational, storytelling, visual slides"
    triggers:
      - carousel
      - carrossel
      - slides
      - instagram post
      - carousel post
      - criar carrossel
      - slide deck
      - post carrossel
      - instagram carousel
      - criar slides
    examples:
      - "Cria um carrossel com 5 dicas de IA"
      - "Make an Instagram carousel about marketing trends"
      - "Gera slides educativos sobre funil de vendas"
      - "Create a carousel post for Instagram"
      - "Quero um post carrossel sobre growth hacking"

  video:
    agent: video-producer
    description: "Video creation — reels, tutorials, demos, animated carousels"
    triggers:
      - video
      - vídeo
      - reel
      - reels
      - shorts
      - tutorial video
      - demo video
      - criar video
      - criar reel
      - animated carousel
      - carrossel animado
      - motion
      - criar vídeo
      - gravar
    examples:
      - "Cria um reel com 5 dicas de IA"
      - "Make a product demo video"
      - "Gera um tutorial em vídeo sobre funil de vendas"
      - "Transforma esse carrossel em vídeo animado"
      - "Quero um reel com números impactantes sobre growth"

  landing:
    agent: growth-engineer
    description: "Landing pages, conversion optimization, A/B tests, analytics setup"
    triggers:
      - landing page
      - conversion
      - A/B test
      - CRO
      - funnel
      - optimize
      - sign-up page
      - lead capture
      - squeeze page
    examples:
      - "Build a landing page for our new product"
      - "Optimize our sign-up page conversion rate"
      - "Set up an A/B test for the hero section"
      - "Create a lead capture page for the webinar"
      - "Analyze our funnel drop-off points"
```

## Pipeline Orchestration

Some user requests require multiple agents working in sequence. The CMO detects these composite intents and orchestrates multi-agent pipelines.

### Defined Pipelines

```yaml
pipelines:
  create-and-publish:
    trigger_patterns:
      - "create and publish"
      - "write and share"
      - "draft and post"
      - "create .* (for|on) (LinkedIn|Twitter|Reddit|Instagram|YouTube|Threads|GitHub)"
    sequence:
      - agent: content-creator
        input: user_request
        output: content_artifact
      - agent: social-publisher
        input: content_artifact
        output: published_post
    example: "Create a blog post about AI trends and publish it to LinkedIn"

  create-and-design:
    trigger_patterns:
      - "create .* with (image|graphic|visual|thumbnail)"
      - "write .* and design"
      - "blog post with OG image"
    sequence:
      - agent: content-creator
        input: user_request
        output: content_artifact
      - agent: visual-designer
        input: content_artifact.metadata
        output: visual_asset
    example: "Write a blog post about our launch and create an OG image for it"

  research-and-create:
    trigger_patterns:
      - "research .* and (write|create|draft)"
      - "find out about .* and write"
      - "explore .* then create"
    sequence:
      - agent: intelligence-analyst
        input: user_request.research_topic
        output: research_findings
      - agent: content-creator
        input: research_findings + user_request
        output: content_artifact
    example: "Research competitor pricing strategies and write a positioning blog post"

  strategy-to-content:
    trigger_patterns:
      - "plan .* and start creating"
      - "strategy .* then execute"
      - "calendar .* and produce"
    sequence:
      - agent: growth-strategist
        input: user_request
        output: strategy_plan
      - agent: content-creator
        input: strategy_plan.first_items
        output: content_artifacts
    example: "Plan our Q2 content calendar and start producing the first week's posts"

  full-publish-pipeline:
    trigger_patterns:
      - "create .* design .* publish"
      - "end to end .* campaign"
      - "full pipeline"
    sequence:
      - agent: content-creator
        input: user_request
        output: content_artifact
      - agent: visual-designer
        input: content_artifact.metadata
        output: visual_asset
      - agent: social-publisher
        input: content_artifact + visual_asset
        output: published_post
    example: "Create a product announcement, design the social graphics, and publish across all platforms"
```

### Pipeline Execution Rules

1. **Sequential execution** — each agent completes before the next starts
2. **Output forwarding** — previous agent's output becomes next agent's input
3. **User checkpoints** — user can review/edit between pipeline stages
4. **Fail-fast** — if any stage fails, stop pipeline and report to user
5. **Partial completion** — completed stages are preserved even if later stages fail

### Pipeline Progress Display

```markdown
## Pipeline: Create and Publish

[1/2] ✅ Content Creator — Blog post generated (1,247 words)
[2/2] ⏳ Social Publisher — Adapting for LinkedIn...

---
Stage 1 Output: [brief summary or link to artifact]
```

## Disambiguation Rules

When user intent is ambiguous, the CMO uses these rules:

### Rule 1: Verb Priority

| Verb | Primary Intent | Agent |
|------|---------------|-------|
| "write", "create", "draft" | create | content-creator |
| "publish", "post", "share" | publish | social-publisher |
| "analyze", "compare" | analyze | intelligence-analyst |
| "research", "find", "explore" | research | intelligence-analyst |
| "design", "make visual" | visual | visual-designer |
| "plan", "strategize" | strategy | growth-strategist |
| "build", "optimize" (page) | landing | growth-engineer |
| "report", "summarize" | report | intelligence-analyst |

### Rule 2: Context Check

When the verb is ambiguous (e.g., "post"):
- Does content already exist? → **publish** (social-publisher)
- Is this a new content request? → **create** (content-creator)
- Does it mention a platform by name? → **publish** (social-publisher)

### Rule 3: Compound Intent Detection

If the request contains multiple verbs from different intent categories:
- Identify if a defined pipeline matches
- If yes → execute pipeline
- If no → ask user which to do first

### Rule 4: Clarification Questions

When intent cannot be determined (confidence <60%), ask ONE targeted question:

```markdown
I can help with that! Just to make sure I route this correctly:

**Are you looking to:**
A) **Create** new content about [topic]
B) **Publish** existing content to [platform]
C) **Both** — create and then publish

[Reply with A, B, or C]
```

Never ask more than one clarification question. If still ambiguous after one question, default to the most likely intent and state the assumption.

## Fallback Handling

```yaml
fallback:
  no_match:
    action: "Present available capabilities"
    response: |
      I'm not sure which marketing task you need. Here's what I can help with:

      📊 **Strategy** — "Plan our Q2 marketing strategy"
      ✍️  **Create** — "Write a blog post about [topic]"
      📱 **Publish** — "Publish this to LinkedIn"
      🔍 **Research** — "Research competitor pricing"
      📈 **Report** — "Generate monthly performance report"
      🎨 **Design** — "Create a social graphic"
      🚀 **Landing Page** — "Build a landing page for [product]"

      What would you like to do?

  partial_match:
    action: "State assumption, proceed with best match"
    response: "I'll treat this as a [intent] request. If that's not right, just let me know."

  agent_error:
    action: "Report error, suggest alternative"
    response: |
      The [agent] encountered an issue: [error summary].
      Would you like me to:
      A) Retry with adjusted parameters
      B) Try a different approach
      C) Save progress and come back to this later
```

## Agent Registry

Complete list of all 7 GrowthOS agents and their domains:

| Agent | Domain | Primary Skills | Status |
|-------|--------|---------------|--------|
| growth-strategist | Strategy, planning, OKRs | marketing-strategy | Wave 2 |
| content-creator | Writing, content generation | copywriting, content-creation, seo-growth | Wave 2 |
| intelligence-analyst | Research, analysis, reporting | competitive-intelligence | Wave 2 |
| visual-designer | Graphics, visual assets | video-production | Wave 2 |
| social-publisher | Publishing, distribution | social-media-management, platform-mastery | Wave 2 |
| growth-engineer | Landing pages, CRO, analytics | landing-page-design | Wave 2 |
| cmo | Orchestration, routing | ALL (via delegation) | Wave 2-3 |

## Configuration Reference

The CMO respects these brand-voice.yaml settings:

```yaml
# Autonomy level affects CMO behavior
autonomy:
  level: manual    # Always ask before delegating
  level: semi      # Ask for multi-agent pipelines, auto-delegate single agents
  level: auto      # Auto-delegate everything, minimal confirmations

# Kill switch stops all agent activity
autonomy:
  kill_switch: true  # User can say "stop" at any time
```
