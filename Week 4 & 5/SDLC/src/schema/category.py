from typing import Any, Optional

from pydantic import BaseModel, ConfigDict
from src.core.constants import ResponseStatus


class BaseCategory(BaseModel):
    """
    Pydantic model for category
    """

    name: str


class CategoryCreate(BaseCategory):
    """
    model for creating new category
    """

    id: Optional[int] = None


class CategoryUpdate(BaseModel):
    """
    Model for category update
    """

    id: int
    name: str


class CategoryResponse(BaseModel):
    """
    Model for category response
    """

    status: ResponseStatus
    message: dict[str, Any]


class CategoryRead(BaseModel):
    """
    Model for reading category data (serializable)
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
