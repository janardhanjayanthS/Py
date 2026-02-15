from typing import Any, Optional

from src.core.config import Errors


class BaseAppException(Exception):
    """Base exception class for all application exceptions."""

    def __init__(
        self,
        message: str,
        error_code: Optional[Errors] = "",
        details: Optional[dict[str, Any]] = None,
        status_code: int = 500,
        headers: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize base application exception.

        Args:
            message: Error message.
            error_code: Error code from Errors enum.
            details: Additional error details.
            status_code: HTTP status code.
            headers: Additional headers.
        """
        self.message = message
        self.error_code = error_code
        self.details = details
        self.status_code = status_code
        self.headers = headers
        super().__init__(self.message)


class WeakPasswordException(BaseAppException):
    """Exception raised when a password does not meet strength requirements.

    Args:
        message: Description of why the password is weak.
    """

    def __init__(self, message: str, field_errors: list[dict[str, str]] = None) -> None:
        """Initialize weak password exception.

        Args:
            message: Description of why the password is weak.
            field_errors: List of field-specific error details.
        """
        super().__init__(
            message=message,
            error_code=Errors.WEAK_PWD_ERROR,
            details=field_errors,
            status_code=400,
        )


class DatabaseException(BaseAppException):
    """Exception raised for database-related errors.

    Args:
        message: Description of the database error.
    """

    def __init__(self, message: str, field_errors: list[dict[str, str]] = None) -> None:
        """Initialize database exception.

        Args:
            message: Description of the database error.
            field_errors: List of field-specific error details.
        """
        details = {"field_errors": field_errors} if field_errors else {}
        super().__init__(
            message=message,
            error_code=Errors.DB_ERROR,
            details=details,
            status_code=400,
        )


class AuthenticationException(BaseAppException):
    """Exception raised for authentication-related errors.

    Args:
        message: Description of the authentication error.
    """

    def __init__(self, message: str, field_errors: list[dict[str, str]] = None) -> None:
        """Initialize authentication exception.

        Args:
            message: Description of the authentication error.
            field_errors: List of field-specific error details.
        """
        details = {"field_errors": field_errors} if field_errors else {}
        super().__init__(
            message=message,
            error_code=Errors.AUTH_ERROR,
            details=details,
            status_code=403,
        )
