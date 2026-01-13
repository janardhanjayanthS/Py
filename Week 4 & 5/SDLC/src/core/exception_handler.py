from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.core.exceptions import WeakPasswordException
from src.core.log import get_logger

logger = get_logger(__name__)


def handle_weak_password_error(
    request: Request, exception: WeakPasswordException
) -> JSONResponse:
    logger.error(exception.message)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"body": exception.message}
    )


def add_exception_handlers_to_app(app: FastAPI) -> None:
    app.add_exception_handler(WeakPasswordException, handle_weak_password_error)

    logger.info("Successfully Registered custom exceptions to application")
