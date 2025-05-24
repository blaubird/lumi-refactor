"""Admin schemas module."""

from datetime import datetime
from typing import List, Optional

# Removed unused import: Dict

from pydantic import BaseModel, Field


class TenantBase(BaseModel):
    """Base tenant schema."""

    name: str = Field(..., description="Name of the tenant")
    api_key: Optional[str] = Field(None, description="API key for the tenant")


class TenantCreate(TenantBase):
    """Tenant creation schema."""

    pass


class TenantUpdate(TenantBase):
    """Tenant update schema."""

    name: Optional[str] = Field(None, description="Name of the tenant")


class Tenant(TenantBase):
    """Tenant schema."""

    id: str = Field(..., description="Unique identifier for the tenant")
    created_at: datetime = Field(
        ..., description="Timestamp when the tenant was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the tenant was last updated"
    )

    class Config:
        """Pydantic config."""

        orm_mode = True


class FAQBase(BaseModel):
    """Base FAQ schema."""

    question: str = Field(..., description="Question text")
    answer: str = Field(..., description="Answer text")


class FAQCreate(FAQBase):
    """FAQ creation schema."""

    pass


class FAQUpdate(BaseModel):
    """FAQ update schema."""

    question: Optional[str] = Field(None, description="Question text")
    answer: Optional[str] = Field(None, description="Answer text")


class FAQ(FAQBase):
    """FAQ schema."""

    id: str = Field(..., description="Unique identifier for the FAQ")
    tenant_id: str = Field(..., description="Tenant ID this FAQ belongs to")
    created_at: datetime = Field(..., description="Timestamp when the FAQ was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when the FAQ was last updated"
    )

    class Config:
        """Pydantic config."""

        orm_mode = True


class FAQList(BaseModel):
    """FAQ list schema."""

    items: List[FAQ] = Field(..., description="List of FAQs")
    total: int = Field(..., description="Total number of FAQs")


class TenantList(BaseModel):
    """Tenant list schema."""

    items: List[Tenant] = Field(..., description="List of tenants")
    total: int = Field(..., description="Total number of tenants")


class APIKeyResponse(BaseModel):
    """API key response schema."""

    api_key: str = Field(..., description="Generated API key")


class StatusResponse(BaseModel):
    """Status response schema."""

    status: str = Field(..., description="Operation status")
    message: str = Field(..., description="Status message")
