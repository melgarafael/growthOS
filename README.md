# GrowthOS

**Autonomous marketing team for Claude Code** — 9 AI agents, 20 skills, 4 MCP servers, one `/grow` command.

GrowthOS turns Claude Code into a full-stack growth engine: strategy, content creation, SEO, social publishing, competitive intelligence, video production, and landing page design — all orchestrated by AI agents with built-in safety controls.

---

## Features

| Category | What You Get |
|----------|-------------|
| **9 AI Agents** | CMO (router), Growth Strategist, Content Creator, Intelligence Analyst, Visual Designer, Social Publisher, Growth Engineer, Carousel Designer, Video Producer |
| **20 Skills** | Marketing Strategy, Copywriting, SEO Growth, Content Creation, Social Media, Competitive Intel, Video Production, Landing Pages, Platform Mastery, Instagram Carousel, Remotion Video, Remotion Pro, + 8 Showcase templates |
| **4 MCP Servers** | Social Publish (Twitter, LinkedIn, Reddit, GitHub, Threads), Social Discover (analytics), Obsidian Vault (knowledge base), Remotion Render (video) |
| **Safety System** | Dry-run by default, progressive autonomy (4 levels), audit logging, circuit breaker |
| **Video Engine** | 11 Remotion compositions for reels, explainers, product demos, walkthroughs |
| **Carousel Engine** | 6 HTML templates (1080x1350) — Minimal, Bold, Gradient, Educator, Dark Premium, Vibrant |
| **Brand Voice** | YAML config for tone, audience, vocabulary, anti-slop filters |

---

## Installation

### Option 1: Claude Code Marketplace (Recommended)

```bash
claude plugin install growthOS
```

### Option 2: Install from GitHub

```bash
# Clone the repository
git clone https://github.com/melgarafael/growthOS.git

# Install as Claude Code plugin
claude plugin add ./growthOS
```

### Option 3: Docker (for MCP servers)

```bash
cd growthOS
cp .env.example .env
# Edit .env with your API keys

docker-compose up -d
docker-compose ps
```

### Post-Installation Setup

After installing, run the onboarding wizard:

```
/grow setup
```

This will guide you through:
1. Setting your brand name and tagline
2. Choosing your tone of voice
3. Selecting your industry
4. Configuring target platforms

The wizard creates a `brand-voice.yaml` file that all agents use to stay on-brand.

---

## Quick Start

Once installed, everything goes through `/grow`:

```bash
# Start here — the setup wizard
/grow setup

# Create a growth strategy
/grow strategy "Launch our new SaaS product in Q3"

# Write content
/grow create blog "Why AI is transforming marketing"
/grow create thread "5 growth hacks for startups"
/grow create newsletter "Monthly product update"

# Create visual content
/grow carousel "10 tips for better landing pages"
/grow video reel "Quick product demo"

# Analyze competitors
/grow analyze "competitor X social strategy"

# Research trends
/grow research "AI marketing tools 2026"

# Generate a landing page
/grow create landing "New feature launch page"

# Or just describe what you need — the CMO agent routes it
/grow "I need content for our product launch next week"
```

---

## Skills Reference

### Core Skills (11)

| Skill | What It Does | Trigger Example |
|-------|-------------|-----------------|
| **Marketing Strategy** | Growth frameworks, OKRs, campaign planning, AARRR funnels | `/grow strategy "Q3 plan"` |
| **Copywriting** | AIDA, PAS, 4U formulas, CTA patterns, emotional triggers | `/grow create copy "headline for launch"` |
| **SEO Growth** | Keyword research, on-page audit, content clusters, E-E-A-T | `/grow create seo "audit our blog"` |
| **Content Creation** | Blog posts, newsletters, docs, editorial workflows | `/grow create blog "topic"` |
| **Social Media Management** | Platform strategies, scheduling, community management | `/grow create social "launch campaign"` |
| **Competitive Intelligence** | SWOT analysis, market trends, competitor tracking | `/grow analyze "competitor X"` |
| **Video Production** | Scripts, storyboards, video SEO, thumbnail concepts | `/grow video script "product demo"` |
| **Landing Page Design** | Conversion-optimized HTML, hero sections, A/B variants | `/grow create landing "feature Y"` |
| **Platform Mastery** | Algorithm knowledge per platform (YouTube, LinkedIn, X, etc.) | `/grow research "LinkedIn algorithm"` |
| **Instagram Carousel** | 6 carousel structures, slide blueprints, engagement triggers | `/grow carousel "10 tips"` |
| **Remotion Video** | Storyboard-to-composition mapping, frame calculations | `/grow video reel "quick tip"` |

