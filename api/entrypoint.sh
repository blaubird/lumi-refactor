#!/bin/bash
# Simple entrypoint that ensures the process stays running

# Set default port
export PORT=${PORT:-8080}

# Run database setup
python scripts/setup_db.py

# Start the application with minimal configuration
# The key is to use 'exec' to replace the shell process
exec hypercorn main:app --bind 0.0.0.0:$PORT
