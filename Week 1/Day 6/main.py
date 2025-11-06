from csv import DictReader
from typing import Any

from model import Product


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
    except Exception as e:
        # log error
        print("-" * 5)
        print(product)
        print(e)
    else:
        # if quantity is less than 10 add it to low_stock_report.txt
        ...


def read_file(filename: str):
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
