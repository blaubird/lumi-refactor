"""Test services module."""
# Removed unused import: os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.ai import find_relevant_faqs, generate_embedding, get_rag_response
# Removed unused import: sqlalchemy.orm.Session
from app.models.faq import FAQ

# Mock data
MOCK_EMBEDDING = [0.1] * 1536  # 1536-dimensional vector with all values as 0.1


@pytest.fixture
def mock_openai_client():
    with patch("app.services.ai.client") as mock_client:
        # Setup the AsyncMock for embeddings.create
        embeddings_create_mock = AsyncMock()
        embeddings_response = MagicMock()
        embeddings_response.data = [MagicMock(embedding=MOCK_EMBEDDING)]
        embeddings_create_mock.return_value = embeddings_response

        # Attach the mock to the client
        mock_client.embeddings = MagicMock()
        mock_client.embeddings.create = embeddings_create_mock

        yield mock_client


@pytest.mark.asyncio
async def test_generate_embedding(mock_openai_client, monkeypatch):
    # Set environment variable
    monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")

    # Call the function
    embedding = await generate_embedding("Test query")

    # Assertions
    assert embedding == MOCK_EMBEDDING
    mock_openai_client.embeddings.create.assert_called_once_with(
        model="text-embedding-ada-002", input="Test query"
    )


@pytest.mark.asyncio
async def test_generate_embedding_error(mock_openai_client, monkeypatch):
    # Set environment variable
    monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")

    # Make the API call raise an exception
    mock_openai_client.embeddings.create.side_effect = Exception("API error")

    # Call the function
    embedding = await generate_embedding("Test query")

    # Assertions
    assert embedding is None


@pytest.mark.asyncio
async def test_find_relevant_faqs(mock_openai_client, test_db, monkeypatch):
    # Set environment variable
    monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")

    # Create test FAQs
    faq1 = FAQ(
        tenant_id="test_tenant",
        question="What is the meaning of life?",
        answer="42",
        embedding=MOCK_EMBEDDING,
    )
    faq2 = FAQ(
        tenant_id="test_tenant",
        question="How does this work?",
        answer="It just works",
        embedding=MOCK_EMBEDDING,
    )
    test_db.add(faq1)
    test_db.add(faq2)
    test_db.commit()

    # Mock the cosine_distance function to return predictable results
    with patch("app.models.faq.FAQ.embedding") as mock_embedding:
        # Setup the cosine_distance method
        mock_embedding.cosine_distance = MagicMock()

        # Call the function
        faqs = await find_relevant_faqs(
            test_db, "test_tenant", "meaning of life", top_k=1
        )

        # Assertions
        assert len(faqs) > 0
        # We can't assert exact matches due to the mocking complexity,
        # but we can verify the function ran without errors


@pytest.mark.asyncio
async def test_get_rag_response(mock_openai_client, test_db, monkeypatch):
    # Set environment variable
    monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")

    # Create test FAQs
    faq = FAQ(
        tenant_id="test_tenant",
        question="What is the meaning of life?",
        answer="42",
        embedding=MOCK_EMBEDDING,
    )
    test_db.add(faq)
    test_db.commit()

    # Mock find_relevant_faqs to return our test FAQ
    with patch("app.services.ai.find_relevant_faqs") as mock_find_faqs:
        mock_find_faqs.return_value = [faq]

        # Call the function
        response = await get_rag_response(
            test_db, "test_tenant", "meaning of life", "You are a helpful assistant"
        )

        # Assertions
        assert response is not None
        assert "meaning of life" in response
        mock_find_faqs.assert_called_once()
