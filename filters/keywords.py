AI_KEYWORDS = {
    # Models & companies
    "gpt", "claude", "gemini", "llama", "mistral", "qwen", "deepseek",
    "gemma", "phi", "falcon", "bloom", "bert", "t5", "grok", "perplexity",
    "openai", "anthropic", "deepmind", "google ai", "meta ai", "nvidia",
    "hugging face", "huggingface", "cohere", "together ai", "groq",
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
