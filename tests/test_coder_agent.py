import os
import sys

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from app.agents.coder.coder_agent import format_history_summary, MainDecisionAgent
from app.agents.agent_utils.read_file import read_file
from unittest.mock import patch, MagicMock

# Test format_history_summary
def test_format_history_summary_empty():
    """Test format_history_summary with empty history."""
    history = []
    result = format_history_summary(history)
    assert result == "No previous actions."

def test_format_history_summary_with_actions():
    """Test format_history_summary with a populated history."""
    history = [
        {
            "tool": "read_file",
            "reason": "Read the main.py file",
            "params": {"target_file": "main.py"},
            "result": {"success": True, "content": "print('Hello World')"}
        },
        {
            "tool": "grep_search",
            "reason": "Search for 'logger' in Python files",
            "params": {"query": "logger"},
            "result": {"success": True, "matches": [{"file": "main.py", "line": 10, "content": "logger.info('Test')"}]}
        }
    ]
    result = format_history_summary(history)
    assert "Action 1:" in result
    assert "- Tool: read_file" in result
    assert "- Content: print('Hello World')" in result
    assert "Action 2:" in result
    assert "- Tool: grep_search" in result
    assert "- Matches: 1" in result

# Test MainDecisionAgent
@patch("app.agents.coder.coder_agent.call_llm")
def test_main_decision_agent_exec(mock_call_llm):
    """Test the exec method of MainDecisionAgent."""
    mock_call_llm.return_value = """tool: read_file
reason: I need to read the main.py file
params:
  target_file: main.py"""

    agent = MainDecisionAgent()
    user_query = "Read the main.py file"
    history = []
    inputs = (user_query, history)

    result = agent.exec(inputs)

    assert result["tool"] == "read_file"
    assert result["reason"] == "I need to read the main.py file"
    assert result["params"]["target_file"] == "main.py"

# Add more test cases for other methods and nodes here
