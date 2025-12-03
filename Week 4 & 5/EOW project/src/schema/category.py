from typing import Optional

from pydantic import BaseModel


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
