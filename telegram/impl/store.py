import logging
import httpx
from aiogram import types

API_URL = "http://localhost:8000/store"

async def handle_store(message: types.Message):
    """
    Handler for the /store command.
    This function builds a store request payload based on the Telegram user's message,
    calls the API endpoint /store, and replies with the inserted count.
    """

    payload = {
        "items": [
            {
                "user_id": message.from_user.id,
                "values": [123, 456],
                "description": "Record from Telegram command"
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            inserted_count = data.get("inserted_count", "unknown")
            reply_text = f"Store command executed successfully. Inserted count: {inserted_count}."
    except Exception as e:
        logging.exception("Error calling store API")
        reply_text = f"Failed to store record: {e}"

    await message.reply(reply_text)
