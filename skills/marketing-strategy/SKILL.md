---
name: marketing-strategy
description: Strategic marketing planning, growth frameworks (AARRR, ICE, RICE), positioning, OKRs, campaign planning, content pillars, and market analysis
---

# Marketing Strategy Skill

## Trigger Conditions

Use this skill when the user asks to:
- Create or refine a marketing strategy
- Plan a campaign or launch
- Define marketing OKRs or KPIs
- Analyze market position or competitive landscape
- Build content pillars or editorial calendars
- Prioritize marketing initiatives
- Conduct TAM/SAM/SOM analysis
- Design a growth model or funnel

---

## Brand Voice Integration

**MANDATORY:** Before generating ANY strategy content, load the brand voice configuration.

```python
from growthOS_shared.config import load_brand_voice
brand = load_brand_voice()
```

All strategy outputs must align with `brand.tone`, respect `brand.avoid` terms, and pass `anti_slop` validation. Strategy documents that ignore brand voice are invalid.

---

## Growth Frameworks

### AARRR — Pirate Metrics Framework

The AARRR framework (Dave McClure, 500 Startups) maps the full customer lifecycle into 5 measurable stages. Use this as the **primary diagnostic framework** when a user needs to understand where their growth is leaking.

| Stage | Question | Example Metrics |
|-------|----------|-----------------|
| **Acquisition** | How do users find us? | Visits, signups, CAC, channel attribution |
| **Activation** | Do they have a great first experience? | Onboarding completion, time-to-value, aha-moment rate |
| **Retention** | Do they come back? | DAU/MAU, churn rate, cohort retention curves |
| **Revenue** | Do they pay? | ARPU, LTV, conversion rate, MRR/ARR |
| **Referral** | Do they tell others? | NPS, viral coefficient (k-factor), referral rate |

**How to apply AARRR:**

1. **Diagnose first** — Ask: "Which stage is the biggest bottleneck?" Use data if available, or hypothesize based on product maturity.
2. **One stage at a time** — Focus resources on the weakest stage. Improving Retention before scaling Acquisition prevents burning budget on users who churn.
3. **Set stage-specific OKRs** — Each stage gets its own Objective and 2-3 Key Results.
4. **Measure cohorts, not aggregates** — Weekly or monthly cohorts reveal trends that aggregate numbers hide.

**Stage-specific playbooks:**

- **Acquisition bottleneck:** Audit channel mix, test 3 new channels with small budget, measure CAC per channel. Consider content marketing (low CAC, slow) vs paid (high CAC, fast).
- **Activation bottleneck:** Map the first 5 minutes of user experience. Identify the "aha moment" (the action that correlates with retention). Reduce steps to reach it.
- **Retention bottleneck:** Build cohort analysis. Identify the "habit loop" — what makes users return? Add engagement hooks (notifications, digests, streaks). Segment by behavior.
- **Revenue bottleneck:** Test pricing tiers. Add annual plans (reduce churn). Identify expansion revenue opportunities (upsell, cross-sell). Optimize trial-to-paid flow.
- **Referral bottleneck:** Add referral program with bilateral incentives. Measure k-factor. Make sharing frictionless and contextual (share after a success moment, not randomly).

### ICE Scoring — Quick Prioritization

ICE (Sean Ellis) is a lightweight scoring model for rapid prioritization of growth experiments.

| Dimension | Score 1-10 | Question |
|-----------|-----------|----------|
| **Impact** | How much will this move the target metric? | 1 = negligible, 10 = 2x improvement |
| **Confidence** | How sure are we this will work? | 1 = wild guess, 10 = proven playbook |
| **Ease** | How easy is it to implement? | 1 = months of eng work, 10 = deploy today |

**ICE Score = (Impact + Confidence + Ease) / 3**

**When to use ICE:** For backlogs of 10-30 ideas that need quick ranking. Not suitable for strategic decisions requiring deeper analysis.

**Pitfalls to avoid:**
- Confidence inflation — teams overestimate confidence on their own ideas. Require evidence links.
- Ease bias — easy tasks get prioritized over high-impact hard tasks. Weight Impact 2x if needed.
- Score anchoring — first scorer sets the range. Use blind scoring then average.

