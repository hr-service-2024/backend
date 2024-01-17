import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from config import TOKEN
from core.handlers.basic import get_start

# 6480850917:AAFOoGKlcttkj97NSCgH5NM4drlaMUm4d2Y
async def start_bot():
    print('[INFO] Бот запущен')


async def stop_bot():
    print('[INFO] Бот остановлен')


async def start():
    bot = Bot(token=TOKEN)

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start, Command(commands=['start', 'run']))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
