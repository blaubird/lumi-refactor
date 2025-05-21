import random
import string
from sqlalchemy.orm import Session
from app.models.tenant import Tenant

def create_test_tenant(db: Session):
    """Create a test tenant for development purposes"""
    # Generate random phone_id
    phone_id = ''.join(random.choices(string.digits, k=15))
    
    # Check if tenant with this phone_id already exists
    existing = db.query(Tenant).filter(Tenant.phone_id == phone_id).first()
    if existing:
        print(f"Tenant with phone_id {phone_id} already exists")
        return existing
    
    # Generate random token
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    # Create new tenant
    tenant = Tenant(
        id=f"tenant_{phone_id}",
        phone_id=phone_id,
        wh_token=token,
        system_prompt="You are a helpful assistant for testing purposes."
    )
    
    # Add to database
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    
    print(f"Created test tenant with ID: {tenant.id}")
    return tenant

if __name__ == "__main__":
    # Import here to avoid circular imports
    from app.core.database import SessionLocal
    
    # Create DB session
    db = SessionLocal()
    try:
        create_test_tenant(db)
    finally:
        db.close()
