import feedparser
from datetime import datetime, timezone, timedelta
from config import LOOKBACK_HOURS

# cs.AI=Artificial Intelligence, cs.LG=Machine Learning,
# cs.CL=Computation & Language, cs.CV=Computer Vision
ARXIV_FEEDS = [
    "https://rss.arxiv.org/rss/cs.AI",
    "https://rss.arxiv.org/rss/cs.LG",
    "https://rss.arxiv.org/rss/cs.CL",
]


def fetch() -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)
    items = []

    for feed_url in ARXIV_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:30]:
                pub = entry.get("published", entry.get("updated", ""))
                try:
                    published_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                except Exception:
                    published_dt = datetime.now(timezone.utc)

                if published_dt < cutoff:
                    continue

                items.append({
                    "title": entry.get("title", "").replace("\n", " ").strip(),
                    "url": entry.get("link", ""),
                    "source": "arXiv",
                    "score": 0,
                    "published": pub,
                    "summary": entry.get("summary", "")[:400],
                })
        except Exception:
            continue

    return items
