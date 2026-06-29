from filters.companies import TRACKED_COMPANIES

_COMPANY_ALIASES = {alias for aliases in TRACKED_COMPANIES.values() for alias in aliases}

AI_KEYWORDS = _COMPANY_ALIASES | {
    # Additional models & providers not in tracked companies
    "qwen", "deepseek", "gemma", "falcon", "bloom", "bert", "t5",
    "cohere", "together ai", "groq", "xai",
    # Concepts
    "llm", "large language model", "transformer", "diffusion", "neural",
    "machine learning", "deep learning", "artificial intelligence", " ai ",
    "natural language", "nlp", "computer vision", "reinforcement learning",
    "fine-tun", "finetun", "rlhf", "rag", "retrieval augmented",
    "vector database", "embedding", "inference", "foundation model",
    "multimodal", "text-to-image", "text-to-video", "speech recognition",
    "agent", "agentic", "autonomous", "copilot", "chatbot",
    # Topics
    "benchmark", "leaderboard", "evals", "open source model", "open-source model",
    "model release", "model weights", "quantization", "lora", "gguf",
    "stable diffusion", "midjourney", "dall-e", "sora", "veo",
}

NOISE_KEYWORDS = {
    "crypto", "bitcoin", "nft", "blockchain", "forex", "stock market",
    "real estate", "recipe", "fashion", "sports", "celebrity",
}


def is_ai_relevant(title: str, summary: str = "") -> bool:
    text = (title + " " + summary).lower()
    if any(noise in text for noise in NOISE_KEYWORDS):
        return False
    return any(kw in text for kw in AI_KEYWORDS)