### Showcase Skills (9)

Advanced video templates for specific use cases:

| Skill | Use Case |
|-------|----------|
| **Remotion Pro** | Advanced video compositions with custom animations |
| **Showcase: Before/After** | Transformation comparisons (9:16 vertical) |
| **Showcase: Course Trailer** | Educational course promos |
| **Showcase: Data Story** | Animated statistics and data visualization |
| **Showcase: Feature Highlight** | Product feature spotlights |
| **Showcase: Product Demo** | Full product walkthroughs (16:9) |
| **Showcase: Social Proof** | Testimonials and social proof reels |
| **Showcase: Tech Terminal** | CLI/terminal demonstration videos |
| **Showcase: Walkthrough** | Step-by-step app tutorials (16:9) |

---

## Agents

GrowthOS uses a **CMO router** that automatically delegates to specialist agents:

| Agent | Role | When It Activates |
|-------|------|-------------------|
| **CMO** | Routes intent to the right specialist | Every `/grow` command |
| **Growth Strategist** | Strategic planning, frameworks, OKRs | Strategy requests |
| **Content Creator** | Writes blogs, threads, newsletters | Content creation |
| **Intelligence Analyst** | Competitor analysis, market research | Analysis requests |
| **Visual Designer** | Carousels, landing pages, visual assets | Visual content |
| **Social Publisher** | Platform-specific content, publishing | Social media tasks |
| **Growth Engineer** | Technical SEO, landing page code | Technical growth |
| **Carousel Designer** | Instagram carousel design and generation | Carousel requests |
| **Video Producer** | Video scripts, Remotion compositions | Video requests |

---

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Required | Description |
|----------|----------|-------------|
| `GROWTHOS_TWITTER_API_KEY` | For Twitter | Twitter/X API key |
| `GROWTHOS_LINKEDIN_TOKEN` | For LinkedIn | LinkedIn access token |
| `GROWTHOS_REDDIT_CLIENT_ID` | For Reddit | Reddit app client ID |
| `GROWTHOS_GITHUB_TOKEN` | For GitHub | GitHub personal access token |
| `GROWTHOS_THREADS_TOKEN` | For Threads | Threads API token |
| `GROWTHOS_VAULT_PATH` | No | Obsidian vault path (default: `./vault`) |
| `GROWTHOS_AUTONOMY_LEVEL` | No | `supervised` \| `assisted` \| `delegated` \| `autonomous` |
| `GROWTHOS_DRY_RUN` | No | `true` \| `false` (default: `true`) |

> **Note:** Social platform API keys are only needed if you want to publish directly. GrowthOS works perfectly for content **generation** without any API keys.

### Brand Voice

Copy `brand-voice.example.yaml` to `brand-voice.yaml` and customize:

```yaml
brand:
  name: "Your Brand"
  tagline: "Your tagline"
  tone:
    - professional
    - conversational
  audience: "Your target audience"
  industry: "Your industry"
```

Or just run `/grow setup` and the wizard handles it for you.

---

## Architecture

