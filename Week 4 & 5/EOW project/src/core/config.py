from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI

from src.core.database import Base, engine

INVENTORY_CSV_FILEPATH = str(
    (Path(__file__).parent.parent.parent / "data" / "new_inventory.csv")
)


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
