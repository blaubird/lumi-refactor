"""Setup database script."""
import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import after path setup
from app.core.database import Base, SessionLocal, engine
from app.models.faq import FAQ
from app.models.tenant import Tenant


def setup_database(create_sample_data: bool = False):
    """Set up the database."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

    if create_sample_data:
        # Create sample data
        db = SessionLocal()
        try:
            # Create sample tenant if it doesn't exist
            tenant = db.query(Tenant).filter(Tenant.name == "sample").first()
            if not tenant:
                tenant = Tenant(name="sample", api_key="sample_api_key")
                db.add(tenant)
                db.commit()
                db.refresh(tenant)
                print(f"Created sample tenant with ID: {tenant.id}")
            else:
                print(f"Sample tenant already exists with ID: {tenant.id}")

            # Create sample FAQs
            sample_faqs = [
                {
                    "question": "What is Lumi?",
                    "answer": "Lumi is an AI-powered knowledge base system."
                },
                {
                    "question": "How do I add new FAQs?",
                    "answer": "You can add new FAQs through the admin API."
                },
                {
                    "question": "What technologies does Lumi use?",
                    "answer": "Lumi uses FastAPI, SQLAlchemy, and OpenAI."
                },
                {
                    "question": "Is Lumi open source?",
                    "answer": "Yes, Lumi is available under the MIT license."
                }
            ]

            for faq_data in sample_faqs:
                faq = FAQ(
                    tenant_id=tenant.id,
                    question=faq_data["question"],
                    answer=faq_data["answer"]
                )
                db.add(faq)

            db.commit()
            print("Sample FAQs created.")
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
