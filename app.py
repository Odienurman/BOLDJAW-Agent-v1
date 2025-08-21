import os
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import List, Optional
from openai import OpenAI

from tools import summarize_url

# ===== Config =====
PROMPT_FILE = os.getenv("PROMPT_FILE", "prompt.txt")  # ganti ke file yang ada
try:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    SYSTEM_PROMPT = "You are BOLDJAWIM v1 — concise, CT-native. (fallback prompt)"

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="BOLDJAWIM Agent", version="1.0.0")

class ToolInput(BaseModel):
    url: Optional[str] = None

class AgentRequest(BaseModel):
    task: str
    context: Optional[str] = ""
    tools: Optional[ToolInput] = None
    style: Optional[str] = "degen"

class AgentResponse(BaseModel):
    output: str
    used_tools: List[str] = Field(default_factory=list)  # <- aman

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/agent/reply", response_model=AgentResponse)
def agent_reply(req: AgentRequest = Body(...)):
    used = []
    extra_context = ""

    if req.tools and req.tools.url:
        try:
            summary = summarize_url(req.tools.url)
            extra_context += f"\n\n[URL SUMMARY]\n{summary}\n"
            used.append("summarize_url")
        except Exception as e:
            extra_context += f"\n\n[URL SUMMARY ERROR] {e}\n"

    user_prompt = f"""
[STYLE]={req.style}
[TASK]={req.task}
[CONTEXT]={req.context}
{extra_context}
== RULES ==
- Jawab singkat, tajam, tanpa spam.
- Jika membuat tweet: <=280 chars (tanpa thread), no emoji berlebihan.
- Jika mendeteksi fake giveaway: sebut 2 alasan singkat + saran aman.
- Tutup output dengan 1 action-step jika relevan.
"""

    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6,
    )

    return AgentResponse(
        output=resp.choices[0].message.content.strip(),
        used_tools=used
    )
