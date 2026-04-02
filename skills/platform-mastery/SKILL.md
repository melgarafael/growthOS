---
name: platform-mastery
description: Platform-by-platform algorithm knowledge, best practices, and content adaptation rules for YouTube, LinkedIn, Twitter/X, Reddit, Instagram, GitHub, Threads, and StackOverflow. Use when optimizing content for a specific platform or adapting cross-platform content.
---

# Platform Mastery Skill

Deep algorithm knowledge and content optimization rules for each social platform. Ensures content is native to each platform rather than cross-posted generically.

## Platform Quick Reference

| Platform | Algorithm Priority | Content Sweet Spot | Tone |
|----------|-------------------|-------------------|------|
| YouTube | Watch time + CTR | 8-15 min long-form | Educational, personality-driven |
| LinkedIn | Comments > reactions | 1200-1500 chars + image | Professional, insight-driven |
| Twitter/X | Engagement rate | 200-280 chars + media | Concise, opinionated |
| Reddit | Upvote ratio + authenticity | Text posts, genuine value | Authentic, humble, no marketing |
| Instagram | Saves + shares | Carousel (10 slides) | Visual-first, aspirational |
| GitHub | Stars + community engagement | README quality + releases | Technical, precise |
| Threads | Conversation + reposts | 300-500 chars | Conversational, casual |
| StackOverflow | Answer quality score | Canonical answers | Technical, helpful, factual |

---

## YouTube

### Algorithm Signals (Priority Order)

1. **Click-through rate (CTR)**: Thumbnail + title combination. Target >5% CTR.
2. **Average view duration**: Percentage of video watched. Target >50%.
3. **Session time**: Does your video lead to more YouTube watching? Playlists help.
4. **Engagement rate**: Likes, comments, shares — comments weighted highest.
5. **Upload consistency**: Regular schedule signals reliability to algorithm.

### Content Rules

- **Hook in first 5 seconds** — no intros, logos, or "hey guys welcome back"
- **Retention triggers** every 60-90 seconds (pattern interrupts, open loops)
- **Chapters** (3+ timestamps starting at 0:00) — improves search + UX
- **End screens** in last 20 seconds — link to related content
- **Thumbnail**: 3-5 words max, readable at 100px width, face + emotion
- **Title**: <60 chars, front-load keyword, curiosity gap

### Optimal Format

```yaml
youtube:
  length: 8-15 minutes (sweet spot for ad revenue + algorithm)
  title_length: "<60 chars"
  description: "first 150 chars critical (shown in search)"
  tags: 10-15
  thumbnail: "1280x720, high contrast, face + text"
  chapters: "minimum 3, start at 0:00"
  end_screen: "last 20s, 1-2 elements"
  posting_time: "weekdays 2-4 PM viewer timezone"
```

### Anti-Patterns

- Asking to "smash that like button" before delivering value
- Thumbnails with >5 words of text
- First 30 seconds of logos, channel intros, sponsor reads
- Generic tags ("tutorial", "how to")

---

## LinkedIn

### Algorithm Signals (Priority Order)

1. **Comments** (especially long comments): Highest weight signal
2. **Dwell time**: Time spent reading your post
3. **Reactions**: Likes and other reactions (comments > reactions)
4. **Shares/reposts**: Signal virality to algorithm
5. **Profile authority**: SSI score, connection relevance

### Content Rules

