import importlib
import pkgutil
from collections.abc import Iterable

import asyncpg

from config.settings import DATABASE_URL


MIGRATIONS_PACKAGE = "database.migrations"


def _iter_migration_modules() -> Iterable[str]:
    package = importlib.import_module(MIGRATIONS_PACKAGE)
    modules = [
        name
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__)
        if not is_pkg and name.startswith("m")
    ]
    return sorted(modules)


async def apply_migrations(conn: asyncpg.Connection) -> None:
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """
    )

    applied_rows = await conn.fetch("SELECT version FROM schema_migrations")
    applied_versions = {row["version"] for row in applied_rows}

    for module_name in _iter_migration_modules():
        if module_name in applied_versions:
            continue

        migration = importlib.import_module(f"{MIGRATIONS_PACKAGE}.{module_name}")
        upgrade = getattr(migration, "upgrade", None)
        if upgrade is None:
            raise RuntimeError(f"Migration {module_name} has no upgrade() function")

        async with conn.transaction():
            await upgrade(conn)
            await conn.execute(
                "INSERT INTO schema_migrations (version) VALUES ($1)",
                module_name,
            )


async def main() -> None:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await apply_migrations(conn)
    finally:
        await conn.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
