from unittest.mock import create_autospec

import pytest
from src.core.utility import check_password_strength, get_initial_product_data_from_csv


class TestGetInitialProductDataFromCSV:
    def test_get_initial_data_fucntion_call(self, get_csv_filepath):
        """
        Test for get_initial_data_from_csv fucntion call

        Args:
            get_csv_filepath: filepath of test_inventory.csv file
        """
        mock_fucntion = create_autospec(get_initial_product_data_from_csv)

        mock_fucntion(get_csv_filepath)

        mock_fucntion.assert_called_once()
        mock_fucntion.assert_called_once_with(get_csv_filepath)

    def test_get_initial_data_return_value(self, get_csv_filepath):
        """
        Test for get_initial_data_from_csv function's return value

        Args:
            get_csv_filepath: filepath of test_inventory.csv file
        """

        return_value = get_initial_product_data_from_csv(get_csv_filepath)

        assert return_value["product"][0]["id"] == "P1"
        assert return_value["product"][0]["name"] == "Test product"
        assert return_value["product"][0]["quantity"] == 150
        assert return_value["product"][0]["price"] == 200
        assert return_value["product"][0]["type"] == "regular"
        assert return_value["product"][0]["days_to_expire"] is None
        assert return_value["product"][0]["is_vegetarian"] is None
        assert return_value["product"][0]["warranty_in_years"] is None

    def test_get_inital_data_with_empty_data(self, get_csv_filepath):
        """
        Test for get_initial_data_from_csv function's return value
        """
        mock_fucntion = create_autospec(
            get_initial_product_data_from_csv, return_value={"product": []}
        )

        return_value = mock_fucntion(get_csv_filepath)

        assert return_value == {"product": []}


class TestCheckPasswordStrength:
    """Test suite for check_password_strength function"""

    # Valid password tests
    def test_valid_strong_password(self):
        """Test that a strong password passes all checks"""
        assert check_password_strength("StrongPass123!") is True

    def test_valid_password_with_all_special_chars(self):
        """Test password with various special characters"""
        special_chars_passwords = [
            "Pass123!word",
            "Pass123@word",
            "Pass123#word",
            "Pass123$word",
            "Pass123%word",
            "Pass123^word",
            "Pass123&word",
            "Pass123*word",
            "Pass123(word)",
            "Pass123,word",
            "Pass123.word",
            "Pass123?word",
            'Pass123"word',
            "Pass123:word",
            "Pass123{word}",
            "Pass123|word",
            "Pass123<word>",
        ]
        for password in special_chars_passwords:
            assert check_password_strength(password) is True, f"Failed for: {password}"

    def test_valid_password_minimum_length(self):
        """Test password with exactly 8 characters (minimum length)"""
        assert check_password_strength("Aa1!bcde") is True

    def test_valid_password_long(self):
        """Test a very long password"""
        assert check_password_strength("VeryLongPassword123!WithManyCharacters") is True

    # Invalid password tests - Length
    def test_invalid_password_too_short(self):
        """Test password with less than 8 characters"""
        assert check_password_strength("Aa1!bcd") is False

    def test_invalid_password_empty(self):
        """Test empty password"""
        assert check_password_strength("") is False

    def test_invalid_password_seven_chars(self):
        """Test password with exactly 7 characters"""
        assert check_password_strength("Aa1!bcd") is False

    # Invalid password tests - Missing lowercase
    def test_invalid_password_no_lowercase(self):
        """Test password without lowercase letters"""
        assert check_password_strength("PASSWORD123!") is False

    # Invalid password tests - Missing uppercase
    def test_invalid_password_no_uppercase(self):
        """Test password without uppercase letters"""
        assert check_password_strength("password123!") is False

    # Invalid password tests - Missing digit
    def test_invalid_password_no_digit(self):
        """Test password without digits"""
        assert check_password_strength("PasswordOnly!") is False

    # Invalid password tests - Missing special character
    def test_invalid_password_no_special_char(self):
        """Test password without special characters"""
        assert check_password_strength("Password123") is False

    # Invalid password tests - Multiple missing requirements
    def test_invalid_password_missing_multiple_requirements(self):
        """Test passwords missing multiple requirements"""
        test_cases = [
            "password",  # No uppercase, digit, special char
            "PASSWORD",  # No lowercase, digit, special char
            "12345678",  # No letters, special char
            "!!!!!!!!!",  # No letters, digits
            "Pass!",  # Too short, no digit
            "Pass123",  # No special char
            "PASS123!",  # No lowercase
            "pass123!",  # No uppercase
        ]
        for password in test_cases:
            assert check_password_strength(password) is False, (
                f"Should fail for: {password}"
            )

    # Edge cases
    def test_password_with_spaces(self):
        """Test password containing spaces"""
        # Should be valid if it meets all other criteria
        assert check_password_strength("Pass word123!") is True

    def test_password_with_unicode_characters(self):
        """Test password with unicode characters"""
        # Unicode characters don't match the special char pattern
        assert check_password_strength("Pässwörd123") is False
        # But should pass with a special char
        assert check_password_strength("Pässwörd123!") is True

    def test_password_only_special_chars_and_numbers(self):
        """Test password with only special chars and numbers"""
        assert check_password_strength("12345678!@#$") is False

    # Parametrized tests for better coverage
    @pytest.mark.parametrize(
        "password,expected",
        [
            ("StrongPass123!", True),
            ("MyP@ssw0rd", True),
            ("Test123!@#", True),
            ("aB3!defgh", True),
            ("weak", False),
            ("NOLOWER1!", False),
            ("noupper1!", False),
            ("NoDigits!", False),
            ("NoSpecial1", False),
            ("Short1!", False),
            ("", False),
            ("       ", False),
        ],
    )
    def test_password_strength_parametrized(self, password, expected):
        """Parametrized test for various password scenarios"""
        assert check_password_strength(password) is expected

    # Boundary tests
    def test_exactly_one_of_each_requirement(self):
        """Test password with exactly one of each required character type"""
        assert check_password_strength("Aa1!aaaa") is True

    def test_password_all_requirements_at_minimum(self):
        """Test minimal valid password"""
        assert check_password_strength("Aa1!xxxx") is True
