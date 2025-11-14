from pydantic import BaseModel, PositiveFloat, PositiveInt, Field
from datetime import datetime, timedelta
from abc import ABC

from .utility import ProductDetails, ProductTypes


class BaseProduct(ABC, BaseModel, validate_assignment=True):
    """
    Defines a product model
    Attributes:
        product_id: id of the product
        product_name: name of the product
        quantity: quantity of the product
        price: price of the product
    """

    product_id: str
    product_name: str = Field(..., min_length=1)
    quantity: PositiveInt
    price: PositiveFloat
    type: ProductTypes

    def __str__(self):
        message = ""
        for key, value in self.__dict__.items():
            if key == "type":
                message += f"{key}: {value.value} | "
            else:
                message += f"{key}: {value} | "
        return message


class RegularProduct(BaseProduct):
    """
    Initializes regular product
    Args:
        product_details: dataclass conatining product information
    """


class FoodProduct(BaseProduct):
    """
    Initializes a food product
    Args:
        product_details: dataclass conatining product information
    Additional Attributes:
        days_to_expire: food's expiry period in days
        is_vegetarian: food's classification
    """

    days_to_expire: PositiveInt
    is_vegetarian: bool

    def get_expiry_date(self) -> str:
        """
        returns exact expiry date
        Returns
            int representing expiry days
        """
        return datetime.strftime(
            timedelta(days=self.days_to_expire) + datetime.now(),  # type: ignore
            "%d-%m-%Y",  # type: ignore
        )


class ElectronicProduct(BaseProduct):
    """
    Initializes electronic product
    Args:
        product_details: dataclass conatining product information
    Additional Attributes:
        warrenty_period_in_years: in years
    """

    warranty_period_in_years: float


class ProductFactory:
    """
    Manages product types
    """

    def create_product(self, product_details: ProductDetails) -> BaseProduct:
        """
        Creates and returns product object based on product type

        Args:
            product_details : contains details about the product

        Returns:
            BaseProduct: the created object type
        """
        if product_details.type == ProductTypes.RP.value:
            return RegularProduct(
                product_id=product_details.id,
                product_name=product_details.name,
                quantity=product_details.quantity,
                price=product_details.price,
                type=product_details.type,
            )
        elif product_details.type == ProductTypes.FP.value:
            return FoodProduct(
                product_id=product_details.id,
                product_name=product_details.name,
                quantity=product_details.quantity,
                price=product_details.price,
                days_to_expire=product_details.days_to_expire,
                is_vegetarian=product_details.is_vegetarian,  # type: ignore
                type=product_details.type,
            )
        elif product_details.type == ProductTypes.EP.value:
            return ElectronicProduct(
                product_id=product_details.id,
                product_name=product_details.name,
                quantity=product_details.quantity,
                price=product_details.price,
                warranty_period_in_years=product_details.warranty_period_in_years,
                type=product_details.type,
            )
        else:
            print(f"Requested product type: {type} not available")
            return  # type: ignore
