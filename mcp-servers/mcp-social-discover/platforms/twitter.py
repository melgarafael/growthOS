"""Twitter/X discovery adapter — returns realistic mock data for agent testing."""

import hashlib
from typing import Any

from platforms.base import DiscoveryAdapter


def _seed(text: str) -> int:
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)


class TwitterDiscoveryAdapter(DiscoveryAdapter):

    @property
    def platform_name(self) -> str:
        return "twitter"

    async def get_analytics(self, date_from: str, date_to: str) -> dict[str, Any]:
        s = _seed(f"twitter-analytics-{date_from}-{date_to}")
        return {
            "platform": "twitter",
            "period": {"from": date_from, "to": date_to},
            "impressions": 45000 + (s % 20000),
            "clicks": 2100 + (s % 800),
            "shares": 580 + (s % 200),
            "comments": 320 + (s % 150),
            "engagement_rate": round(3.1 + (s % 25) / 10, 1),
            "followers_gained": 78 + (s % 50),
            "top_posts": [
                {
                    "id": f"tw-{s % 10000}",
                    "text": "Thread: 10 things we learned shipping v2.0 🧵",
                    "impressions": 18500,
                    "engagement_rate": 9.2,
                },
                {
                    "id": f"tw-{(s + 1) % 10000}",
                    "text": "Hot take: The best marketing is a great product.",
                    "impressions": 12300,
                    "engagement_rate": 7.5,
                },
            ],
            "_mock": True,
        }

    async def discover_trends(self, topic: str) -> dict[str, Any]:
        s = _seed(f"twitter-trends-{topic}")
        return {
            "platform": "twitter",
            "topic": topic,
            "trending_hashtags": [
                f"#{topic.replace(' ', '')}",
                f"#{topic.replace(' ', '')}Twitter",
                "#TechTwitter",
                "#BuildInPublic",
                "#Trending",
            ],
            "trending_topics": [
                {"topic": f"{topic} drama", "volume": 52000 + (s % 20000), "growth": "+45%"},
                {"topic": f"Why {topic} matters", "volume": 23000 + (s % 10000), "growth": "+18%"},
                {"topic": f"{topic} alternatives", "volume": 14000 + (s % 5000), "growth": "+12%"},
            ],
            "popular_formats": [
                {"format": "thread", "engagement_multiplier": 3.2},
                {"format": "quote_tweet", "engagement_multiplier": 2.1},
                {"format": "poll", "engagement_multiplier": 1.9},
                {"format": "image", "engagement_multiplier": 1.5},
            ],
            "insights": [
                "Threads with 5-8 tweets get highest completion rates on X",
                f"'{topic}' conversations spike on weekday evenings 6-9 PM",
                "Quote tweets with added context get 2x more impressions",
            ],
            "_mock": True,
        }

    async def search_mentions(self, query: str, limit: int = 50) -> dict[str, Any]:
        s = _seed(f"twitter-mentions-{query}")
        count = min(limit, 5)
        mentions = [
            {
                "id": f"tw-mention-{s + i}",
                "author": f"@user_{s + i}",
                "content": [
                    f"Just tried {query} and I'm impressed. The onboarding is 🔥",
                    f"Anyone else using {query}? Curious about your experience.",
                    f"Switched from competitor to {query}. Night and day difference.",
                    f"{query} needs to fix their API rate limits. Pretty frustrating.",
                    f"Great thread by {query} team on scaling challenges.",
                ][i % 5],
                "timestamp": f"2026-03-{28 + i}T{14 + i}:30:00Z",
                "sentiment": ["positive", "neutral", "positive", "negative", "positive"][i % 5],
                "engagement": {"likes": 120 + (s + i) % 100, "retweets": 35 + (s + i) % 30, "replies": 18 + (s + i) % 15},
                "url": f"https://x.com/user_{s + i}/status/{s + i}",
            }
            for i in range(count)
        ]
        return {
            "platform": "twitter",
            "query": query,
            "mentions": mentions,
            "total_count": 890 + (s % 500),
            "sentiment_breakdown": {"positive": 55, "neutral": 30, "negative": 15},
            "_mock": True,
        }

    async def get_competitor_activity(self, competitor: str) -> dict[str, Any]:
        s = _seed(f"twitter-competitor-{competitor}")
        return {
            "platform": "twitter",
            "competitor": competitor,
            "followers": 45000 + (s % 30000),
            "posting_frequency": "5-8 tweets/day",
            "avg_engagement": {
                "likes": 340 + (s % 200),
                "retweets": 85 + (s % 60),
                "replies": 42 + (s % 30),
            },
            "recent_posts": [
                {
                    "text": f"Excited to announce {competitor} v3.0! 🚀 Here's what's new...",
                    "date": "2026-03-29",
                    "engagement_rate": 6.8,
                    "format": "thread",
                },
                {
                    "text": f"Our team at {competitor} just hit a major milestone.",
                    "date": "2026-03-27",
                    "engagement_rate": 4.2,
                    "format": "image",
                },
            ],
            "top_content": {
                "best_format": "thread",
                "best_posting_time": "Monday 10:00 AM",
                "most_used_hashtags": ["#BuildInPublic", "#StartupLife", f"#{competitor.replace(' ', '')}"],
            },
            "_mock": True,
        }

    async def get_hashtag_performance(self, hashtag: str) -> dict[str, Any]:
        tag = hashtag.lstrip("#")
        s = _seed(f"twitter-hashtag-{tag}")
        return {
            "platform": "twitter",
            "hashtag": f"#{tag}",
            "reach": 250000 + (s % 150000),
            "posts_count": 5400 + (s % 3000),
            "engagement_rate": round(2.8 + (s % 35) / 10, 1),
            "peak_hours": ["10:00 AM", "1:00 PM", "7:00 PM"],
            "related_hashtags": [f"#{tag}Community", "#Tech", "#Trending", "#Viral"],
            "trend": "viral" if s % 5 == 0 else "rising" if s % 3 == 0 else "stable",
            "_mock": True,
        }
