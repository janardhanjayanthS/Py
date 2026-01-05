from enum import Enum
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

CURRENT_DIR = Path(__file__).parent
ENV_FILE = CURRENT_DIR / ".env"


class Settings(BaseSettings):
    INVENTORY_CSV_FILEPATH: str = str(
        (Path(__file__).parent.parent.parent / "data" / "new_inventory.csv")
    )

    # POSTGRESQL
    postgresql_pwd: str = Field(validation_alias="POSTGRESQL_PWD")

    # JWT
    JWT_SECRET_KEY: str = Field(validation_alias="JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://postgres:{self.postgresql_pwd}@localhost:5432/inventory_manager"

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
