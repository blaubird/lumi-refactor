import os
import sys
import psycopg2
from alembic.config import Config
from alembic import command

def setup_database():
    """Set up the database before running the application"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    # Add the parent directory to sys.path to make 'app' importable
    sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    
    # Connect to the database
    conn = psycopg2.connect(database_url)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Activate pgvector
    cursor.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    
    # Reset alembic_version table to fix migration history mismatch
    try:
        cursor.execute('DROP TABLE IF EXISTS alembic_version;')
        print("Dropped alembic_version table to reset migration history")
    except Exception as e:
        print(f"Error dropping alembic_version table: {e}")
    
    # Close the connection
    cursor.close()
    conn.close()
    
    # Apply migrations
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    
if __name__ == "__main__":
    setup_database()
