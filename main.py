from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import httpx, os, json
from dotenv import load_dotenv

load_dotenv()

# Define Pydantic models
class Setting(BaseModel):
    label: str
    type: str
    required: bool
    default: str

class TelexMessagePayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]
    content: str

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Get environment variable (Render automatically provides it)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

async def send_to_discord(message: str):
    """Send a message to Discord webhook."""
    discord_payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(DISCORD_WEBHOOK_URL, json=discord_payload, headers=headers)
        return response.status_code

async def process_telex_message(payload: TelexMessagePayload):
    """Background task to forward Telex messages to Discord."""
    message_content = payload.content if payload.content else "No content received"
    discord_message = f"**New Telex Message:**\n{message_content}"
    await send_to_discord(discord_message)

@app.post("/telex-webhook", status_code=202)
def receive_telex_message(payload: TelexMessagePayload, background_tasks: BackgroundTasks):
    """Receive a message from Telex and forward it to Discord in the background."""
    background_tasks.add_task(process_telex_message, payload)
    return {"status": "success"}

@app.get("/integration.json")
def get_integration_json(request: Request):
    base_url = str(request.base_url).rstrip("/")
    integration_json = {
        "data": {
            "date": {"created_at": "2025-02-19", "updated_at": "2025-02-20"},
            "descriptions": {
                "app_name": "Telex to Discord",
                "app_description": "Routes Telex messages to a Discord channel using Discord Webhooks.",
                "app_logo": f"{base_url}/img/coming-soon.png",
                "app_url": base_url,
                "background_color": "#fff",
            },
            "integration_category": "Communication & Collaboration",
            "integration_type": "output",
            "is_active": True,
            "output": [
                {"label": "discord_channel_1", "value": True},
                {"label": "discord_channel_2", "value": False}
            ],
            "key_features": [
                "Forwards messages from Telex to Discord.",
                "Uses Discord Webhooks for message delivery.",
                "No need for scheduled tasks.",
                "Works asynchronously for efficiency."
            ],
            "author": "Baydre",
            "permissions": {
                "monitoring_user": {
                    "always_online": True,
                    "display_name": "Telex Monitor"
                }
            },
            "settings": [
                {"label": "Webhook URL", "type": "text", "required": True, "default": ""},
                {"label": "Enable Logging", "type": "checkbox", "required": False, "default": "Yes"},
                {"label": "Retry Attempts", "type": "number", "required": True, "default": "3"},
                {"label": "Alert Level", "type": "dropdown", "required": True, "default": "Normal", "options": ["High", "Normal", "Low"]},
                {"label": "Notify Roles", "type": "multi-checkbox", "required": False, "default": "Admin", "options": ["Admin", "Moderator", "User"]}
            ],
            "tick_url": f"{base_url}/tick",
            "target_url": f"{base_url}/telex-webhook"
        }
    }
    return integration_json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)