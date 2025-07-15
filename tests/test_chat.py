import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_chat_unauthorized():
    response = client.post("/chat", json={"message": "Hello", "session_id": "test"})
    assert response.status_code == 422  # missing API key header

def test_chat_missing_fields():
    response = client.post("/chat", headers={"x-api-key": "wrong"}, json={})
    assert response.status_code in [400, 401]