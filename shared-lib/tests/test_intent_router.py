"""Tests for GrowthOS intent router — subcommand parsing and NLP classification.

Covers all 6 subcommands, argument parsing, welcome/help messages,
intent classification with 20+ NLP samples, and pipeline detection.
"""

import os
from unittest.mock import patch

import pytest

from growthOS_shared.intent_router import (
    AGENT_MAP,
    CONTENT_TYPES,
    Intent,
    PLATFORMS,
    REPORT_PERIODS,
    SUBCOMMAND_KEYWORDS,
    check_first_run,
    classify_intent,
    route,
)


# ── Welcome / No-args ──────────────────────────────────────────────


class TestWelcome:
    """AC2: /grow with no args shows welcome message."""

    def test_no_args_returns_welcome(self):
        result = route(None)
        assert result.intent == Intent.WELCOME
        assert result.agent is None

    def test_empty_string_returns_welcome(self):
        result = route("")
        assert result.intent == Intent.WELCOME

    def test_whitespace_only_returns_welcome(self):
        result = route("   ")
        assert result.intent == Intent.WELCOME


# ── First-Run Detection ────────────────────────────────────────────


class TestFirstRunDetection:
    """AC4: First-run detects missing brand-voice.yaml."""

    def test_first_run_when_no_config(self, tmp_path):
        assert check_first_run(str(tmp_path)) is True

    def test_not_first_run_when_config_exists(self, tmp_path):
        (tmp_path / "brand-voice.yaml").write_text("brand:\n  name: Test")
        assert check_first_run(str(tmp_path)) is False

    def test_not_first_run_when_config_in_subdir(self, tmp_path):
        growthos_dir = tmp_path / "growthOS"
        growthos_dir.mkdir()
        (growthos_dir / "brand-voice.yaml").write_text("brand:\n  name: Test")
        assert check_first_run(str(tmp_path)) is False

    def test_first_run_ignores_example_file(self, tmp_path):
        (tmp_path / "brand-voice.example.yaml").write_text("brand:\n  name: Example")
        assert check_first_run(str(tmp_path)) is True

    def test_env_var_override(self, tmp_path):
        (tmp_path / "brand-voice.yaml").write_text("brand:\n  name: Test")
        with patch.dict(os.environ, {"GROWTHOS_CONFIG_DIR": str(tmp_path)}):
            assert check_first_run() is False


# ── Subcommand: strategy ───────────────────────────────────────────


class TestStrategySubcommand:
    """AC1: /grow strategy [topic] → growth-strategist."""

    def test_strategy_with_topic(self):
        result = route("strategy Q2 content plan")
        assert result.intent == Intent.STRATEGY
        assert result.agent == "growth-strategist"
        assert result.args["topic"] == "Q2 content plan"
        assert result.confidence == 1.0
        assert result.needs_help is False

    def test_strategy_no_args_shows_help(self):
        result = route("strategy")
        assert result.intent == Intent.STRATEGY
        assert result.agent == "growth-strategist"
        assert result.needs_help is True

    def test_strategy_complex_topic(self):
        result = route("strategy go-to-market plan for SaaS product launch")
        assert result.args["topic"] == "go-to-market plan for SaaS product launch"


# ── Subcommand: create ─────────────────────────────────────────────


