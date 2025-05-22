#!/usr/bin/env python3
import os
import sys
import psycopg2
from alembic.config import Config
from alembic import command
import logging

# Add parent directory to sys.path to make 'app' importable
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Configure basic logging since we can't import app.core.logging yet
logging.basicConfig(
    format="%(levelname)s [%(name)s] [%(module)s:%(lineno)d] %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def setup_database():
    """Set up database before application startup"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    logger.info("Setting up database...")
    
    # Connect to database
    conn = psycopg2.connect(database_url)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Activate pgvector extension
    logger.info("Activating pgvector extension...")
    cursor.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    
    # Close connection
    cursor.close()
    conn.close()
    
    # Apply migrations
    logger.info("Applying migrations...")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    
    logger.info("Database setup complete")

if __name__ == "__main__":
    setup_database()
