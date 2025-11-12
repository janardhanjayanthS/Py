from typing import Any

from .config import ConfigLoader
from .utility import dict_to_str
from .model import BaseProduct


config: ConfigLoader = ConfigLoader()


def check_low_stock_or_print_details(product: BaseProduct) -> None:
    """
    Checks if prodcut is low, if so then appends it to low stock report
    else prints product detail
    Args:
        product: object of Product form model.py
    """
    if product.quantity and check_low_stock(product_quantity=product.quantity):
        append_low_stock_report(product=product)
    else:
        product.details()


def check_low_stock(product_quantity: int) -> bool | None:
    """
    Checks if the quantity of a product is than 10
    Args:
        product_quantity: quantity of product
    Returns:
        True if quantity is less than 10, False otherwise
    """
    try:
        if int(product_quantity) < config.get_low_quality_threshold():
            return True
        return False
    except TypeError as e:
        print(f"Encountered type error: {e}")


def append_low_stock_report(product: BaseProduct) -> None:
    """
    Writes low stock data to low_stock_report.txt
    if it exists otherwise creates then writes
    Args:
        product: object of Product form model.py
    """
    print(f"Requested product is available in less quantity {product.quantity}")
    print(f"Product details: {product.details()}")
    filename = "low_stock_report.txt"
    try:
        append_content(filename, product.details())
    except FileNotFoundError:
        print("low_stock_report.txt does not exist")
        create_file(filename=filename)
        append_content(filename, product.details())


def append_content(filename: str, content: str) -> None:
    """
    Writes content to file
    Args:
        filename: file to write
        content: content to write
    """
    with open(filename, "a") as file:
        file.write(content + "\n")
    print(f"success fully appended to {filename}")


def create_file(filename: str) -> None:
    """
    creates a file with provided file name
    Args:
        filename: name of file to create
    """
    with open(filename, "x") as _:
        print(f"File {filename} created successfully")
