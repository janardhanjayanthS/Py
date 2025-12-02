from contextlib import asynccontextmanager
from os import getenv
from typing import AsyncGenerator

from fastapi import FastAPI

from src.core.database import Base, engine

TESTING = getenv("TESTING")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Stratup:
    print("🚀 Starting application...")
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")

    # data seeding: use once when app is created
    if TESTING != "1":
        pass
        # seed_db()

    yield  # Application runs here

    # Shutdown:
    print("👋 Shutting down application...")
