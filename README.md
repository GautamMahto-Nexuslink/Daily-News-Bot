# 🧠 AI Daily News Bot

An automated pipeline that collects, filters, ranks, and delivers a daily digest of AI/ML/LLM news — **100% free, no paid APIs required**.

Delivers every morning to your **Gmail** or **Telegram**, automatically via **GitHub Actions**.

---

## Features

- **5 news sources** — arXiv, Hacker News, Reddit, GitHub Trending, company blogs
- **10 tracked AI companies** — OpenAI, Anthropic, Google DeepMind, Meta AI, Microsoft AI, NVIDIA, xAI, Hugging Face, Mistral AI, Perplexity
- **Smart filtering** — keyword-based AI relevance check, noise removal
- **Deduplication** — SQLite history prevents sending the same article twice
- **Ranking** — source credibility + keyword bonuses + HN upvotes
- **🚀 Model Release Priority** — new model launches automatically float to the top with a visual badge
- **Company tagging** — colored labels on each article showing which AI company it's about
- **AI Summarization** — local Ollama LLM (optional) or article scraping fallback
- **Dual delivery** — Gmail (SMTP) and/or Telegram bot
- **Scheduled** — GitHub Actions cron runs at 8:00 AM IST daily, zero infrastructure cost

---

## Project Structure

```
Daily_news_Bot/
├── main.py                    # Pipeline entry point
├── config.py                  # All settings via environment variables
├── requirements.txt
│
├── collectors/                # News source fetchers
│   ├── arxiv.py               # arXiv RSS (cs.AI, cs.LG, cs.CL)
│   ├── blogs.py               # Company blog RSS feeds
│   ├── hackernews.py          # Hacker News Algolia API
│   ├── reddit.py              # Reddit RSS
│   └── github.py             # GitHub Trending scraper
│
├── filters/
│   ├── keywords.py            # AI relevance keyword filter
│   ├── companies.py           # Tracked company definitions + detector
│   ├── duplicate.py           # SQLite deduplication
│   └── ranking.py             # Scoring + model release detection
│
├── summarizer/
│   ├── ollama.py              # Local LLM summarization via Ollama
│   └── scraper.py             # Article snippet scraper (fallback)
│
├── sender/
│   ├── email_sender.py        # Gmail SMTP delivery (HTML email)
│   └── telegram.py            # Telegram bot delivery
│
├── database/
│   └── history.sqlite         # Dedup history (auto-created)
│
├── logs/
│   └── bot.log                # Run logs (auto-created)
│
└── .github/
    └── workflows/
        └── daily_digest.yml   # GitHub Actions cron schedule
```

---

## How the Pipeline Works

```
Collect → Filter (AI relevance) → Deduplicate → Rank → Summarize → Deliver
```

1. **Collect** — Fetches articles from all 5 sources in parallel
2. **Filter** — Drops articles not about AI/ML using keyword matching; removes noise (crypto, sports, etc.)
3. **Deduplicate** — Checks URL+title hash against SQLite history; skips already-sent articles
4. **Rank** — Scores each article by source credibility, keyword bonuses, and HN upvotes; model releases get a +15 priority boost
5. **Summarize** — Either Ollama LLM (if enabled) or scrapes article text for a snippet
6. **Deliver** — Sends top 10 articles via Gmail and/or Telegram

---

## Installation

### Prerequisites

