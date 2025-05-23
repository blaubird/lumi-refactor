"""Bulk import schemas module."""
from typing import List

from pydantic import BaseModel, Field


class FAQImportItem(BaseModel):
    """FAQ import item schema."""

    question: str = Field(..., description="Question text")
    answer: str = Field(..., description="Answer text")


class FAQBulkImport(BaseModel):
    """FAQ bulk import schema."""

    items: List[FAQImportItem] = Field(
        ..., description="List of FAQs to import"
    )


class BulkImportResponse(BaseModel):
    """Bulk import response schema."""

    success_count: int = Field(
        ..., description="Number of successfully imported items"
    )
    error_count: int = Field(..., description="Number of failed imports")
    errors: List[str] = Field(..., description="List of error messages")
