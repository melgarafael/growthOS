"""LinkedIn discovery adapter — returns realistic mock data for agent testing."""

import hashlib
from typing import Any

from platforms.base import DiscoveryAdapter


def _seed(text: str) -> int:
    """Deterministic seed from text so mock data is reproducible."""
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)


class LinkedInDiscoveryAdapter(DiscoveryAdapter):

    @property
    def platform_name(self) -> str:
        return "linkedin"

    async def get_analytics(self, date_from: str, date_to: str) -> dict[str, Any]:
        s = _seed(f"linkedin-analytics-{date_from}-{date_to}")
        return {
            "platform": "linkedin",
            "period": {"from": date_from, "to": date_to},
            "impressions": 12400 + (s % 5000),
            "clicks": 890 + (s % 300),
            "shares": 145 + (s % 80),
            "comments": 67 + (s % 40),
            "engagement_rate": round(4.2 + (s % 30) / 10, 1),
            "followers_gained": 34 + (s % 20),
            "top_posts": [
                {
                    "id": f"li-post-{s % 1000}",
                    "title": "How We Scaled Our Engineering Team",
                    "impressions": 4200,
                    "engagement_rate": 8.3,
                },
                {
                    "id": f"li-post-{(s + 1) % 1000}",
                    "title": "5 Lessons from Our Product Launch",
                    "impressions": 3100,
                    "engagement_rate": 6.7,
                },
            ],
            "_mock": True,
        }

    async def discover_trends(self, topic: str) -> dict[str, Any]:
        s = _seed(f"linkedin-trends-{topic}")
        return {
            "platform": "linkedin",
            "topic": topic,
            "trending_hashtags": [
                f"#{topic.replace(' ', '')}",
                "#Innovation",
                "#Leadership",
                "#FutureOfWork",
                "#TechTrends",
            ],
            "trending_topics": [
                {"topic": f"AI in {topic}", "volume": 15000 + (s % 5000), "growth": "+23%"},
                {"topic": f"{topic} best practices", "volume": 8200 + (s % 3000), "growth": "+15%"},
                {"topic": f"Remote {topic}", "volume": 6100 + (s % 2000), "growth": "+8%"},
            ],
            "popular_formats": [
                {"format": "carousel", "engagement_multiplier": 2.1},
                {"format": "long_form_article", "engagement_multiplier": 1.8},
                {"format": "poll", "engagement_multiplier": 1.6},
                {"format": "video", "engagement_multiplier": 1.4},
            ],
            "insights": [
                "Carousel posts get 2x more engagement than text-only posts on LinkedIn",
                f"'{topic}' discussions peak on Tuesday-Thursday mornings",
                "Articles over 1500 words perform best for thought leadership",
            ],
            "_mock": True,
        }

    async def search_mentions(self, query: str, limit: int = 50) -> dict[str, Any]:
        s = _seed(f"linkedin-mentions-{query}")
        count = min(limit, 5)
        mentions = [
            {
                "id": f"li-mention-{s + i}",
                "author": f"Professional User {i + 1}",
                "content": f"Great insights from {query} on building scalable teams. Highly recommend their approach.",
                "timestamp": f"2026-03-{28 + i}T10:{i * 15:02d}:00Z",
                "sentiment": ["positive", "positive", "neutral", "positive", "negative"][i % 5],
                "engagement": {"likes": 45 + (s + i) % 30, "comments": 8 + (s + i) % 10},
                "url": f"https://linkedin.com/posts/{s + i}",
            }
            for i in range(count)
        ]
        return {
            "platform": "linkedin",
            "query": query,
            "mentions": mentions,
            "total_count": 230 + (s % 100),
            "sentiment_breakdown": {"positive": 62, "neutral": 28, "negative": 10},
            "_mock": True,
        }

    async def get_competitor_activity(self, competitor: str) -> dict[str, Any]:
        s = _seed(f"linkedin-competitor-{competitor}")
        return {
            "platform": "linkedin",
            "competitor": competitor,
            "followers": 15000 + (s % 10000),
            "posting_frequency": "3-4 posts/week",
            "avg_engagement": {
                "likes": 120 + (s % 80),
                "comments": 25 + (s % 20),
                "shares": 18 + (s % 15),
            },
            "recent_posts": [
                {
                    "title": f"{competitor}'s Q1 Results Deep Dive",
                    "date": "2026-03-28",
                    "engagement_rate": 5.2,
                    "format": "article",
                },
                {
                    "title": f"How {competitor} Approaches Innovation",
                    "date": "2026-03-25",
                    "engagement_rate": 4.8,
                    "format": "carousel",
                },
            ],
            "top_content": {
                "best_format": "carousel",
                "best_posting_time": "Tuesday 9:00 AM",
                "most_used_hashtags": ["#Innovation", "#Growth", f"#{competitor.replace(' ', '')}"],
            },
            "_mock": True,
        }

    async def get_hashtag_performance(self, hashtag: str) -> dict[str, Any]:
        tag = hashtag.lstrip("#")
        s = _seed(f"linkedin-hashtag-{tag}")
        return {
            "platform": "linkedin",
            "hashtag": f"#{tag}",
            "reach": 85000 + (s % 50000),
            "posts_count": 1200 + (s % 800),
            "engagement_rate": round(3.5 + (s % 40) / 10, 1),
            "peak_hours": ["9:00 AM", "12:00 PM", "5:00 PM"],
            "related_hashtags": [f"#{tag}Tips", "#Professional", "#Industry", "#Growth"],
            "trend": "rising" if s % 3 == 0 else "stable",
            "_mock": True,
        }
