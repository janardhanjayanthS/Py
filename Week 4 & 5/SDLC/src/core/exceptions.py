from typing import Any, Optional

from src.core.config import Errors


class BaseAppException(Exception):
    def __init__(
        self,
        message: str,
        error_code: Optional[Errors] = "",
        details: Optional[dict[str, Any]] = None,
        status_code: int = 500,
        headers: Optional[dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.details = details
        self.status_code = status_code
        self.headers = headers
        super().__init__(self.messages)


class WeakPasswordException(BaseAppException):
    """Exception raised when a password does not meet strength requirements.

    Args:
        message: Description of why the password is weak.
    """

    def __init__(self, message: str, field_errors: list[dict[str, str]] = None) -> None:
        details = {"field_errors": field_errors} if field_errors else {}
        super().__init__(
            message=message,
            error_code=Errors.WEAK_PWD_ERROR,
            details=details,
            status_code=400,
        )


class DatabaseException(BaseAppException):
    """Exception raised when a password does not meet strength requirements.

    Args:
        message: Description of why the password is weak.
    """

    def __init__(self, message: str, field_errors: list[dict[str, str]] = None) -> None:
        details = {"field_errors": field_errors} if field_errors else {}
        super().__init__(
            message=message,
            error_code=Errors.DB_ERROR,
            details=details,
            status_code=500,
        )


class AuthenticationException(BaseAppException):
    """Exception raised when a password does not meet strength requirements.

    Args:
        message: Description of why the password is weak.
    """

    def __init__(self, message: str, field_errors: list[dict[str, str]] = None) -> None:
        details = {"field_errors": field_errors} if field_errors else {}
        super().__init__(
            message=message,
            error_code=Errors.AUTH_ERROR,
            details=details,
            status_code=403,
        )
