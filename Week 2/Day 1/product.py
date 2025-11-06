from pydantic import BaseModel, PositiveFloat, PositiveInt
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


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
    def __init__(
        self,
        product_id: str,
        product_name: str,
        quantity: PositiveInt,
        price: PositiveFloat,
    ):
        super().__init__(
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            price=price,
        )

    def details(self) -> str:
        """
        returns string contining product details
        """
        return f"ID: {self.product_id} \nName: {self.product_name} \nQantity: {self.quantity} \nprice: {self.price}"


class FoodProduct(BaseProduct):
    def __init__(
        self,
        product_id: str,
        product_name: str,
        quantity: PositiveInt,
        price: PositiveFloat,
        days_to_expire: PositiveInt,
        is_vegetarian: bool,
    ):
        """
        Additional Attributes:
            days_to_expire: food's expiry period in days
        """
        super().__init__(
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            price=price,
        )
        self.days_to_expire = days_to_expire
        self.is_vegetarian = is_vegetarian

    def get_expiry_date(self) -> str:
        """
        returns exact expiry date
        Returns
            int representing expiry days
        """
        return datetime.strftime(
            timedelta(days=self.days_to_expire) + datetime.now(), "%d-%m-%Y"
        )

    def details(self) -> str:
        """
        returns string contining product details
        """
        return f"ID: {self.product_id} \nName: {self.product_name} \nQantity: {self.quantity} \nprice: {self.price}"
