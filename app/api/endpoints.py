from fastapi import APIRouter, BackgroundTasks, Request
from app.models import TelexMessagePayload
from app.utils.discord import process_telex_message

router = APIRouter()

@router.post("/telex-webhook", status_code=204)
def receive_telex_message(payload: TelexMessagePayload, background_tasks: BackgroundTasks):
    """Receive a message from Telex and forward it to Discord in the background."""
    background_tasks.add_task(process_telex_message, payload)
    return {"status": "success"}

@router.get("/integration.json")
def get_integration_json(request: Request):
    base_url = str(request.base_url).rstrip("/")
    integration_json = {
        "data": {
            "date": {"created_at": "2025-02-19", "updated_at": "2025-02-23"},
            "descriptions": {
                "app_name": "Telex to Discord",
                "app_description": "Routes Telex messages to a Discord channel using Discord Webhooks.",
                "app_logo": "/img/image.png",
                "app_url": base_url,
                "background_color": "#006400",
            },
            "integration_category": "Communication & Collaboration",
            "integration_type": "output",
            "is_active": True,
            "key_features": [
                "Forwards messages from Telex to Discord.",
                "Uses Discord Webhooks for message delivery.",
                "No need for scheduled tasks.",
                "Works asynchronously for efficiency."
            ],
            "author": "Baydre",
            "settings": [
                {"label": "Webhook URL", "type": "text", "required": True, "default": ""},
                {"label": "Enable Logging", "type": "checkbox", "required": False, "default": "Yes"},
                {"label": "Retry Attempts", "type": "number", "required": True, "default": "3"},
                {"label": "Alert Level", "type": "dropdown", "required": True, "default": "Normal", "options": ["High", "Normal", "Low"]},
                {"label": "Notify Roles", "type": "multi-checkbox", "required": False, "default": "Admin", "options": ["Admin", "Moderator", "User"]}
            ],
            "tick_url": "null",
            "target_url": f"{base_url}/telex-webhook",

            "endpoints": [
                {
                "function": "forward_to_discord",
                "url": "/webhook",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "payload": {"message": "{{message}}"}
                }
            ]
        }
    }
    return integration_json