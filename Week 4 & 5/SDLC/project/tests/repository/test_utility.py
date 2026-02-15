# test_utility.py - Tests for repository utility functions
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.repository.utility import (
    check_password_strength,
    password_does_not_exist,
    strong_password,
    get_integer_product_id,
    get_category_id_from_type,
    get_initial_product_category_data,
    get_initial_product_data,
    get_initial_data_from_csv,
)


class TestPasswordStrength:
    """Test password strength validation"""

    def test_strong_password_valid(self):
        """Test strong password returns True"""
        valid_passwords = [
            "Password123!",
            "C0mplex@Pass",
            "Test#123Abc",
            "Secure$Pass1",
            "MyP@ssw0rd",
        ]

        for password in valid_passwords:
            assert strong_password(password) is True

    def test_strong_password_missing_lowercase(self):
        """Test password without lowercase returns False"""
        password = "PASSWORD123!"
        assert strong_password(password) is False

    def test_strong_password_missing_uppercase(self):
        """Test password without uppercase returns False"""
        password = "password123!"
        assert strong_password(password) is False

    def test_strong_password_missing_digit(self):
        """Test password without digit returns False"""
        password = "Password!"
        assert strong_password(password) is False

    def test_strong_password_missing_special_char(self):
        """Test password without special character returns False"""
        password = "Password123"
        assert strong_password(password) is False

    def test_strong_password_too_short(self):
        """Test password shorter than 8 characters returns False"""
        password = "Pass1!"
        assert strong_password(password) is False

    def test_strong_password_minimum_length(self):
        """Test password with exactly 8 characters"""
        password = "Pass123!"
        assert strong_password(password) is True

    def test_strong_password_with_spaces(self):
        """Test password with spaces"""
        password = "Pass 123!"
        assert strong_password(password) is True

    def test_strong_password_various_special_chars(self):
        """Test password with various special characters"""
        special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

        for char in special_chars:
            password = f"Password123{char}"
            assert strong_password(password) is True


class TestPasswordDoesNotExist:
    """Test password existence check"""

    def test_password_exists(self):
        """Test valid password returns False"""
        password = "ValidPassword123!"
        assert password_does_not_exist(password) is False

    def test_password_is_none(self):
        """Test None password returns True"""
        assert password_does_not_exist(None) is True

    def test_password_is_empty_string(self):
        """Test empty string password returns True"""
        assert password_does_not_exist("") is True

    def test_password_is_whitespace(self):
        """Test whitespace password returns False (truthy)"""
        assert password_does_not_exist("   ") is False


class TestCheckPasswordStrength:
    """Test combined password strength check"""

    def test_check_password_strength_valid(self):
        """Test valid strong password returns True"""
        password = "StrongPass123!"
        assert check_password_strength(password) is True

    def test_check_password_strength_none(self):
        """Test None password returns False"""
        assert check_password_strength(None) is False

    def test_check_password_strength_empty(self):
        """Test empty password returns False"""
        assert check_password_strength("") is False

    def test_check_password_strength_weak(self):
        """Test weak password returns False"""
        weak_passwords = [
            "password",  # Missing uppercase, digit, special char
            "PASSWORD",  # Missing lowercase, digit, special char
            "Pass1!",    # Too short
            "Password1", # Missing special char
            "Password!", # Missing digit
        ]

        for password in weak_passwords:
            assert check_password_strength(password) is False

    def test_check_password_strength_edge_cases(self):
        """Test edge cases for password strength"""
        # Just meets requirements
        assert check_password_strength("Pass123!") is True

        # Very long password
        assert check_password_strength("VeryLongPassword123!WithManyCharacters") is True


class TestGetIntegerProductId:
    """Test product ID extraction"""

    def test_get_integer_product_id_valid(self):
        """Test extracting integer from valid product ID"""
        assert get_integer_product_id("P001") == 1
        assert get_integer_product_id("P010") == 10
        assert get_integer_product_id("P100") == 100
        assert get_integer_product_id("P999") == 999

    def test_get_integer_product_id_leading_zeros(self):
        """Test product ID with leading zeros"""
        assert get_integer_product_id("P000") == 0
        assert get_integer_product_id("P005") == 5
        assert get_integer_product_id("P050") == 50

    def test_get_integer_product_id_invalid_format(self):
        """Test invalid product ID format - function doesn't validate prefix"""
        # The function just slices from index 1, doesn't validate "P" prefix
        # "001" -> "01" -> 1
        assert get_integer_product_id("001") == 1

        # "PABC" -> "ABC" raises ValueError when converting to int
        with pytest.raises(ValueError):
            get_integer_product_id("PABC")  # Non-numeric suffix

    def test_get_integer_product_id_empty(self):
        """Test empty product ID raises error"""
        # Empty string sliced from index 1 gives empty string, which raises ValueError
        with pytest.raises(ValueError):
            get_integer_product_id("")


