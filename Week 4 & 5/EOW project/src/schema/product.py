from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveFloat,
    PositiveInt,
)


class BaseProduct(BaseModel):
    """
    Schema to create attributes

    Args:
        BaseModel (_type_): _description_
    """

    id: int
    name: str
    quantity: PositiveInt
    price: PositiveFloat
    category_id: int


class ProductCreate(BaseModel):
    """
    Schema for creating POST new product to
    the db

    Args:
        BaseProduct: base class with product attributes

    Raises:
        ValueError: if validation checks fail
    """

    id: Optional[int] = None
    name: str
    quantity: PositiveInt
    price: PositiveFloat
    category_id: int


class ProductUpdate(BaseModel):
    """
    Schema to upgrade product details
    """

    name: Optional[str] = Field(None, min_length=5, max_length=100)
    quantity: Optional[PositiveInt] = None  # type: ignore
    price: Optional[PositiveFloat] = None  # type: ignore
    category_id: Optional[int] = None


class ProductResponse(BaseProduct):
    model_config = ConfigDict(from_attributes=True)
