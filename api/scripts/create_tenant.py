"""Create tenant script."""
import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import after path setup
from app.core.database import SessionLocal
from app.models.tenant import Tenant


def create_tenant(name: str, api_key: str = None):
    """Create a new tenant."""
    # Create database session
    db = SessionLocal()

    try:
        # Check if tenant already exists
        existing_tenant = db.query(Tenant).filter(Tenant.name == name).first()
        if existing_tenant:
            print(f"Tenant '{name}' already exists with ID: {existing_tenant.id}")
            return existing_tenant.id

        # Create new tenant
        tenant = Tenant(name=name, api_key=api_key)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

        print(f"Created tenant '{name}' with ID: {tenant.id}")
        return tenant.id
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new tenant")
    parser.add_argument("name", help="Name of the tenant")
    parser.add_argument("--api-key", help="API key for the tenant (optional)")
    args = parser.parse_args()

    # Create tenant
    create_tenant(name=args.name, api_key=args.api_key)
