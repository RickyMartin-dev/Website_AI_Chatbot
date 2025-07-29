# import pytest
# import sys
# sys.path.insert(1, '/src')
# from src.main import ChatAgent

# def test_basic_chat_response():
#     agent = ChatAgent(system_prompt="You are a test bot.")
#     result = agent.chat(user_input="Hello", session_id="test-session")
    
#     assert isinstance(result, dict)
#     assert "output" in result
#     assert isinstance(result["output"], str)
#     assert len(result["output"]) > 0

import pytest
from unittest.mock import patch
from src.main import agent

@patch("src.main.get_bedrock_response", return_value="Mocked reply")
def test_basic_chat_response(mock_bedrock):
    response = agent.chat(user_input="Hello!", session_id="test123")
    assert "Mocked" in response["output"]