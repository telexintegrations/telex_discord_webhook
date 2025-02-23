import httpx, logging
from app.models import TelexMessagePayload
from app.core.config import DISCORD_WEBHOOK_URL

logger = logging.getLogger(__name__)

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
    discord_message = f"**🚨 Alert! New Telex message:**\n{message_content}"

    # Log the message content
    logger.info(f"Received Telex message: {message_content}")

    await send_to_discord(discord_message)