## Clone repo
```sh
git clone https://github.com/<username>/boldjaw-agent-v1.git
```
```sh
cd boldjaw-agent-v1
```
```sh
pip install -r requirements.txt
```

## Siapkan .env
```sh
OPENAI_API_KEY=sk-xxxxx
OPENAI_MODEL=gpt-4o-mini
PROMPT_FILE=prompt.txt
```

## Jalankan
```sh
uvicorn app:app --reload --port 8000
```

## Test
```sh
curl http://localhost:8000/health
```


## 🐳 Jalankan dengan Docker
```sh
docker-compose build
docker-compose up -d
```
```sh
curl http://localhost:8000/health
```

## 🔑 Contoh Request
```sh
curl -X POST http://localhost:8000/agent/reply \
  -H "Content-Type: application/json" \
  -d '{
    "task": "buat 1 tweet informatif soal Recall",
    "context": "announce hackathon",
    "style": "clean"
  }'
```

## Contoh response:
{
  "output": "🚀 Recall is excited to announce our upcoming hackathon! Join us to innovate and create solutions...",
  "used_tools": []
}
