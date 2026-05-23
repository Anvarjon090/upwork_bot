import html

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from config.settings import SKILLS
from scheduler.checker import check_jobs

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 <b>Upwork Job Bot ishga tushdi!</b>\n\n"
        "Men har 30 daqiqada Upwork'dagi yangi ishlarni tekshiraman "
        "va sizning skilllaringizga mos kelganlarini yuboraman.\n\n"
        "📌 Buyruqlar:\n"
        "/skills — kuzatilayotgan skilllar ro'yxati\n"
        "/check — hozir tekshirishni boshlash\n"
        "/status — bot holati",
        parse_mode="HTML",
    )


@router.message(Command("skills"))
async def cmd_skills(message: Message):
    skills_text = "\n".join(f"• <code>{html.escape(skill)}</code>" for skill in SKILLS)
    await message.answer(
        f"🏷 <b>Kuzatilayotgan skilllar:</b>\n\n{skills_text}",
        parse_mode="HTML",
    )


@router.message(Command("status"))
async def cmd_status(message: Message):
    await message.answer(
        "✅ <b>Bot faol</b>\n\n"
        "Har 30 daqiqada Upwork RSS tekshirilmoqda.\n"
        "Yangi mos ish topilsa darhol xabar keladi.",
        parse_mode="HTML",
    )


@router.message(Command("check"))
async def cmd_check(message: Message, bot: Bot):
    await message.answer("🔍 Tekshirish boshlandi...")
    await check_jobs(bot)
    await message.answer("✅ Tekshirish tugadi!")
