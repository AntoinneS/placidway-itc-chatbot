"""
PlacidWay Website Knowledge Chatbot — content ingestion
Antoinne Stewart — AI Automation Engineer assessment

Re-fetches ONLY the 7 PlacidWay URLs named in the assessment doc,
at ~1 request per second, with a clear User-Agent, as the doc asks.
It does NOT crawl beyond those URLs.

It extracts the main text of each page (title, headings, paragraphs,
tables, lists), strips navigation / scripts / styles, and writes
a clean, human-readable snapshot to data/raw/ plus a short
ingestion report (ingestion-report.md) with the date, URL, status,
and character count for each page.

The curated knowledge base (knowledge-base.json) is built from
that snapshot by hand — every chunk is checked against the page
text before it ships, so the bot can only answer from verified
content. Re-running this script does not silently change answers:
after a refresh, re-check knowledge-base.json, re-run the 8 test
questions, and update the "Last updated" stamp in index.html.

Usage:
    python3 ingest.py
Requires: requests, beautifulsoup4
    pip install requests beautifulsoup4
"""
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER_AGENT = "PlacidWay-Assessment-Bot/1.0 (Antoinne Stewart; assessment ingestion only)"
SOURCES = [
    ("profile", "https://www.placidway.com/profile/5/Alternative-Cancer-Treatment-by-ITC-Immunity-Therapy-Center"),
    ("adenocarcinoma", "https://www.placidway.com/package/7903/Alternative-Adenocarcinoma-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC"),
    ("adrenal", "https://www.placidway.com/package/7902/Alternative-Adrenal-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC"),
    ("anal", "https://www.placidway.com/package/7901/Alternative-Anal-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC"),
    ("videos", "https://www.placidway.com/profile-videos/5/Alternative-Cancer-Treatment-by-ITC-Immunity-Therapy-Center"),
    ("price-list", "https://www.placidway.com/price-list/5/Alternative-Cancer-Treatment-by-ITC-Immunity-Therapy-Center"),
    ("price-comparison", "https://www.placidway.com/search-medical-pricings/Alternative-Medicine/All/1"),
]

OUT = Path(__file__).parent / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

def clean_text(html: str) -> str:
    """Return the visible text of the main content, one line per block."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "noscript"]):
        tag.decompose()
    lines = []
    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "td", "th"]):
        text = " ".join(el.get_text(" ", strip=True).split())
        if text:
            lines.append(text)
    return "\n".join(lines)

def main() -> None:
    report = ["# Ingestion report", "", f"Date: {time.strftime('%Y-%m-%d')}", ""]
    for name, url in SOURCES:
        try:
            resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
            resp.raise_for_status()
            text = clean_text(resp.text)
            (OUT / f"{name}.txt").write_text(text, encoding="utf-8")
            line = f"- {name}: HTTP {resp.status_code}, {len(text)} chars — {url}"
            print(line)
            report.append(line)
        except Exception as exc:  # keep the report honest when a page fails
            line = f"- {name}: FAILED ({exc}) — {url}"
            print(line)
            report.append(line)
        time.sleep(1.1)  # ~1 request per second, per the assessment doc
    (Path(__file__).parent / "ingestion-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("Done. Raw snapshots in data/raw/, report in ingestion-report.md")
    print("Next: diff the snapshots against knowledge-base.json, re-run the 8 test questions, then update the Last updated stamp.")

if __name__ == "__main__":
    main()
