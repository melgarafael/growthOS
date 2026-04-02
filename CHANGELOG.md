# Changelog

All notable changes to GrowthOS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-02

### Added

- **9 AI Agents**: CMO (router), Growth Strategist, Content Creator, Intelligence Analyst, Visual Designer, Social Publisher, Growth Engineer, Carousel Designer, Video Producer
- **20 Skills**: Marketing Strategy, Copywriting, SEO Growth, Content Creation, Social Media Management, Competitive Intelligence, Video Production, Landing Page Design, Platform Mastery, Instagram Carousel, Remotion Video, Remotion Pro, and 8 Showcase templates (Before/After, Course Trailer, Data Story, Feature Highlight, Product Demo, Social Proof, Tech Terminal, Walkthrough)
- **4 MCP Servers**: Social Publish (5 platforms), Social Discover (analytics), Obsidian Vault (knowledge base), Remotion Render (video production)
- **4 Safety Hooks**: Audit Logger, Circuit Breaker, Preview Before Publish, Dry Run Guard
- **1 Command**: `/grow` with subcommands (strategy, create, publish, analyze, research, report, carousel, video, setup)
- **Shared Library**: Config management, intent routing, autonomy system, rate limiting, circuit breaker, audit logging, carousel generator
- **Remotion Video System**: 11 compositions (ReelTips, ReelBeforeAfter, ReelNumbers, ExplainerSteps, ExplainerDemo, CarouselAnimated, ComponentShowcase, TechTerminal, ProductDemo, AppWalkthrough, TechTerminalPro)
- **6 Carousel Templates**: Minimal, Bold, Gradient, Clean Educator, Dark Premium, Vibrant Creator
- **Brand Voice System**: YAML-based configuration with tone, audience, anti-slop filters
- **Progressive Autonomy**: 4 levels (supervised, assisted, delegated, autonomous) with kill switch
- **Docker Support**: docker-compose setup for all MCP servers
- **CI/CD**: GitHub Actions workflow with lint, test, security scan

### Known Limitations

- Social platform adapters (Twitter, LinkedIn, Reddit, GitHub, Threads) return preview data but publishing is pending API integration — use dry-run mode for content generation workflows
