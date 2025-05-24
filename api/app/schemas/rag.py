"""RAG schemas module."""

from typing import List, Optional

from pydantic import BaseModel, Field


class RAGQuery(BaseModel):
    """RAG query schema."""

    query: str = Field(..., description="Query text")
    system_prompt: Optional[str] = Field(None, description="System prompt for the LLM")
    top_k: Optional[int] = Field(
        3, description="Number of FAQs to retrieve for context"
    )


class RAGResponse(BaseModel):
    """RAG response schema."""

    response: str = Field(..., description="Generated response")
    sources: List[str] = Field(..., description="Source FAQ IDs used for context")
