from typing import Any


def dict_to_str(product: dict[str, Any]) -> str:
    """
    Converts product details from dict to string format
    Args:
        product: dict containing product details
    Returns:
        str containing product details
    """
    result = []
    for key, value in product.items():
        result.append(f'{key}: {value}')
    return ', '.join(result)
