from aiogram import Bot, Dispatcher
import asyncio
import os

from handlers import main_router

from database.base import DataBase

bot_app = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(main_router)


def on_start():
    print('Bot is started...')


def on_shutdown():
    print('Bot is down...')


async def start_bot():
    db = DataBase()
    db.create_main_table()
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot_app)


if __name__ == '__main__':
    asyncio.run(start_bot())
