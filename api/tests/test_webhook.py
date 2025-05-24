"""Test webhook module."""

from unittest.mock import patch

from app.api.endpoints.webhook import process_webhook


@patch("app.api.endpoints.webhook.logger")
def test_process_webhook_success(mock_logger):
    """Test successful webhook processing."""
    # Mock request data
    request_data = {
        "event": "faq_created",
        "tenant_id": "test_tenant",
        "data": {"question": "Test question?", "answer": "Test answer."},
    }

    # Call the function
    result = process_webhook(request_data)

    # Assertions
    assert result["status"] == "success"
    assert "processed" in result["message"]
    mock_logger.info.assert_called_once()


@patch("app.api.endpoints.webhook.logger")
def test_process_webhook_missing_fields(mock_logger):
    """Test webhook processing with missing fields."""
    # Mock request data with missing fields
    request_data = {
        "event": "faq_created",
        # Missing tenant_id
        "data": {"question": "Test question?", "answer": "Test answer."},
    }

    # Call the function
    result = process_webhook(request_data)

    # Assertions
    assert result["status"] == "error"
    assert "missing" in result["message"].lower()
    mock_logger.error.assert_called_once()


@patch("app.api.endpoints.webhook.logger")
def test_process_webhook_exception(mock_logger):
    """Test webhook processing with exception."""
    # Mock request data
    request_data = {
        "event": "faq_created",
        "tenant_id": "test_tenant",
        "data": {"question": "Test question?", "answer": "Test answer."},
    }

    # Make the function raise an exception
    with patch(
        "app.api.endpoints.webhook.process_webhook_event",
        side_effect=Exception("Test exception"),
    ):
        # Call the function
        result = process_webhook(request_data)

        # Assertions
        assert result["status"] == "error"
        assert "exception" in result["message"].lower()
        mock_logger.error.assert_called_once()
