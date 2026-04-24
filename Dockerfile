# ==============================================================
# Dockerfile — Network Security System (FastAPI + Uvicorn)
# ==============================================================

FROM python:3.10-slim-buster

# Set working directory inside the container
WORKDIR /app

# Install system-level dependencies
RUN apt-get update -y && apt-get install -y \
    awscli \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (leverages Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project source code
COPY . .

# Install the project as a local package (required by -e . in requirements.txt)
RUN pip install --no-cache-dir -e .

# ------------------------------------------------------------------
# Runtime environment variables
# Overridden at container run-time via the CI/CD workflow.
# Never hard-code secrets here.
# ------------------------------------------------------------------
ENV MONGO_DB_URL=""
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_DEFAULT_REGION=""
ENV MLFLOW_TRACKING_URI=""
ENV MLFLOW_TRACKING_USERNAME=""
ENV MLFLOW_TRACKING_PASSWORD=""

# Expose FastAPI port
EXPOSE 8080

# Start FastAPI app via uvicorn on 0.0.0.0:8080
# app:app  →  filename: app.py, FastAPI instance variable: app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]