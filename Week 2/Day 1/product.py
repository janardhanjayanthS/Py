from pydantic import BaseModel, PositiveFloat, PositiveInt


class Product(BaseModel):
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

    def details(self) -> str:
        """
        returns string contining product details
        """ 
        return f'ID: {self.product_id} \nName: {self.product_name} \nQantity: {self.quantity} \nprice: {self.price}'