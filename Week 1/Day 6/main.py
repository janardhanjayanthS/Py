from csv import DictReader
from typing import Any
from pydantic import ValidationError

from model import Product
from log import logger, contruct_log_message
from utility import dict_to_str


def validate_product(product: dict[str, Any]) -> None:
    """
    validates product
    Args:
        product: dictionary containing information about a praticular product
    """
    try:
        Product(
            product_id=product["product_id"],
            product_name=product["product_name"],
            quantity=product["quantity"],
            price=product["price"],
        )
        print(product)
    except ValidationError as e:
        logger.error(contruct_log_message(
            product_id=product['product_id'],
            message=e.errors()[0]['msg'],
            product=product
        ))
    else:
        if product['quantity'] < 10:
            write_low_stock_report(product)

def write_low_stock_report(product: dict[str, Any]) -> None:
    """
    Writes low stock data to low_stock_report.txt 
    if it exists otherwise creates then writes
    Args:
        product: dictionary representing a row from inventory.csv
    """
    filename = 'low_stock_report.txt'
    try:
        write_content(filename, dict_to_str(product=product))
    except FileNotFoundError:
        print('low_stock_report.txt does not exist')
        create_file(filename=filename)
        write_content(filename, dict_to_str(product=product))

def write_content(filename: str, content: str) -> None:
    """
    Writes content to file
    Args:
        filename: file to write 
        content: content to write
    """
    with open(filename, 'w') as file:
        file.write(content)


def create_file(filename: str) -> None:
    """
    creates a file with provided file name
    Args:
        filename: name of file to create    
    """
    with open(filename, 'x') as _:
        print(f'File {filename} created successfully')

def read_file(filename: str) -> None:
    """
    Reads data from csv file
    Args:
        filename: csv file to read
    """
    try:
        with open(filename, "r") as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                validate_product(product=row)
    except FileNotFoundError as e:
        print(f"File not found {e}")


if __name__ == "__main__":
    read_file("inventory.csv")
