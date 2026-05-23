import asyncpg

from config.settings import DATABASE_URL
from database.migrate import apply_migrations
from database.models import SentJob

_pool: asyncpg.Pool | None = None


def _require_database_url() -> str:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    return DATABASE_URL


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(_require_database_url())
    return _pool


async def init_db() -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await apply_migrations(conn)


async def is_job_sent(job_id: str) -> bool:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id FROM sent_jobs WHERE job_id = $1",
            job_id,
        )
        return row is not None


async def save_job(job_id: str, title: str) -> SentJob:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO sent_jobs (job_id, title)
            VALUES ($1, $2)
            ON CONFLICT (job_id) DO UPDATE
            SET title = EXCLUDED.title
            RETURNING id, job_id, title, sent_at
            """,
            job_id,
            title,
        )

    return SentJob(
        id=row["id"],
        job_id=row["job_id"],
        title=row["title"],
        sent_at=row["sent_at"],
    )
