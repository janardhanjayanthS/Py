from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.core.config import settings
from src.core.log import get_logger, log_settings, setup_logging
from src.repository.database import Base, engine

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown lifecycle.

    Args:
        app: FastAPI application instance.

    Yields:
        None: Application runs during this period.
    """
    # Stratup:
    setup_logging()
    logger.info("🚀 Starting application...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("✅ Database initialized successfully")

    # LOGGING .env vars
    logger.info(f"Executing in {settings.environment} environ")
    logger.info(f"Log level at {log_settings.LOG_LEVEL}")
    # For seeding: run after alembic migration or first app start up
    # from src.core.database import seed_db
    #
    # seed_db()

    yield  # Application runs here

    # Shutdown:
    logger.info("👋 Shutprintting down application...")
