"""Test main module."""

# Removed unused import: pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Lumi API"
    # Line shortened to comply with line length limit
    assert "version" in response.json()
