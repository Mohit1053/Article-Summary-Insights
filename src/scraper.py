import re

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Article:
    """Extracted article data."""

    url: str
    title: str
    content: str
    author: str = None
    published_date: str = None


def scrape_article(url: str) -> Article:
    """Extract clean article content from a URL.

    Fetches the page, strips non-content elements (nav, ads, scripts),
    and pulls out the article text, title, author, and date.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    # Strip non-content elements
    for tag in soup(
        ["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]
    ):
        tag.decompose()

    # Title
    title = ""
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)
    elif soup.find("title"):
        title = soup.find("title").get_text(strip=True)

    # Article body — try common container elements
    article_el = (
        soup.find("article")
        or soup.find("div", class_=re.compile(r"article|post|content|story", re.I))
        or soup.find("main")
    )

    if article_el:
        paragraphs = article_el.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    content = "\n\n".join(
        p.get_text(strip=True)
        for p in paragraphs
        if len(p.get_text(strip=True)) > 30
    )

    # Fallback to full page text if nothing extracted
    if not content:
        content = soup.get_text(separator="\n", strip=True)

    # Author (best effort)
    author = None
    author_meta = soup.find("meta", attrs={"name": "author"})
    if author_meta:
        author = author_meta.get("content")

    # Published date (best effort)
    published_date = None
    date_meta = soup.find("meta", attrs={"property": "article:published_time"})
    if date_meta:
        published_date = date_meta.get("content", "")[:10]
    else:
        time_tag = soup.find("time")
        if time_tag:
            raw = time_tag.get("datetime") or time_tag.get_text(strip=True)
            published_date = raw[:10] if raw else None

    return Article(
        url=url,
        title=title,
        content=content,
        author=author,
        published_date=published_date,
    )
