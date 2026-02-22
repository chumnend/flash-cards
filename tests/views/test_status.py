
import pytest
import datetime
from unittest.mock import patch

from flashly.views.status import status_check


class TestStatusViews:
    """Test cases for status view functions."""

    def test_status_check_success(self, mock_request):
        """Test successful status check."""
        with patch('datetime.datetime') as mock_datetime:
            # Mock the datetime.utcnow() call
            mock_now = datetime.datetime(2023, 1, 1, 12, 0, 0)
            mock_datetime.utcnow.return_value = mock_now
            
            result = status_check(mock_request)
            
            assert result["status"] == "running"
            assert result["message"] == "Backend is healthy"
            assert "timestamp" in result
            assert result["timestamp"].endswith("Z")
