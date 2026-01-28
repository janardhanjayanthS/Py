# test_utility.py - Tests for service utility functions
import pytest
from src.core.exceptions import DatabaseException
from src.services.utility import check_id_type


class TestCheckIdType:
    """Test check_id_type validation function"""

    def test_check_id_type_valid_integer(self):
        """Test valid integer IDs don't raise exception"""
        valid_ids = [1, 10, 100, 999, 1000000]

        for id_value in valid_ids:
            # Should not raise exception
            check_id_type(id=id_value)

    def test_check_id_type_zero(self):
        """Test zero ID is valid"""
        # Should not raise exception
        check_id_type(id=0)

    def test_check_id_type_negative_integer(self):
        """Test negative integers are valid"""
        # Should not raise exception for negative integers
        check_id_type(id=-1)
        check_id_type(id=-100)

    def test_check_id_type_string(self):
        """Test string ID raises exception"""
        with pytest.raises(DatabaseException) as exc_info:
            check_id_type(id="123")

        assert "type int" in str(exc_info.value).lower()
        assert "str" in str(exc_info.value)

    def test_check_id_type_float(self):
        """Test float ID raises exception"""
        with pytest.raises(DatabaseException) as exc_info:
            check_id_type(id=123.45)

        assert "type int" in str(exc_info.value).lower()
        assert "float" in str(exc_info.value)

    def test_check_id_type_none(self):
        """Test None ID doesn't raise exception"""
        # According to source code: "if id and not isinstance(id, int)"
        # None is falsy, so it should not raise exception
        check_id_type(id=None)

    def test_check_id_type_list(self):
        """Test list ID raises exception"""
        with pytest.raises(DatabaseException) as exc_info:
            check_id_type(id=[1, 2, 3])

        assert "type int" in str(exc_info.value).lower()
        assert "list" in str(exc_info.value)

    def test_check_id_type_dict(self):
        """Test dict ID raises exception"""
        with pytest.raises(DatabaseException) as exc_info:
            check_id_type(id={"id": 1})

        assert "type int" in str(exc_info.value).lower()
        assert "dict" in str(exc_info.value)

    def test_check_id_type_boolean(self):
        """Test boolean ID raises exception"""
        # In Python, bool is a subclass of int, so True/False are valid integers
        # True == 1, False == 0
        # This should NOT raise exception
        check_id_type(id=True)
        check_id_type(id=False)

    def test_check_id_type_numeric_string(self):
        """Test numeric string raises exception"""
        numeric_strings = ["1", "10", "999", "-1", "0"]

        for id_value in numeric_strings:
            with pytest.raises(DatabaseException) as exc_info:
                check_id_type(id=id_value)

            assert "str" in str(exc_info.value)

    def test_check_id_type_empty_string(self):
        """Test empty string doesn't raise exception"""
        # Empty string is falsy, so it should not raise exception
        check_id_type(id="")

    def test_check_id_type_exception_message(self):
        """Test exception message contains helpful information"""
        with pytest.raises(DatabaseException) as exc_info:
            check_id_type(id="invalid")

        error = exc_info.value
        assert "id should be type int" in str(error).lower()
        assert "str" in str(error)

    def test_check_id_type_exception_field_errors(self):
        """Test exception contains field errors"""
        with pytest.raises(DatabaseException) as exc_info:
            check_id_type(id=12.5)

        error = exc_info.value
        # DatabaseException has field_errors in details dict
        assert 'details' in error.__dict__
        assert 'field_errors' in error.__dict__['details']


class TestCheckIdTypeEdgeCases:
    """Test edge cases for check_id_type"""

    def test_check_id_type_very_large_integer(self):
        """Test very large integer IDs"""
        large_ids = [
            10**10,  # 10 billion
            10**15,  # 1 quadrillion
            2**31 - 1,  # Max 32-bit signed integer
            2**63 - 1,  # Max 64-bit signed integer
        ]

        for id_value in large_ids:
            # Should not raise exception
            check_id_type(id=id_value)

    def test_check_id_type_object(self):
        """Test object ID raises exception"""
        class CustomObject:
            pass

        with pytest.raises(DatabaseException):
            check_id_type(id=CustomObject())

    def test_check_id_type_bytes(self):
        """Test bytes ID raises exception"""
        with pytest.raises(DatabaseException):
            check_id_type(id=b"123")

    def test_check_id_type_set(self):
        """Test set ID raises exception"""
        with pytest.raises(DatabaseException):
            check_id_type(id={1, 2, 3})

    def test_check_id_type_tuple(self):
        """Test tuple ID raises exception"""
        with pytest.raises(DatabaseException):
            check_id_type(id=(1, 2, 3))

    def test_check_id_type_complex_number(self):
        """Test complex number ID raises exception"""
        with pytest.raises(DatabaseException):
            check_id_type(id=complex(1, 2))


class TestCheckIdTypeIntegration:
    """Integration tests for check_id_type"""

    def test_typical_workflow_valid_ids(self):
        """Test typical workflow with valid IDs"""
        # Simulating typical use cases
        test_cases = [
            1,      # User ID
            10,     # Product ID
            100,    # Category ID
            0,      # Edge case - zero ID
        ]

        for test_id in test_cases:
            try:
                check_id_type(id=test_id)
                # If we get here, validation passed
                assert True
            except DatabaseException:
                # Should not happen with valid IDs
                pytest.fail(f"Valid ID {test_id} raised exception")

    def test_typical_workflow_invalid_ids(self):
        """Test typical workflow with invalid IDs"""
        # Common mistakes in API calls
        invalid_cases = [
            "1",        # String instead of int
            "abc",      # Non-numeric string
            1.5,        # Float instead of int
            [1],        # List instead of int
            {"id": 1},  # Dict instead of int
        ]

        for invalid_id in invalid_cases:
            with pytest.raises(DatabaseException):
                check_id_type(id=invalid_id)

    def test_api_parameter_validation_scenario(self):
        """Test simulating API parameter validation"""
        # Scenario: Validating product_id from API request

        # Valid API call
        product_id = 42
        check_id_type(id=product_id)  # Should pass

        # Invalid API call - user sent string
        product_id_str = "42"
        with pytest.raises(DatabaseException):
            check_id_type(id=product_id_str)

        # Invalid API call - user sent float
        product_id_float = 42.0
        with pytest.raises(DatabaseException):
            check_id_type(id=product_id_float)

    def test_optional_id_parameter(self):
        """Test validation when ID is optional"""
        # Some endpoints might have optional IDs
        optional_id = None
        check_id_type(id=optional_id)  # Should not raise exception

        # But when provided, must be integer
        with pytest.raises(DatabaseException):
            check_id_type(id="optional")


class TestCheckIdTypeErrorMessages:
    """Test error messages for check_id_type"""

    def test_error_message_includes_actual_type(self):
        """Test error message includes the actual type received"""
        test_cases = [
            ("string", "str"),
            (12.5, "float"),
            ([1, 2], "list"),
            ({"key": "value"}, "dict"),
        ]

        for value, expected_type in test_cases:
            with pytest.raises(DatabaseException) as exc_info:
                check_id_type(id=value)

            error_message = str(exc_info.value)
            assert expected_type in error_message.lower()

    def test_error_message_is_user_friendly(self):
        """Test error messages are helpful for API users"""
        with pytest.raises(DatabaseException) as exc_info:
            check_id_type(id="invalid")

        error_message = str(exc_info.value)

        # Should mention both expected and actual types
        assert "int" in error_message.lower()
        assert "str" in error_message.lower()

        # Should indicate it's an ID field
        assert "id" in error_message.lower()
