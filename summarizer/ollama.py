import logging
import requests
from config import OLLAMA_HOST, OLLAMA_MODEL, MAX_SUMMARY_WORDS

log = logging.getLogger(__name__)


def summarize(title: str, existing_summary: str) -> str:
    if existing_summary.strip():
        prompt = (
            f"Summarize this AI news item in {MAX_SUMMARY_WORDS} words or fewer. "
            f"Be specific and factual. No filler phrases.\n\n"
            f"Title: {title}\n"
            f"Content: {existing_summary}\n\n"
            f"Summary:"
        )
    else:
        # No existing content — generate a brief description from the title alone
        prompt = (
            f"Based on this AI/tech news headline, write a {MAX_SUMMARY_WORDS}-word or fewer "
            f"factual description of what the story is likely about. "
            f"Be specific. No filler phrases.\n\n"
            f"Headline: {title}\n\n"
            f"Description:"
        )

    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=60,
        )
        resp.raise_for_status()
        result = resp.json().get("response", "").strip()
        return result if result else existing_summary[:200]
    except Exception as e:
        log.warning(f"Ollama summarization failed: {e}")
        return existing_summary[:200]


def truncate_summary(text: str, max_words: int = None) -> str:
    if max_words is None:
        max_words = MAX_SUMMARY_WORDS
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "…"
