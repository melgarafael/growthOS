---
name: seo-growth
description: Keyword research methodology, on-page SEO checklist, content cluster strategy, meta description templates, internal linking, SERP analysis, and E-E-A-T signals
---

# SEO Growth Skill

## Trigger Conditions

Use this skill when the user asks to:
- Research keywords or build a keyword strategy
- Optimize content for search engines
- Build a content cluster or topic hub
- Write or improve meta descriptions and title tags
- Plan an internal linking strategy
- Analyze SERPs or competitor search performance
- Improve E-E-A-T signals
- Audit on-page SEO elements
- Plan a content strategy with SEO focus

---

## Brand Voice Integration

**MANDATORY:** Before generating ANY SEO content, load the brand voice configuration.

```python
from growthOS_shared.config import load_brand_voice
brand = load_brand_voice()
```

SEO content must:
1. Pass `anti_slop` validation — search engines increasingly penalize generic AI content
2. Match `brand.tone` — consistency across all content builds brand authority
3. Provide genuine value — Google's Helpful Content Update rewards content made for humans

---

## Keyword Research Methodology

### The 5-Layer Keyword Research Process

#### Layer 1: Seed Keywords from Business Context

Start with the business, not the tool. Extract seed keywords from:

- Product features and use cases
- Customer support tickets (actual language customers use)
- Sales call transcripts (how prospects describe their problem)
- Competitor landing pages (what terms they target)
- Industry forums and communities (Reddit, specialized forums)

**Template for seed extraction:**
```yaml
seed_keywords:
  from_product:
    - "[feature] + [use case]"  # e.g., "content calendar automation"
  from_customer_language:
    - "[how customers describe the problem]"  # e.g., "spending too much time on social media"
  from_competitors:
    - "[terms competitors rank for]"
  from_communities:
    - "[questions people ask]"  # e.g., "how to plan content for LinkedIn"
```

#### Layer 2: Keyword Expansion

For each seed keyword, expand using these methods:

| Method | What It Finds | Example |
|--------|--------------|---------|
| **Google Autocomplete** | Real user queries | Type seed → note suggestions |
| **People Also Ask (PAA)** | Question-form queries | Search seed → extract PAA boxes |
| **Related Searches** | Semantic variations | Bottom of SERP → related queries |
| **Forum Mining** | Long-tail, problem-aware queries | Reddit/Quora → actual questions |
| **Competitor Gap** | Keywords competitors rank for that you don't | Tools: Ahrefs, SEMrush content gap |

#### Layer 3: Intent Classification

Every keyword has a search intent. Mismatching intent = wasted content.

| Intent | Searcher Wants | Content Format | Funnel Stage |
|--------|---------------|----------------|-------------|
| **Informational** | Learn or understand | Blog post, guide, video, infographic | TOFU |
| **Navigational** | Find a specific site/page | Brand page, login page | N/A |
| **Commercial Investigation** | Compare options | Comparison post, review, "best X" list | MOFU |
| **Transactional** | Buy or take action | Landing page, pricing page, product page | BOFU |

**How to determine intent:**
1. Google the keyword and analyze the top 5 results
2. Are they blog posts (informational), product pages (transactional), or comparison articles (commercial)?
3. Match your content format to what Google is already ranking

#### Layer 4: Prioritization Scoring

Score each keyword opportunity:

```yaml
keyword_score:
  keyword: "[term]"
  monthly_volume: "[number]"
  keyword_difficulty: "[0-100]"
  search_intent: "[informational | commercial | transactional]"
  business_relevance: "[1-5, how close to your product's value]"
  current_ranking: "[position or 'not ranking']"
  content_exists: "[yes/no — do you already have content for this?]"
  priority_score: "[calculated: relevance × (volume / difficulty)]"
```