### RICE Prioritization — Data-Driven Ranking

RICE (Intercom) adds Reach to create a more rigorous prioritization model.

| Dimension | Definition | Unit |
|-----------|-----------|------|
| **Reach** | How many people will this affect per time period? | Users/quarter |
| **Impact** | How much will each person be affected? | 0.25 (minimal) to 3 (massive) |
| **Confidence** | How confident are we in estimates? | 50%-100% |
| **Effort** | How much work is required? | Person-months |

**RICE Score = (Reach × Impact × Confidence) / Effort**

**When to use RICE:** For roadmap prioritization with 5+ competing initiatives. Best when you have data on Reach.

**Confidence calibration:**
- 100% = have data proving it works
- 80% = strong qualitative signal (user interviews, competitor proof)
- 50% = intuition only — acceptable but flag it

---

## Positioning Frameworks

### Category Design

Category design (Play Bigger methodology) means defining and owning a new market category rather than competing in an existing one.

**Steps:**
1. **Identify the problem the market doesn't know it has** — Frame a "before" and "after" that shifts perception.
2. **Name the category** — The name should be intuitive, memorable, and googlable. Test with 5 people outside your industry.
3. **Lightning strike** — Coordinate a launch event that educates the market on the category and your position as the leader.
4. **Category POV document** — Write a 2-3 page manifesto explaining why the old way is broken and what the new category enables.

**When NOT to use:** If you're entering an established category with a better/cheaper product, compete on positioning within that category instead.

### Jobs-to-be-Done (JTBD)

JTBD (Clayton Christensen, Tony Ulwick) reframes positioning around the job the customer is hiring your product to do.

**Job statement formula:**
```
When [situation], I want to [motivation], so I can [expected outcome].
```

**Example:**
```
When I'm planning next quarter's content, I want to quickly generate
platform-specific posts, so I can maintain consistent presence without
spending 20 hours per week on content.
```

**Applying JTBD to positioning:**
1. Interview 10-15 customers about their last purchase decision
2. Extract the functional, emotional, and social jobs
3. Identify over-served jobs (competitors do this well) and under-served jobs (gap)
4. Position your product around the under-served jobs
5. Write messaging that directly addresses the job, not your features

### Positioning Canvas

Use this structured canvas to define positioning:

```yaml
positioning:
  target_customer: "[Specific persona with problem]"
  category: "[Market category you compete in or create]"
  key_differentiator: "[The one thing you do uniquely well]"
  proof_points:
    - "[Data point or case study 1]"
    - "[Data point or case study 2]"
    - "[Data point or case study 3]"
  competitive_alternative: "[What customers use today instead]"
  unique_value: "[The transformation you enable]"
```

---

## Content Pillar Methodology

Content pillars are 3-5 core themes that all content maps back to. They ensure consistency, reduce content planning overhead, and build topical authority.

### Building Content Pillars

**Step 1: Audit your expertise zones**
List everything your team/product knows deeply. Group into 5-8 clusters.

**Step 2: Map to audience jobs**
For each cluster, answer: "Does my audience actively seek information about this?"
Eliminate clusters with no audience demand.

**Step 3: Narrow to 3-5 pillars**
Criteria for a strong pillar:
- You have genuine expertise (not generic takes)
- Your audience has proven demand (search volume, community questions)
- Competitors underserve this topic
- It connects to your product's value proposition

**Step 4: Define sub-topics per pillar**
Each pillar should have 10-20 sub-topics. These become individual content pieces.

**Step 5: Map pillars to funnel stages**
```
Pillar A → TOFU (awareness) + MOFU (consideration)
Pillar B → MOFU (consideration) + BOFU (decision)
Pillar C → TOFU (awareness)
```

### Content Pillar Template

```yaml
pillar:
  name: "[Pillar Name]"
  description: "[1-2 sentence description]"
  target_persona: "[Primary persona]"
  funnel_stages: [awareness, consideration, decision]
  sub_topics:
    - name: "[Sub-topic]"
      format: [blog, video, social, newsletter]
      priority: [high, medium, low]
      search_intent: [informational, navigational, transactional]
  kpis:
    - metric: "[e.g., organic traffic to pillar pages]"
      target: "[e.g., 5,000 visits/month within 6 months]"
```

---

## Campaign Planning Structure

### Campaign Brief Template

Every campaign should start with a brief that answers these questions:

```yaml
campaign:
  name: "[Campaign Name]"
  objective: "[Single clear objective — use SMART format]"
  target_audience:
    primary: "[Persona with demographics and psychographics]"
    secondary: "[If applicable]"
  key_message: "[One sentence — what should the audience think/feel/do?]"
  channels:
    - channel: "[e.g., LinkedIn]"
      role: "[e.g., thought leadership, lead gen]"
      budget: "[If applicable]"
      content_types: ["posts", "articles", "ads"]
  timeline:
    start: "YYYY-MM-DD"
    end: "YYYY-MM-DD"
    milestones:
      - date: "YYYY-MM-DD"
        deliverable: "[What ships]"
  success_metrics:
    primary: "[The ONE metric that defines success]"
    secondary:
      - "[Supporting metric 1]"
      - "[Supporting metric 2]"
  budget:
    total: "[Amount]"
    breakdown:
      - category: "[e.g., paid ads, tools, freelancers]"
        amount: "[Amount]"
  risks:
    - risk: "[What could go wrong]"
      mitigation: "[How to prevent or respond]"
```

### Campaign Types and Playbooks

| Type | Duration | Focus | Example |
|------|----------|-------|---------|
| **Launch** | 2-4 weeks | Awareness + Activation | Product launch, feature release |
| **Evergreen** | Ongoing | SEO + Content authority | Blog series, resource hub |
| **Seasonal** | 1-2 weeks | Relevance + Urgency | Black Friday, industry events |
| **Nurture** | 4-8 weeks | Education + Conversion | Email sequence, webinar series |
| **Referral** | Ongoing | Viral + Retention | Referral program, community |

---

## Competitive Positioning Matrix

### Building a Competitive Matrix

**Step 1: Identify competitors**
- Direct competitors (same solution, same audience)
- Indirect competitors (different solution, same problem)
- Substitutes (what people use instead, including doing nothing)

**Step 2: Define comparison dimensions**
Choose 5-8 dimensions that matter to your target buyer. Examples:
- Price, ease of use, feature depth, integrations, support quality, time-to-value

**Step 3: Score honestly**
Rate each competitor 1-5 on each dimension. Be honest — inflating your score undermines the exercise.

**Step 4: Find your wedge**
The wedge is the dimension where you score highest AND competitors score lowest. This becomes your primary positioning angle.

```yaml
competitive_matrix:
  dimensions:
    - name: "[Dimension]"
      weight: [1-5]  # How important to buyer
  competitors:
    - name: "[Competitor]"
      scores:
        "[Dimension]": [1-5]
      positioning: "[Their main claim]"
  your_wedge: "[Dimension where you win]"
  messaging_angle: "[How to frame your advantage]"
```

---

## OKR Writing for Marketing

### OKR Structure

**Objective:** Qualitative, inspirational, time-bound.
**Key Results:** Quantitative, measurable, challenging but achievable (70% hit rate target).

### Marketing OKR Templates

**Growth-stage OKR:**
```
O: Establish [Brand] as the go-to solution for [Job-to-be-Done]
  KR1: Grow organic traffic from [X] to [Y] monthly visits
  KR2: Achieve [X]% trial-to-paid conversion rate (from [current]%)
  KR3: Reach [X] qualified leads per month via content marketing
```

**Retention-focused OKR:**
```
O: Build a community of engaged users who advocate for [Brand]
  KR1: Increase NPS from [X] to [Y]
  KR2: Grow referral-sourced signups from [X]% to [Y]% of total
  KR3: Achieve [X]% monthly active rate among paid users
```

