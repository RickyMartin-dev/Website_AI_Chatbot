# import pytest
# from fastapi.testclient import TestClient
# import sys
# # caution: path[0] is reserved for script path (or '' in REPL)
# sys.path.insert(1, '/src')
# from src.main import app, API_KEY

# client = TestClient(app)

# def test_chat_endpoint_success():
#     payload = {
#         "input": "Hello there!",
#         "session_id": "test123"
#     }

#     headers = {
#         "x-api-key": API_KEY,
#         "Origin": "https://rickymartin-dev.github.io"
#     }

#     response = client.post("/chat", json=payload, headers=headers)
#     assert response.status_code == 200
#     data = response.json()
#     assert "message" in data
#     assert isinstance(data["message"], str)

# def test_chat_endpoint_missing_api_key():
#     payload = {
#         "input": "This should fail.",
#         "session_id": "test123"
#     }

#     response = client.post("/chat", json=payload)
#     assert response.status_code == 422 or response.status_code == 403

from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch

client = TestClient(app)

@patch("src.bedrock.get_bedrock_response", return_value="Hello from mock!")
def test_chat_endpoint_success(mock_bedrock):
    payload = {"input": "Hello", "session_id": "test123"}
    headers = {"x-api-key": "for_now_this_is_for_testing"}
    response = client.post("/chat", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Hello from mock!"
