import os
import pytest
from unittest.mock import patch
from fastapi import HTTPException

def test_verify_webhook_success(client, monkeypatch):
    # Set environment variable
    monkeypatch.setenv("WH_TOKEN", "test_token")
    
    # Test successful verification
    response = client.get(
        "/webhook?hub_mode=subscribe&hub_verify_token=test_token&hub_challenge=1234"
    )
    assert response.status_code == 200
    assert response.json() == 1234

def test_verify_webhook_failure_wrong_token(client, monkeypatch):
    # Set environment variable
    monkeypatch.setenv("WH_TOKEN", "test_token")
    
    # Test with wrong token
    response = client.get(
        "/webhook?hub_mode=subscribe&hub_verify_token=wrong_token&hub_challenge=1234"
    )
    assert response.status_code == 403
    assert "Verification failed" in response.text

def test_verify_webhook_failure_wrong_mode(client, monkeypatch):
    # Set environment variable
    monkeypatch.setenv("WH_TOKEN", "test_token")
    
    # Test with wrong mode
    response = client.get(
        "/webhook?hub_mode=wrong_mode&hub_verify_token=test_token&hub_challenge=1234"
    )
    assert response.status_code == 403
    assert "Verification failed" in response.text

def test_webhook_handler_success(client):
    # Test successful webhook handling
    response = client.post("/webhook", json={"message": "test"})
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("app.api.endpoints.webhook.logger")
def test_webhook_handler_logs_request(mock_logger, client):
    # Test that logger.info is called
    client.post("/webhook", json={"message": "test"})
    mock_logger.info.assert_called_once_with("Received webhook request")

@patch("app.api.endpoints.webhook.logger")
def test_webhook_handler_exception(mock_logger, client):
    # Create a test exception
    def side_effect(*args, **kwargs):
        raise Exception("Test exception")
    
    # Apply the side effect to the logger.info method
    mock_logger.info.side_effect = side_effect
    
    # Test exception handling
    response = client.post("/webhook", json={"message": "test"})
    assert response.status_code == 200
    assert response.json() == {"status": "error", "message": "Test exception"}
    mock_logger.error.assert_called_once()
