from contextlib import asynccontextmanager
from enum import Enum
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
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


CURRENT_DIR = Path(__file__).parent
ENV_FILE = CURRENT_DIR / ".env"


class Settings(BaseSettings):
    INVENTORY_CSV_FILEPATH: str = str(
        (Path(__file__).parent.parent.parent / "data" / "new_inventory.csv")
    )

    # POSTGRESQL
    postgresql_pwd: str = Field(validation_alias="POSTGRESQL_PWD")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://postgres:{self.postgresql_pwd}@localhost:5432/inventory_manager"

    # JWT
    JWT_SECRET_KEY: str = Field(validation_alias="JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # LOGGING
    DEV_ENV: str = Field(validation_alias="DEV_ENV")
    LOG_LEVEL: str = Field(validation_alias="LOG_LEVEL")

    # .env settings
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", env_prefix="", extra="ignore"
    )


settings = Settings()


class ResponseStatus(str, Enum):
    """
    Response status enum

    Attributes:
        S: success string
        E: error string
    """

    S = "success"
    E = "error"
