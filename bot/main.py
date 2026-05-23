from bot.handlers import commands

from aiogram import Dispatcher


def setup_handlers(dp: Dispatcher):
    dp.include_router(commands.router)
