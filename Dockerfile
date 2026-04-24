FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs are printed directly
ENV PYTHONUNBUFFERED=1

COPY . .

RUN apt update -y && apt install awscli -y

RUN apt-get update 
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]