**Prioritization rules:**
- High relevance + low difficulty = quick wins (do first)
- High relevance + high difficulty = strategic investments (plan long-term)
- Low relevance + any difficulty = skip (doesn't matter if you rank)
- Always prioritize business relevance over raw volume

#### Layer 5: Keyword Mapping

Map keywords to content and URLs:

```yaml
keyword_map:
  - primary_keyword: "[main target]"
    secondary_keywords:
      - "[variation 1]"
      - "[variation 2]"
    target_url: "[/path/to/content]"
    content_type: "[blog | landing | guide | comparison]"
    status: "[planned | draft | published | needs-update]"
    cluster: "[which content cluster this belongs to]"
```

---

## On-Page SEO Checklist

Use this checklist for every piece of content before publishing.

### Title Tag (most important on-page element)

- [ ] Primary keyword appears in title tag
- [ ] Title is 50-60 characters (not truncated in SERPs)
- [ ] Title is compelling to click (not just keyword-stuffed)
- [ ] Title is unique across the site (no duplicates)
- [ ] Brand name at end if space allows: "Topic — Brand"
- [ ] Front-loads the primary keyword (first 3-4 words)

**Title tag formulas:**
```
[Number] + [Adjective] + [Keyword] + [Promise]
→ "7 Proven Content Calendar Templates That Save 10 Hours/Week"

How to + [Keyword] + [Without Objection]
→ "How to Build a Content Strategy Without a Full Marketing Team"

[Keyword]: [Specific Benefit or Framework]
→ "Content Clusters: The Hub-and-Spoke Model for Topical Authority"
```

### Meta Description

- [ ] 150-160 characters (not truncated)
- [ ] Contains primary keyword naturally
- [ ] Includes a clear value proposition
- [ ] Has a call-to-action or curiosity hook
- [ ] Unique per page (no duplicates)
- [ ] Accurately describes page content

**Meta description templates:**

```
[Benefit statement]. [Specific detail]. [CTA].
→ "Build your content calendar in 10 minutes. Includes templates for
LinkedIn, Twitter, and email. Get the free guide."

[Question that matches search intent]? [Answer preview]. [CTA].
→ "Struggling with consistent content? Here's the 3-pillar framework
used by 500+ marketing teams. Start planning today."

[Problem] → [Solution]. [Proof]. [CTA].
→ "Spending 15 hours/week on social content? Automate your workflow
with GrowthOS. Trusted by 2,400+ teams. Try free."
```

### Headings (H1-H6)

- [ ] H1 contains primary keyword (one H1 per page)
- [ ] H2s contain secondary keywords or question-form queries
- [ ] Heading hierarchy is logical (H2 → H3 → H4, no skipping)
- [ ] Headings are descriptive (scannable — reader gets value from headings alone)
- [ ] At least one H2 matches a "People Also Ask" question

### Content Body

- [ ] Primary keyword in first 100 words
- [ ] Secondary keywords distributed naturally (not forced)
- [ ] Content length matches or exceeds top-ranking competitors
- [ ] Content provides unique value (original data, frameworks, examples)
- [ ] Uses semantic variations (LSI keywords) not just exact match
- [ ] Paragraphs ≤ 3-4 sentences (mobile readability)
- [ ] Uses bullet points and numbered lists for scanability
- [ ] Includes at least 1 original image, chart, or diagram

### URL Structure

- [ ] URL is short, descriptive, and contains primary keyword
- [ ] Uses hyphens, not underscores
- [ ] No parameters, IDs, or dates in URL
- [ ] Lowercase only
- [ ] Max 3-5 words in the URL slug

```
✅ /content-calendar-templates
❌ /blog/2025/03/15/content-calendar-templates-for-marketing-teams-2025
```

### Images

- [ ] Alt text describes image AND includes keyword where natural
- [ ] File names are descriptive: `content-calendar-template.png` not `IMG_4521.png`
- [ ] Images are compressed (WebP or optimized PNG/JPG)
- [ ] Images add value (not stock filler)
- [ ] Lazy loading enabled for below-fold images

### Internal Links

- [ ] Links to 3-5 related internal pages
- [ ] Anchor text is descriptive (not "click here")
- [ ] Links from high-authority internal pages to this page
- [ ] No orphan pages (every page has at least 1 internal link pointing to it)

### Technical

- [ ] Page loads in < 3 seconds
- [ ] Mobile-responsive
- [ ] No broken links
- [ ] Canonical tag set correctly
- [ ] Schema markup added where applicable (FAQ, HowTo, Article)

---

## Content Cluster Strategy

### The Hub-and-Spoke Model

Content clusters (also called topic clusters) are the foundation of modern SEO architecture. They build topical authority and help Google understand your expertise.

**Structure:**
```
                    ┌── Spoke: "How to Write LinkedIn Posts"
                    │
Pillar (Hub): ──────┼── Spoke: "Content Calendar Templates"
"Content Marketing   │
Strategy Guide"     ├── Spoke: "B2B vs B2C Content Strategy"
                    │
                    ├── Spoke: "Content Distribution Channels"
                    │
                    └── Spoke: "Measuring Content ROI"
```

### Building a Content Cluster

**Step 1: Choose the pillar topic**
- Broad enough to support 10-20 sub-topics
- Competitive enough to be worth the investment
- Aligned with your product's value proposition

**Step 2: Map spoke topics**
```yaml
content_cluster:
  pillar:
    topic: "[Broad topic]"
    target_keyword: "[High-volume head term]"
    url: "/[topic-slug]"
    format: "comprehensive guide (3,000-5,000 words)"
    intent: "informational"
  spokes:
    - topic: "[Sub-topic 1]"
      target_keyword: "[Long-tail keyword]"
      url: "/[topic-slug]/[sub-topic-slug]"
      format: "[blog post | how-to | comparison | template]"
      intent: "[informational | commercial]"
      links_to_pillar: true
      internal_links:
        - "[other spoke URL that's related]"
```

**Step 3: Internal linking rules**
- Every spoke links to the pillar page (required)
- Pillar page links to every spoke (required)
- Spokes link to each other when contextually relevant (recommended)
- Anchor text varies — don't use the same text for every link

**Step 4: Content creation order**
1. Publish the pillar page first (even in draft form)
2. Publish spoke articles, linking to pillar as they go live
3. Update pillar to link to new spokes
4. Revisit and update cluster quarterly

### Cluster Quality Metrics

| Metric | Target | Why |
|--------|--------|-----|
| Spokes per cluster | 8-15 | Enough for authority, not so many you're thin |
| Internal links per spoke | 3-5 | Distributes authority without over-linking |
| Cluster traffic growth | 20%+ QoQ | Proves topical authority is building |
| Pillar page ranking | Top 10 for head term | The goal of the whole cluster |
| Spoke conversion rate | > site average | Spokes should drive qualified traffic |

---

## SERP Analysis

### How to Analyze a SERP Before Writing

Before creating content for any keyword, study what's already ranking:

**Step 1: Search the primary keyword**
Note:
- What type of content ranks? (blog, product page, tool, video)
- What format? (listicle, how-to, comparison, guide)
- What length? (500 words or 5,000 words?)
- SERP features present? (Featured snippet, PAA, video carousel, local pack)

**Step 2: Analyze top 3 results**
```yaml
serp_analysis:
  keyword: "[target keyword]"
  serp_features:
    featured_snippet: "[yes/no — type if yes]"
    people_also_ask: "[list top 4 PAA questions]"
    video_carousel: "[yes/no]"
    local_pack: "[yes/no]"
    knowledge_panel: "[yes/no]"
  top_results:
    - position: 1
      url: "[URL]"
      title: "[Title tag]"
      content_type: "[blog | guide | tool | landing]"
      word_count: "[approximate]"
      strengths: "[what they do well]"
      gaps: "[what they miss that we can cover]"
    - position: 2
      # ...same structure
    - position: 3
      # ...same structure
  content_strategy:
    format: "[what format to use based on SERP]"
    angle: "[unique angle that fills gaps]"
    target_length: "[word count based on competitors]"
    featured_snippet_opportunity: "[yes/no — and how to target it]"
```

**Step 3: Identify the content gap**
The gap is what makes your content worth ranking over what already exists:
- Missing depth on a subtopic
- No original data or examples
- Outdated information
- Poor user experience (wall of text, no visuals)
- Missing a specific audience perspective

### Featured Snippet Optimization

If a featured snippet exists for your keyword, optimize for it:

| Snippet Type | How to Target |
|-------------|--------------|
| **Paragraph** | Answer the question in 40-50 words directly under an H2 that matches the query |
| **List** | Use an ordered or unordered list with H2 matching the query |
| **Table** | Use an HTML table with clear headers |
| **Video** | Create a video with the keyword in title, timestamped chapters |

---

## E-E-A-T Signals

### What E-E-A-T Means

E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) is Google's framework for evaluating content quality. It's not a direct ranking factor but influences how quality raters evaluate your site.

