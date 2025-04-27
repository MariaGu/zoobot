import sys
import asyncio

if sys.platform == "win32":
    # переключаем политику на селекторный цикл
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from utils.logger import setup_logger
from bot.router import router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в файле .env")
logger = setup_logger("zoobot")

async def main():
    # Инициализируем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp  = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    try:
        logger.info("Запуск ZooBot.")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("ZooBot остановлен")

if __name__ == "__main__":
    asyncio.run(main())