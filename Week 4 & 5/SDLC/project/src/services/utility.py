from typing import Any

from src.core.exceptions import DatabaseException
from src.core.log import get_logger

logger = get_logger(__name__)


def check_id_type(id: Any):
    """Validate that the id parameter is an integer type.

    Args:
        id: The id value to validate.

    Raises:
        DatabaseException: If id is not None/falsy and not an integer, raises 422
            Unprocessable Content error with details about the type mismatch.
    """
    if id and not isinstance(id, int):
        logger.error("ID should be numbers(integers)")
        raise DatabaseException(
            message=f"id should be type int but got type: {id.__class__.__name__}",
            field_errors=[
                {
                    "field": "id",
                    "message": f"ID must be an integer, got {id.__class__.__name__}",
                }
            ],
        )
