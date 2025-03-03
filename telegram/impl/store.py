import logging
import aiohttp
from aiogram import types

API_URL = "http://localhost:8000/store"


def parse_store_command(message: types.Message) -> (int, str):
    """
    Parse the store command text.
    Expects one integer and optionally a description.
    Order doesn't matter. Returns (measurement, description).
    Raises ValueError if no integer is found.
    """
    tokens = message.text.split()[1:]
    if len(tokens) > 2:
        raise ValueError("Provide no more than 2 arguments")
    if len(tokens) == 0:
        raise ValueError("Provide at least one argument")

    value = None
    description = None

    for token in tokens:
        try:
            value = int(token)
        except ValueError:
            description = token

    if value is None:
        raise ValueError("No integer value found in the command.")
    if description is None and len(tokens) > 1:
        raise ValueError(f"Can't parse this sequence: {tokens}")

    return value, description

async def handle_store(message: types.Message):
    """
    Handler for the /store command.
    Constructs a store request payload based on the Telegram user's message,
    sends it to the API using aiohttp, and replies with the result.
    """

    try:
        value, desc = parse_store_command(message)
    except ValueError as e:
        await message.reply(f"Error parsing command: {e}")
        return

    payload = {
        "user_id": message.from_user.id,
        "items": [
            {
                "value": value,
                "description": desc
            }
        ]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=payload) as response:
                response.raise_for_status()  # Raise an exception for non-2xx responses.
                data = await response.json()
                inserted_count = len(data.get("uuids", []))
                reply_text = f"Store command executed successfully. Inserted count: {inserted_count}."
    except Exception as e:
        logging.exception("Error calling store API")
        reply_text = f"Failed to store record: {e}"

    await message.reply(reply_text)
