"""Test models module."""

import pytest
from app.models.faq import FAQ
from app.models.message import Message
from app.models.tenant import Tenant
from sqlalchemy.exc import IntegrityError


def test_tenant_creation(test_db):
    """Test tenant creation."""
    # Create tenant
    tenant = Tenant(name="Test Tenant", api_key="test_api_key")
    test_db.add(tenant)
    test_db.commit()

    # Retrieve tenant
    retrieved = test_db.query(Tenant).filter(Tenant.id == tenant.id).first()

    # Assertions
    assert retrieved is not None
    assert retrieved.name == "Test Tenant"
    assert retrieved.api_key == "test_api_key"


def test_faq_creation(test_db):
    """Test FAQ creation."""
    # Create tenant
    tenant = Tenant(name="Test Tenant", api_key="test_api_key")
    test_db.add(tenant)
    test_db.commit()

    # Create FAQ
    faq = FAQ(tenant_id=tenant.id, question="Test question?", answer="Test answer.")
    test_db.add(faq)
    test_db.commit()

    # Retrieve FAQ
    retrieved = test_db.query(FAQ).filter(FAQ.id == faq.id).first()

    # Assertions
    assert retrieved is not None
    assert retrieved.question == "Test question?"
    assert retrieved.answer == "Test answer."
    assert retrieved.tenant_id == tenant.id


def test_message_creation(test_db):
    """Test message creation."""
    # Create tenant
    tenant = Tenant(name="Test Tenant", api_key="test_api_key")
    test_db.add(tenant)
    test_db.commit()

    # Create message
    message = Message(
        tenant_id=tenant.id, user_id="test_user", content="Test message", role="user"
    )
    test_db.add(message)
    test_db.commit()

    # Retrieve message
    retrieved = test_db.query(Message).filter(Message.id == message.id).first()

    # Assertions
    assert retrieved is not None
    assert retrieved.content == "Test message"
    assert retrieved.user_id == "test_user"
    assert retrieved.role == "user"
    assert retrieved.tenant_id == tenant.id


def test_faq_tenant_relationship(test_db):
    """Test FAQ-tenant relationship."""
    # Create tenant
    tenant = Tenant(name="Test Tenant", api_key="test_api_key")
    test_db.add(tenant)
    test_db.commit()

    # Create FAQ
    faq = FAQ(tenant_id=tenant.id, question="Test question?", answer="Test answer.")
    test_db.add(faq)
    test_db.commit()

    # Delete tenant
    test_db.delete(tenant)
    test_db.commit()

    # Try to retrieve FAQ (should be deleted due to CASCADE)
    retrieved = test_db.query(FAQ).filter(FAQ.id == faq.id).first()

    # Assertions
    assert retrieved is None
