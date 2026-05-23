import asyncpg
from config.settings import DATABASE_URL

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL)
    return _pool


async def init_db():
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS sent_jobs (
                id SERIAL PRIMARY KEY,
                job_id TEXT UNIQUE NOT NULL,
                title TEXT,
                sent_at TIMESTAMP DEFAULT NOW()
            )
        """)


async def is_job_sent(job_id: str) -> bool:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id FROM sent_jobs WHERE job_id = $1", job_id
        )
        return row is not None


async def save_job(job_id: str, title: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO sent_jobs (job_id, title) VALUES ($1, $2) ON CONFLICT DO NOTHING",
            job_id, title,
        )
