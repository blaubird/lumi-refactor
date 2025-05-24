"""Message model module."""

from sqlalchemy import Column, ForeignKey, String, Text

from app.models.base import BaseModel


class Message(BaseModel):
    """Message model."""

    tenant_id = Column(
        String, ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False, default="user")  # 'user' or 'assistant'
