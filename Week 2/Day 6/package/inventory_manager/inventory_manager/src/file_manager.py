from typing import Any

from .config import ConfigLoader
from .utility import dict_to_str


config: ConfigLoader = ConfigLoader()


def check_low_stock_or_print_details(product: dict[str, Any]) -> None:
    """
    Checks if prodcut is low, if so then appends it to low stock report
    else prints product detail
    Args:
        product: dictionary containing product information
    """
    if product["quantity"] and check_low_stock(product=product):
        append_low_stock_report(product=product)
    else:
        print(
            f"Requested product {product['product_name']} is ${product['price']} available quantity {product['quantity']}"
        )


def check_low_stock(product: dict[str, Any]) -> bool | None:
    """
    Checks if the quantity of a product is than 10
    Args:
        product: dictionary containing product details
    Returns:
        True if quantity is less than 10, False otherwise
    """
    try:
        if int(product["quantity"]) < config.get_low_quality_threshold():
            return True
        return False
    except TypeError as e:
        print(f"Encountered type error: {e}")


def append_low_stock_report(product: dict[str, Any]) -> None:
    """
    Writes low stock data to low_stock_report.txt
    if it exists otherwise creates then writes
    Args:
        product: dictionary representing a row from inventory.csv
    """
    print(f"Requested product is available in less quantity {product['quantity']}")
    print(f"Product details: {dict_to_str(product=product)}")
    filename = "low_stock_report.txt"
    try:
        append_content(filename, dict_to_str(product=product))
    except FileNotFoundError:
        print("low_stock_report.txt does not exist")
        create_file(filename=filename)
        append_content(filename, dict_to_str(product=product))


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
