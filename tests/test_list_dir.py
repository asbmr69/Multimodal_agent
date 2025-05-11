import pytest
from unittest.mock import patch
from app.agents.agent_utils.dir_ops import list_dir

def test_list_dir_success():
    """Test list_dir function for successful directory listing."""
    mock_tree = "mocked tree structure"
    with patch("app.agents.agent_utils.dir_ops.list_dir", return_value=(True, mock_tree)) as mock_list:
        success, tree = list_dir("dummy_path")
        assert success is True
        assert tree == mock_tree
        mock_list.assert_called_once_with("dummy_path")

def test_list_dir_failure():
    """Test list_dir function for failure."""
    with patch("app.agents.agent_utils.dir_ops.list_dir", return_value=(False, "")) as mock_list:
        success, tree = list_dir("dummy_path")
        assert success is False
        assert tree == ""
        mock_list.assert_called_once_with("dummy_path")
