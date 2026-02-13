import logging

from .utility import dict_to_str


logger = logging.getLogger(__name__)
logging.basicConfig(filename="errors.log", encoding="utf-8", level=logging.ERROR)


def construct_log_message(message: str, product_dict) -> str:
    """
    returns a log message for errors.log file

    Args:
        message: error message by Pydantic
        product_dict: dictionary containing product detail

    Returns:
        str: _description_
    """
    return f"Product ID: {product_dict['product_id']} | message: {message} | Row: {dict_to_str(product=product_dict)}"

def log_error(message: str) -> None:
    """
    Logs error message into errors.log file

    Args:
        message: error message to log
    """
    logger.error(msg=message)
