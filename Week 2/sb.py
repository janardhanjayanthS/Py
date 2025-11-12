"""SANDBOX"""

from datetime import timedelta, datetime
from enum import Enum
from pydantic import BaseModel


diff = datetime.now() - timedelta(days=10)
str_diff = datetime.strftime(diff, "%d-%m-%Y")
# print(diff, type(diff))
# print(str_diff, type(str_diff))


# class syntax
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    @classmethod
    def get_values(cls) -> list:
        return [enum.value for enum in cls]


# if __name__ == "__main__":
#     # s = Sample(name="yelp")
#     # print(s)
#     # print(type(s))
#     print(Color)
#     print(Color.get_values())


# prompts for product details

# from .utility import ProductTypes


# def prompt_id(id_set: set[str]) -> str:
#     """
#     prompt for product id

#     Args:
#         id_set (set[str]): set of product ids

#     Returns:
#         str: product id
#     """
#     while True:
#         id = input("Enter product id: ")
#         if id not in id_set:
#             return id
#         else:
#             print(f"Given ID {id} already exists, Enter a new one")


# def prompt_name() -> str:
#     """
#     Prompt for product name

#     Returns:
#         str: product name
#     """
#     name = input("Enter product name: ")
#     return name


# def prompt_quantity() -> int:
#     """
#     Prompt for product quantity

#     Returns:
#         int: product's quantity
#     """
#     while True:
#         try:
#             qty = int(input("Enter product quantity: "))
#             if qty > 0:
#                 return qty
#             else:
#                 print("quantity must be positive")
#         except ValueError as e:
#             print(f"{qty} is not valid, enter a valid intger. {e}")


# def prompt_price() -> float:
#     """
#     Prompt for product price

#     Returns:
#         float: product's price
#     """
#     while True:
#         try:
#             price = float(input("Enter product's price: "))
#             if price > 0:
#                 return price
#             else:
#                 print("Price must be positive")
#         except ValueError as e:
#             print(f"{price} is not valid, enter a valid price: {e}")


# def prompt_type() -> str:
#     """
#     Prompt for product type

#     Returns:
#         str: type of product
#     """
#     valid_products = ProductTypes.get_values()
#     while True:
#         product_type = input("Enter product type: ")
#         if product_type in valid_products:
#             return product_type
#         else:
#             print(
#                 f"Entered product type: {product_type} is not in exisiting product types: {valid_products}"
#             )


# def prompt_days_to_expire() -> int:
#     """
#     pormpt for days to expire

#     Returns:
#         int: product's days to expire
#     """
#     while True:
#         try:
#             days_to_expire = int(input("Enter product's days for expiry: "))
#             if days_to_expire > 0:
#                 return days_to_expire
#             else:
#                 print("Price must be positive")
#         except ValueError as e:
#             print(f"{days_to_expire} is not valid, enter a valid price: {e}")


# def prompt_is_vegetarian() -> bool:
#     """
#     Prompt for is_vegetarian

#     Returns:
#         bool: True if the food product is vegetarian, False otherwise
#     """
#     valid_answers = {"y", "yes", "n", "no"}
#     while True:
#         is_veg = input("Is the food product Vegetarian (y/yes|n/no): ").lower()
#         if is_veg in valid_answers:
#             return True if is_veg.startswith("y") else False
#         else:
#             print(
#                 f"your input {is_veg} is invalid, Enter a valid prompt answer: {valid_answers}"
#             )

# def prompt_warranty_period_in_years() -> int:
#     """
#     Prompt for electronic product's warranty period

#     Returns:
#         int: warranty period of an electronic product
#     """
#     while True:
#         try:
#             warranty_period = int(input("Enter electronic product's warranty period in years: "))
#             if warranty_period > 0:
#                 return warranty_period
#             else:
#                 print("Price must be positive")
#         except ValueError as e:
#             print(f"{warranty_period} is not valid, enter a valid price: {e}")


# ---------------------------------


class Sample:
    def __init__(self) -> None:
        self.val = '101'
    
    def __str__(self) -> str:
        print(self.__dict__)
        return f'from __str__ dundder method!!! {self.val}'


if __name__ == '__main__':
    s = Sample()
    print(s)