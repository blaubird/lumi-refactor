"""Optimized entrypoint script for Railway deployment."""

#!/bin/bash
# entrypoint.sh - Optimized startup for the FastAPI application

# Set default port if not provided
export PORT=${PORT:-8080}

# Configure logging
echo "Starting application initialization at $(date)"

# Run database setup with error handling
echo "Running database setup..."
python scripts/setup_db.py || {
    echo "Database setup failed with exit code $?"
    echo "Continuing with application startup anyway..."
}

# Verify WhatsApp and OpenAI credentials
echo "Verifying API credentials..."
python -c "import os; missing = [k for k in ['WHATSAPP_API_TOKEN', 'WHATSAPP_PHONE_NUMBER_ID', 'WH_TOKEN', 'OPENAI_API_KEY'] if not os.getenv(k)]; print(f'Missing credentials: {missing}' if missing else 'All credentials verified')"

# Start the application with optimized Hypercorn settings
echo "Starting Hypercorn server on port $PORT..."
exec hypercorn main:app \
    --bind 0.0.0.0:$PORT \
    --worker-class asyncio \
    --workers 1 \
    --keep-alive 60 \
    --graceful-timeout 30 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
