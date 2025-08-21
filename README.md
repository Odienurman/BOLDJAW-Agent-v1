pip install -r requirements.txt

Siapkan .env
OPENAI_API_KEY=sk-xxxxx
OPENAI_MODEL=gpt-4o-mini
PROMPT_FILE=prompt.txt

Jalankan
uvicorn app:app --reload --port 8000

Test
curl http://localhost:8000/health


🐳 Jalankan dengan Docker
docker-compose build
docker-compose up -d

curl http://localhost:8000/health

🔑 Contoh Request
curl -X POST http://localhost:8000/agent/reply \
  -H "Content-Type: application/json" \
  -d '{
    "task": "buat 1 tweet informatif soal Recall",
    "context": "announce hackathon",
    "style": "clean"
  }'

Contoh response:
{
  "output": "🚀 Recall is excited to announce our upcoming hackathon! Join us to innovate and create solutions...",
  "used_tools": []
}
