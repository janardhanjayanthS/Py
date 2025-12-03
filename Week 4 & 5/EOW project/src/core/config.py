from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Stratup:
    print("🚀 Starting application...")
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")

    # For seeding: run after alembic migration or first app start up
    # from src.core.database import seed_db
    # seed_db()

    yield  # Application runs here

    # Shutdown:
    print("👋 Shutting down application...")
