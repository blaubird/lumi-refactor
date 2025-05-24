"""Database module."""

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import sessionmaker

# Create engine
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create declarative base
Base = declarative_base()


class BaseModel(Base):
    """Base class for all models."""
    
    __abstract__ = True
    
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
