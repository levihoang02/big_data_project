FROM python:3.11-slim

WORKDIR /app

# Install required packages

RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your consumer code
COPY . .

CMD ["python", "stream_consumer.py"]