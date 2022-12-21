import logging
from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.settings import config

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher(storage=MemoryStorage())
