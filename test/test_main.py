import os
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app, send_to_discord, TelexMessagePayload

client = TestClient(app)

@pytest.fixture
def telex_payload():
    return {
        "channel_id": "12345",
        "return_url": "https://example.com/return",
        "settings": [
            {"label": "Webhook URL", "type": "text", "required": True, "default": ""},
            {"label": "Enable Logging", "type": "checkbox", "required": False, "default": "Yes"},
            {"label": "Retry Attempts", "type": "number", "required": True, "default": "3"},
            {"label": "Alert Level", "type": "dropdown", "required": True, "default": "Normal", "options": ["High", "Normal", "Low"]},
            {"label": "Notify Roles", "type": "multi-checkbox", "required": False, "default": "Admin", "options": ["Admin", "Moderator", "User"]}
        ],
        "content": "Test message content"
    }

@pytest.mark.asyncio
async def test_send_to_discord(monkeypatch):
    async def mock_post(url, json, headers):
        class MockResponse:
            status_code = 200
        return MockResponse()

    monkeypatch.setattr(AsyncClient, "post", mock_post)
    response_status = await send_to_discord("Test message")
    assert response_status == 200

def test_receive_telex_message(telex_payload):
    response = client.post("/telex-webhook", json=telex_payload)
    assert response.status_code == 202
    assert response.json() == {"status": "success"}

def test_get_integration_json():
    response = client.get("/integration.json")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["descriptions"]["app_name"] == "Telex to Discord"