import html

from aiogram import Bot
from aiogram.enums import ParseMode
from scraper.upwork_rss import fetch_all_jobs
from scraper.filter import is_matching
from database.db import is_job_sent, save_job
from config.settings import RSS_SOURCES, CHAT_ID


def format_message(job, matched_skills: list[str]) -> str:
    skills_text = ", ".join(f"<code>{html.escape(s)}</code>" for s in matched_skills)
    title = html.escape(job.title)
    budget = html.escape(job.budget)
    published = html.escape(job.published)
    description = html.escape(job.description[:300])
    link = html.escape(job.link, quote=True)
    return (
        f"🆕 <b>Yangi ish topildi!</b>\n\n"
        f"💼 <b>{title}</b>\n"
        f"💰 Budjet: {budget}\n"
        f"🕐 {published}\n\n"
        f"📝 {description}...\n\n"
        f"🏷 Tegishli: {skills_text}\n\n"
        f'🔗 <a href="{link}">Ishga o\'tish</a>'
    )


async def check_jobs(bot: Bot):
    seen_ids = set()
    jobs = await fetch_all_jobs(RSS_SOURCES)

    for job in jobs:
            if job.id in seen_ids:
                continue
            seen_ids.add(job.id)

            if await is_job_sent(job.id):
                continue

            matched, skills = is_matching(job)
            if not matched:
                continue

            message = format_message(job, skills)
            await bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
            await save_job(job.id, job.title)
