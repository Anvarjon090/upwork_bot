from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", 30))


def _build_database_url() -> str | None:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", "5432")

    if all([db_name, db_user, db_password, db_host]):
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    return None


DATABASE_URL = _build_database_url()

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

RSS_SOURCES = [
    ("https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss", "WeWorkRemotely"),
    ("https://www.freelancer.com/rss/jobs/python.xml", "Freelancer"),
    ("https://jobicy.com/?feed=job_feed&job_categories=engineer&job_tags=python", "Jobicy"),
]