```
growthOS/
├── plugin.json                  # Plugin manifest (entry point)
├── brand-voice.example.yaml     # Brand config template
├── .env.example                 # Environment variables template
│
├── agents/                      # 9 AI agents
│   ├── cmo/                     #   CMO — intent router
│   ├── growth-strategist/       #   Strategic planning
│   ├── content-creator/         #   Content production
│   ├── intelligence-analyst/    #   Competitive intel
│   ├── visual-designer/         #   Visual assets
│   ├── social-publisher/        #   Social media ops
│   ├── growth-engineer/         #   Technical growth
│   ├── carousel-designer/       #   Carousel generation
│   └── video-producer/          #   Video production
│
├── skills/                      # 20 specialized skills
│   ├── marketing-strategy/      #   Core skills (11)
│   ├── copywriting/
│   ├── seo-growth/
│   ├── content-creation/
│   ├── social-media-management/
│   ├── competitive-intelligence/
│   ├── video-production/
│   ├── landing-page-design/
│   ├── platform-mastery/
│   ├── instagram-carousel/
│   ├── remotion-video/
│   ├── remotion-pro/            #   Showcase skills (9)
│   ├── showcase-before-after/
│   ├── showcase-course-trailer/
│   ├── showcase-data-story/
│   ├── showcase-feature-highlight/
│   ├── showcase-product-demo/
│   ├── showcase-social-proof/
│   ├── showcase-tech-terminal/
│   └── showcase-walkthrough/
│
├── mcp-servers/                 # 4 MCP servers (Python/FastMCP)
│   ├── mcp-social-publish/      #   Publish to 5 platforms
│   ├── mcp-social-discover/     #   Trend & analytics
│   ├── mcp-obsidian-vault/      #   Knowledge base CRUD
│   └── mcp-remotion-render/     #   Video rendering
│
├── shared-lib/                  # Python shared library
│   └── growthOS_shared/
│       ├── config.py            #   Brand voice config (Pydantic)
│       ├── intent_router.py     #   NLP intent classification
│       ├── autonomy.py          #   Progressive autonomy + kill switch
│       ├── token_manager.py     #   Rate limiting
│       ├── circuit_breaker.py   #   Circuit breaker pattern
│       ├── audit_logger.py      #   Action audit trail
│       ├── carousel_generator.py#   HTML carousel generation
│       └── scheduler.py         #   Content scheduling
│
├── hooks/                       # 4 safety hooks
│   ├── audit-logger.md          #   Log all actions
│   ├── circuit-breaker.md       #   Failure protection
│   ├── preview-before-publish.md#   Preview before sending
│   └── dry-run-guard.md         #   Block real calls in dry-run
│
├── commands/                    # CLI commands
│   └── grow/                    #   /grow entry point + setup
│
├── remotion/                    # Video rendering engine
│   └── src/
│       ├── Root.tsx             #   Composition registry
│       ├── compositions/        #   11 video compositions
│       └── components/          #   Reusable animation components
│
└── templates/                   # Output templates
    ├── carousels/               #   6 HTML carousel templates
    ├── content/                 #   Content templates
    └── landing/                 #   Landing page templates
```

---

## Safety and Security

GrowthOS is designed with safety-first principles:

| Feature | Description |
|---------|-------------|
| **Dry-run mode** | Enabled by default — no real API calls until you disable it |
| **Progressive autonomy** | 4 levels: `supervised` → `assisted` → `delegated` → `autonomous` |
| **Kill switch** | Instantly revoke all autonomous permissions |
| **Audit logging** | Every action recorded in `.growthOS/audit/` |
| **Circuit breaker** | Auto-stops on repeated API failures |
| **Preview hook** | See exactly what will be published before it goes live |
| **Path validation** | Vault operations prevent directory traversal attacks |
| **Safe rendering** | Remotion uses subprocess isolation to prevent injection |

See [SECURITY.md](SECURITY.md) for the responsible disclosure policy.

---

## Development

### Prerequisites

- Node.js 18+
- Python 3.10+
- Claude Code CLI

### Setup

```bash
# Clone
git clone https://github.com/melgarafael/growthOS.git
cd growthOS

# Install Python shared library (development mode)
pip install -e shared-lib/

# Install Node.js dependencies (for Remotion)
npm install

# Run tests
cd shared-lib && pytest
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines, coding standards, and PR process.

---

## Roadmap

- [x] Core agent system (CMO + 8 specialists)
- [x] 20 marketing skills
- [x] Remotion video engine (11 compositions)
- [x] Instagram carousel generator (6 templates)
- [x] Obsidian vault integration
- [x] Brand voice system
- [x] Safety hooks (audit, circuit breaker, dry-run, preview)
- [ ] Live social publishing (Twitter, LinkedIn, Reddit, GitHub, Threads)
- [ ] Analytics dashboard
- [ ] A/B testing framework
- [ ] Multi-language content support

---

## License

MIT — see [LICENSE](LICENSE) for details.
