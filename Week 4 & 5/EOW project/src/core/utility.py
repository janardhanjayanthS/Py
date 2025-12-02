import re

from inventory_manager import Inventory


def get_initial_product_data_from_csv(csv_filepath: str) -> dict[str, list]:
    """
    reads data from inventory.csv using Inventory() from inventory_manager package (from EOW Week2)

    Args:
        csv_filepath: filepath for inventory.csv

    Returns:
        dict: containing table name as key (eg: product) and list of dict for each product
    """
    initial_data: dict[str, list] = {"product": []}
    inv = Inventory()
    inv.load_from_csv(csv_filepath)
    for product in inv.products:
        initial_data["product"].append(
            {
                "id": product.product_id,
                "name": product.product_name,
                "quantity": product.quantity,
                "price": product.price,
                "type": product.type.value,
                "days_to_expire": product.days_to_expire
                if product.type.value == "food"
                else None,
                "is_vegetarian": product.is_vegetarian
                if product.type.value == "food"
                else None,
                "warranty_in_years": product.warranty_period_in_years
                if product.type.value == "electronic"
                else None,
            }
        )
    return initial_data


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
