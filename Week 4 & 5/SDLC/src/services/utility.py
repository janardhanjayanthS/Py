from typing import Any

from fastapi import HTTPException, status

from src.core.log import get_logger

logger = get_logger(__name__)


def check_id_type(id: Any):
    """Validate that the id parameter is an integer type.

    Args:
        id: The id value to validate.

    Raises:
        HTTPException: If id is not None/falsy and not an integer, raises 422
            Unprocessable Content error with details about the type mismatch.
    """
    if id and not isinstance(id, int):
        logger.error("ID should be numbers(integers)")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"id should be type int but got type: {id.__class__.__name__}",
        )
