"""Setup database script."""
import argparse
import logging
import os
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import after path setup
try:
    from app.core.database import Base, SessionLocal, engine
    from app.models.faq import FAQ
    from app.models.tenant import Tenant
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)

def setup_database(create_sample_data: bool = False):
    """Set up the database."""
    try:
        # Check if database exists and has tables
        # We'll use a different approach than creating tables directly
        # to avoid conflicts with Alembic migrations
        logger.info("Checking database status...")
        
        # Check if alembic_version table exists
        # If it doesn't, we'll assume this is a fresh database
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        
        # Check if tables exist
        existing_tables = inspector.get_table_names()
        logger.info(f"Found existing tables: {existing_tables}")
        
        if "alembic_version" not in existing_tables:
            logger.info("No alembic_version table found, running migrations...")
            # Run Alembic migrations instead of creating tables directly
            try:
                from alembic.config import Config
                from alembic import command
                
                # Get the directory of this script
                script_dir = Path(__file__).parent
                # Get the parent directory (project root)
                project_root = script_dir.parent
                # Path to alembic.ini
                alembic_ini = project_root / "alembic.ini"
                
                if not alembic_ini.exists():
                    logger.error(f"Alembic config not found at {alembic_ini}")
                    # Fall back to direct table creation as a last resort
                    logger.warning("Falling back to direct table creation")
                    Base.metadata.create_all(bind=engine)
                else:
                    # Run migrations
                    alembic_cfg = Config(str(alembic_ini))
                    command.upgrade(alembic_cfg, "head")
                    logger.info("Alembic migrations applied successfully")
            except Exception as e:
                logger.error(f"Failed to run migrations: {e}")
                # Fall back to direct table creation as a last resort
                logger.warning("Falling back to direct table creation")
                Base.metadata.create_all(bind=engine)
        else:
            logger.info("Database already initialized with Alembic")
        
        logger.info("Database setup complete")
        
        # Create sample data if requested
        if create_sample_data:
            create_sample_data_func()
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        # Don't exit, let the application continue

def create_sample_data_func():
    """Create sample data in the database."""
    logger.info("Creating sample data...")
    db = SessionLocal()
    try:
        # Create sample tenant if it doesn't exist
        tenant = db.query(Tenant).filter(Tenant.name == "sample").first()
        if not tenant:
            tenant = Tenant(name="sample", api_key="sample_api_key")
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            logger.info(f"Created sample tenant with ID: {tenant.id}")
        else:
            logger.info(f"Sample tenant already exists with ID: {tenant.id}")
        
        # Create sample FAQs
        sample_faqs = [
            {
                "question": "What is Lumi?",
                "answer": "Lumi is an AI-powered knowledge base system.",
            },
            {
                "question": "How do I add new FAQs?",
                "answer": "You can add new FAQs through the admin API.",
            },
            {
                "question": "What technologies does Lumi use?",
                "answer": "Lumi uses FastAPI, SQLAlchemy, and OpenAI.",
            },
            {
                "question": "Is Lumi open source?",
                "answer": "Yes, Lumi is available under the MIT license.",
            },
        ]
        
        for faq_data in sample_faqs:
            # Check if FAQ already exists
            existing_faq = db.query(FAQ).filter(
                FAQ.tenant_id == tenant.id,
                FAQ.question == faq_data["question"]
            ).first()
            
            if not existing_faq:
                faq = FAQ(
                    tenant_id=tenant.id,
                    question=faq_data["question"],
                    answer=faq_data["answer"],
                )
                db.add(faq)
                logger.info(f"Added FAQ: {faq_data['question']}")
        
        db.commit()
        logger.info("Sample data creation complete")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up the database")
    parser.add_argument(
        "--sample-data",
        action="store_true",
        help="Create sample data",
    )
    args = parser.parse_args()
    
    # Set up database
    setup_database(create_sample_data=args.sample_data)
