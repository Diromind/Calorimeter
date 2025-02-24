import logging
import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram.filters import Command

from impl.save import check_in
from impl.get import results
from impl.delete import delete
from impl.help import help_handler
from impl.save_shortcuts import today_handler, yesterday_handler
from impl.graph import send_graph

load_dotenv()
API_TOKEN = os.getenv("TG_API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../common.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


# Define the command handler for /start
async def send_welcome(message: types.Message):
    await message.reply("Hi! I am your Telegram bot. How can I assist you?")

# Register the handlers with filters
dp.message.register(send_welcome, Command('start'))
dp.message.register(check_in, Command('check_in'))
dp.message.register(check_in, Command('save'))
dp.message.register(results, Command('results'))
dp.message.register(delete, Command('delete'))
dp.message.register(help_handler, Command('help'))
dp.message.register(today_handler, Command('today'))
dp.message.register(yesterday_handler, Command('yesterday'))
dp.message.register(send_graph, Command('graph'))

# Start the bot's polling mechanism
async def on_start():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_start())
