import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT, SMTP_HOST, SMTP_PORT

SOURCE_EMOJI = {
    "OpenAI Blog": "🤖", "Anthropic Blog": "🧠", "Google DeepMind": "🔬",
    "arXiv": "📄", "GitHub Trending": "⭐", "Hacker News": "🔶",
    "Hugging Face Blog": "🤗",
}


def send_digest(articles: list[dict], date_str: str):
    if not (EMAIL_SENDER and EMAIL_PASSWORD and EMAIL_RECIPIENT):
        raise ValueError("Email credentials not configured")

    html = _build_html(articles, date_str)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🧠 AI Daily Digest — {date_str}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())


def _build_html(articles: list[dict], date_str: str) -> str:
    rows = ""
    for i, a in enumerate(articles, 1):
        emoji = SOURCE_EMOJI.get(a["source"], "📰")
        summary = a.get("summary", "")
        summary_html = f"<p style='color:#555;font-size:14px'>{summary[:300]}</p>" if summary else ""
        rows += f"""
        <tr>
          <td style='padding:16px 0;border-bottom:1px solid #eee'>
            <b>{i}. <a href='{a["url"]}' style='color:#1a73e8;text-decoration:none'>{a["title"]}</a></b>
            <br><span style='color:#888;font-size:12px'>{emoji} {a["source"]}</span>
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
