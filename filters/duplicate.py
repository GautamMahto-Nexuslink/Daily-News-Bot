import hashlib
import sqlite3
from config import DB_PATH


def _url_hash(url: str) -> str:
    return hashlib.sha256(url.strip().lower().encode()).hexdigest()


def _title_hash(title: str) -> str:
    normalized = " ".join(title.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS seen_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_hash TEXT UNIQUE,
                title_hash TEXT,
                title TEXT,
                url TEXT,
                source TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def filter_new(articles: list[dict]) -> list[dict]:
    if not articles:
        return []

    with sqlite3.connect(DB_PATH) as conn:
        new_articles = []
        for article in articles:
            uh = _url_hash(article["url"])
            th = _title_hash(article["title"])
            row = conn.execute(
                "SELECT 1 FROM seen_articles WHERE url_hash=? OR title_hash=?", (uh, th)
            ).fetchone()
            if not row:
                new_articles.append({**article, "_url_hash": uh, "_title_hash": th})
        return new_articles


def mark_sent(articles: list[dict]):
    with sqlite3.connect(DB_PATH) as conn:
        for article in articles:
            try:
                conn.execute(
                    "INSERT OR IGNORE INTO seen_articles (url_hash, title_hash, title, url, source) VALUES (?,?,?,?,?)",
                    (
                        article["_url_hash"],
                        article["_title_hash"],
                        article["title"][:500],
                        article["url"][:1000],
                        article["source"],
                    ),
                )
            except Exception:
                pass
        conn.commit()
