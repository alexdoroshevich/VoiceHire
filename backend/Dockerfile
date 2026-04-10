# ── Base ──────────────────────────────────────────────────────────────────────
FROM python:3.13-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

# ── Development ───────────────────────────────────────────────────────────────
FROM base AS development

RUN pip install --no-cache-dir -e ".[dev]"
COPY . .
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

# ── Production ────────────────────────────────────────────────────────────────
FROM base AS production

COPY . .
RUN pip install --no-cache-dir . gunicorn

EXPOSE 8080

CMD ["gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "2", \
     "--bind", "0.0.0.0:8080", \
     "--timeout", "120", \
     "--graceful-timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
