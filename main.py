"""Entry point for Learning Insights Tracker."""

from pathlib import Path

from markdown_generator import generate_markdown, write_markdown_if_changed
from scraper import scrape_learning_insights


def main() -> None:
    output_path = Path("output") / "learning_insights.md"

    insights = scrape_learning_insights()
    markdown = generate_markdown(insights)
    has_changed = write_markdown_if_changed(str(output_path), markdown)

    print(f"Collected {len(insights)} insights.")
    if has_changed:
        print(f"Updated report: {output_path}")
    else:
        print("No changes detected. Skipping update.")


if __name__ == "__main__":
    main()
