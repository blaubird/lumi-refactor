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
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if role_enum type already exists and drop it if needed
        logger.info("Checking for existing enum types...")
        cursor.execute("SELECT typname FROM pg_type WHERE typname = 'role_enum';")
        if cursor.fetchone():
            logger.info("Dropping existing role_enum type...")
            # Check if any tables use this enum
            cursor.execute("""
                SELECT c.relname 
                FROM pg_class c 
                JOIN pg_attribute a ON a.attrelid = c.oid 
                JOIN pg_type t ON a.atttypid = t.oid 
                WHERE t.typname = 'role_enum' AND c.relkind = 'r';
            """)
            tables = cursor.fetchall()
            
            if tables:
                logger.info(f"Found tables using role_enum: {tables}")
                # Drop tables that use the enum
                for table in tables:
                    logger.info(f"Dropping table {table[0]}...")
                    cursor.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE;")
            
            # Now drop the enum type
            cursor.execute("DROP TYPE role_enum;")
            logger.info("Dropped role_enum type")
        
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
    except Exception as e:
        logger.error(f"Error setting up database: {str(e)}")
        raise

if __name__ == "__main__":
    setup_database()
