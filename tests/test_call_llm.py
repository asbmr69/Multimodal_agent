import pytest
import os
import json
from unittest.mock import patch, MagicMock
from app.agents.agent_utils.call_llm import call_llm, clear_cache

# Test call_llm function
@patch("app.agents.agent_utils.call_llm.Anthropic")
def test_call_llm_with_cache(mock_anthropic):
    """Test call_llm with caching enabled."""
    mock_client = MagicMock()
    mock_anthropic.return_value = mock_client
    mock_client.messages.create.return_value = MagicMock(content=[MagicMock(text="Mocked response")])

    # Create a temporary cache file
    cache_file = "llm_cache.json"
    if os.path.exists(cache_file):
        os.remove(cache_file)

    prompt = "Test prompt"

    # First call (should hit the API)
    response = call_llm(prompt, use_cache=True)
    assert response == "Mocked response"

    # Second call (should hit the cache)
    response = call_llm(prompt, use_cache=True)
    assert response == "Mocked response"

    # Clean up
    if os.path.exists(cache_file):
        os.remove(cache_file)

@patch("app.agents.agent_utils.call_llm.Anthropic")
def test_call_llm_without_cache(mock_anthropic):
    """Test call_llm with caching disabled."""
    mock_client = MagicMock()
    mock_anthropic.return_value = mock_client
    mock_client.messages.create.return_value = MagicMock(content=[MagicMock(text="Mocked response")])

    prompt = "Test prompt"

    # Call without cache
    response = call_llm(prompt, use_cache=False)
    assert response == "Mocked response"

# Test clear_cache function
def test_clear_cache():
    """Test clear_cache function."""
    cache_file = "llm_cache.json"

    # Create a dummy cache file
    with open(cache_file, "w") as f:
        json.dump({"dummy": "data"}, f)

    assert os.path.exists(cache_file)

    # Clear the cache
    clear_cache()

    assert not os.path.exists(cache_file)
