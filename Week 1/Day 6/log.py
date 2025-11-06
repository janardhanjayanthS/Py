import logging
from typing import Any

from utility import dict_to_str


logger = logging.getLogger(__name__)
logging.basicConfig(filename="errors.log", encoding="utf-8", level=logging.ERROR)


def contruct_log_message(product_id: str, message: str, product: dict[str, Any]) -> str:
    """
    Construcs a log message for an invalid product
    Returns:
        str containing details for logging
    """
    ...
    return f"P roduct ID: {product_id} | message: {message} | Row: {dict_to_str(product=product)}"
