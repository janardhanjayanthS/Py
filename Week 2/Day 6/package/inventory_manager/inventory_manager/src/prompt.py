from .utility import ProductTypes


def prompt_id(id_set: set[str]) -> str:
    """
    prompt for product id

    Args:
        id_set (set[str]): set of product ids

    Returns:
        str: product id
    """
    while True:
        id = input("Enter product id: ")
        if id not in id_set:
            return id
        else:
            print(f"Given ID {id} already exists, Enter a new one")


def prompt_name() -> str:
    """
    Prompt for product name

    Returns:
        str: product name
    """
    name = input("Enter product name: ")
    return name


def prompt_quantity() -> int:
    """
    Prompt for product quantity

    Returns:
        int: product's quantity
    """
    while True:
        try:
            qty = int(input("Enter product quantity: "))
            if qty > 0:
                return qty
            else:
                print("quantity must be positive")
        except ValueError as e:
            print(f"{qty} is not valid, enter a valid intger. {e}")


def prompt_price() -> float:
    """
    Prompt for product price

    Returns:
        float: product's price
    """
    while True:
        try:
            price = float(input("Enter product's price: "))
            if price > 0:
                return price
            else:
                print("Price must be positive")
        except ValueError as e:
            print(f"{price} is not valid, enter a valid price: {e}")


def prompt_type() -> str:
    while True:
        product_type = input("Enter product type: ")
        if product_type in ProductTypes.get_values()
            ...
