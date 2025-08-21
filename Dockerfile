# 1. Base image
FROM python:3.11-slim

# 2. Set working dir
WORKDIR /app

# 3. Copy requirements & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy source code
COPY . .

# 5. Env defaults
ENV PORT=8000
ENV HOST=0.0.0.0

# 6. Expose port
EXPOSE 8000

# 7. Run app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
