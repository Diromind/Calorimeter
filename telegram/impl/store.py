import logging
import aiohttp
from aiogram import types

API_URL = "http://localhost:8000/store"


async def handle_store(message: types.Message):
    """
    Handler for the /store command.
    Constructs a store request payload based on the Telegram user's message,
    sends it to the API using aiohttp, and replies with the result.
    """
    payload = {
        "user_id": message.from_user.id,
        "items": [
            {
                "value": 123,
                "description": "Record from Telegram command"
            },
            {
                "value": 456,
                "description": "Dummy msg"
            }
        ]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=payload) as response:
                # Raise an exception for non-2xx responses.
                response.raise_for_status()
                data = await response.json()
                # Expecting API response to include an "inserted_count" field.
                inserted_count = data.get("inserted_count", "unknown")
                reply_text = f"Store command executed successfully. Inserted count: {inserted_count}."
    except Exception as e:
        logging.exception("Error calling store API")
        reply_text = f"Failed to store record: {e}"

    await message.reply(reply_text)
