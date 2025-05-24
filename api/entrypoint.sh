#!/bin/bash
# entrypoint.sh - Enhanced startup for the FastAPI application with improved error handling

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

# Check if application can import all dependencies
echo "Verifying dependencies..."
python -c "from app.core.database import Base, SessionLocal, engine; print('Core dependencies verified')" || {
    echo "WARNING: Failed to import core dependencies, application may not start correctly"
}

# Start the application with optimized Hypercorn settings and keep-alive
echo "Starting Hypercorn server on port $PORT..."
exec hypercorn main:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --worker-class asyncio \
    --keep-alive 120 \
    --graceful-timeout 10 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug
