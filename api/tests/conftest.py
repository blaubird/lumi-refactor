"""Test conftest module."""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base


@pytest.fixture
def test_db():
    """Create a test database."""
    # Create in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    
    # Create tables
    Base.metadata.create_all(engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
