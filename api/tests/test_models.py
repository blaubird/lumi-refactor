import pytest
from sqlalchemy.exc import IntegrityError
from app.models.tenant import Tenant

def test_tenant_create(test_db):
    # Create a test tenant
    tenant = Tenant(
        id="test_tenant_1",
        phone_id="123456789",
        wh_token="test_token",
        system_prompt="Test system prompt"
    )
    
    # Add to database
    test_db.add(tenant)
    test_db.commit()
    
    # Query to verify
    db_tenant = test_db.query(Tenant).filter(Tenant.id == "test_tenant_1").first()
    
    # Assertions
    assert db_tenant is not None
    assert db_tenant.id == "test_tenant_1"
    assert db_tenant.phone_id == "123456789"
    assert db_tenant.wh_token == "test_token"
    assert db_tenant.system_prompt == "Test system prompt"

def test_tenant_default_system_prompt(test_db):
    # Create a tenant without specifying system_prompt
    tenant = Tenant(
        id="test_tenant_2",
        phone_id="987654321",
        wh_token="another_token"
    )
    
    # Add to database
    test_db.add(tenant)
    test_db.commit()
    
    # Query to verify
    db_tenant = test_db.query(Tenant).filter(Tenant.id == "test_tenant_2").first()
    
    # Assert default system prompt is set
    assert db_tenant.system_prompt == "You are a helpful assistant."

def test_tenant_unique_phone_id(test_db):
    # Create first tenant
    tenant1 = Tenant(
        id="test_tenant_3",
        phone_id="555555555",
        wh_token="token1"
    )
    test_db.add(tenant1)
    test_db.commit()
    
    # Create second tenant with same phone_id
    tenant2 = Tenant(
        id="test_tenant_4",
        phone_id="555555555",  # Same phone_id as tenant1
        wh_token="token2"
    )
    test_db.add(tenant2)
    
    # Should raise IntegrityError due to unique constraint
    with pytest.raises(IntegrityError):
        test_db.commit()
    
    # Rollback for cleanup
    test_db.rollback()

def test_tenant_nullable_fields(test_db):
    # Test that required fields cannot be null
    tenant = Tenant(
        id="test_tenant_5",
        phone_id=None,  # This should cause an error
        wh_token="token"
    )
    test_db.add(tenant)
    
    # Should raise IntegrityError due to NOT NULL constraint
    with pytest.raises(IntegrityError):
        test_db.commit()
    
    # Rollback for cleanup
    test_db.rollback()
