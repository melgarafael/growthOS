"""Reddit discovery adapter — returns realistic mock data for agent testing."""

import hashlib
from typing import Any

from platforms.base import DiscoveryAdapter


def _seed(text: str) -> int:
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)


class RedditDiscoveryAdapter(DiscoveryAdapter):

    @property
    def platform_name(self) -> str:
        return "reddit"

    async def get_analytics(self, date_from: str, date_to: str) -> dict[str, Any]:
        s = _seed(f"reddit-analytics-{date_from}-{date_to}")
        return {
            "platform": "reddit",
            "period": {"from": date_from, "to": date_to},
            "impressions": 8500 + (s % 4000),
            "clicks": 620 + (s % 300),
            "shares": 45 + (s % 30),
            "comments": 180 + (s % 100),
            "engagement_rate": round(5.8 + (s % 30) / 10, 1),
            "karma_gained": 420 + (s % 200),
            "top_posts": [
                {
                    "id": f"reddit-{s % 10000}",
                    "title": "We open-sourced our internal tool — here's what we learned",
                    "subreddit": "r/programming",
                    "upvotes": 850,
                    "comments": 124,
                },
                {
                    "id": f"reddit-{(s + 1) % 10000}",
                    "title": "AMA: Building a startup from scratch in 2026",
                    "subreddit": "r/startups",
                    "upvotes": 420,
                    "comments": 89,
                },
            ],
            "_mock": True,
        }

    async def discover_trends(self, topic: str) -> dict[str, Any]:
        s = _seed(f"reddit-trends-{topic}")
        return {
            "platform": "reddit",
            "topic": topic,
            "trending_hashtags": [],
            "trending_topics": [
                {"topic": f"r/{topic.replace(' ', '').lower()}", "volume": 8500 + (s % 4000), "growth": "+32%"},
                {"topic": f"{topic} megathread", "volume": 3200 + (s % 2000), "growth": "+20%"},
                {"topic": f"ELI5: {topic}", "volume": 2100 + (s % 1000), "growth": "+10%"},
            ],
            "popular_formats": [
                {"format": "detailed_text_post", "engagement_multiplier": 2.5},
                {"format": "ama", "engagement_multiplier": 2.2},
                {"format": "tutorial_guide", "engagement_multiplier": 1.9},
                {"format": "link_post", "engagement_multiplier": 1.0},
            ],
            "insights": [
                "Reddit values authenticity — overly promotional content gets downvoted",
                f"r/{topic.replace(' ', '').lower()} most active on weekday evenings",
                "Long-form posts with actionable advice get highest engagement",
            ],
            "top_subreddits": [
                f"r/{topic.replace(' ', '').lower()}",
                "r/technology",
                "r/startups",
                "r/SideProject",
            ],
            "_mock": True,
        }

    async def search_mentions(self, query: str, limit: int = 50) -> dict[str, Any]:
        s = _seed(f"reddit-mentions-{query}")
        count = min(limit, 5)
        mentions = [
            {
                "id": f"reddit-mention-{s + i}",
                "author": f"u/redditor_{s + i}",
                "content": [
                    f"Been using {query} for 6 months. Here's my honest review...",
                    f"Can anyone recommend {query}? Saw it mentioned on HN.",
                    f"{query} is underrated IMO. Their docs are excellent.",
                    f"Tried {query} but went back to [competitor]. Here's why.",
                    f"PSA: {query} just released a major update. Worth checking out.",
                ][i % 5],
                "subreddit": ["r/technology", "r/startups", "r/programming", "r/SaaS", "r/software"][i % 5],
                "timestamp": f"2026-03-{28 + i}T{18 + i}:00:00Z",
                "sentiment": ["positive", "neutral", "positive", "negative", "positive"][i % 5],
                "engagement": {"upvotes": 85 + (s + i) % 60, "comments": 23 + (s + i) % 20},
                "url": f"https://reddit.com/r/technology/comments/{s + i}",
            }
            for i in range(count)
        ]
        return {
            "platform": "reddit",
            "query": query,
            "mentions": mentions,
            "total_count": 340 + (s % 200),
            "sentiment_breakdown": {"positive": 48, "neutral": 35, "negative": 17},
            "_mock": True,
        }

    async def get_competitor_activity(self, competitor: str) -> dict[str, Any]:
        s = _seed(f"reddit-competitor-{competitor}")
        return {
            "platform": "reddit",
            "competitor": competitor,
            "mentions_count": 180 + (s % 100),
            "posting_frequency": "1-2 posts/week (official account)",
            "avg_engagement": {
                "upvotes": 220 + (s % 150),
                "comments": 55 + (s % 40),
            },
            "recent_posts": [
                {
                    "title": f"{competitor} AMA with the founding team",
                    "subreddit": "r/startups",
                    "date": "2026-03-27",
                    "upvotes": 340,
                    "comments": 89,
                },
                {
                    "title": f"Honest review of {competitor} after 1 year",
                    "subreddit": "r/SaaS",
                    "date": "2026-03-24",
                    "upvotes": 180,
                    "comments": 45,
                },
            ],
            "top_content": {
                "best_format": "ama",
                "best_subreddits": ["r/startups", "r/technology", "r/SaaS"],
                "community_sentiment": "mixed",
            },
            "_mock": True,
        }

    async def get_hashtag_performance(self, hashtag: str) -> dict[str, Any]:
        tag = hashtag.lstrip("#")
        s = _seed(f"reddit-hashtag-{tag}")
        return {
            "platform": "reddit",
            "hashtag": f"#{tag}",
            "note": "Reddit does not use hashtags natively — results are keyword-based",
            "reach": 12000 + (s % 8000),
            "posts_count": 340 + (s % 200),
            "engagement_rate": round(6.2 + (s % 30) / 10, 1),
            "peak_hours": ["6:00 PM", "8:00 PM", "10:00 PM"],
            "related_hashtags": [],
            "related_subreddits": [f"r/{tag.lower()}", "r/technology", "r/programming"],
            "trend": "niche" if s % 3 == 0 else "stable",
            "_mock": True,
        }
