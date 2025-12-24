from typing import Any, Self

from pydantic import BaseModel

from src.core.constants import ResponseType


class CustomResponse(BaseModel):
    response: ResponseType
    message: dict[str, Any]

    @staticmethod
    def get_response(response_type: ResponseType, message: dict[str, Any]) -> Self:
        return CustomResponse(response=response_type.value, message=message)

