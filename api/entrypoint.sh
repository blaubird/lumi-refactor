#!/bin/bash
# entrypoint.sh - Handles startup for the FastAPI application

# Set default port if not provided
export PORT=${PORT:-8080}

# Run database setup
python scripts/setup_db.py

# Start the application with the correct port
exec hypercorn main:app --bind 0.0.0.0:$PORT
