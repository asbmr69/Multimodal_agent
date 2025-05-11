import pytest
import os
from unittest.mock import patch
from app.agents.agent_utils.delete_file import delete_file

def test_delete_file_success():
    """Test delete_file function for successful deletion."""
    with patch("os.remove") as mock_remove:
        success, message = delete_file("dummy.txt")
        assert success is True
        assert message == "File deleted successfully."
        mock_remove.assert_called_once_with("dummy.txt")

def test_delete_file_failure():
    """Test delete_file function for file not found."""
    with patch("os.remove", side_effect=FileNotFoundError):
        success, message = delete_file("nonexistent.txt")
        assert success is False
        assert message == "File not found."
