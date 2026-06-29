TRACKED_COMPANIES = {
    "OpenAI":          ["openai", "chatgpt", "gpt-4", "gpt-5", "dall-e", "sora", "o1", "o3"],
    "Anthropic":       ["anthropic", "claude"],
    "Google DeepMind": ["deepmind", "gemini", "google ai", "google deepmind", "veo", "imagen", "bard"],
    "Meta AI":         ["meta ai", "llama", "meta llama"],
    "Microsoft AI":    ["microsoft ai", "microsoft copilot", "azure ai", "phi-", "phi model"],
    "NVIDIA":          ["nvidia", "cuda", "tensorrt", "nvidia nim"],
    "xAI":             ["xai", "grok", "x.ai"],
    "Hugging Face":    ["hugging face", "huggingface"],
    "Mistral AI":      ["mistral", "mixtral", "le chat"],
    "Perplexity":      ["perplexity"],
}


def detect_companies(title: str, summary: str = "") -> list[str]:
    """Return list of tracked company names mentioned in title or summary."""
    text = (title + " " + summary).lower()
    return [company for company, aliases in TRACKED_COMPANIES.items()
            if any(alias in text for alias in aliases)]
