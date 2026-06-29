import requests
from config import OLLAMA_HOST, OLLAMA_MODEL, MAX_SUMMARY_WORDS


def summarize(title: str, existing_summary: str) -> str:
    if not existing_summary.strip():
        return ""

    prompt = (
        f"Summarize this AI news item in {MAX_SUMMARY_WORDS} words or fewer. "
        f"Be specific and factual. No filler phrases.\n\n"
        f"Title: {title}\n"
        f"Content: {existing_summary}\n\n"
        f"Summary:"
    )

    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception:
        return existing_summary[:200]


def truncate_summary(text: str, max_words: int = None) -> str:
    if max_words is None:
        max_words = MAX_SUMMARY_WORDS
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "…"