| Signal | Definition | How to Demonstrate |
|--------|-----------|-------------------|
| **Experience** | First-hand experience with the topic | Share personal/company results, case studies, screenshots, original data |
| **Expertise** | Deep knowledge in the subject area | Author bios, credentials, detailed technical content, cite primary sources |
| **Authoritativeness** | Recognized authority in the field | Backlinks from authoritative sites, mentions, industry recognition, original research |
| **Trustworthiness** | Accurate, honest, and transparent | HTTPS, clear author identity, sources cited, corrections policy, no misleading claims |

### E-E-A-T Implementation Checklist

#### Content Level
- [ ] Author name and bio on every article
- [ ] Author has demonstrable expertise in the topic
- [ ] Content includes original data, examples, or case studies
- [ ] Sources are cited for factual claims
- [ ] Content is updated regularly (shows "last updated" date)
- [ ] Distinguishes between opinion and fact
- [ ] Acknowledges limitations or counterarguments

#### Site Level
- [ ] About page with company/team information
- [ ] Contact page with real contact information
- [ ] Privacy policy and terms of service
- [ ] HTTPS across all pages
- [ ] Clear editorial policy or content standards
- [ ] Author pages linking to their content

#### Technical E-E-A-T
- [ ] Schema markup for authors (Person schema)
- [ ] Schema markup for organization (Organization schema)
- [ ] Schema markup for articles (Article schema with author, datePublished, dateModified)
- [ ] Consistent NAP (Name, Address, Phone) if local business

