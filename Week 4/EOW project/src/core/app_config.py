from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from .db_config import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Stratup:
    print("🚀 Starting application...")
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")

    yield  # Application runs here

    # Shutdown:
    print("👋 Shutting down application...")
