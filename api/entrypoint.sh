#!/bin/bash
# Railway-specific entrypoint

export PORT=${PORT:-8080}

# Run database setup
python scripts/setup_db.py

# Start with Railway-specific network settings
exec hypercorn main:app \
    --bind 0.0.0.0:$PORT \
    --worker-class asyncio \
    --keep-alive 60 \
    --graceful-timeout 30 \
    --access-logfile - \
    --error-logfile -