- **First 3 lines** are everything — hook before "...see more" truncation
- **Line breaks** after every 1-2 sentences (mobile readability)
- **End with a question** — drives comments (algorithm's top signal)
- **Personal stories** outperform corporate content 3-5x
- **Images** increase engagement 2x (single image > carousel on LinkedIn)
- **Native documents** (PDF carousels) get high dwell time
- **No external links in post body** — put links in first comment

### Post Format

```markdown
[Hook line — bold claim, counterintuitive take, or personal story opener]

[blank line — critical for mobile]

[2-3 short paragraphs, each 1-2 sentences]

[Key insight or framework — optionally use bullet points]

• Point 1
• Point 2
• Point 3

[Personal reflection or lesson learned]

[Question to drive comments]

#[hashtag1] #[hashtag2] #[hashtag3]
```

### Optimal Format

```yaml
linkedin:
  length: 1200-1500 chars (sweet spot)
  hashtags: 3-5 (more looks spammy)
  images: 1 (native upload, not link preview)
  links: "in first comment, never in post body"
  posting_time: "Tue-Thu 8-10 AM viewer timezone"
  format: "short paragraphs, line breaks between"
  hook: "first 210 chars (before ...see more)"
```

### Anti-Patterns

- Starting with "I'm excited to announce..."
- Wall of text without line breaks
- External links in post body (kills reach)
- Hashtag stuffing (>5 hashtags)
- Corporate jargon ("synergy", "leverage", "disrupt")

---

## Twitter/X

### Algorithm Signals (Priority Order)

1. **Engagement rate**: Replies + retweets + likes relative to impressions
2. **Media attachments**: Images/video boost distribution
3. **Recency**: Tweets decay fast — timing matters
4. **Thread completion**: Full thread reads signal quality
5. **Profile engagement history**: Algorithm favors accounts you interact with

### Content Rules

- **One idea per tweet** — don't cram multiple concepts
- **Strong opening** — first 7 words determine if people read
- **Threads** for long-form: Tweet 1 is the hook, each tweet is self-contained
- **Media boosts reach**: Image, screenshot, or short video
- **Quote tweets** with commentary outperform plain retweets
- **Reply to your own tweet** with additional context or links

### Tweet Formats

```markdown
# Single tweet (high-impact)
[Bold statement or hot take]

[Supporting evidence or example in 1 sentence]

[Optional: image/screenshot]

# Thread format
🧵 [Hook — why should I read this thread?]

1/ [First point — must stand alone as a tweet]

2/ [Second point — builds on first]

[...]

n/ [Conclusion + CTA — follow, bookmark, retweet]
```

### Optimal Format

```yaml
twitter:
  tweet_length: 200-280 chars (near limit performs well)
  thread_length: 5-12 tweets
  media: "1 image or 1 short video per tweet"
  hashtags: 0-2 (hashtags less important than on other platforms)
  posting_time: "weekdays 9-11 AM or 1-3 PM"
  reply_strategy: "reply to own tweet with link, add context"
  quote_tweet: "add 1-2 sentences of commentary"
```

### Anti-Patterns

- Hashtag stuffing (Twitter isn't Instagram)
- Threads that could be a single tweet
- Starting tweets with "1/" without a hook
- Posting only links without commentary
- Engagement bait ("Like if you agree")

---

## Reddit

### Algorithm Signals (Priority Order)

1. **Upvote-to-downvote ratio** in first hour: Critical window
2. **Comment volume and quality**: Active discussion signals value
3. **Community fit**: Content matching subreddit culture
4. **Account karma + age**: Spam filtering mechanism
5. **Report ratio**: Low reports = trusted content

### Content Rules (CRITICAL: Reddit is Anti-Marketing)

- **NO marketing speak** — Reddit users detect and punish self-promotion
- **Value-first, brand-never**: Share knowledge, not products
- **Read subreddit rules** before posting — each sub has specific requirements
- **Authentic tone**: Write like a human, not a brand
- **Text posts** outperform links in most subreddits
- **Respond to every comment** on your posts (signals engagement)
- **The 10:1 rule**: 10 genuine community interactions per 1 self-promotional post

### Post Format

```markdown
# Title: [Specific, descriptive, no clickbait — subreddit convention]

[Context: Why you're sharing this. Personal experience preferred.]

[The actual value: step-by-step, findings, data, analysis]

[What you learned or what surprised you]

[Open question: "Has anyone else experienced this?" or "What would you do differently?"]
```

### Optimal Format

```yaml
reddit:
  title: "descriptive, follows subreddit conventions"
  length: "varies by subreddit — check top posts for norm"
  tone: "authentic, casual, humble"
  self_promotion: "max 10% of activity"
  posting_time: "Sun-Mon morning (US timezones)"
  images: "imgur links for image posts (subreddit dependent)"
  flair: "always use if subreddit requires it"
  crosspost: "use native crosspost, not duplicate posts"
```

### Anti-Patterns

- Sounding like a press release
- Using marketing buzzwords ("game-changer", "revolutionary")
- Posting the same content to multiple subreddits without adaptation
- Not reading subreddit rules before posting
- Ignoring comments on your posts
- New account with only self-promotional posts

---

## Instagram

### Algorithm Signals (Priority Order)

1. **Saves**: Strongest signal — content worth returning to
2. **Shares** (DMs): Content worth sharing privately
3. **Comments**: Engagement depth
4. **Reach to non-followers**: Explore page potential
5. **Reel completion rate**: For video content

### Content Rules

- **Visual-first** — text is secondary to visual impact
- **Carousels** get highest engagement (10 slides, save-worthy)
- **Reels** for reach, carousels for engagement, Stories for community
- **Caption structure**: Hook line → value → CTA → hashtags
- **Hashtag strategy**: 5-15 relevant hashtags, mix of sizes
- **Stories**: 3-7 per day, use polls/questions for engagement
- **Alt text**: Always add for accessibility + SEO

### Optimal Format

```yaml
instagram:
  post_types:
    carousel: "highest engagement, 10 slides, educational"
    reel: "highest reach, 15-30s, trending audio"
    story: "community building, 3-7/day, interactive stickers"
    static: "brand aesthetic, quotes, announcements"
  caption_length: "150-300 chars (before ...more)"
  hashtags: 5-15 in caption or first comment
  image_ratio: "1:1 (feed), 9:16 (reels/stories), 4:5 (portrait)"
  posting_time: "weekdays 11 AM-1 PM or 7-9 PM"
  alt_text: "always include, descriptive"
```

### Anti-Patterns

- Text-heavy images (Instagram is visual-first)
- Using all 30 hashtags (looks spammy)
- Ignoring Stories and Reels (feed-only strategy is dead)
- Cross-posting Twitter screenshots
- No alt text on images

---

## GitHub

### Algorithm Signals (Visibility)

1. **Stars**: Primary popularity metric
2. **Forks**: Community adoption signal
3. **Contributor count**: Active community
4. **README quality**: First impression, determines stars
5. **Release frequency**: Active maintenance signal
6. **Issue response time**: Community health

### Content Rules

- **README is your landing page** — treat it like a conversion page
- **Structured README**: Badge bar → hero → install → quickstart → docs link
- **Release notes**: Detailed, categorized (Added, Changed, Fixed, Removed)
- **Discussions**: Use for community engagement, not just Issues
- **Contributing guide**: Lower barrier to contribution
- **Issue templates**: Structured bug reports and feature requests

### README Format

```markdown
# Project Name

[One-line description]

[Badges: CI status, version, license, downloads]

## Quick Start

[3-5 lines to get running — must be copy-pasteable]

## Features

[Bullet list of key features]

## Installation

[Step-by-step, multiple methods if applicable]

## Documentation

[Link to full docs]

## Contributing

[Link to CONTRIBUTING.md]

## License

[License type]
```

### Optimal Format

```yaml
github:
  readme: "hero + badges + quickstart + features + install"
  releases: "semantic versioning, categorized changelog"
  issues: "templates for bug reports, feature requests"
  discussions: "enabled, categories for Q&A and ideas"
  topics: "5-10 relevant topics/tags"
  social_preview: "1280x640 image"
  license: "always include"
```

---

## Threads

### Algorithm Signals

1. **Reposts**: Highest distribution signal
2. **Replies**: Conversation depth
3. **Likes**: Engagement signal
4. **Cross-posted from Instagram**: Slight boost for connected accounts
5. **Recency**: Fast-moving feed

### Content Rules

- **Conversational tone** — Threads is casual, not professional
- **Shorter than Twitter** — 300-500 chars sweet spot
- **No hashtags** (minimal hashtag culture)
- **Cross-post from Instagram** for connected reach
- **Early-adopter advantage** — algorithm still favoring content

### Optimal Format

```yaml
threads:
  length: 300-500 chars
  tone: "casual, conversational, authentic"
  hashtags: 0-2 (platform culture is minimal hashtags)
  images: "optional, less visual than Instagram"
  posting_time: "mirrors Instagram timing"
  cross_post: "from Instagram for additional reach"
```

---

## StackOverflow

### Algorithm Signals

1. **Answer score**: Upvotes - downvotes on answers
2. **Accepted answer**: Marked by question asker
3. **Answer age + activity**: Canonical answers that stay updated
4. **User reputation**: Higher rep = more privileges + trust

### Content Rules

- **Answer the question directly first** — explanation after
- **Code examples** are mandatory for programming questions
- **Cite documentation** — link to official sources
- **Edit and improve** — update answers as languages/frameworks evolve
- **No opinions** — factual, documented, reproducible answers
- **Formatting matters** — code blocks, headers, lists

### Optimal Format

```yaml
stackoverflow:
  answer_structure: "direct answer → code → explanation → docs link"
  tone: "technical, factual, helpful, no opinions"
  code: "always include, tested, minimal reproduction"
  links: "official docs preferred"
  edits: "keep answers current as APIs change"
  questions: "include version, error message, minimal reproduction"
```

### Anti-Patterns

- Opinion-based answers without documentation backing
- Link-only answers
- "Did you try googling?" responses
- Answering without code examples
- Not including version numbers

---

## Cross-Platform Adaptation Framework

When adapting content across platforms, transform — don't copy-paste:

```yaml
adaptation:
  source_platform: "[original platform]"
  target_platform: "[target platform]"
  transformations:
    tone: "[adjust formality level]"
    length: "[compress or expand]"
    format: "[restructure for platform norms]"
    visuals: "[add/remove visual elements]"
    cta: "[platform-appropriate action]"
    hashtags: "[platform-specific strategy]"
```

### Cross-Platform Content Matrix

| Source | → LinkedIn | → Twitter/X | → Reddit | → Instagram |
|--------|-----------|-------------|----------|-------------|
| Blog post | Extract key insight + personal angle | Thread or key quote tweet | Summarize findings, ask for discussion | Carousel with key points |
| Video | Key takeaway + behind-scenes | Clip + hook | Text summary of findings | Reel (15-30s clip) |
| Data/research | Professional analysis post | Data point tweet + image | Deep analysis post | Infographic carousel |
| Product update | Feature benefit story | Quick announcement + screenshot | "We built X because Y" story | Before/after carousel |

## Platform Algorithm Updates

Algorithm knowledge requires periodic updates. When referencing algorithm behavior:

- State the **general principle** (durable) separately from **specific weights** (temporal)
- Note that exact algorithm weights change frequently
- Focus on **user behavior signals** — these are more stable than algorithm internals
- Test assumptions with data rather than relying on hearsay
