#!/bin/bash
# entrypoint.sh - Final version with network timeout fixes

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

# Start the application with network-optimized settings
echo "Starting Hypercorn server on port $PORT..."
exec hypercorn main:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --worker-class asyncio \
    --keep-alive 75 \
    --graceful-timeout 30 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
