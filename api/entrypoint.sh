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

# Start the application with optimized Hypercorn settings
echo "Starting Hypercorn server on port $PORT..."
exec hypercorn main:app --bind 0.0.0.0:$PORT --workers 4 --worker-class=asyncio --access-logfile - --error-logfile - --log-level info
