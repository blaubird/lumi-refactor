import pytest
from fastapi.testclient import TestClient
from main import app

def test_root_endpoint():
    """Test the root endpoint returns a successful response"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "LuminiteQ API is running"}

def test_health_check():
    """Test the health check endpoint returns a healthy status"""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
