# test_exceptions.py - Tests for custom exception classes
import pytest
from src.core.exceptions import (
    AuthenticationException,
    AuthorizationException,
    BadRequestException,
    DatabaseException,
    InternalServerErrorException,
    NotFoundException,
    ValidationException,
)


class TestAuthenticationException:
    """Test suite for AuthenticationException"""

    def test_authentication_exception_initialization(self):
        """Test AuthenticationException initialization"""
        exception = AuthenticationException(
            message="Authentication failed",
            field_errors=[{"field": "email", "message": "Invalid email"}],
        )

        assert exception.message == "Authentication failed"
        assert exception.field_errors == [
            {"field": "email", "message": "Invalid email"}
        ]

    def test_authentication_exception_without_field_errors(self):
        """Test AuthenticationException without field errors"""
        exception = AuthenticationException(message="Invalid credentials")

        assert exception.message == "Invalid credentials"
        assert exception.field_errors is None

    def test_authentication_exception_empty_field_errors(self):
        """Test AuthenticationException with empty field errors"""
        exception = AuthenticationException(
            message="Validation failed", field_errors=[]
        )

        assert exception.message == "Validation failed"
        assert exception.field_errors == []

    def test_authentication_exception_multiple_field_errors(self):
        """Test AuthenticationException with multiple field errors"""
        field_errors = [
            {"field": "email", "message": "Invalid email format"},
            {"field": "password", "message": "Password too short"},
            {"field": "name", "message": "Name is required"},
        ]
        exception = AuthenticationException(
            message="Multiple validation errors", field_errors=field_errors
        )

        assert exception.message == "Multiple validation errors"
        assert len(exception.field_errors) == 3
        assert exception.field_errors[0]["field"] == "email"
        assert exception.field_errors[1]["field"] == "password"
        assert exception.field_errors[2]["field"] == "name"


class TestAuthorizationException:
    """Test suite for AuthorizationException"""

    def test_authorization_exception_initialization(self):
        """Test AuthorizationException initialization"""
        exception = AuthorizationException(
            message="Access denied", required_role="admin", current_role="user"
        )

        assert exception.message == "Access denied"
        assert exception.required_role == "admin"
        assert exception.current_role == "user"

    def test_authorization_exception_without_roles(self):
        """Test AuthorizationException without role information"""
        exception = AuthorizationException(message="Access denied")

        assert exception.message == "Access denied"
        assert exception.required_role is None
        assert exception.current_role is None

    def test_authorization_exception_same_role(self):
        """Test AuthorizationException when user has required role but still denied"""
        exception = AuthorizationException(
            message="Resource access denied",
            required_role="admin",
            current_role="admin",
        )

        assert exception.message == "Resource access denied"
        assert exception.required_role == "admin"
        assert exception.current_role == "admin"


class TestDatabaseException:
    """Test suite for DatabaseException"""

    def test_database_exception_initialization(self):
        """Test DatabaseException initialization"""
        exception = DatabaseException(
            message="Database connection failed",
            field_errors=[{"field": "database", "message": "Connection timeout"}],
        )

        assert exception.message == "Database connection failed"
        assert exception.field_errors == [
            {"field": "database", "message": "Connection timeout"}
        ]

    def test_database_exception_without_field_errors(self):
        """Test DatabaseException without field errors"""
        exception = DatabaseException(message="Query failed")

        assert exception.message == "Query failed"
        assert exception.field_errors is None

    def test_database_exception_multiple_errors(self):
        """Test DatabaseException with multiple field errors"""
        field_errors = [
            {"field": "connection", "message": "Unable to connect"},
            {"field": "timeout", "message": "Connection timeout after 30 seconds"},
        ]
        exception = DatabaseException(
            message="Multiple database errors", field_errors=field_errors
        )

        assert exception.message == "Multiple database errors"
        assert len(exception.field_errors) == 2


class TestValidationException:
    """Test suite for ValidationException"""

    def test_validation_exception_initialization(self):
        """Test ValidationException initialization"""
        exception = ValidationException(
            message="Validation failed",
            field_errors=[{"field": "email", "message": "Invalid email format"}],
        )

        assert exception.message == "Validation failed"
        assert exception.field_errors == [
            {"field": "email", "message": "Invalid email format"}
        ]

    def test_validation_empty_field_errors(self):
        """Test ValidationException with empty field errors"""
        exception = ValidationException(message="No data provided", field_errors=[])

        assert exception.message == "No data provided"
        assert exception.field_errors == []

    def test_validation_complex_field_errors(self):
        """Test ValidationException with complex field errors"""
        field_errors = [
            {
                "field": "product",
                "message": "Product validation failed",
                "sub_errors": [
                    {"field": "price", "message": "Price must be positive"},
                    {"field": "stock", "message": "Stock cannot be negative"},
                ],
            }
        ]
        exception = ValidationException(
            message="Product validation failed", field_errors=field_errors
        )

        assert exception.message == "Product validation failed"
        assert len(exception.field_errors) == 1
        assert "sub_errors" in exception.field_errors[0]


class TestNotFoundException:
    """Test suite for NotFoundException"""

    def test_not_found_exception_initialization(self):
        """Test NotFoundException initialization"""
        exception = NotFoundException(
            message="User not found", resource_type="User", resource_id=123
        )

        assert exception.message == "User not found"
        assert exception.resource_type == "User"
        assert exception.resource_id == 123

    def test_not_found_exception_without_resource_info(self):
        """Test NotFoundException without resource information"""
        exception = NotFoundException(message="Resource not found")

        assert exception.message == "Resource not found"
        assert exception.resource_type is None
        assert exception.resource_id is None

    def test_not_found_exception_string_id(self):
        """Test NotFoundException with string resource ID"""
        exception = NotFoundException(
            message="Product not found", resource_type="Product", resource_id="PROD-123"
        )

        assert exception.message == "Product not found"
        assert exception.resource_type == "Product"
        assert exception.resource_id == "PROD-123"


