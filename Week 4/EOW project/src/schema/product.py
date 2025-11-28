from typing import Optional

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt, field_validator

PRODUCT_TYPES = {"food", "regular", "electronic"}


class BaseProduct(BaseModel):
    """
    Schema to create attributes

    Args:
        BaseModel (_type_): _description_
    """

    id: str
    name: str = Field(min_length=5, max_length=100)
    quantity: PositiveInt
    price: PositiveFloat
    type: str


class ProductCreate(BaseProduct):
    """
    Schema for creating POST new product to
    the db

    Args:
        BaseProduct: base class with product attributes

    Raises:
        ValueError: if validation checks fail
    """

    days_to_expire: Optional[int] = None
    is_vegetarian: Optional[bool] = None
    warranty_in_years: Optional[float] = None

    @field_validator("type")
    @classmethod
    def validate_product_type(cls, t: str) -> str:
        """
        Custom validation to check if given product
        is one of existing product type

        Args:
            t: product type

        Raises:
            ValueError: if given unknown type

        Returns:
            str: product type
        """
        if t not in PRODUCT_TYPES:
            raise ValueError(f"Product must be of the following types: {PRODUCT_TYPES}")
        return t

    def reset_regular_product_attributes(self):
        """
        to set is_vegetarian, days_to_expire & warranty_in_years to None
        for a regular product
        """
        if self.type == "regular":
            self.is_vegetarian = self.days_to_expire = self.warranty_in_years = None


class ProductUpdate(BaseProduct):
    """
    Schema to upgrade product details

    Args:
        BaseProduct: base class with product attributes
    """

    name: str | None
    quantity: str | None
    price: str | None


class ProductResponse(BaseProduct):
    class Config:
        orm_mode = True
        from_attributes = True
