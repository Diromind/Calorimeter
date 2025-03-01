import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from utils import fetch_lockbox_secret as utils
from utils import get_config

from telegram.impl.store import handle_store

config = get_config.get_config_value("telegram")
API_TOKEN = utils.fetch_secret("token_secret_id")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Register the /store command handler.
dp.message.register(handle_store, Command("store"))

async def on_start():
    logging.info("Starting Telegram bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(on_start())
