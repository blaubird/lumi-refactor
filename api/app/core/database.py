"""Database module."""

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker

# Create engine
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base:
    """Base class for all models."""

    @declared_attr
    def __tablename__(cls):
        """Generate __tablename__ automatically."""
        return cls.__name__.lower()


# Dependency to get DB session
def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
