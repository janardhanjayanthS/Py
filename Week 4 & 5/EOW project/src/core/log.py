import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="errors.log", encoding="utf-8", level=logging.ERROR)


def log_error(message: str) -> None:
    """
    Logs error message into errors.log file

    Args:
        message: error message to log
    """
    logger.error(msg=message)
