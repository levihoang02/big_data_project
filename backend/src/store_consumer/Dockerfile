FROM python:3.11-slim

WORKDIR /app

# Install only essential build dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add debugging for database connection
ENV PYTHONUNBUFFERED=1

CMD ["python", "storage_consumer.py"]