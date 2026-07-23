"""Scraper utilities for Learning Insights Tracker."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "LearningInsightsTracker/1.0 (+https://github.com/your-username/"
    "learning-insights-tracker)"
)
REQUEST_TIMEOUT = 20


@dataclass
class LearningInsight:
    """Represents one extracted learning insight."""

    title: str
    source: str
    url: str
    summary: str
    category: str


def _clean_text(value: str, max_length: int = 220) -> str:
    """Normalize and shorten extracted text for markdown readability."""
    cleaned = " ".join(value.split())
    if len(cleaned) <= max_length:
        return cleaned
    return f"{cleaned[: max_length - 3].rstrip()}..."


def _fetch_content(url: str) -> str:
    """Download page/feed content with a custom User-Agent."""
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text


def scrape_feed(
    *,
    feed_url: str,
    source_name: str,
    category: str,
    limit: int = 5,
) -> List[LearningInsight]:
    """
    Scrape RSS/Atom feed entries.

    Returns an empty list on network or parsing failures.
    """
    try:
        content = _fetch_content(feed_url)
    except requests.RequestException as exc:
        print(f"[WARN] Failed to fetch {source_name} ({feed_url}): {exc}")
        return []

    soup = BeautifulSoup(content, "xml")
    entries = soup.find_all(["item", "entry"])
    if not entries:
        print(f"[WARN] No feed entries found for {source_name} ({feed_url}).")
        return []

    insights: List[LearningInsight] = []
    for entry in entries[:limit]:
        title_tag = entry.find("title")
        if not title_tag or not title_tag.text.strip():
            continue

        link_tag = entry.find("link")
        link = ""
        if link_tag:
            link = link_tag.get("href", "").strip() or link_tag.text.strip()
        if not link:
            continue

        summary_tag = entry.find("description") or entry.find("summary")
        summary_text = summary_tag.text if summary_tag else "No summary available."
        summary = _clean_text(BeautifulSoup(summary_text, "html.parser").get_text(" "))

        insights.append(
            LearningInsight(
                title=_clean_text(title_tag.text, max_length=120),
                source=source_name,
                url=link,
                summary=summary,
                category=category,
            )
        )

    return insights


def scrape_learning_insights() -> List[LearningInsight]:
    """Collect insights from selected public learning-related sources."""
    source_configs = [
        {
            "feed_url": "https://www.freecodecamp.org/news/rss/",
            "source_name": "freeCodeCamp News",
            "category": "Learning Article",
            "limit": 5,
        },
        {
            "feed_url": "https://dev.to/feed/tag/career",
            "source_name": "DEV Community",
            "category": "Career Guidance",
            "limit": 5,
        },
        {
            "feed_url": "https://dev.to/feed/tag/programming",
            "source_name": "DEV Community",
            "category": "Programming Tips",
            "limit": 5,
        },
        {
            "feed_url": "https://realpython.com/atom.xml",
            "source_name": "Real Python",
            "category": "Developer Blog",
            "limit": 5,
        },
    ]

    all_items: List[LearningInsight] = []
    for config in source_configs:
        items = scrape_feed(**config)
        all_items.extend(items)

    seen = set()
    unique_items: List[LearningInsight] = []
    for item in all_items:
        key = (item.title.lower(), item.url.lower())
        if key in seen:
            continue
        seen.add(key)
        unique_items.append(item)

    return unique_items
