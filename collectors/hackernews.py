import requests
from datetime import datetime, timezone, timedelta
from config import LOOKBACK_HOURS

HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"

AI_QUERIES = [
    "LLM", "large language model", "GPT", "Claude", "Gemini",
    "machine learning", "artificial intelligence", "deep learning",
    "transformer", "neural network", "AI agent", "diffusion model",
    "Llama", "Mistral", "Qwen", "DeepSeek", "Ollama", "fine-tuning",
    "RAG", "vector database", "embedding model",
    "xAI", "Grok", "Perplexity", "Microsoft AI", "Copilot AI",
    "Hugging Face", "NVIDIA AI",
]


def fetch() -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)
    seen_ids = set()
    items = []

    for query in AI_QUERIES[:8]:  # limit queries to avoid rate-limit
        try:
            params = {
                "query": query,
                "tags": "story",
                "numericFilters": f"created_at_i>{int(cutoff.timestamp())}",
                "hitsPerPage": 20,
            }
            resp = requests.get(HN_SEARCH_URL, params=params, timeout=10)
            resp.raise_for_status()
            for hit in resp.json().get("hits", []):
                if hit["objectID"] in seen_ids:
                    continue
                seen_ids.add(hit["objectID"])
                url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}"
                items.append({
                    "title": hit.get("title", ""),
                    "url": url,
                    "source": "Hacker News",
                    "score": hit.get("points", 0),
                    "published": hit.get("created_at", ""),
                    "summary": "",
                })
        except Exception:
            continue

    return items
