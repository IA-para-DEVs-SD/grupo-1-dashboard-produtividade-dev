# --- Stage 1: build ---
FROM python:3.12-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# --- Stage 2: runtime ---
FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