class TestCreateSubcommand:
    """AC2: /grow create [type] [topic] → content-creator."""

    def test_create_blog_with_topic(self):
        result = route("create blog post about AI agents")
        assert result.intent == Intent.CREATE
        assert result.agent == "content-creator"
        assert result.args["type"] == "blog"
        assert result.args["topic"] == "post about AI agents"

    def test_create_social_with_topic(self):
        result = route("create social announcing our new feature")
        assert result.args["type"] == "social"
        assert result.args["topic"] == "announcing our new feature"

    def test_create_newsletter_with_topic(self):
        result = route("create newsletter weekly digest")
        assert result.args["type"] == "newsletter"
        assert result.args["topic"] == "weekly digest"

    def test_create_email_with_topic(self):
        result = route("create email onboarding sequence")
        assert result.args["type"] == "email"
        assert result.args["topic"] == "onboarding sequence"

    def test_create_thread_with_topic(self):
        result = route("create thread 5 lessons from scaling")
        assert result.args["type"] == "thread"
        assert result.args["topic"] == "5 lessons from scaling"

    def test_create_article_with_topic(self):
        result = route("create article about remote work trends")
        assert result.args["type"] == "article"
        assert result.args["topic"] == "about remote work trends"

    def test_create_carousel_with_topic(self):
        result = route("create carousel top 10 marketing tips")
        assert result.args["type"] == "carousel"
        assert result.args["topic"] == "top 10 marketing tips"

    def test_create_type_without_topic_needs_help(self):
        result = route("create blog")
        assert result.args["type"] == "blog"
        assert result.args["topic"] is None
        assert result.needs_help is True

    def test_create_no_type_infers_from_context(self):
        result = route("create a LinkedIn post about remote work")
        assert result.args["type"] is None
        assert result.args["topic"] == "a LinkedIn post about remote work"

    def test_create_no_args_shows_help(self):
        result = route("create")
        assert result.intent == Intent.CREATE
        assert result.needs_help is True

    def test_all_content_types_recognized(self):
        for ctype in CONTENT_TYPES:
            result = route(f"create {ctype} test topic")
            assert result.args["type"] == ctype, f"Failed for type: {ctype}"


# ── Subcommand: publish ────────────────────────────────────────────


class TestPublishSubcommand:
    """AC3: /grow publish [platform] [content] → social-publisher."""

    def test_publish_linkedin(self):
        result = route("publish linkedin this blog post")
        assert result.intent == Intent.PUBLISH
        assert result.agent == "social-publisher"
        assert result.args["platform"] == "linkedin"
        assert result.args["content"] == "this blog post"

    def test_publish_twitter(self):
        result = route("publish twitter thread about our launch")
        assert result.args["platform"] == "twitter"

    def test_publish_reddit(self):
        result = route("publish reddit r/programming this article")
        assert result.args["platform"] == "reddit"

    def test_publish_no_platform(self):
        result = route("publish this across all channels")
        assert result.args["platform"] is None
        assert result.args["content"] == "this across all channels"

    def test_publish_platform_no_content(self):
        result = route("publish linkedin")
        assert result.args["platform"] == "linkedin"
        assert result.args["content"] is None

    def test_publish_no_args_shows_help(self):
        result = route("publish")
        assert result.needs_help is True

    def test_all_platforms_recognized(self):
        for platform in PLATFORMS:
            result = route(f"publish {platform} test content")
            assert result.args["platform"] == platform, f"Failed for platform: {platform}"


# ── Subcommand: analyze ────────────────────────────────────────────


class TestAnalyzeSubcommand:
    """AC4: /grow analyze [subject] → intelligence-analyst."""

    def test_analyze_competitors(self):
        result = route("analyze our top 3 competitors")
        assert result.intent == Intent.ANALYZE
        assert result.agent == "intelligence-analyst"
        assert result.args["subject"] == "our top 3 competitors"

    def test_analyze_market(self):
        result = route("analyze market trends in SaaS")
        assert result.args["subject"] == "market trends in SaaS"

    def test_analyze_no_args_shows_help(self):
        result = route("analyze")
        assert result.needs_help is True


# ── Subcommand: research ───────────────────────────────────────────


class TestResearchSubcommand:
    """AC5: /grow research [topic] → intelligence-analyst."""

    def test_research_topic(self):
        result = route("research best practices for B2B email")
        assert result.intent == Intent.RESEARCH
        assert result.agent == "intelligence-analyst"
        assert result.args["topic"] == "best practices for B2B email"

    def test_research_no_args_shows_help(self):
        result = route("research")
        assert result.needs_help is True


