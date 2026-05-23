from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from bot.handlers import commands
from scheduler.checker import check_jobs

router = commands.router


async def cmd_check(message: Message, bot: Bot):
    await message.answer("🔍 Tekshirish boshlandi...")
    await check_jobs(bot)
    await message.answer("✅ Tekshirish tugadi!")


def setup_handlers(dp: Dispatcher, bot: Bot):
    dp.include_router(router)
    router.message.register(
        lambda msg: cmd_check(msg, bot),
        Command("check")
    )
