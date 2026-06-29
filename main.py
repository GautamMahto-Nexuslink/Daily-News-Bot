#!/usr/bin/env python3
import logging
import sys
from datetime import datetime

from config import (
    DB_PATH, LOG_PATH, TOP_N_ARTICLES, OLLAMA_ENABLED,
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
    EMAIL_SENDER, EMAIL_RECIPIENT,
)
from collectors import hackernews, reddit, arxiv, blogs, github
from filters.keywords import is_ai_relevant
from filters.duplicate import init_db, filter_new, mark_sent
from filters.ranking import rank
from summarizer.ollama import summarize, truncate_summary
from summarizer.scraper import fetch_snippet
from sender import telegram as tg
from sender import email_sender

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


def collect_all() -> list[dict]:
    log.info("Collecting news from all sources…")
    sources = [
        ("Blogs/RSS",    blogs.fetch),
        ("arXiv",        arxiv.fetch),
        ("Hacker News",  hackernews.fetch),
        # ("Reddit",       reddit.fetch),
        ("GitHub",       github.fetch),
    ]
    all_items = []
    for name, fn in sources:
        try:
            items = fn()
            log.info(f"  {name}: {len(items)} items")
            all_items.extend(items)
        except Exception as exc:
            log.warning(f"  {name} failed: {exc}")
    return all_items


def run():
    log.info("=" * 60)
    log.info("AI News Bot starting")

    init_db()

    # 1. Collect
    raw = collect_all()
    log.info(f"Total collected: {len(raw)}")

    # 2. Filter by AI relevance
    relevant = [a for a in raw if is_ai_relevant(a["title"], a.get("summary", ""))]
    log.info(f"AI-relevant: {len(relevant)}")

    # 3. Deduplicate against history
    new_articles = filter_new(relevant)
    log.info(f"New (not seen before): {len(new_articles)}")

    if not new_articles:
        log.info("Nothing new today — skipping delivery.")
        return

    # 4. Rank
    ranked = rank(new_articles)

    # 5. Take top N
    top = ranked[:TOP_N_ARTICLES]

    # 6. Summarize — Ollama if enabled, else scrape snippet from URL
    if OLLAMA_ENABLED:
        log.info("Summarizing with Ollama…")
        for article in top:
            article["summary"] = summarize(article["title"], article.get("summary", ""))
    else:
        log.info("Fetching article snippets…")
        for article in top:
            existing = article.get("summary", "").strip()
            if existing:
                article["summary"] = truncate_summary(existing, max_words=50)
            else:
                article["summary"] = fetch_snippet(article["url"])

    # 7. Deliver
    date_str = datetime.now().strftime("%B %d, %Y")
    delivered = False

    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            tg.send_digest(top, date_str)
            log.info(f"Sent {len(top)} articles via Telegram")
            delivered = True
        except Exception as exc:
            log.error(f"Telegram delivery failed: {exc}")

    if EMAIL_SENDER and EMAIL_RECIPIENT:
        try:
            email_sender.send_digest(top, date_str)
            log.info(f"Sent {len(top)} articles via Email")
            delivered = True
        except Exception as exc:
            log.error(f"Email delivery failed: {exc}")

    if not delivered:
        log.warning("No delivery channel configured. Add TELEGRAM_BOT_TOKEN or EMAIL_SENDER to .env")
        _print_digest(top, date_str)

    # 8. Mark as sent
    mark_sent(top)
    log.info("Done.")


def _print_digest(articles: list[dict], date_str: str):
    print(f"\n{'='*60}")
    print(f"  AI Daily Digest — {date_str}  ({len(articles)} stories)")
    print(f"{'='*60}\n")
    for i, a in enumerate(articles, 1):
        print(f"{i}. [{a['source']}] {a['title']}")
        if a.get("summary"):
            print(f"   {a['summary'][:150]}")
        print(f"   {a['url']}\n")


if __name__ == "__main__":
    run()
