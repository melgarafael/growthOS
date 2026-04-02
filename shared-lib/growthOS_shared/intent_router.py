"""GrowthOS intent router — subcommand parsing and NLP intent classification.

Mirrors the routing logic defined in commands/grow/COMMAND.md for testability.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Intent(str, Enum):
    STRATEGY = "strategy"
    CREATE = "create"
    PUBLISH = "publish"
    ANALYZE = "analyze"
    RESEARCH = "research"
    REPORT = "report"
    VISUAL = "visual"
    LANDING = "landing"
    SETUP = "setup"
    WELCOME = "welcome"
    UNKNOWN = "unknown"


AGENT_MAP: dict[Intent, str] = {
    Intent.STRATEGY: "growth-strategist",
    Intent.CREATE: "content-creator",
    Intent.PUBLISH: "social-publisher",
    Intent.ANALYZE: "intelligence-analyst",
    Intent.RESEARCH: "intelligence-analyst",
    Intent.REPORT: "intelligence-analyst",
    Intent.VISUAL: "visual-designer",
    Intent.LANDING: "growth-engineer",
}

SUBCOMMAND_KEYWORDS: dict[str, Intent] = {
    "strategy": Intent.STRATEGY,
    "create": Intent.CREATE,
    "publish": Intent.PUBLISH,
    "analyze": Intent.ANALYZE,
    "research": Intent.RESEARCH,
    "report": Intent.REPORT,
    "visual": Intent.VISUAL,
    "design": Intent.VISUAL,
    "landing": Intent.LANDING,
    "setup": Intent.SETUP,
}

CONTENT_TYPES = {"blog", "social", "newsletter", "email", "thread", "article", "carousel"}

PLATFORMS = {
    "linkedin", "twitter", "x", "reddit", "threads",
    "github", "youtube", "instagram", "stackoverflow",
}

REPORT_PERIODS = {
    "weekly", "monthly", "quarterly", "yearly", "ytd",
    "last-week", "last-month", "last-quarter",
}

INTENT_TRIGGERS: dict[Intent, list[str]] = {
    Intent.STRATEGY: [
        "plan", "strategy", "okr", "roadmap", "calendar",
        "campaign plan", "go-to-market", "gtm", "quarterly plan",
        "content strategy", "marketing plan",
    ],
    Intent.CREATE: [
        "write", "create", "draft", "blog", "article",
        "newsletter", "email", "copy", "thread", "content",
    ],
    Intent.PUBLISH: [
        "publish", "share", "schedule", "distribute",
        "send", "push live", "go live",
    ],
    Intent.ANALYZE: [
        "analyze", "competitor", "market", "trend", "swot",
        "benchmark", "compare", "landscape",
    ],
    Intent.RESEARCH: [
        "research", "find", "explore", "discover",
        "investigate", "look into", "dig into", "learn about",
    ],
    Intent.REPORT: [
        "report", "summary", "metrics", "performance",
        "dashboard", "analytics", "kpis", "results",
    ],
    Intent.VISUAL: [
        "design", "visual", "image", "graphic", "thumbnail",
        "banner", "og image", "social graphic", "infographic",
        "carousel design",
    ],
    Intent.LANDING: [
        "landing page", "conversion", "a/b test", "cro",
        "funnel", "sign-up page", "lead capture", "squeeze page",
    ],
}

PIPELINE_PATTERNS: dict[str, list[Intent]] = {
    "create-and-publish": [Intent.CREATE, Intent.PUBLISH],
    "create-and-design": [Intent.CREATE, Intent.VISUAL],
    "research-and-create": [Intent.RESEARCH, Intent.CREATE],
    "full-publish-pipeline": [Intent.CREATE, Intent.VISUAL, Intent.PUBLISH],
}

PIPELINE_TRIGGERS: dict[str, list[str]] = {
    "create-and-publish": [
        "create and publish", "write and share", "draft and post",
    ],
    "create-and-design": [
        "create with image", "create with graphic", "create with visual",
        "write and design", "blog post with og image",
    ],
    "research-and-create": [
        "research and write", "research and create", "research and draft",
        "find out about and write",
    ],
    "full-publish-pipeline": [
        "create, design, and publish", "end to end campaign",
        "full pipeline",
    ],
}


@dataclass
class SubcommandResult:
    """Result of subcommand argument parsing."""
    intent: Intent
    agent: str | None
    args: dict[str, str | None] = field(default_factory=dict)
    needs_help: bool = False


@dataclass
class RouteResult:
    """Result of the full routing decision."""
    intent: Intent
    agent: str | None
    confidence: float = 1.0
    pipeline: str | None = None
    pipeline_agents: list[str] = field(default_factory=list)
    args: dict[str, str | None] = field(default_factory=dict)
    needs_help: bool = False
    is_first_run: bool = False


def check_first_run(config_dir: str | None = None) -> bool:
    """Check if brand-voice.yaml exists (first-run detection)."""
    search_dir = config_dir or os.environ.get("GROWTHOS_CONFIG_DIR", ".")
    paths_to_check = [
        Path(search_dir) / "brand-voice.yaml",
        Path(search_dir) / "growthOS" / "brand-voice.yaml",
    ]
    return not any(p.exists() for p in paths_to_check)


def parse_subcommand(keyword: str, remaining: str) -> SubcommandResult:
    """Parse arguments for a known subcommand keyword."""
    intent = SUBCOMMAND_KEYWORDS[keyword]
    agent = AGENT_MAP.get(intent)
    remaining = remaining.strip()

    if not remaining:
        return SubcommandResult(intent=intent, agent=agent, needs_help=True)

    if intent == Intent.STRATEGY:
        return SubcommandResult(intent=intent, agent=agent, args={"topic": remaining})

    if intent == Intent.CREATE:
        words = remaining.split(None, 1)
        first_word = words[0].lower()
        if first_word in CONTENT_TYPES:
            topic = words[1] if len(words) > 1 else None
            return SubcommandResult(
                intent=intent, agent=agent,
                args={"type": first_word, "topic": topic},
                needs_help=topic is None,
            )
        return SubcommandResult(
            intent=intent, agent=agent,
            args={"type": None, "topic": remaining},
        )

    if intent == Intent.PUBLISH:
        words = remaining.split(None, 1)
        first_word = words[0].lower()
        if first_word in PLATFORMS:
            content = words[1] if len(words) > 1 else None
            return SubcommandResult(
                intent=intent, agent=agent,
                args={"platform": first_word, "content": content},
            )
        return SubcommandResult(
            intent=intent, agent=agent,
            args={"platform": None, "content": remaining},
        )

    if intent == Intent.ANALYZE:
        return SubcommandResult(intent=intent, agent=agent, args={"subject": remaining})

    if intent == Intent.RESEARCH:
        return SubcommandResult(intent=intent, agent=agent, args={"topic": remaining})

    if intent == Intent.REPORT:
        words = remaining.split(None, 1)
        first_word = words[0].lower()
        if first_word in REPORT_PERIODS:
            focus = words[1] if len(words) > 1 else None
            return SubcommandResult(
                intent=intent, agent=agent,
                args={"period": first_word, "focus": focus},
            )
        return SubcommandResult(
            intent=intent, agent=agent,
            args={"period": "monthly", "focus": remaining},
        )

    return SubcommandResult(intent=intent, agent=agent, args={"raw": remaining})


def _check_pipeline(text_lower: str) -> RouteResult | None:
    """Check if input matches a multi-agent pipeline pattern."""
    # Exact substring match
    for pipeline_name, triggers in PIPELINE_TRIGGERS.items():
        for trigger in triggers:
            if trigger in text_lower:
                agents = [AGENT_MAP[i] for i in PIPELINE_PATTERNS[pipeline_name]]
                return RouteResult(
                    intent=PIPELINE_PATTERNS[pipeline_name][0],
                    agent=agents[0],
                    confidence=0.9,
                    pipeline=pipeline_name,
                    pipeline_agents=agents,
                )

    # Detect compound intents: multiple intent categories present
    # e.g., "create ... and publish", "write ... and share", "research ... and create"
    found_intents: list[Intent] = []
    words = set(text_lower.split())
    # Use distinct verbs per intent to avoid false matches
    # "post" is excluded — too ambiguous between create and publish
    verb_map = {
        Intent.CREATE: {"write", "create", "draft"},
        Intent.PUBLISH: {"publish", "share", "distribute"},
        Intent.RESEARCH: {"research", "explore", "investigate"},
        Intent.VISUAL: {"design"},
    }
    for intent, verbs in verb_map.items():
        if words & verbs:
            found_intents.append(intent)

    if len(found_intents) >= 2:
        # Check if any defined pipeline matches the found intent combination
        for pipeline_name, pipeline_intents in PIPELINE_PATTERNS.items():
            if all(i in found_intents for i in pipeline_intents):
                agents = [AGENT_MAP[i] for i in pipeline_intents]
                return RouteResult(
                    intent=pipeline_intents[0],
                    agent=agents[0],
                    confidence=0.85,
                    pipeline=pipeline_name,
                    pipeline_agents=agents,
                )

    return None


# Primary verb detection — the FIRST verb in the sentence drives intent
_VERB_INTENT_MAP: dict[str, Intent] = {
    "write": Intent.CREATE,
    "draft": Intent.CREATE,
    "plan": Intent.STRATEGY,
    "strategize": Intent.STRATEGY,
    "publish": Intent.PUBLISH,
    "share": Intent.PUBLISH,
    "schedule": Intent.PUBLISH,
    "distribute": Intent.PUBLISH,
    "analyze": Intent.ANALYZE,
    "benchmark": Intent.ANALYZE,
    "compare": Intent.ANALYZE,
    "research": Intent.RESEARCH,
    "explore": Intent.RESEARCH,
    "investigate": Intent.RESEARCH,
    "discover": Intent.RESEARCH,
    "find": Intent.RESEARCH,
    "report": Intent.REPORT,
    "summarize": Intent.REPORT,
    "generate": Intent.REPORT,
    "design": Intent.VISUAL,
    "make": Intent.VISUAL,
    "build": Intent.LANDING,
    "optimize": Intent.LANDING,
}


def classify_intent(text: str) -> RouteResult:
    """Classify natural language input into an intent with confidence scoring."""
    text_lower = text.lower()

    # Check for pipeline patterns first
    pipeline_result = _check_pipeline(text_lower)
    if pipeline_result is not None:
        return pipeline_result

    # Score each intent by trigger matches
    scores: dict[Intent, float] = {}
    for intent, triggers in INTENT_TRIGGERS.items():
        score = 0.0
        for trigger in triggers:
            if trigger in text_lower:
                # Multi-word triggers are much more specific — heavy weight
                weight = 4.0 if " " in trigger else 1.0
                score += weight
        if score > 0:
            scores[intent] = score

    # Primary verb boost: the first verb in the sentence gets a bonus,
    # but only if no multi-word trigger already scored higher for another intent
    words = text_lower.split()
    for word in words[:4]:  # Check first 4 words for the primary verb
        if word in _VERB_INTENT_MAP:
            verb_intent = _VERB_INTENT_MAP[word]
            # Only apply verb boost if no other intent has a strong multi-word match
            other_max = max(
                (s for i, s in scores.items() if i != verb_intent),
                default=0,
            )
            if other_max < 4.0:  # No strong multi-word competitor
                scores[verb_intent] = scores.get(verb_intent, 0) + 3.0
            else:
                scores[verb_intent] = scores.get(verb_intent, 0) + 1.0
            break

    if not scores:
        return RouteResult(intent=Intent.UNKNOWN, agent=None, confidence=0.0)

    best_intent = max(scores, key=scores.get)  # type: ignore[arg-type]
    # Confidence: ratio of best score to max possible, capped at 0.95 for NLP
    max_score = max(scores.values())
    second_best = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0
    confidence = min(0.95, max_score / (max_score + second_best) if second_best > 0 else 0.9)

    return RouteResult(
        intent=best_intent,
        agent=AGENT_MAP.get(best_intent),
        confidence=confidence,
    )


def route(user_input: str | None) -> RouteResult:
    """Main routing function — mirrors COMMAND.md Step 2-4 logic."""
    # Step 2: No arguments → welcome
    if not user_input or not user_input.strip():
        return RouteResult(intent=Intent.WELCOME, agent=None)

    text = user_input.strip()
    words = text.split(None, 1)
    first_word = words[0].lower()

    # Step 3: Subcommand keyword bypass
    if first_word in SUBCOMMAND_KEYWORDS:
        remaining = words[1] if len(words) > 1 else ""
        sub = parse_subcommand(first_word, remaining)
        return RouteResult(
            intent=sub.intent,
            agent=sub.agent,
            confidence=1.0,
            args=sub.args,
            needs_help=sub.needs_help,
        )

    # Step 4: NLP intent classification
    return classify_intent(text)
