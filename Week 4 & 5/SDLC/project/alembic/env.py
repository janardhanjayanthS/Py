import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from src.core.config import settings
from src.models.category import Category  # noqa: F401
from src.models.product import Product  # noqa: F401
from src.models.user import User  # noqa: F401
from src.repository.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the URL from your settings
DATABASE_URL = settings.DATABASE_URL
target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Helper to configure context and run migrations."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an AsyncEngine."""

    # Create the AsyncEngine
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # We use run_sync to bridge the gap between async connection
        # and alembic's synchronous migration logic
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # This is the entry point for the async online migration
    asyncio.run(run_migrations_online())
