from csv import DictReader
from typing import Any
from pydantic import ValidationError

from model import Product
from log import logger, contruct_log_message


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
        # log error
        logger.error(contruct_log_message(
            product_id=product['product_id'],
            message=e.errors()[0]['msg'],
            product=product
        ))
        print("-" * 5)
        print(product)
        print(e.errors())
    else:
        # if quantity is less than 10 add it to low_stock_report.txt
        ...


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
