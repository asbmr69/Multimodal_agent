import pytest
from unittest.mock import patch
from app.agents.agent_utils.search_ops import grep_search

def test_grep_search_success():
    """Test grep_search function for successful search."""
    mock_matches = [
        {"file": "file1.py", "line": 10, "content": "match1"},
        {"file": "file2.py", "line": 20, "content": "match2"}
    ]
    with patch("app.agents.agent_utils.search_ops.grep_search", return_value=(True, mock_matches)) as mock_search:
        success, matches = grep_search("query")
        assert success is True
        assert matches == mock_matches
        mock_search.assert_called_once_with("query")

def test_grep_search_failure():
    """Test grep_search function for failure."""
    with patch("app.agents.agent_utils.search_ops.grep_search", return_value=(False, [])) as mock_search:
        success, matches = grep_search("query")
        assert success is False
        assert matches == []
        mock_search.assert_called_once_with("query")
