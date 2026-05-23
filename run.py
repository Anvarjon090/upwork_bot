import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.db import init_db
from bot.main import setup_handlers
from scheduler.checker import check_jobs
from config.settings import BOT_TOKEN, CHECK_INTERVAL_MINUTES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await init_db()
    setup_handlers(dp)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_jobs,
        trigger="interval",
        minutes=CHECK_INTERVAL_MINUTES,
        args=[bot],
        id="upwork_checker",
    )
    scheduler.start()
    logger.info(f"Scheduler ishga tushdi. Har {CHECK_INTERVAL_MINUTES} daqiqada tekshiriladi.")

    logger.info("Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
