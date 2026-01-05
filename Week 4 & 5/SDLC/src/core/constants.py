from enum import Enum
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    INVENTORY_CSV_FILEPATH: str = str(
        (Path(__file__).parent.parent.parent / "data" / "new_inventory.csv")
    )

    # POSTGRESQL
    postgresql_pwd: str = Field(validation_alias="POSTGRESQL_PWD")

    DATABASE_URL = (
        f"postgresql://postgres:{postgresql_pwd}@localhost:5432/inventory_manager"
    )

    # JWT
    JWT_SECRET_KEY = Field(validation_alias="JWT_SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # .env settings
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix=""
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
