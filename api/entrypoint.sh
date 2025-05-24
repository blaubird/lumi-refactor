#!/bin/bash
# Minimal entrypoint script that ensures the process stays running

# Set default port
export PORT=${PORT:-8000}

# Run database setup
python scripts/setup_db.py

# Start the application with minimal configuration
# The 'exec' command is critical - it replaces the shell process with Hypercorn
exec hypercorn main:app --bind 0.0.0.0:$PORT --worker-class asyncio