### E-E-A-T for AI-Generated Content

Google's stance: AI-generated content is fine IF it demonstrates E-E-A-T. The key is:

1. **Human review** — AI generates, human reviews and adds expertise
2. **Experience layer** — Add real examples, data, and case studies that AI can't fabricate
3. **Transparency** — Don't pretend AI content is human-written if it's not
4. **Value test** — Would this content exist if there were no search engines? If yes, it's probably valuable.

---

## Link Building Strategy (Internal)

### Internal Linking Rules

Internal links are the most underrated SEO lever — they're free, you control them, and they directly influence crawl behavior and authority distribution.

**Core rules:**

1. **Every new page gets 3-5 internal links pointing to it within 48 hours**
   - From the pillar page (if part of a cluster)
   - From related blog posts
   - From resource/guide pages

2. **Anchor text distribution:**
   ```
   50% — Exact or partial keyword match
   30% — Descriptive / contextual phrase
   20% — Branded or generic ("this guide", "our analysis")
   ```

3. **Link equity flow:**
   - Homepage → Pillar pages → Spoke pages
   - High-traffic pages should link to strategic conversion pages
   - Don't dilute important pages with too many outbound internal links (max 100 per page as a guideline)

4. **Orphan page audit:**
   - Quarterly check: any page with 0 internal links pointing to it?
   - Fix immediately — orphan pages are effectively invisible to search engines

