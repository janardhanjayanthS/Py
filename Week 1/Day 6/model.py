from pydantic import BaseModel, PositiveFloat, PositiveInt


class Product(BaseModel):
    product_id: str
    product_name: str
    quantity: PositiveInt
    price: PositiveFloat
