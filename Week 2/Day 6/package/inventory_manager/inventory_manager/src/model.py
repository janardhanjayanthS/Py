from pydantic import BaseModel, PositiveFloat, PositiveInt
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

from .utility import ProductDetails


class BaseProduct(ABC, BaseModel):
    """
    Defines a product model
    Attributes:
        product_id: id of the product
        product_name: name of the product
        quantity: quantity of the product
        price: price of the product
    """

    product_id: str
    product_name: str
    quantity: PositiveInt
    price: PositiveFloat

    @abstractmethod
    def details(self) -> str:
        pass


class RegularProduct(BaseProduct):
    def __init__(self, product_details: ProductDetails):
        """
        Initializes regular product
        Args: 
            product_details: dataclass conatining product information
        """
        super().__init__(
            product_id=ProductDetails.id,
            product_name=product_details.name,
            quantity=product_details.quantity,
            price=product_details.price,
        )

    def details(self) -> str:
        """
        returns string contining product details
        """
        return f"ID: {self.product_id} \nName: {self.product_name} \nQantity: {self.quantity} \nprice: {self.price}"


class FoodProduct(BaseProduct):
    def __init__(self, product_details: ProductDetails):
        """
        Initializes a food product
        Args: 
            product_details: dataclass conatining product information
        Additional Attributes:
            days_to_expire: food's expiry period in days
            is_vegetarian: food's classification
        """
        super().__init__(
            product_id=ProductDetails.id,
            product_name=product_details.name,
            quantity=product_details.quantity,
            price=product_details.price,
        )
        self.days_to_expire = product_details.days_to_expire
        self.is_vegetarian = product_details.is_vegetarian

    def get_expiry_date(self) -> str:
        """
        returns exact expiry date
        Returns
            int representing expiry days
        """
        return datetime.strftime(
            timedelta(days=self.days_to_expire) + datetime.now(), # type: ignore
            "%d-%m-%Y",  # type: ignore
        )

    def details(self) -> str:
        """
        returns string contining product details
        """
        return f"ID: {self.product_id} \nName: {self.product_name} \nQantity: {self.quantity} \nprice: {self.price} \nDays to expire: {self.days_to_expire} \nIs Veg: {self.is_vegetarian}"


class ElectronicProduct(BaseProduct):
    def __init__(self, product_details: ProductDetails):
        """
        Initializes electronic product
        Args: 
            product_details: dataclass conatining product information
        Additional Attributes:
            warrenty_period_in_years: in years
        """
        super().__init__(
            product_id=ProductDetails.id,
            product_name=product_details.name,
            quantity=product_details.quantity,
            price=product_details.price,
        )
        self.warrenty_period_in_years = ProductDetails.warrenty_period_in_years

    def details(self) -> str:
        """
        returns string contining product details
        """
        return f"ID: {self.product_id} \nName: {self.product_name} \nQantity: {self.quantity} \nprice: {self.price} \nWarrenty period: {self.warrenty_period_in_years} years"


class ProductFactory:
    """
    Manages product types
    """

    def create_product(self, type: str, product_details: ProductDetails) -> BaseProduct:
        if type == "regular":
            return RegularProduct(product_details=product_details)
        elif type == "food":
            return FoodProduct(product_details=product_details)
        elif type == "electronic":
            return ElectronicProduct(product_details=product_details)
        else:
            raise Exception(f"Requested product type: {type} not available")
