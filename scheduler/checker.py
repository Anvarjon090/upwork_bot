from aiogram import Bot
from scraper.upwork_rss import fetch_jobs
from scraper.filter import is_matching
from database.db import is_job_sent, save_job
from config.settings import UPWORK_RSS_URLS, CHAT_ID


def format_message(job, matched_skills: list[str]) -> str:
    skills_text = ", ".join(f"`{s}`" for s in matched_skills)
    return (
        f"🆕 *Yangi ish topildi!*\n\n"
        f"💼 *{job.title}*\n"
        f"💰 Budjet: {job.budget}\n"
        f"🕐 {job.published}\n\n"
        f"📝 {job.description[:300]}...\n\n"
        f"🏷 Tegishli: {skills_text}\n\n"
        f"🔗 [Ishga o'tish]({job.link})"
    )


async def check_jobs(bot: Bot):
    seen_ids = set()

    for rss_url in UPWORK_RSS_URLS:
        jobs = fetch_jobs(rss_url)

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
                parse_mode="Markdown",
                disable_web_page_preview=True,
            )
            await save_job(job.id, job.title)
