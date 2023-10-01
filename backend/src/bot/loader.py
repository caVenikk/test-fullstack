from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.config import Config

config = Config.load()
memory_storage = MemoryStorage()
bot = Bot(token=config.telegram.bot_token, parse_mode="HTML")
dp = Dispatcher(storage=memory_storage)
