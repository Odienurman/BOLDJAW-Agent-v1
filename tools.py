import requests
from bs4 import BeautifulSoup

def summarize_url(url: str, max_chars: int = 1200) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (AgentSummarizer/1.0)"}
    r = requests.get(url, timeout=15, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else ""
    paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    text = (title + "\n" + "\n".join(paras)).strip()
    text = " ".join(text.split())
    return text[:max_chars]
