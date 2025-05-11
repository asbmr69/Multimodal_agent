import pytest
from unittest.mock import patch, mock_open
from app.agents.agent_utils.read_file import read_file

def test_read_file_success():
    """Test read_file function for successful file read."""
    mock_content = "File content"
    with patch("builtins.open", mock_open(read_data=mock_content)) as mock_file:
        content, success = read_file("dummy.txt")
        assert success is True
        assert content == mock_content
        mock_file.assert_called_once_with("dummy.txt", "r")

def test_read_file_failure():
    """Test read_file function for file not found."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        content, success = read_file("nonexistent.txt")
        assert success is False
        assert content == ""
