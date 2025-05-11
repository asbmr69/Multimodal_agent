import pytest
from unittest.mock import patch, mock_open
from app.agents.agent_utils.replace_file import replace_file

def test_replace_file_success():
    """Test replace_file function for successful replacement."""
    mock_content = "New content"
    with patch("builtins.open", mock_open()) as mock_file:
        success, message = replace_file("dummy.txt", mock_content)
        assert success is True
        assert message == "File replaced successfully."
        mock_file.assert_called_once_with("dummy.txt", "w")
        mock_file().write.assert_called_once_with(mock_content)

def test_replace_file_failure():
    """Test replace_file function for failure."""
    with patch("builtins.open", side_effect=PermissionError):
        success, message = replace_file("dummy.txt", "New content")
        assert success is False
        assert message == "Failed to replace file."
