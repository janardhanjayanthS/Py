from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.filepath import ENV_FILE
from src.core.log import get_logger
from src.core.singleton_pattern import Singleton

logger = get_logger(__name__)


class Settings(BaseSettings, metaclass=Singleton):
    """Application configuration settings.

    Handles environment variables and application-wide settings.
    """

    INVENTORY_CSV_FILEPATH: str = str(
        (Path(__file__).parent.parent.parent / "data" / "new_inventory.csv")
    )

    # POSTGRESQL
    postgresql_pwd: str = Field(
        validation_alias=AliasChoices("POSTGRESQL_PWD", "db_password")
    )
    db_host: str = Field(
        default="localhost",
        validation_alias=AliasChoices("DB_HOST", "db_host")
    )

    # ENVIRONMENT
    environment: str = Field(validation_alias="ENVIRONMENT")

    @property
    def DATABASE_URL(self) -> str:
        """Generate PostgreSQL database URL.

        Returns:
            Database connection string.
        """
        return f"postgresql+asyncpg://postgres:{self.postgresql_pwd}@{self.db_host}:5432/inventory_manager"

    # JWT
    JWT_SECRET_KEY: str = Field(validation_alias="JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # .env settings
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        secrets_dir="/run/secrets",
        env_prefix="",
        extra="ignore",
    )


settings = Settings()


class Errors(str, Enum):
    WEAK_PWD_ERROR = "WEAK_PASSWORD_ERROR"
    DB_ERROR = "DATABASE_ERROR"
    AUTH_ERROR = "AUTH_ERROR"


@dataclass
class ErrorDetails:
    message: str
    error_code: str
    status_code: int
    details: dict[str, Any]
