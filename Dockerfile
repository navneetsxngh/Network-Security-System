# ─────────────────────────────────────────────────────────────
# Stage 1 – Builder
#   Installs all Python dependencies into an isolated layer so
#   the final image doesn't need build-time tools.
# ─────────────────────────────────────────────────────────────
FROM python:3.11.9-slim AS builder
 
WORKDIR /build
 
# System deps needed only to compile wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
    && rm -rf /var/lib/apt/lists/*
 
COPY requirements.txt .
COPY setup.py .
COPY networksecurity/ ./networksecurity/
COPY Network_Security.egg-info/ ./Network_Security.egg-info/
 
# Install into a prefix so we can copy the whole tree cleanly
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && pip install --no-cache-dir --prefix=/install -e .