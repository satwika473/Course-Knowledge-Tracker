# Learning Insights Tracker

Learning Insights Tracker is a simple Python automation project that collects useful learning-related insights from public educational sources, generates a clean Markdown report, and supports automatic daily updates via GitHub Actions.

## Features

- Scrapes public learning resources (articles, career guidance, programming tips, blogs).
- Extracts:
  - Title
  - Source Website
  - URL
  - Short Summary
  - Category
- Generates `output/learning_insights.md`.
- Compares generated content with the previous report.
- Updates the report only when content changes.
- Uses a custom User-Agent for HTTP requests.
- Handles network failures gracefully and continues with available sources.
- Includes daily GitHub Actions automation for commit-and-push on changes.

## Project Structure

```text
.
├── .github/workflows/scraper.yml
├── main.py
├── markdown_generator.py
├── output/learning_insights.md
├── requirements.txt
└── scraper.py
```

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the project:

```bash
python main.py
```

The report will be created/updated at:

- `output/learning_insights.md`

## GitHub Actions Automation

The workflow at `.github/workflows/scraper.yml`:

- runs daily (`cron: 0 2 * * *`) and on manual trigger
- installs dependencies
- runs `python main.py`
- commits and pushes only when `output/learning_insights.md` changed

Commit message used by automation:

- `Update learning insights`
