import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENTS, SMTP_HOST, SMTP_PORT
from filters.companies import detect_companies

SOURCE_EMOJI = {
    "OpenAI Blog": "🤖", "Anthropic Blog": "🧠", "Google DeepMind": "🔬",
    "arXiv": "📄", "GitHub Trending": "⭐", "Hacker News": "🔶",
    "Hugging Face Blog": "🤗", "Microsoft AI Blog": "🪟",
    "Mistral AI Blog": "💨", "Meta AI Blog": "🌐",
    "NVIDIA AI Blog": "💚", "Perplexity Blog": "🔍",
}

COMPANY_COLORS = {
    "OpenAI":          "#10a37f",
    "Anthropic":       "#d97706",
    "Google DeepMind": "#4285f4",
    "Meta AI":         "#0866ff",
    "Microsoft AI":    "#00a4ef",
    "NVIDIA":          "#76b900",
    "xAI":             "#1a1a1a",
    "Hugging Face":    "#ff9d00",
    "Mistral AI":      "#f43f5e",
    "Perplexity":      "#20b2aa",
}


def send_digest(articles: list[dict], date_str: str):
    if not (EMAIL_SENDER and EMAIL_PASSWORD and EMAIL_RECIPIENTS):
        raise ValueError("Email credentials not configured")

    html = _build_html(articles, date_str)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🧠 AI Daily Digest — {date_str}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(EMAIL_RECIPIENTS)
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, msg.as_string())


def _company_tags_html(title: str, summary: str) -> str:
    companies = detect_companies(title, summary)
    if not companies:
        return ""
    tags = ""
    for c in companies:
        color = COMPANY_COLORS.get(c, "#666")
        tags += f"<span style='display:inline-block;margin:2px 4px 2px 0;padding:1px 7px;border-radius:10px;font-size:11px;font-weight:600;background:{color}20;color:{color};border:1px solid {color}40'>{c}</span>"
    return f"<div style='margin:4px 0'>{tags}</div>"


def _build_html(articles: list[dict], date_str: str) -> str:
    rows = ""
    for i, a in enumerate(articles, 1):
        emoji = SOURCE_EMOJI.get(a["source"], "📰")
        summary = a.get("summary", "")
        summary_html = f"<p style='color:#555;font-size:14px;margin:6px 0 0'>{summary[:300]}</p>" if summary else ""
        company_tags = _company_tags_html(a["title"], summary)

        if a.get("_is_model_release"):
            release_badge = "<span style='display:inline-block;margin-right:6px;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700;background:#fff3e0;color:#e65100;border:1px solid #ffb74d'>🚀 NEW RELEASE</span>"
            row_style = "padding:16px 0;border-bottom:1px solid #eee;border-left:3px solid #e65100;padding-left:12px"
        else:
            release_badge = ""
            row_style = "padding:16px 0;border-bottom:1px solid #eee"

        rows += f"""
        <tr>
          <td style='{row_style}'>
            {release_badge}<b>{i}. <a href='{a["url"]}' style='color:#1a73e8;text-decoration:none'>{a["title"]}</a></b>
            <br><span style='color:#888;font-size:12px'>{emoji} {a["source"]}</span>
            {company_tags}
            {summary_html}
          </td>
        </tr>"""

    return f"""
    <html><body style='font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px'>
      <h1 style='color:#1a1a1a'>🧠 AI Daily Digest</h1>
      <p style='color:#666'>{date_str} &mdash; {len(articles)} stories</p>
      <table style='width:100%;border-collapse:collapse'>{rows}</table>
      <p style='color:#aaa;font-size:12px;margin-top:32px'>
        Powered by AI News Bot &mdash; sources: HN, Reddit, arXiv, GitHub, Blogs
      </p>
    </body></html>"""
