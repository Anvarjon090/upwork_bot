from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config.settings import SKILLS

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 *Upwork Job Bot ishga tushdi!*\n\n"
        "Men har 30 daqiqada Upwork'dagi yangi ishlarni tekshiraman "
        "va sizning skilllaringizga mos kelganlarini yuboraman.\n\n"
        "📌 Buyruqlar:\n"
        "/skills — kuzatilayotgan skilllar ro'yxati\n"
        "/check — hozir tekshirishni boshlash\n"
        "/status — bot holati",
        parse_mode="Markdown",
    )


@router.message(Command("skills"))
async def cmd_skills(message: Message):
    skills_text = "\n".join(f"• `{skill}`" for skill in SKILLS)
    await message.answer(
        f"🏷 *Kuzatilayotgan skilllar:*\n\n{skills_text}",
        parse_mode="Markdown",
    )


@router.message(Command("status"))
async def cmd_status(message: Message):
    await message.answer(
        "✅ *Bot faol*\n\n"
        "Har 30 daqiqada Upwork RSS tekshirilmoqda.\n"
        "Yangi mos ish topilsa darhol xabar keladi.",
        parse_mode="Markdown",
    )
