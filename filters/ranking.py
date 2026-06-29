MODEL_RELEASE_ACTIONS = {
    "releases", "released", "launch", "launches", "launched",
    "introduces", "introduced", "unveils", "unveiled",
    "announces", "announced", "ships", "now available",
    "available now", "open source", "open-source",
}

MODEL_RELEASE_SIGNALS = {
    "model", "gpt-", "claude", "gemini", "llama", "mistral",
    "grok", "phi-", "qwen", "deepseek", "gemma", "falcon",
    "diffusion", "v1.", "v2.", "v3.", "2.0", "3.0", "4.0",
    "weights", "checkpoint", "api",
}


def is_model_release(title: str) -> bool:
    t = title.lower()
    has_action = any(a in t for a in MODEL_RELEASE_ACTIONS)
    has_signal = any(s in t for s in MODEL_RELEASE_SIGNALS)
    return has_action and has_signal


SOURCE_SCORES = {
    "OpenAI Blog": 10,
    "Anthropic Blog": 10,
    "Google DeepMind": 10,
    "Google AI Blog": 9,
    "Meta AI Blog": 9,
    "NVIDIA AI Blog": 8,
    "Hugging Face Blog": 8,
    "Mistral AI Blog": 8,
    "Microsoft AI Blog": 9,
    "Perplexity Blog": 8,
    "arXiv": 7,
    "GitHub Trending": 6,
    "Hacker News": 5,
    "Papers With Code": 7,
    "The Gradient": 6,
}

HIGH_VALUE_KEYWORDS = {
    "release": 4, "launch": 4, "introduces": 3, "announce": 3,
    "open source": 3, "open-source": 3, "new model": 4,
    "benchmark": 2, "beats": 2, "surpass": 2, "sota": 3,
    "gpt-": 3, "claude": 3, "gemini": 3, "llama": 2,
    "agent": 2, "multimodal": 2, "reasoning": 2,
    "funding": 2, "billion": 1, "million": 1,
    "paper": 1, "research": 1,
}


def score(article: dict) -> int:
    base = SOURCE_SCORES.get(article["source"], 3)
    title_lower = article["title"].lower()
    bonus = sum(v for kw, v in HIGH_VALUE_KEYWORDS.items() if kw in title_lower)
    # Normalize HN upvotes: every 100 upvotes = +1 point, capped at 5
    hn_bonus = min(5, article.get("score", 0) // 100)
    # Model release gets highest priority — always floats to top
    release_bonus = 15 if is_model_release(article["title"]) else 0
    return base + bonus + hn_bonus + release_bonus


def rank(articles: list[dict]) -> list[dict]:
    for article in articles:
        article["_rank_score"] = score(article)
        article["_is_model_release"] = is_model_release(article["title"])
    return sorted(articles, key=lambda a: a["_rank_score"], reverse=True)
