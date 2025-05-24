FROM python:3.12-slim

WORKDIR /app

# Install only essential build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install dependencies with optimized pip settings
RUN pip install --no-cache-dir --compile --no-deps -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Run the application using the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
