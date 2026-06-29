import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Email (optional)
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# Ollama (optional local LLM summarization)
OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "false").lower() == "true"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3")

# Digest settings
TOP_N_ARTICLES = int(os.getenv("TOP_N_ARTICLES", "10"))
MAX_SUMMARY_WORDS = int(os.getenv("MAX_SUMMARY_WORDS", "60"))
LOOKBACK_HOURS = int(os.getenv("LOOKBACK_HOURS", "24"))

# Database
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "history.sqlite")

# Logging
LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "bot.log")
