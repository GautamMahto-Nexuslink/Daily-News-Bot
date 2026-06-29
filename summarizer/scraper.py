import requests
from bs4 import BeautifulSoup
from config import MAX_SUMMARY_WORDS

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AINewsBot/1.0)"}


def fetch_snippet(url: str, max_words: int = None) -> str:
    if max_words is None:
        max_words = MAX_SUMMARY_WORDS
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # Remove noise
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()

        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 60]
        text = " ".join(paragraphs[:5])

        words = text.split()
        if not words:
            return ""
        if len(words) <= max_words:
            return text
        return " ".join(words[:max_words]) + "…"
    except Exception:
        return ""
