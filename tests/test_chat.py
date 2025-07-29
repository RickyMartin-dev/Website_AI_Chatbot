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
from fastapi.testclient import TestClient
from src.main import app, agent

client = TestClient(app)

# ✅ Test the agent logic directly
@patch("src.bedrock.get_bedrock_response", return_value="Mocked reply")
def test_basic_chat_response(mock_bedrock):
    response = agent.chat(user_input="Hello!", session_id="unit-test-123")
    assert response["output"] == "Mocked reply"

# ✅ Test FastAPI endpoint with a valid request
@patch("src.bedrock.get_bedrock_response", return_value="Hi there!")
def test_chat_endpoint_success(mock_bedrock):
    payload = {
        "input": "Hi!",
        "session_id": "unit-test-456"
    }
    headers = {
        "x-api-key": "for_now_this_is_for_testing",  # Must match your env/API_KEY
        "origin": "https://rickymartin-dev.github.io"             # Must be in ALLOWED_ORIGINS
    }
    response = client.post("/chat", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Hi there!"