from csv import DictReader
from typing import Any, Iterator, Optional
from pydantic import ValidationError

from .model import ProductFactory
from .log import logger, contruct_log_message
from .utility import dict_to_str, ProductDetails, convert_to_bool

product_factory: ProductFactory = ProductFactory()


def validate_product(product: dict[str, Any]) -> None:
    """
    validates a product
    Args:
        product: dictionary containing information about a praticular product
    """
    try:
        product_factory.create_product(
            product_details=ProductDetails(
                id=product["product_id"],
                name=product["product_name"],
                type=product["type"],
                quantity=product["quantity"],
                price=product["price"],
                days_to_expire=product["days_to_expire"],
                is_vegetarian=convert_to_bool(data=product["is_vegetarian"]),
                warranty_period_in_years=product["warranty_period_in_years"],
            )
        )
        if product["quantity"] and check_low_stock(product=product):
            append_low_stock_report(product=product)
        else:
            print(
                f"Requested product {product['product_name']} is ${product['price']} available quantity {product['quantity']}"
            )
    except ValidationError as e:
        print(
            f"Requested product {product['product_name']} has a validation error: {e.errors()[0]['msg']}"
        )
        logger.error(
            contruct_log_message(
                product_id=product["product_id"],
                message=e.errors()[0]["msg"],
                product=product,
            )
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
        if int(product["quantity"]) < 10:
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


# def read_file(filename: str) -> None:
#     """
#     Reads data from csv file
#     Args:
#         filename: csv file to read
#     """
#     try:
#         with open(filename, "r") as csv_file:
#             reader = DictReader(csv_file)
#             for row in reader:
#                 # validate_product(product=row)
#                 ...
#     except FileNotFoundError as e:
#         print(f"File not found {e}")


def get_product(filename: str) -> Optional[Iterator[dict[str, Any]]]:
    """
    Yields row from csv file
    Args:
        filename: file name to look for products
    Yields:
        A dictionary containing a product (row from csv)
    """
    try:
        with open(filename, "r") as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                yield row
    except FileNotFoundError as e:
        print(f"File not found {e}")
        return


def mainloop(inventory_data: str) -> None:
    """
    Contians mainloop
    Args:
        inventory_data: file path for inventory csv data
    """
    # print(os.getcwd())
    # read_file("inventory.csv")

    # products = get_product(inventory_data)
    # products_set = set(products.keys())
    print("Inventory Data Processor")

    while True:
        print("-" * 30)
        choice = input("Enter a product name to search (or) 'e' to exit: ").strip()
        if choice in {"e", "E"}:
            break
        else:
            if get_product(inventory_data) is not None:
                for product in get_product(inventory_data):  # type: ignore
                    if product["product_name"] == choice:
                        validate_product(product=product)
                        print("-" * 30)
            else:
                print(f"Cannot find product {choice} from inventory")