### Internal Link Template

```yaml
internal_linking_plan:
  target_page:
    url: "[new page URL]"
    primary_keyword: "[target keyword]"
  inbound_links:
    - source_url: "[page linking TO the new page]"
      anchor_text: "[text used for the link]"
      context: "[paragraph where link is placed]"
      type: "[contextual | navigational | footer]"
  outbound_links:
    - target_url: "[page the new page links TO]"
      anchor_text: "[text used]"
      relevance: "[why this link makes sense for the reader]"
```

---

## Technical SEO Essentials

### Core Web Vitals

| Metric | Target | What It Measures |
|--------|--------|-----------------|
| **LCP** (Largest Contentful Paint) | < 2.5s | Loading performance |
| **INP** (Interaction to Next Paint) | < 200ms | Interactivity |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Visual stability |

### Schema Markup Priority

| Schema Type | When to Use | Impact |
|------------|-------------|--------|
| **Article** | Blog posts, guides | Rich results, author display |
| **FAQ** | Pages with Q&A sections | FAQ rich results, more SERP real estate |
| **HowTo** | Tutorial/process content | Step-by-step rich results |
| **Product** | Product pages | Price, availability, reviews in SERPs |
| **Organization** | Homepage | Knowledge panel data |
| **BreadcrumbList** | All pages | Better SERP display, navigation context |

### Crawl Budget Optimization

- Block irrelevant pages from indexing (filters, pagination, internal search results)
- Use XML sitemap with only valuable, indexable pages
- Fix crawl errors promptly (404s, 5xx errors)
- Ensure flat site architecture (max 3 clicks from homepage to any page)

---

## SEO Content Calendar Template

```yaml
seo_content_calendar:
  month: "YYYY-MM"
  cluster: "[content cluster name]"
  items:
    - week: 1
      keyword: "[target keyword]"
      title: "[working title]"
      format: "[blog | guide | comparison | template]"
      intent: "[informational | commercial | transactional]"
      word_count_target: "[based on SERP analysis]"
      author: "[who writes]"
      status: "[planned | writing | review | published]"
      target_url: "[planned URL]"
      internal_links_from: ["[list of pages that will link to this]"]
      notes: "[any special considerations]"
```

---

## Output Contract

### SEO Content Schema

```yaml
output_contract:
  format: markdown
  required_sections:
    - frontmatter:
        type: string  # "seo-content"
        subtype: string  # "keyword-research" | "content-brief" | "on-page-audit" | "cluster-plan" | "serp-analysis"
        status: string  # "draft" | "review" | "approved"
        date: string  # ISO 8601
        author: string  # "growthOS/seo-growth"
        target_keyword: string  # primary keyword
        search_intent: string  # "informational" | "commercial" | "transactional"
    - seo_metadata:
        title_tag: string  # 50-60 chars
        meta_description: string  # 150-160 chars
        url_slug: string  # short, keyword-rich
        primary_keyword: string
        secondary_keywords: list
        target_word_count: integer
    - content:
        format: string  # matches SERP intent
        sections: list  # H2 outline with keywords mapped
        internal_links: list  # planned internal links
        schema_markup: string  # recommended schema type
    - competitive_context:
        serp_analysis: object  # top 3 competitors analyzed
        content_gap: string  # what unique angle we take
        featured_snippet_target: boolean
    - quality_gates:
        on_page_checklist_passed: boolean
        eeat_signals_present: boolean
        anti_slop_passed: boolean
        brand_voice_aligned: boolean
  validation:
    anti_slop: true
    brand_voice: true
    title_length: "50-60 chars"
    meta_description_length: "150-160 chars"
    min_internal_links: 3
    schema_markup_required: true
```
