from app.core.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

# Export dependencies
__all__ = ["get_db"]
