import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

SOURCE_EMOJI = {
    "OpenAI Blog": "🤖",
    "Anthropic Blog": "🧠",
    "Google DeepMind": "🔬",
    "Google AI Blog": "🔬",
    "Meta AI Blog": "📘",
    "NVIDIA AI Blog": "💚",
    "Hugging Face Blog": "🤗",
    "Mistral AI Blog": "🌀",
    "arXiv": "📄",
    "GitHub Trending": "⭐",
    "Hacker News": "🔶",
    "Papers With Code": "📊",
    "The Gradient": "📐",
    "Towards Data Science": "📈",
}

DEFAULT_EMOJI = "📰"


def _escape(text: str) -> str:
    """Escape special chars for Telegram MarkdownV2."""
    for ch in r"\_*[]()~`>#+-=|{}.!":
        text = text.replace(ch, f"\\{ch}")
    return text


def send_digest(articles: list[dict], date_str: str):
    if not articles:
        _send_text("No new AI/ML/LLM news found today.")
        return

    header = f"🧠 *AI Daily Digest — {_escape(date_str)}*\n_{len(articles)} stories_\n"
    chunks = [header]
    current = header

    for i, article in enumerate(articles, 1):
        emoji = SOURCE_EMOJI.get(article["source"], DEFAULT_EMOJI)
        title = _escape(article["title"][:120])
        source = _escape(article["source"])
        url = article["url"]
        summary = article.get("summary", "").strip()

        block = f"\n*{i}\\. {title}*\n"
        block += f"{emoji} _{source}_\n"
        if summary:
            block += f"{_escape(summary[:200])}\n"
        block += f"[Read more]({url})\n"
        block += "\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\n"

        # Telegram message limit is ~4096 chars; split into multiple messages
        if len(current) + len(block) > 3800:
            _send_text(current)
            current = block
        else:
            current += block

    if current.strip():
        _send_text(current)


def _send_text(text: str):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }
    resp = requests.post(f"{BASE_URL}/sendMessage", json=payload, timeout=15)
    if not resp.ok:
        # Fallback: send as plain text if markdown fails
        payload["parse_mode"] = "HTML"
        payload["text"] = text.replace("\\", "")
        requests.post(f"{BASE_URL}/sendMessage", json=payload, timeout=15)


def test_connection() -> bool:
    try:
        resp = requests.get(f"{BASE_URL}/getMe", timeout=10)
        return resp.ok
    except Exception:
        return False
