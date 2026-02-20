import os
import re

import click

from src.scraper import scrape_article
from src.agents import analyze_article
from src.report import build_report
from src.config import settings


@click.command()
@click.argument("url")
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--model", "-m", default=None, help="OpenAI model (default: gpt-4o-mini)")
def main(url: str, output: str, model: str):
    """Analyze a financial article and generate an insights report."""
    if not settings.openai_api_key:
        click.echo("Error: OPENAI_API_KEY not set. Copy .env.example to .env and add your key.")
        raise SystemExit(1)

    if model:
        settings.model = model

    # Scrape
    click.echo(f"Scraping: {url}")
    article = scrape_article(url)
    click.echo(f"Title: {article.title}")
    click.echo(f"Extracted: {len(article.content):,} characters")

    # Analyze
    def progress(agent_name, step, total):
        click.echo(f"  [{step}/{total}] {agent_name}...")

    click.echo("\nRunning analysis pipeline:")
    analysis = analyze_article(article.title, article.content, on_progress=progress)
    click.echo("Done.\n")

    # Report
    report = build_report(article.title, article.url, analysis)

    if output is None:
        os.makedirs(settings.output_dir, exist_ok=True)
        slug = re.sub(r"[^\w\s-]", "", article.title[:60]).strip().lower()
        slug = re.sub(r"\s+", "-", slug)
        output = os.path.join(settings.output_dir, f"{slug}.md")

    with open(output, "w", encoding="utf-8") as f:
        f.write(report)

    click.echo(f"Report saved: {output}")


if __name__ == "__main__":
    main()
