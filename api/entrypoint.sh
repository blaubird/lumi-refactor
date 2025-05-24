#!/bin/bash
# entrypoint.sh - Handles startup for the FastAPI application

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

# Start the application with the correct port and keep it running
echo "Starting Hypercorn server on port $PORT..."
exec hypercorn main:app --bind 0.0.0.0:$PORT --workers 2 --access-logfile - --error-logfile - --log-level info
