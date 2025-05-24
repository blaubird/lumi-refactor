"""RAG endpoints module."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_tenant_id
from app.schemas.rag import RAGQuery, RAGResponse
from app.services.ai import get_rag_response

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.post("/query", response_model=RAGResponse)
async def query(
    query: RAGQuery,
    tenant_id: str = Depends(get_tenant_id),
    db: Session = Depends(get_db),
):
    """
    Query the RAG system.

    This endpoint takes a query and returns a response generated using
    relevant FAQs as context.
    """
    try:
        # Log the query
        logger.info(f"RAG query received from tenant {tenant_id}: {query.query}")

        # Get response
        response = await get_rag_response(
            db,
            tenant_id,
            query.query,
            system_prompt=query.system_prompt,
            top_k=query.top_k,
        )

        # Return response
        return {
            "response": response,
            "sources": [],  # In a real implementation, this would include source IDs
        }
    except Exception as e:
        # Log the error
        logger.error(f"Error processing RAG query: {str(e)}")

        # Return error
        raise HTTPException(
            status_code=500, detail="An error occurred while processing your query."
        )
