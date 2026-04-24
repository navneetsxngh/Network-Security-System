# Use a modern, supported base image
FROM python:3.11-slim-bookworm

# Prevent Python from writing pyc files & enable logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (fixes pip build issues)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (for caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --prefer-binary -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose port (change if your app uses another port)
EXPOSE 8000

# Run the app (update this based on your entry file)
CMD ["python", "app.py"]