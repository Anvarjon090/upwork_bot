async def upgrade(conn):
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sent_jobs (
            id BIGSERIAL PRIMARY KEY,
            job_id TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """
    )

    await conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_sent_jobs_sent_at
        ON sent_jobs (sent_at DESC)
        """
    )
