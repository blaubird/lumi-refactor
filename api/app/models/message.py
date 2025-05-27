from sqlalchemy import String, Text, DateTime, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base

class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id"), index=True)
    wa_msg_id: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[str] = mapped_column(Enum("user", "assistant", "system", name="role_enum"))
    text: Mapped[str] = mapped_column(Text)
    ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
