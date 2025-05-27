from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

# Export dependencies
__all__ = ["get_db"]