# ── Subcommand: report ─────────────────────────────────────────────


class TestReportSubcommand:
    """AC6: /grow report [period] → intelligence-analyst."""

    def test_report_monthly(self):
        result = route("report monthly")
        assert result.intent == Intent.REPORT
        assert result.agent == "intelligence-analyst"
        assert result.args["period"] == "monthly"
        assert result.args["focus"] is None

    def test_report_weekly_with_focus(self):
        result = route("report weekly social media performance")
        assert result.args["period"] == "weekly"
        assert result.args["focus"] == "social media performance"

    def test_report_quarterly(self):
        result = route("report quarterly content ROI")
        assert result.args["period"] == "quarterly"
        assert result.args["focus"] == "content ROI"

    def test_report_ytd(self):
        result = route("report ytd growth summary")
        assert result.args["period"] == "ytd"

    def test_report_no_period_defaults_monthly(self):
        result = route("report KPI dashboard for marketing")
        assert result.args["period"] == "monthly"
        assert result.args["focus"] == "KPI dashboard for marketing"

    def test_report_no_args_shows_help(self):
        result = route("report")
        assert result.needs_help is True

    def test_all_periods_recognized(self):
        for period in REPORT_PERIODS:
            result = route(f"report {period}")
            assert result.args["period"] == period, f"Failed for period: {period}"


# ── NLP Intent Classification ──────────────────────────────────────


class TestNLPIntentClassification:
    """AC1/AC3: Natural language routes through CMO intent classification."""

    @pytest.mark.parametrize("input_text,expected_intent", [
        # Strategy intents — unambiguous verb
        ("plan our Q2 marketing strategy", Intent.STRATEGY),
        ("define OKRs for the marketing team", Intent.STRATEGY),
        ("strategize our go-to-market approach", Intent.STRATEGY),
        # Create intents
        ("write a blog post about AI in healthcare", Intent.CREATE),
        ("draft a newsletter for this week", Intent.CREATE),
        ("write email copy for our onboarding sequence", Intent.CREATE),
        # Publish intents
        ("publish this to LinkedIn", Intent.PUBLISH),
        ("schedule a tweet for tomorrow", Intent.PUBLISH),
        ("share this across all platforms", Intent.PUBLISH),
        # Analyze intents
        ("analyze our top 3 competitors", Intent.ANALYZE),
        ("do a SWOT analysis for our positioning", Intent.ANALYZE),
        ("benchmark our content against competitors", Intent.ANALYZE),
        # Research intents
        ("research the best practices for B2B email marketing", Intent.RESEARCH),
        ("explore emerging platforms for developer marketing", Intent.RESEARCH),
        ("investigate the ROI of podcast marketing", Intent.RESEARCH),
        # Report intents
        ("generate a monthly marketing report", Intent.REPORT),
        ("show me our content performance metrics", Intent.REPORT),
        ("summarize our social media results", Intent.REPORT),
        # Visual intents — unambiguous verb
        ("design a social graphic for our product launch", Intent.VISUAL),
        ("make a social graphic for our product launch", Intent.VISUAL),
        # Landing intents
        ("build a landing page for our new product", Intent.LANDING),
        ("optimize our sign-up page conversion rate", Intent.LANDING),
    ])
    def test_nlp_classification(self, input_text, expected_intent):
        result = classify_intent(input_text)
        assert result.intent == expected_intent, (
            f"Input '{input_text}' classified as {result.intent}, expected {expected_intent}"
        )
        assert result.agent == AGENT_MAP[expected_intent]
        assert result.confidence > 0

    @pytest.mark.parametrize("input_text,acceptable_intents", [
        # "create" + strategy object → verb wins (create) but strategy is also valid
        ("create a content calendar for next month", {Intent.CREATE, Intent.STRATEGY}),
        # "design" + strategy object → verb wins (visual) but strategy is also valid
        ("design a go-to-market plan for our launch", {Intent.VISUAL, Intent.STRATEGY}),
        # "create" + visual object → verb wins (create) but visual is also valid
        ("create a thumbnail for our YouTube video", {Intent.CREATE, Intent.VISUAL}),
    ])
    def test_ambiguous_inputs_route_to_acceptable_intent(self, input_text, acceptable_intents):
        """Edge cases where verb and object suggest different intents.
        In runtime, the CMO (Claude) resolves these with semantic understanding.
        The deterministic parser picks based on verb priority, which is acceptable."""
        result = classify_intent(input_text)
        assert result.intent in acceptable_intents, (
            f"Input '{input_text}' classified as {result.intent}, "
            f"expected one of {acceptable_intents}"
        )

    def test_unknown_input_returns_unknown(self):
        result = classify_intent("hello how are you")
        assert result.intent == Intent.UNKNOWN
        assert result.confidence == 0.0


