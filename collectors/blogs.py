import feedparser
from datetime import datetime, timezone, timedelta
from config import LOOKBACK_HOURS

RSS_FEEDS = [
    ("OpenAI Blog",         "https://openai.com/news/rss.xml"),
    ("Anthropic Blog",      "https://www.anthropic.com/rss.xml"),
    ("Google DeepMind",     "https://deepmind.google/blog/rss.xml"),
    ("Google AI Blog",      "https://blog.google/technology/ai/rss/"),
    ("Meta AI Blog",        "https://ai.meta.com/blog/rss/"),
    ("NVIDIA AI Blog",      "https://blogs.nvidia.com/blog/category/artificial-intelligence/feed/"),
    ("Hugging Face Blog",   "https://huggingface.co/blog/feed.xml"),
    ("Mistral AI Blog",     "https://mistral.ai/news/rss.xml"),
    ("Papers With Code",    "https://paperswithcode.com/latest.rss"),
    ("The Gradient",        "https://thegradient.pub/rss/"),
    ("Towards Data Science","https://towardsdatascience.com/feed"),
]


def _parse_published(entry) -> datetime:
    for field in ("published_parsed", "updated_parsed"):
        t = entry.get(field)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return datetime.now(timezone.utc)


def fetch() -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)
    items = []

    for name, url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                published_dt = _parse_published(entry)
                if published_dt < cutoff:
                    continue
                items.append({
                    "title": entry.get("title", "").strip(),
                    "url": entry.get("link", ""),
                    "source": name,
                    "score": 0,
                    "published": entry.get("published", entry.get("updated", "")),
                    "summary": entry.get("summary", "")[:400],
                })
        except Exception:
            continue

    return items
