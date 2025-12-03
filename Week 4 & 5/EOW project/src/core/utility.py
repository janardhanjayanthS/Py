import re

from inventory_manager import Inventory


def get_initial_data_from_csv(csv_filepath: str) -> dict[str, list]:
    initial_data: dict[str, list] = {"product": [], "product_category": []}
    inv = Inventory()
    inv.load_from_csv(csv_filepath)
    get_initial_product_category_data(products=inv.products, initial_data=initial_data)
    get_initial_product_data(products=inv.products, initial_data=initial_data)
    return initial_data


def get_initial_product_category_data(products: list, initial_data: dict):
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
                "id": product.product_id,
                "name": product.product_name,
                "quantity": product.quantity,
                "price": product.price,
                "category_id": get_category_id_from_type(
                    type=product.type.value, initial_data=initial_data
                ),
            }
        )


def get_category_id_from_type(type: str, initial_data: dict):
    for category in initial_data["product_category"]:
        if category["name"] == type:
            return category["id"]
    return None


def check_password_strength(password) -> bool:
    """
    Checks if user's password is strong

    Args:
        password: plain text password

    Returns:
        bool: returns True if password is strong, False otherwise
    """

    if (
        not password
        or password is None
        or len(password) < 8
        or not re.search(r"[a-z]", password)
        or not re.search(r"[A-Z]", password)
        or not re.search(r"\d", password)
        or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    ):
        return False
    return True
