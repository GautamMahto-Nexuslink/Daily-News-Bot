import requests
from bs4 import BeautifulSoup

GITHUB_TRENDING_URL = "https://github.com/trending?since=daily&spoken_language_code=en"

AI_KEYWORDS = {
    "llm", "ai", "ml", "neural", "transformer", "diffusion",
    "gpt", "llama", "mistral", "ollama", "langchain", "rag",
    "embedding", "inference", "training", "finetune", "agent",
    "multimodal", "vision", "nlp", "chatbot", "stable-diffusion",
}


def fetch() -> list[dict]:
    try:
        headers = {"User-Agent": "AINewsBot/1.0"}
        resp = requests.get(GITHUB_TRENDING_URL, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
    except Exception:
        return []

    items = []
    for article in soup.select("article.Box-row"):
        try:
            h2 = article.select_one("h2 a")
            if not h2:
                continue
            path = h2["href"].strip("/")
            title = path.replace("/", " / ")
            desc_el = article.select_one("p")
            description = desc_el.get_text(strip=True) if desc_el else ""

            combined = (title + " " + description).lower()
            if not any(kw in combined for kw in AI_KEYWORDS):
                continue

            stars_el = article.select_one("span.d-inline-block.float-sm-right")
            stars = 0
            if stars_el:
                stars_text = stars_el.get_text(strip=True).replace(",", "").replace(" ", "")
                try:
                    stars = int(stars_text)
                except ValueError:
                    pass

            items.append({
                "title": f"[GitHub] {title}",
                "url": f"https://github.com/{path}",
                "source": "GitHub Trending",
                "score": stars,
                "published": "",
                "summary": description,
            })
        except Exception:
            continue

    return items