**Brand-building OKR:**
```
O: Own the [Category] conversation in [Industry]
  KR1: Publish [X] thought leadership pieces with [Y]+ average shares
  KR2: Secure [X] media mentions or podcast appearances
  KR3: Grow LinkedIn followers from [X] to [Y] with [Z]%+ engagement rate
```

### OKR Anti-patterns

- **Vanity KRs:** "Get 10,000 followers" without engagement or conversion context
- **Activity KRs:** "Publish 20 blog posts" — measure outcomes, not outputs
- **Sandbagging:** KRs you'll hit at 100% aren't ambitious enough
- **Too many KRs:** Max 3-4 per Objective. If you need more, split the Objective.

---

## TAM/SAM/SOM Analysis

### Definitions

| Level | Definition | Method |
|-------|-----------|--------|
| **TAM** (Total Addressable Market) | Total revenue opportunity if you captured 100% of the market | Top-down: industry reports. Bottom-up: # of potential customers × annual value |
| **SAM** (Serviceable Addressable Market) | Portion of TAM you can reach with your current product and channels | TAM filtered by geography, segment, and product fit |
| **SOM** (Serviceable Obtainable Market) | Realistic share you can capture in 1-3 years | SAM × realistic market share % based on competitive position |

### Calculation Template

```yaml
tam_sam_som:
  tam:
    method: "[top-down or bottom-up]"
    total_potential_customers: "[Number]"
    average_annual_value: "[Amount per customer]"
    total: "[TAM = customers × value]"
    source: "[Where data came from]"
  sam:
    geographic_filter: "[Markets you can serve]"
    segment_filter: "[Customer segments you target]"
    product_fit_filter: "[Who your product actually serves]"
    total: "[SAM after filters]"
  som:
    market_share_target: "[Realistic % — typically 1-5% for startups]"
    timeline: "[1-3 years]"
    total: "[SOM = SAM × share %]"
    assumptions:
      - "[Key assumption 1]"
      - "[Key assumption 2]"
```

### Quality Checks

- TAM should come from at least 2 sources (cross-validate)
- SAM should be less than 50% of TAM (if higher, your filters are too loose)
- SOM should feel uncomfortably small (if it feels easy, you're overestimating)
- Always list assumptions — investors and stakeholders will challenge them

---

## Strategy Document Output Format

All strategy outputs must follow this format:

```yaml
---
type: strategy
subtype: "[campaign | positioning | growth-model | okr | competitive-analysis | market-sizing]"
status: draft
date: "YYYY-MM-DD"
author: growthOS/marketing-strategy
brand: "[from brand-voice.yaml]"
tags:
  - "[relevant tags]"
---
```

### Anti-Slop Validation

Before finalizing any strategy document:

1. Scan for banned phrases from `brand-voice.yaml → anti_slop.banned_phrases`
2. Replace any matches with specific, evidence-backed language
3. Verify active voice is used throughout
4. Ensure no superlatives appear without supporting data
5. Check that headlines are specific, not generic clickbait

---

## Output Contract

### Strategy Document Schema

```yaml
output_contract:
  format: markdown
  required_sections:
    - frontmatter:
        type: string  # "strategy"
        subtype: string  # specific strategy type
        status: string  # "draft" | "review" | "approved"
        date: string  # ISO 8601
        author: string  # "growthOS/marketing-strategy"
    - executive_summary:
        max_words: 150
        must_include: [objective, approach, expected_outcome]
    - analysis:
        frameworks_used: list  # which frameworks were applied
        data_sources: list  # where data came from
    - recommendations:
        format: prioritized_list
        each_item:
          - action: string
          - rationale: string
          - priority: string  # "P0" | "P1" | "P2"
          - effort: string  # "low" | "medium" | "high"
          - expected_impact: string
    - success_metrics:
        format: table
        columns: [metric, current, target, timeline]
    - next_steps:
        format: checklist
        max_items: 7
  validation:
    anti_slop: true  # must pass anti-slop scan
    brand_voice: true  # must align with brand-voice.yaml
    min_word_count: 500
    max_word_count: 5000
```
