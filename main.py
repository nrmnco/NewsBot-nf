import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand

from app import bot, dp
from app.routers import (
    main_router,
    fakenews_router
)

logging.basicConfig(level=logging.INFO)


async def setup_bot_commands():
    bot_commands = [
        BotCommand(command="/start", description="Start"),
        BotCommand(command="/check_news", description="Check news for authenticity"),
    ]
    await bot.set_my_commands(bot_commands)


async def start_bot(bot: Bot):
    await bot.send_message(529158582, 'BOT STARTED')
    await setup_bot_commands()



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    dp.startup.register(start_bot)
    dp.include_router(main_router.router)
    dp.include_router(fakenews_router.router)
    asyncio.get_event_loop().run_until_complete(main())