class TestGetCategoryIdFromType:
    """Test category ID retrieval"""

    def test_get_category_id_from_type_exists(self):
        """Test getting category ID when type exists"""
        initial_data = {
            "product_category": [
                {"id": 1, "name": "electronics"},
                {"id": 2, "name": "books"},
                {"id": 3, "name": "clothing"}
            ]
        }

        assert get_category_id_from_type("electronics", initial_data) == 1
        assert get_category_id_from_type("books", initial_data) == 2
        assert get_category_id_from_type("clothing", initial_data) == 3

    def test_get_category_id_from_type_not_exists(self):
        """Test getting category ID when type doesn't exist"""
        initial_data = {
            "product_category": [
                {"id": 1, "name": "electronics"}
            ]
        }

        assert get_category_id_from_type("nonexistent", initial_data) is None

    def test_get_category_id_from_type_empty_data(self):
        """Test getting category ID from empty data"""
        initial_data = {"product_category": []}

        assert get_category_id_from_type("electronics", initial_data) is None

    def test_get_category_id_from_type_case_sensitive(self):
        """Test that category lookup is case sensitive"""
        initial_data = {
            "product_category": [
                {"id": 1, "name": "electronics"}
            ]
        }

        # Should not match with different case
        assert get_category_id_from_type("Electronics", initial_data) is None
        assert get_category_id_from_type("ELECTRONICS", initial_data) is None


class TestGetInitialProductCategoryData:
    """Test initial product category data extraction"""

    def test_get_initial_product_category_data_unique_categories(self):
        """Test extracting unique categories from products"""
        # Mock product objects
        mock_products = []

        for i, category in enumerate(["electronics", "books", "clothing"]):
            mock_product = Mock()
            mock_product.type.value = category
            mock_products.append(mock_product)

        initial_data = {"product_category": []}

        get_initial_product_category_data(products=mock_products, initial_data=initial_data)

        # Should have 3 unique categories
        assert len(initial_data["product_category"]) == 3

        # Check IDs are sequential
        ids = [cat["id"] for cat in initial_data["product_category"]]
        assert ids == [1, 2, 3]

        # Check all category names are present
        names = {cat["name"] for cat in initial_data["product_category"]}
        assert names == {"electronics", "books", "clothing"}

    def test_get_initial_product_category_data_duplicate_categories(self):
        """Test that duplicate categories are handled"""
        # Mock products with duplicate categories
        mock_products = []

        for category in ["electronics", "electronics", "books", "electronics"]:
            mock_product = Mock()
            mock_product.type.value = category
            mock_products.append(mock_product)

        initial_data = {"product_category": []}

        get_initial_product_category_data(products=mock_products, initial_data=initial_data)

        # Should have only 2 unique categories
        assert len(initial_data["product_category"]) == 2

        names = {cat["name"] for cat in initial_data["product_category"]}
        assert names == {"electronics", "books"}

    def test_get_initial_product_category_data_empty_products(self):
        """Test with empty products list"""
        initial_data = {"product_category": []}

        get_initial_product_category_data(products=[], initial_data=initial_data)

        assert len(initial_data["product_category"]) == 0


class TestGetInitialProductData:
    """Test initial product data extraction"""

    def test_get_initial_product_data_valid(self):
        """Test extracting product data"""
        # Mock products
        mock_product = Mock()
        mock_product.product_id = "P001"
        mock_product.product_name = "Laptop"
        mock_product.quantity = 10
        mock_product.price = 999
        mock_product.type.value = "electronics"

        initial_data = {
            "product": [],
            "product_category": [
                {"id": 1, "name": "electronics"}
            ]
        }

        get_initial_product_data(products=[mock_product], initial_data=initial_data)

        # Verify product data
        assert len(initial_data["product"]) == 1

        product = initial_data["product"][0]
        assert product["id"] == 1
        assert product["name"] == "Laptop"
        assert product["quantity"] == 10
        assert product["price"] == 999
        assert product["category_id"] == 1

    def test_get_initial_product_data_multiple_products(self):
        """Test extracting multiple products"""
        mock_products = []

        for i in range(3):
            mock_product = Mock()
            mock_product.product_id = f"P00{i+1}"
            mock_product.product_name = f"Product {i+1}"
            mock_product.quantity = 10 * (i + 1)
            mock_product.price = 100 * (i + 1)
            mock_product.type.value = "electronics"
            mock_products.append(mock_product)

        initial_data = {
            "product": [],
            "product_category": [
                {"id": 1, "name": "electronics"}
            ]
        }

        get_initial_product_data(products=mock_products, initial_data=initial_data)

        assert len(initial_data["product"]) == 3

        for i, product in enumerate(initial_data["product"]):
            assert product["id"] == i + 1
            assert product["category_id"] == 1

    def test_get_initial_product_data_empty_products(self):
        """Test with empty products list"""
        initial_data = {
            "product": [],
            "product_category": []
        }

        get_initial_product_data(products=[], initial_data=initial_data)

        assert len(initial_data["product"]) == 0


