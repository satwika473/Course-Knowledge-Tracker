"""Markdown generation utilities for Learning Insights Tracker."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from scraper import LearningInsight


def generate_markdown(insights: Iterable[LearningInsight]) -> str:
    """Build a clean markdown report from scraped insights."""
    sorted_insights = sorted(insights, key=lambda item: item.title.lower())
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Learning Insights",
        "",
        f"_Generated on: {generated_at}_",
        "",
    ]

    if not sorted_insights:
        lines.extend(
            [
                "No insights were collected in this run.",
                "",
            ]
        )
        return "\n".join(lines)

    for insight in sorted_insights:
        lines.extend(
            [
                f"## {insight.title}",
                "",
                f"- Source: {insight.source}",
                f"- Category: {insight.category}",
                f"- Summary: {insight.summary}",
                f"- Link: {insight.url}",
                "",
                "---",
                "",
            ]
        )

    return "\n".join(lines)


def write_markdown_if_changed(file_path: str, new_content: str) -> bool:
    """
    Write markdown only when content changes.

    Returns True when file content was updated, otherwise False.
    """
    output_file = Path(file_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    old_content = ""
    if output_file.exists():
        old_content = output_file.read_text(encoding="utf-8")

    if old_content == new_content:
        return False

    output_file.write_text(new_content, encoding="utf-8")
    return True
