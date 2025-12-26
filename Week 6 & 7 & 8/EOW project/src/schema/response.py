from typing import Any

from pydantic import BaseModel, Field

from src.core.constants import ResponseType


class APIResponse(BaseModel):
    response: ResponseType = Field(..., description="type of response success or fail")
    message: dict[str, Any] = Field(..., description="message dictionary")

    class Config:
        use_enum_values = True

