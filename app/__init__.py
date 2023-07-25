from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import config

bot: Bot = Bot(token=config.BOT_TOKEN.get_secret_value())
dp: Dispatcher = Dispatcher(storage=MemoryStorage())