import re
from typing import Optional

from inventory_manager import Inventory


def get_initial_data_from_csv(csv_filepath: str) -> dict[str, list]:
    """Load inventory data from CSV and extract initial product and category data.

    Reads inventory information from a CSV file, processes the products to extract
    unique categories, and organizes both product and product category data into
    a structured dictionary format.

    Args:
        csv_filepath: Path to the CSV file containing inventory data.

    Returns:
        A dictionary containing two lists:
            - 'product': List of product data dictionaries
            - 'product_category': List of product category data dictionaries

    Example:
        >>> data = get_initial_data_from_csv('inventory.csv')
        >>> data['product_category']
        [{'id': 1, 'name': 'Electronics'}, {'id': 2, 'name': 'Clothing'}]
    """
    initial_data: dict[str, list] = {"product": [], "product_category": []}
    inv = Inventory()
    inv.load_from_csv(csv_filepath)
    get_initial_product_category_data(products=inv.products, initial_data=initial_data)
    get_initial_product_data(products=inv.products, initial_data=initial_data)
    return initial_data


def get_initial_product_category_data(products: list, initial_data: dict):
    """Extract unique product categories and populate initial data dictionary.

    Iterates through the provided products to identify all unique product categories,
    then adds each category to the initial_data dictionary with a sequential ID.

    Args:
        products: List of product objects, each containing a 'type' attribute with
            an enum value representing the product category.
        initial_data: Dictionary to be populated with product category data. Must
            contain a 'product_category' key with an empty list value.

    Returns:
        None. Modifies the initial_data dictionary in place by appending category
        dictionaries to the 'product_category' list.

    Note:
        Each category dictionary contains 'id' (sequential integer starting from 1)
        and 'name' (string value of the category).
    """
    unique_categories = set()
    for product in products:
        unique_categories.add(product.type.value)
    for i, category in enumerate(unique_categories, start=1):
        initial_data["product_category"].append({"id": i, "name": category})


def get_initial_product_data(products: list, initial_data: dict):
    """
    reads data from inventory.csv using Inventory() from inventory_manager package (from EOW Week2)

    Args:
        csv_filepath: filepath for inventory.csv

    Returns:
        dict: containing table name as key (eg: product) and list of dict for each product
    """
    for product in products:
        initial_data["product"].append(
            {
                "id": get_integer_product_id(product_id=product.product_id),
                "name": product.product_name,
                "quantity": product.quantity,
                "price": product.price,
                "category_id": get_category_id_from_type(
                    type=product.type.value, initial_data=initial_data
                ),
            }
        )


def get_integer_product_id(product_id: str) -> int:
    """
    gets integer number from string product_id
    eg:
    P001 -> 1

    Args:
        product_id: string product id

    Returns:
        int: int version of product_id
    """
    return int(product_id[1:])


def get_category_id_from_type(type: str, initial_data: dict) -> int | None:
    """
    gets category id for a specific product type (from csv)

    Args:
        type: product type as string
        initial_data: dict containing all product_category information

    Returns:
        int | None: category id if exists else None
    """
    for category in initial_data["product_category"]:
        if category["name"] == type:
            return category["id"]
    return None


def check_password_strength(password: Optional[str]) -> bool:
    """
    Checks if user's password is strong

    Args:
        password: plain text password

    Returns:
        bool: returns True if password is strong, False otherwise
    """
    if password_does_not_exist(password=password):
        return False
    return strong_password(password=password)


def password_does_not_exist(password: Optional[str]) -> bool:
    """Check if password is None or empty.

    Args:
        password: Password string to check.

    Returns:
        True if password is None or empty/falsy, False otherwise.
    """
    return not password or password is None


def strong_password(password: Optional[str]) -> bool:
    """Check if a password does not meet strong password requirements.

    Validates that a password fails to meet one or more security criteria.
    A strong password must be at least 8 characters long and contain at least
    one lowercase letter, one uppercase letter, one digit, and one special
    character.

    Args:
        password: The password string to validate, or None.

    Returns:
        True if the password is weak (fails to meet requirements), False if
        the password is strong (meets all requirements).
    """
    return bool(
        len(password) >= 8
        and re.search(r"[a-z]", password)
        and re.search(r"[A-Z]", password)
        and re.search(r"\d", password)
        and re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )
