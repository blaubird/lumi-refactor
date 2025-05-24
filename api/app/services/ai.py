"""AI services module."""

import logging
import os
from typing import List, Optional

import openai
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.faq import FAQ
from app.services.monitoring import track_embedding_generation, track_rag_query

# Configure logging
logger = logging.getLogger(__name__)

# Configure OpenAI client
client = openai.AsyncClient(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_embedding(text: str) -> Optional[List[float]]:
    """Generate embedding for text using OpenAI API."""
    try:
        # Track embedding generation (will be successful if no exception)
        track_embedding_generation(tenant_id="system", success=True)

        # Generate embedding
        response = await client.embeddings.create(
            model="text-embedding-ada-002", input=text
        )
        return response.data[0].embedding
    except Exception as e:
        # Track embedding generation failure
        track_embedding_generation(tenant_id="system", success=False)
        logger.error(f"Error generating embedding: {str(e)}")
        return None


async def find_relevant_faqs(
    db: Session, tenant_id: str, query: str, top_k: int = 3
) -> List[FAQ]:
    """Find relevant FAQs for a query using vector similarity."""
    try:
        # Generate embedding for query
        query_embedding = await generate_embedding(query)
        if not query_embedding:
            logger.error("Failed to generate embedding for query")
            return []

        # Get all FAQs for tenant
        faqs = db.query(FAQ).filter(FAQ.tenant_id == tenant_id).all()
        if not faqs:
            logger.warning(f"No FAQs found for tenant {tenant_id}")
            return []

        # Calculate similarity scores
        scored_faqs = []
        for faq in faqs:
            # Skip FAQs without embeddings
            if not faq.embedding:
                continue

            # Calculate cosine similarity
            similarity = faq.embedding.cosine_similarity(query_embedding)
            scored_faqs.append((faq, similarity))

        # Sort by similarity (descending) and take top_k
        scored_faqs.sort(key=lambda x: x[1], reverse=True)
        return [faq for faq, _ in scored_faqs[:top_k]]
    except Exception as e:
        logger.error(f"Error finding relevant FAQs: {str(e)}")
        return []


async def get_rag_response(
    db: Session,
    tenant_id: str,
    query: str,
    system_prompt: str = None,
    top_k: int = 3,
) -> Optional[str]:
    """Generate RAG response for a query."""
    try:
        # Track RAG query (will be successful if no exception)
        track_rag_query(tenant_id=tenant_id, success=True)

        # Find relevant FAQs
        relevant_faqs = await find_relevant_faqs(db, tenant_id, query, top_k=top_k)
        if not relevant_faqs:
            logger.warning("No relevant FAQs found")
            return "I couldn't find any relevant information to answer your question."

        # Construct context from relevant FAQs
        context = "\n\n".join(
            [f"Q: {faq.question}\nA: {faq.answer}" for faq in relevant_faqs]
        )

        # Set default system prompt if not provided
        if not system_prompt:
            system_prompt = (
                "You are a helpful assistant. Answer the question based on the "
                "provided context. If the context doesn't contain relevant "
                "information, say so."
            )

        # Generate response using OpenAI API
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}",
                },
            ],
            temperature=0.7,
            max_tokens=500,
        )

        return response.choices[0].message.content
    except Exception as e:
        # Track RAG query failure
        track_rag_query(tenant_id=tenant_id, success=False)
        logger.error(f"Error generating RAG response: {str(e)}")
        return "Sorry, I encountered an error while processing your request."
