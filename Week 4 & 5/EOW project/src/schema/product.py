from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveFloat,
    PositiveInt,
)

PRODUCT_TYPES = {"food", "regular", "electronic"}


class BaseProduct(BaseModel):
    """
    Schema to create attributes

    Args:
        BaseModel (_type_): _description_
    """

    id: str
    name: str
    quantity: PositiveInt
    price: PositiveFloat
    category_id: int


class ProductCreate(BaseProduct):
    """
    Schema for creating POST new product to
    the db

    Args:
        BaseProduct: base class with product attributes

    Raises:
        ValueError: if validation checks fail
    """


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
