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
    
    # Check if tables exist before resetting alembic_version
    cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'tenants')")
    tables_exist = cursor.fetchone()[0]
    
    if tables_exist:
        # If tables exist but we're redeploying, just reset alembic_version to match our migration
        try:
            cursor.execute("DROP TABLE IF EXISTS alembic_version")
            cursor.execute("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)")
            cursor.execute("INSERT INTO alembic_version VALUES ('001_initial_schema')")
            print("Reset alembic_version table to match existing schema")
        except Exception as e:
            print(f"Error resetting alembic_version table: {e}")
    
    # Close the connection
    cursor.close()
    conn.close()
    
    # Apply migrations if tables don't exist
    if not tables_exist:
        try:
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
            print("Applied migrations successfully")
        except Exception as e:
            print(f"Error applying migrations: {e}")
            # If migration fails, try to recover by manually creating alembic_version
            try:
                conn = psycopg2.connect(database_url)
                conn.autocommit = True
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) NOT NULL)")
                cursor.execute("DELETE FROM alembic_version")
                cursor.execute("INSERT INTO alembic_version VALUES ('001_initial_schema')")
                cursor.close()
                conn.close()
                print("Created alembic_version table manually as recovery")
            except Exception as recovery_error:
                print(f"Recovery attempt failed: {recovery_error}")
    
if __name__ == "__main__":
    setup_database()
