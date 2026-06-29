import feedparser
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from config import LOOKBACK_HOURS

SUBREDDITS = [
    "MachineLearning",
    "LocalLLaMA",
    "artificial",
    "OpenAI",
    "singularity",
    "ChatGPT",
]


def _parse_date(entry) -> datetime:
    try:
        return parsedate_to_datetime(entry.get("published", "")).astimezone(timezone.utc)
    except Exception:
        return datetime.now(timezone.utc)


def fetch() -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)
    items = []

    for sub in SUBREDDITS:
        try:
            feed = feedparser.parse(
                f"https://www.reddit.com/r/{sub}/hot/.rss",
                request_headers={"User-Agent": "AINewsBot/1.0"},
            )
            for entry in feed.entries:
                published = _parse_date(entry)
                if published < cutoff:
                    continue
                items.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "source": f"r/{sub}",
                    "score": 0,
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", "")[:300],
                })
        except Exception:
            continue

    return items
