from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.core.database import Base, engine
from src.core.log import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Stratup:
    setup_logging()
    logger.info("🚀 Starting application...")
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database initialized successfully")

    # For seeding: run after alembic migration or first app start up
    # from src.core.database import seed_db
    #
    # seed_db()

    yield  # Application runs here

    # Shutdown:
    logger.info("👋 Shutprintting down application...")
