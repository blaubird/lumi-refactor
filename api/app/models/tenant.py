from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Tenant(Base):
    __tablename__ = "tenants"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    phone_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    wh_token: Mapped[str] = mapped_column(Text, nullable=False)
    system_prompt: Mapped[str] = mapped_column(Text, default="You are a helpful assistant.")
