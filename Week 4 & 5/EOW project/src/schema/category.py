from pydantic import BaseModel, Field


class BaseCategory(BaseModel):
    """
    Pydantic model for category
    """

    name: str


class CategoryCreate(BaseCategory):
    """
    model for creating new category
    """

    name: str = Field(min_length=5, max_length=25)


class CategoryUpdate(BaseModel):
    """
    Model for category update
    """

    id: int
    name: str
