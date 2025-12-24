from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from src.core.database import engine
from src.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    print("Starting application")
    Base.metadata.create_all(bind=engine)

    yield

    print("Shutting down application")
