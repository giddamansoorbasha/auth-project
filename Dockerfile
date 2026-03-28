# ── Base Image ──────────────────────────────
FROM python:3.12-slim

# ── Set working directory ───────────────────
WORKDIR /app

# ── Install dependencies first (layer cache) ─
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy app code ───────────────────────────
COPY . .

# ── Expose port ─────────────────────────────
EXPOSE 8000

# ── Run the app ─────────────────────────────
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]