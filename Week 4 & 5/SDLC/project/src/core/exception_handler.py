from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.core.config import ErrorDetails
from src.core.exceptions import (
    AuthenticationException,
    DatabaseException,
    WeakPasswordException,
)
from src.core.log import get_logger

logger = get_logger(__name__)


def get_error_response(error: ErrorDetails) -> dict:
    """Create standardized error response.

    Args:
        error: Error details object.

    Returns:
        Dictionary containing formatted error response.
    """
    return {
        "error": {
            "message": error.message,
            "status code": error.status_code,
            "error code": error.error_code,
            "details": error.details,
        }
    }


def handle_weak_password_error(
    request: Request, exception: WeakPasswordException
) -> JSONResponse:
    """Handle weak password exception.

    Args:
        request: HTTP request object.
        exception: Weak password exception.

    Returns:
        JSON response with error details.
    """
    logger.error(exception.message)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=get_error_response(
            ErrorDetails(
                message=exception.message,
                error_code=exception.error_code,
                status_code=exception.status_code,
                details=exception.details,
            )
        ),
    )


def handle_database_exception(
    request: Request, exception: DatabaseException
) -> JSONResponse:
    """Handle database exception.

    Args:
        request: HTTP request object.
        exception: Database exception.

    Returns:
        JSON response with error details.
    """
    logger.error(exception.message)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=get_error_response(
            ErrorDetails(
                message=exception.message,
                error_code=exception.error_code,
                status_code=exception.status_code,
                details=exception.details,
            )
        ),
    )


def handle_auth_exception(
    request: Request, exception: AuthenticationException
) -> JSONResponse:
    """Handle authentication exception.

    Args:
        request: HTTP request object.
        exception: Authentication exception.

    Returns:
        JSON response with error details.
    """
    logger.error(exception)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=get_error_response(
            ErrorDetails(
                message=exception.message,
                error_code=exception.error_code,
                status_code=exception.status_code,
                details=exception.details,
            )
        ),
    )


def add_exception_handlers_to_app(app: FastAPI) -> None:
    """Register custom exception handlers with FastAPI app.

    Args:
        app: FastAPI application instance.
    """
    app.add_exception_handler(WeakPasswordException, handle_weak_password_error)
    app.add_exception_handler(DatabaseException, handle_database_exception)
    app.add_exception_handler(AuthenticationException, handle_auth_exception)

    logger.info("Successfully Registered custom exceptions to application")
