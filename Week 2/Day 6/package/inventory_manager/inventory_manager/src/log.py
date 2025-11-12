import logging

from .model import BaseProduct


logger = logging.getLogger(__name__)
logging.basicConfig(filename="errors.log", encoding="utf-8", level=logging.ERROR)


def construct_log_message(message: str, product: BaseProduct) -> str:
    """
    returns a log message for errors.log file

    Args:
        message: error message by Pydantic
        product: Product object from model.py

    Returns:
        str: _description_
    """
    return f"Product ID: {product.product_id} | message: {message} | Row: {product.details()}"