# ── Pipeline Detection ─────────────────────────────────────────────


class TestPipelineDetection:
    """Compound intents detect multi-agent pipelines."""

    def test_create_and_publish_pipeline(self):
        result = classify_intent("create a blog post and publish it")
        assert result.pipeline == "create-and-publish"
        assert result.pipeline_agents == ["content-creator", "social-publisher"]

    def test_write_and_share_pipeline(self):
        result = classify_intent("write a post and share it on LinkedIn")
        assert result.pipeline == "create-and-publish"

    def test_research_and_create_pipeline(self):
        result = classify_intent("research competitor pricing and create a report")
        assert result.pipeline == "research-and-create"
        assert result.pipeline_agents == ["intelligence-analyst", "content-creator"]

    def test_full_pipeline(self):
        result = classify_intent("end to end campaign for product launch")
        assert result.pipeline == "full-publish-pipeline"
        assert len(result.pipeline_agents) == 3

    def test_create_and_design_pipeline(self):
        result = classify_intent("write a blog post and design the OG image")
        assert result.pipeline == "create-and-design"


# ── Subcommand Bypass vs NLP ───────────────────────────────────────


class TestSubcommandBypass:
    """AC5: Known subcommands bypass NLP routing."""

    def test_keyword_routes_directly(self):
        for keyword in SUBCOMMAND_KEYWORDS:
            if keyword == "setup":
                continue
            result = route(f"{keyword} test input")
            assert result.confidence == 1.0, (
                f"Keyword '{keyword}' should bypass NLP with confidence 1.0"
            )

    def test_non_keyword_goes_through_nlp(self):
        result = route("write a blog post about testing")
        # "write" is not a subcommand keyword, so goes through NLP
        assert result.intent == Intent.CREATE
        assert result.confidence <= 0.95  # NLP confidence is capped below 1.0

    def test_case_insensitive_keyword(self):
        result = route("Strategy Q2 plan")
        assert result.intent == Intent.STRATEGY
        assert result.confidence == 1.0

    def test_design_keyword_routes_to_visual(self):
        result = route("design a banner for our launch")
        assert result.intent == Intent.VISUAL
        assert result.agent == "visual-designer"


# ── Agent Map Completeness ─────────────────────────────────────────


class TestAgentMapCompleteness:
    """Verify all routable intents have an agent mapping."""

    def test_all_intents_except_meta_have_agents(self):
        meta_intents = {Intent.WELCOME, Intent.UNKNOWN, Intent.SETUP}
        for intent in Intent:
            if intent in meta_intents:
                continue
            assert intent in AGENT_MAP, f"Intent {intent} missing from AGENT_MAP"

    def test_seven_unique_agents(self):
        unique_agents = set(AGENT_MAP.values())
        assert len(unique_agents) == 6  # intelligence-analyst serves 3 intents
        assert "growth-strategist" in unique_agents
        assert "content-creator" in unique_agents
        assert "social-publisher" in unique_agents
        assert "intelligence-analyst" in unique_agents
        assert "visual-designer" in unique_agents
        assert "growth-engineer" in unique_agents
