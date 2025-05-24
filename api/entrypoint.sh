#!/bin/bash
# Railway-specific entrypoint with proper configuration

# Set default port with explicit logging
export PORT=${PORT:-8080}
echo "PORT environment variable is set to: $PORT"

# Run database setup
echo "Running database setup..."
python scripts/setup_db.py

# Start the application with Railway-specific configuration
# The 'exec' command is critical - it replaces the shell process with Hypercorn
echo "Starting Hypercorn server on port $PORT..."
exec hypercorn main:app --bind 0.0.0.0:$PORT --worker-class asyncio
