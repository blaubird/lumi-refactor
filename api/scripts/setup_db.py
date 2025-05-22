#!/usr/bin/env python3
import os
import psycopg2
from alembic.config import Config
from alembic import command
from app.core.logging import logger

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