- Python 3.10+
- Git
- A Gmail account (with App Password enabled)
- *(Optional)* Ollama installed for local AI summaries

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Daily-news-Bot.git
cd Daily-news-Bot
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials (see [Configuration](#configuration) below).

### 5. Run locally

```bash
python3 main.py
```

---

## Configuration

All settings live in `.env`. Copy `.env.example` to get started.

### Gmail (required for email delivery)

| Variable | Description |
|---|---|
| `EMAIL_SENDER` | Your Gmail address (e.g. `you@gmail.com`) |
| `EMAIL_PASSWORD` | Gmail **App Password** (16 chars, not your login password) |
| `EMAIL_RECIPIENT` | Where to send the digest (can be same as sender) |
| `SMTP_HOST` | Default: `smtp.gmail.com` |
| `SMTP_PORT` | Default: `587` |

**Getting a Gmail App Password:**
1. Go to [myaccount.google.com](https://myaccount.google.com) → Security
2. Enable **2-Step Verification**
3. Search for **App passwords** → create one for "Mail"
4. Copy the 16-character password and paste it as `EMAIL_PASSWORD`

### Telegram (optional)

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Token from [@BotFather](https://t.me/BotFather) → `/newbot` |
| `TELEGRAM_CHAT_ID` | Your chat ID — visit `https://api.telegram.org/bot<TOKEN>/getUpdates` after messaging your bot |

### Ollama — Local AI Summarization (optional)

| Variable | Description | Default |
|---|---|---|
| `OLLAMA_ENABLED` | Set `true` to enable | `false` |
| `OLLAMA_HOST` | Ollama API address | `http://localhost:11434` |
| `OLLAMA_MODEL` | Model to use | `qwen2.5:1.5b` |

**Setting up Ollama:**
```bash
# Install Ollama: https://ollama.com
# Pull a model that fits your available RAM:

ollama pull qwen2.5:1.5b    # ~1.2 GB RAM — recommended for most machines
ollama pull qwen2.5:3b      # ~2 GB RAM — better quality
ollama pull phi3:mini        # ~2.3 GB RAM — good alternative
```

Then set in `.env`:
```ini
OLLAMA_ENABLED=true
OLLAMA_MODEL=qwen2.5:1.5b
```

> If Ollama is disabled, the bot scrapes the first few paragraphs from each article URL as a summary fallback.

### Digest Settings

| Variable | Description | Default |
|---|---|---|
| `TOP_N_ARTICLES` | Number of articles per digest | `10` |
| `MAX_SUMMARY_WORDS` | Max words per summary | `60` |
| `LOOKBACK_HOURS` | How far back to look for news | `24` |

### Example `.env`

```ini
# Gmail
EMAIL_SENDER=you@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
EMAIL_RECIPIENT=you@gmail.com

# Telegram (leave blank to skip)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Ollama
OLLAMA_ENABLED=true
OLLAMA_MODEL=qwen2.5:1.5b

# Digest
TOP_N_ARTICLES=10
LOOKBACK_HOURS=24
```

---

## News Sources

### Company Blogs (RSS)

| Source | Feed |
|---|---|
| OpenAI Blog | openai.com/news/rss.xml |
| Anthropic Blog | anthropic.com/rss.xml |
| Google DeepMind | deepmind.google/blog/rss.xml |
| Google AI Blog | blog.google/technology/ai/rss/ |
| Meta AI Blog | ai.meta.com/blog/rss/ |
| NVIDIA AI Blog | blogs.nvidia.com/…/feed/ |
| Hugging Face Blog | huggingface.co/blog/feed.xml |
| Mistral AI Blog | mistral.ai/news/rss.xml |
| Microsoft AI Blog | blogs.microsoft.com/ai/feed/ |
| Perplexity Blog | perplexity.ai/hub/blog/feed |
| Papers With Code | paperswithcode.com/latest.rss |
| The Gradient | thegradient.pub/rss/ |

### Other Sources

| Source | Method |
|---|---|
| arXiv | RSS — cs.AI, cs.LG, cs.CL categories |
| Hacker News | Algolia search API — AI/ML keyword queries |
| Reddit | RSS — r/MachineLearning, r/artificial, etc. |
| GitHub Trending | HTML scraper |

---

## Tracked Companies

The bot auto-detects and tags articles mentioning these companies:

| Company | Detected via |
|---|---|
| OpenAI | openai, chatgpt, gpt-4, gpt-5, dall-e, sora, o1, o3 |
| Anthropic | anthropic, claude |
| Google DeepMind | deepmind, gemini, google ai, veo, imagen |
| Meta AI | meta ai, llama, meta llama |
| Microsoft AI | microsoft ai, copilot, azure ai, phi- |
| NVIDIA | nvidia, cuda, tensorrt |
| xAI | xai, grok, x.ai |
| Hugging Face | hugging face, huggingface |
| Mistral AI | mistral, mixtral, le chat |
| Perplexity | perplexity |

---

## Ranking System

Each article gets a score based on:

| Factor | Points |
|---|---|
| Source credibility (OpenAI/Anthropic blog) | +10 |
| Source credibility (HN) | +5 |
| Title keyword bonus (release, launch, new model) | +3 to +4 each |
| HN upvotes (per 100, capped at 5) | +1 to +5 |
| **🚀 Model release detected** | **+15 (always top)** |

Model release detection looks for action words (`releases`, `launches`, `unveils`, `announces`, `ships`) combined with model signals (`model`, `gpt-`, `claude`, version numbers like `v2.0`, `3.0`, etc.).

---

## GitHub Actions — Automated Daily Delivery

The bot runs automatically every day at **8:00 AM IST** (2:30 AM UTC) via GitHub Actions — no server required.

### Setup

**Step 1 — Push to GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
gh repo create Daily-news-Bot --public --source=. --remote=origin --push
```

**Step 2 — Add secrets**

```bash
gh secret set EMAIL_SENDER
gh secret set EMAIL_PASSWORD
gh secret set EMAIL_RECIPIENT

# Optional — Telegram
gh secret set TELEGRAM_BOT_TOKEN
gh secret set TELEGRAM_CHAT_ID
```

Or go to: GitHub repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

**Step 3 — Done**

The workflow in `.github/workflows/daily_digest.yml` runs on schedule automatically. You can also trigger it manually from the **Actions** tab → **AI Daily Digest** → **Run workflow**.

> **Note:** Ollama is not supported in GitHub Actions (no local GPU/CPU). When running in Actions, set `OLLAMA_ENABLED=false` — the scraper fallback runs instead.

### SQLite History in CI

The workflow uses GitHub Actions cache to persist `database/history.sqlite` between runs, so articles are not re-sent after each run.

---

## Running Manually

```bash
# Run the full pipeline
python3 main.py

# Reset article history (re-sends today's news)
python3 -c "
import sqlite3
conn = sqlite3.connect('database/history.sqlite')
conn.execute('DELETE FROM seen_articles')
conn.commit()
conn.close()
print('History cleared')
"
```

---

## Adding New Sources

### Add a blog RSS feed

Edit [`collectors/blogs.py`](collectors/blogs.py) and add a tuple to `RSS_FEEDS`:

```python
("Company Blog Name", "https://example.com/blog/rss.xml"),
```

Then add the source score in [`filters/ranking.py`](filters/ranking.py):

```python
"Company Blog Name": 8,
```

### Add a tracked company

Edit [`filters/companies.py`](filters/companies.py) and add an entry to `TRACKED_COMPANIES`:

```python
"New Company": ["alias1", "alias2", "model-name"],
```

The company will automatically appear as a colored tag in emails and be included in keyword filtering.

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| No email received | Gmail credentials wrong | Double-check App Password (not login password) |
| `SMTPAuthenticationError` | 2-Step Verification not enabled | Enable it in Google Account → Security |
| Articles have no summary | `OLLAMA_ENABLED=false` and scraper blocked | Enable Ollama, or check if sites block scrapers |
| Ollama out of memory | Model too large for available RAM | Use `qwen2.5:1.5b` (~1.2 GB) |
| Wrong Ollama model | `gemma3` not pulled | Run `ollama pull qwen2.5:1.5b` |
| "Nothing new today" | Dedup history has all articles | Clear history DB (see above) |
| Telegram SSL error | Corporate/VPN proxy intercepts SSL | Use Gmail delivery instead |
| GitHub Actions not running | Secrets not added | Add secrets in repo Settings → Secrets |

---

## Dependencies

```
feedparser       — RSS feed parsing
requests         — HTTP client for APIs and scraping
beautifulsoup4   — HTML parsing for article scraping
lxml             — Fast HTML/XML parser
python-dotenv    — Load .env file
```

---

## License

MIT — free to use, modify, and distribute.
