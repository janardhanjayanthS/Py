from typing import Any
from dataclasses import dataclass
from enum import Enum


def dict_to_str(product: dict[str, Any]) -> str:
    """
    Converts product details from dict to string format
    Args:
        product: dict containing product details
    Returns:
        str containing product details
    """
    result = []
    for key, value in product.items():
        result.append(f"{key}: {value}")
    return ", ".join(result)


def convert_to_bool(data: str) -> bool | None:
    if data.lower() == "yes":
        return True
    elif data.lower() == "no":
        return False
    else:
        pass
        # print(f"Unknown value for data: {data}")

class ProductTypes(Enum):
    RP = 'regular'
    FP = 'food'
    EP = 'electronic'

    @classmethod
    def get_values(cls) -> list[str]:
        return [enum.value for enum in cls]

@dataclass
class ProductDetails:
    """
    Dataclass for product information
    Args:
        id: id of product
        name: name of product
        type: type of product
        price: price of product
        quantity: quantity available
        days_to_expire: expiration days (only for FoodProduct)
        is_vegetarian: is the food vegetarian (only for FoodProduct)
        warrenty_period_in_years: warrenty period in years (only for ElectronicProduct)
    """
    id: str
    name: str
    type: str
    price: float
    quantity: int
    days_to_expire: int
    is_vegetarian: bool | str | None
    warranty_period_in_years: int 


