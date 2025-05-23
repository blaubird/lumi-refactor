"""Base model module."""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """Base model for all database models."""

    __abstract__ = True

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