class TestBadRequestException:
    """Test suite for BadRequestException"""

    def test_bad_request_exception_initialization(self):
        """Test BadRequestException initialization"""
        exception = BadRequestException(
            message="Invalid request parameters",
            field_errors=[{"field": "limit", "message": "Limit must be positive"}],
        )

        assert exception.message == "Invalid request parameters"
        assert exception.field_errors == [
            {"field": "limit", "message": "Limit must be positive"}
        ]

    def test_bad_request_exception_without_field_errors(self):
        """Test BadRequestException without field errors"""
        exception = BadRequestException(message="Malformed request")

        assert exception.message == "Malformed request"
        assert exception.field_errors is None

    def test_bad_request_multiple_parameters(self):
        """Test BadRequestException with multiple parameter errors"""
        field_errors = [
            {"field": "page", "message": "Page must be greater than 0"},
            {"field": "limit", "message": "Limit cannot exceed 100"},
            {"field": "sort", "message": "Invalid sort field"},
        ]
        exception = BadRequestException(
            message="Invalid query parameters", field_errors=field_errors
        )

        assert exception.message == "Invalid query parameters"
        assert len(exception.field_errors) == 3


class TestInternalServerErrorException:
    """Test suite for InternalServerErrorException"""

    def test_internal_server_error_exception_initialization(self):
        """Test InternalServerErrorException initialization"""
        exception = InternalServerErrorException(
            message="Internal server error occurred",
            error_code="ERR_500",
            details="Unexpected error in user service",
        )

        assert exception.message == "Internal server error occurred"
        assert exception.error_code == "ERR_500"
        assert exception.details == "Unexpected error in user service"

    def test_internal_server_error_exception_without_details(self):
        """Test InternalServerErrorException without additional details"""
        exception = InternalServerErrorException(message="Server error")

        assert exception.message == "Server error"
        assert exception.error_code is None
        assert exception.details is None

    def test_internal_server_error_exception_with_only_error_code(self):
        """Test InternalServerErrorException with only error code"""
        exception = InternalServerErrorException(
            message="Database error", error_code="DB_ERROR"
        )

        assert exception.message == "Database error"
        assert exception.error_code == "DB_ERROR"
        assert exception.details is None


class TestExceptionInheritance:
    """Test suite for exception inheritance and behavior"""

    def test_exception_inheritance_from_base_exception(self):
        """Test that all custom exceptions inherit from base Exception"""
        exceptions = [
            AuthenticationException("test"),
            AuthorizationException("test"),
            DatabaseException("test"),
            ValidationException("test"),
            NotFoundException("test"),
            BadRequestException("test"),
            InternalServerErrorException("test"),
        ]

        for exception in exceptions:
            assert isinstance(exception, Exception)
            assert hasattr(exception, "message")

    def test_exception_str_representation(self):
        """Test string representation of exceptions"""
        exception = AuthenticationException(message="Test message")
        assert str(exception) == "Test message"

    def test_exception_repr_representation(self):
        """Test repr representation of exceptions"""
        exception = DatabaseException(message="DB error")
        repr_str = repr(exception)
        assert "DatabaseException" in repr_str
        assert "DB error" in repr_str

    def test_exception_equality(self):
        """Test exception equality comparison"""
        exc1 = AuthenticationException(message="Same message")
        exc2 = AuthenticationException(message="Same message")
        exc3 = AuthenticationException(message="Different message")

        # Exceptions with same message should be equal
        assert exc1.message == exc2.message
        assert exc1.message != exc3.message

    def test_exception_with_none_message(self):
        """Test exception with None message"""
        with pytest.raises(TypeError):
            AuthenticationException(message=None)


class TestExceptionIntegration:
    """Integration tests for exception handling"""

    def test_exception_chaining(self):
        """Test exception chaining (cause and effect)"""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as original_error:
                raise DatabaseException(
                    message="Database operation failed",
                    field_errors=[{"field": "query", "message": "Invalid SQL"}],
                ) from original_error
        except DatabaseException as db_error:
            assert db_error.__cause__ is not None
            assert isinstance(db_error.__cause__, ValueError)
            assert str(db_error.__cause__) == "Original error"

    def test_exception_in_context_manager(self):
        """Test exceptions in context manager scenarios"""

        class TestContextManager:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is not None:
                    # Re-raise as different exception
                    raise InternalServerErrorException(
                        message="Context manager error", details=str(exc_val)
                    ) from exc_val
                return True

        with pytest.raises(InternalServerErrorException) as exc_info:
            with TestContextManager():
                raise ValueError("Original context error")

        assert "Context manager error" in str(exc_info.value)
        assert exc_info.value.__cause__ is not None

    def test_exception_field_error_validation(self):
        """Test field error structure validation"""
        # Valid field error
        valid_error = {"field": "email", "message": "Invalid email"}
        exception = ValidationException(
            message="Validation error", field_errors=[valid_error]
        )
        assert exception.field_errors[0]["field"] == "email"
        assert exception.field_errors[0]["message"] == "Invalid email"

        # Multiple field errors
        multiple_errors = [
            {"field": "name", "message": "Name required"},
            {"field": "email", "message": "Email invalid"},
            {"field": "age", "message": "Age must be positive"},
        ]
        exception = ValidationException(
            message="Multiple validation errors", field_errors=multiple_errors
        )
        assert len(exception.field_errors) == 3

        # Verify all fields are present
        for error in exception.field_errors:
            assert "field" in error
            assert "message" in error
            assert isinstance(error["field"], str)
            assert isinstance(error["message"], str)
