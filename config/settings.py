from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", 30))
DATABASE_URL = os.getenv("DATABASE_URL")

SKILLS = [
    "python",
    "django",
    "fastapi",
    "postgresql",
    "mongodb",
    "rest api",
    "sqlalchemy",
    "websocket",
    "backend",
    "flask",
    "redis",
    "celery",
    "docker",
]

UPWORK_RSS_URLS = [
    "https://www.upwork.com/ab/feed/jobs/rss?q=python+django+fastapi&sort=recency&paging=0%3B10",
    "https://www.upwork.com/ab/feed/jobs/rss?q=python+backend+developer&sort=recency&paging=0%3B10",
    "https://www.upwork.com/ab/feed/jobs/rss?q=fastapi+postgresql&sort=recency&paging=0%3B10",
    "https://www.upwork.com/ab/feed/jobs/rss?q=django+rest+api&sort=recency&paging=0%3B10",
]