class TestGetInitialDataFromCsv:
    """Test CSV data loading"""

    @patch('src.repository.utility.Inventory')
    def test_get_initial_data_from_csv_success(self, mock_inventory_class):
        """Test successful CSV data loading"""
        # Mock Inventory instance
        mock_inventory = Mock()
        mock_inventory_class.return_value = mock_inventory

        # Mock product
        mock_product = Mock()
        mock_product.product_id = "P001"
        mock_product.product_name = "Test Product"
        mock_product.quantity = 10
        mock_product.price = 99
        mock_product.type.value = "electronics"

        mock_inventory.products = [mock_product]

        # Execute
        result = get_initial_data_from_csv("test.csv")

        # Verify
        assert "product" in result
        assert "product_category" in result
        assert len(result["product"]) == 1
        assert len(result["product_category"]) == 1

        # Verify inventory methods were called
        mock_inventory.load_from_csv.assert_called_once_with("test.csv")

    @patch('src.repository.utility.Inventory')
    def test_get_initial_data_from_csv_multiple_products(self, mock_inventory_class):
        """Test loading multiple products from CSV"""
        mock_inventory = Mock()
        mock_inventory_class.return_value = mock_inventory

        # Create multiple mock products with different categories
        mock_products = []
        for i, category in enumerate(["electronics", "books", "clothing"]):
            mock_product = Mock()
            mock_product.product_id = f"P00{i+1}"
            mock_product.product_name = f"Product {i+1}"
            mock_product.quantity = 10
            mock_product.price = 100
            mock_product.type.value = category
            mock_products.append(mock_product)

        mock_inventory.products = mock_products

        # Execute
        result = get_initial_data_from_csv("test.csv")

        # Verify
        assert len(result["product"]) == 3
        assert len(result["product_category"]) == 3

    @patch('src.repository.utility.Inventory')
    def test_get_initial_data_from_csv_empty_inventory(self, mock_inventory_class):
        """Test loading from empty inventory"""
        mock_inventory = Mock()
        mock_inventory_class.return_value = mock_inventory
        mock_inventory.products = []

        # Execute
        result = get_initial_data_from_csv("test.csv")

        # Verify
        assert len(result["product"]) == 0
        assert len(result["product_category"]) == 0


class TestUtilityIntegration:
    """Integration tests for utility functions"""

    def test_password_validation_workflow(self):
        """Test complete password validation workflow"""
        # Strong passwords should pass
        strong_passwords = [
            "MyP@ssw0rd123",
            "Str0ng!Pass",
            "C0mplex#Pass"
        ]

        for password in strong_passwords:
            assert check_password_strength(password) is True

        # Weak passwords should fail
        weak_passwords = [
            None,
            "",
            "password",
            "Pass123",
            "Short1!"
        ]

        for password in weak_passwords:
            assert check_password_strength(password) is False

    def test_product_data_extraction_workflow(self):
        """Test complete product data extraction workflow"""
        # Create mock products
        mock_products = []

        categories = ["electronics", "books"]
        for i, category in enumerate(categories):
            mock_product = Mock()
            mock_product.product_id = f"P00{i+1}"
            mock_product.product_name = f"Product {i+1}"
            mock_product.quantity = 10
            mock_product.price = 100
            mock_product.type.value = category
            mock_products.append(mock_product)

        # Initialize data
        initial_data = {"product": [], "product_category": []}

        # Extract categories first
        get_initial_product_category_data(products=mock_products, initial_data=initial_data)

        # Then extract products
        get_initial_product_data(products=mock_products, initial_data=initial_data)

        # Verify results
        assert len(initial_data["product_category"]) == 2
        assert len(initial_data["product"]) == 2

        # Verify category IDs are correctly assigned
        for product in initial_data["product"]:
            assert product["category_id"] is not None
            assert 1 <= product["category_id"] <= 2
