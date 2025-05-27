FROM python:3.12-slim
WORKDIR /app
# Install only essential build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
# Copy requirements file
COPY requirements.txt .
# Update pip and install dependencies with optimized settings
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --compile -r requirements.txt
# Copy application code
COPY . .
# Use CMD without worker-class asyncio flag
CMD hypercorn main:app --bind 0.0.0.0:$PORT
