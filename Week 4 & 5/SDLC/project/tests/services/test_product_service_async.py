# test_product_service_async.py - Comprehensive async tests for product service
import pytest
from unittest.mock import AsyncMock, Mock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import DatabaseException
from src.models.category import Category
from src.models.product import Product
from src.schema.product import ProductCreate, ProductUpdate
from src.services.product_service import (
    check_existing_product_using_id,
    check_existing_product_using_name,
    delete_product,
    get_all_products,
    get_category_specific_products,
    get_specific_product,
    handle_missing_product,
    post_product,
    apply_discount_or_tax,
)
from src.services.models import ResponseStatus


class TestCheckExistingProductUsingName:
    """Test check_existing_product_using_name with async operations"""

    @pytest.mark.asyncio
    async def test_product_exists_raises_exception(self):
        """Test that function raises exception when product exists"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock existing product
        mock_product = Product(id=1, name="Existing Product", price=100, quantity=10, category_id=1)

        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_product
        mock_db.execute.return_value = mock_result

        product_data = ProductCreate(
            name="Existing Product",
            price=100.0,
            quantity=10,
            category_id=1,
        )

        with pytest.raises(DatabaseException) as exc_info:
            await check_existing_product_using_name(product=product_data, db=mock_db)

        assert "already exists" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_product_not_exists_no_exception(self):
        """Test that function doesn't raise exception when product doesn't exist"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock no existing product
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute.return_value = mock_result

        product_data = ProductCreate(
            name="New Product",
            price=100.0,
            quantity=10,
            category_id=1,
        )

        # Should not raise exception
        await check_existing_product_using_name(product=product_data, db=mock_db)


class TestCheckExistingProductUsingId:
    """Test check_existing_product_using_id with async operations"""

    @pytest.mark.asyncio
    async def test_product_exists_raises_exception(self):
        """Test that function raises exception when product with ID exists"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock existing product
        mock_product = Product(id=1, name="Product", price=100, quantity=10, category_id=1)

        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_product
        mock_db.execute.return_value = mock_result

        product_data = ProductCreate(
            id=1,
            name="New Product",
            price=100.0,
            quantity=10,
            category_id=1,
        )

        with pytest.raises(DatabaseException) as exc_info:
            await check_existing_product_using_id(product=product_data, db=mock_db)

        assert "already exists" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_product_not_exists_no_exception(self):
        """Test that function doesn't raise exception when product doesn't exist"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock no existing product
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute.return_value = mock_result

        product_data = ProductCreate(
            id=999,
            name="New Product",
            price=100.0,
            quantity=10,
            category_id=1,
        )

        # Should not raise exception
        await check_existing_product_using_id(product=product_data, db=mock_db)


class TestHandleMissingProduct:
    """Test handle_missing_product function"""

    def test_handle_missing_product_returns_error(self):
        """Test missing product handler returns error response"""
        response = handle_missing_product(product_id="999")

        assert response["status"] == ResponseStatus.E.value
        assert "not found" in response["message"]["response"].lower()
        assert "999" in response["message"]["response"]

    def test_handle_missing_product_various_ids(self):
        """Test with various product IDs"""
        test_ids = ["1", "999", "abc", "0"]

        for product_id in test_ids:
            response = handle_missing_product(product_id=product_id)

            assert response["status"] == ResponseStatus.E.value
            assert product_id in response["message"]["response"]


class TestApplyDiscountOrTax:
    """Test apply_discount_or_tax function"""

    def test_apply_discount_even_id(self):
        """Test applying tax to product with even ID"""
        product = Product(id=2, name="Test", price=100, quantity=10, category_id=1)

        # Mock the decorator pattern
        with patch('src.services.product_service.ConcretePrice') as mock_concrete, \
             patch('src.services.product_service.TaxDecorator') as mock_tax:

            mock_price = Mock()
            mock_price.get_amount.return_value = 120  # 20% tax
            mock_tax.return_value = mock_price
            mock_concrete.return_value = Mock()

            result = apply_discount_or_tax(product)

            assert result.price_type == "taxed"

    def test_apply_tax_odd_id(self):
        """Test applying discount to product with odd ID"""
        product = Product(id=1, name="Test", price=100, quantity=10, category_id=1)

        # Mock the decorator pattern
        with patch('src.services.product_service.ConcretePrice') as mock_concrete, \
             patch('src.services.product_service.DiscountDecorator') as mock_discount:

            mock_price = Mock()
            mock_price.get_amount.return_value = 80  # 20% discount
            mock_discount.return_value = mock_price
            mock_concrete.return_value = Mock()

            result = apply_discount_or_tax(product)

            assert result.price_type == "discounted"


class TestPostProduct:
    """Test post_product function with async operations"""

    @pytest.mark.asyncio
    async def test_create_product_success(self):
        """Test successful product creation"""
        mock_db = AsyncMock(spec=AsyncSession)

        product_data = ProductCreate(
            name="New Product",
            price=150.0,
            quantity=20,
            category_id=1,
        )

        # Mock no existing product (name check)
        mock_result_name = Mock()
        mock_result_name.scalars.return_value.first.return_value = None

        # Mock no existing product (id check)
        mock_result_id = Mock()
        mock_result_id.scalars.return_value.first.return_value = None

        # Mock category exists
        mock_category = Category(id=1, name="electronics")
        mock_result_category = Mock()
        mock_result_category.scalars.return_value.first.return_value = mock_category

        mock_db.execute = AsyncMock(side_effect=[mock_result_name, mock_result_id, mock_result_category])

        # Mock database operations
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        # Execute
        response = await post_product(
            user_email="test@test.com",
            product=product_data,
            db=mock_db
        )

        # Verify
        assert response["status"] == ResponseStatus.S.value
        assert "inserted product" in response["message"]

    @pytest.mark.asyncio
    async def test_create_product_missing_category(self):
        """Test product creation with non-existent category"""
        mock_db = AsyncMock(spec=AsyncSession)

        product_data = ProductCreate(
            name="Orphan Product",
            price=100.0,
            quantity=10,
            category_id=999,
        )

        # Mock no existing product (name check)
        mock_result_name = Mock()
        mock_result_name.scalars.return_value.first.return_value = None

        # Mock no existing product (id check)
        mock_result_id = Mock()
        mock_result_id.scalars.return_value.first.return_value = None

        # Mock category doesn't exist
        mock_result_category = Mock()
        mock_result_category.scalars.return_value.first.return_value = None

        mock_db.execute = AsyncMock(side_effect=[mock_result_name, mock_result_id, mock_result_category])

        # Execute
        response = await post_product(
            user_email="test@test.com",
            product=product_data,
            db=mock_db
        )

        # Verify
        assert response["status"] == ResponseStatus.E.value
        assert "category" in response["message"]["response"].lower()


class TestGetAllProducts:
    """Test get_all_products function"""

    @pytest.mark.asyncio
    async def test_get_all_products_empty(self):
        """Test getting all products when none exist"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock empty result
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result

        # Execute
        response = await get_all_products(user_email="test@test.com", db=mock_db)

        # Verify
        assert response["status"] == ResponseStatus.S.value
        assert isinstance(response["message"]["products"], list)
        assert len(response["message"]["products"]) == 0

    @pytest.mark.asyncio
    async def test_get_all_products_with_data(self):
        """Test getting all products when products exist"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock products
        mock_products = [
            Product(id=1, name="Product 1", price=100, quantity=10, category_id=1),
            Product(id=2, name="Product 2", price=200, quantity=20, category_id=1),
        ]

        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_products
        mock_db.execute.return_value = mock_result

        # Execute
        response = await get_all_products(user_email="test@test.com", db=mock_db)

        # Verify
        assert response["status"] == ResponseStatus.S.value
        products = response["message"]["products"]
        assert len(products) == 2


class TestGetSpecificProduct:
    """Test get_specific_product function"""

    @pytest.mark.asyncio
    async def test_get_existing_product(self):
        """Test getting an existing product by ID"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock product
        mock_product = Product(id=1, name="Test Product", price=100, quantity=10, category_id=1)

        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_product
        mock_db.execute.return_value = mock_result

        # Execute
        response = await get_specific_product(
            user_email="test@test.com",
            product_id=1,
            db=mock_db
        )

        # Verify
        assert response["status"] == ResponseStatus.S.value
        product = response["message"]["product"]
        assert product.id == 1
        assert product.name == "Test Product"

    @pytest.mark.asyncio
    async def test_get_nonexistent_product(self):
        """Test getting a non-existent product by ID"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock no product found
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute.return_value = mock_result

        # Execute
        response = await get_specific_product(
            user_email="test@test.com",
            product_id=999,
            db=mock_db
        )

        # Verify
        assert response["status"] == ResponseStatus.E.value
        assert "not found" in response["message"]["response"].lower()


class TestGetCategorySpecificProducts:
    """Test get_category_specific_products function"""

    @pytest.mark.asyncio
    async def test_get_products_by_existing_category(self):
        """Test getting products by existing category"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock products
        mock_products = [
            Product(id=1, name="Product 1", price=100, quantity=10, category_id=1),
            Product(id=2, name="Product 2", price=200, quantity=20, category_id=1),
        ]

        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_products
        mock_db.execute.return_value = mock_result

        # Execute
        response = await get_category_specific_products(
            user_email="test@test.com",
            category_id=1,
            db=mock_db
        )

        # Verify
        assert response["status"] == ResponseStatus.S.value
        products = response["message"][f"products with category id: 1"]
        assert len(products) == 2

    @pytest.mark.asyncio
    async def test_get_products_by_nonexistent_category(self):
        """Test getting products by non-existent category"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock empty result
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result

        # Execute
        response = await get_category_specific_products(
            user_email="test@test.com",
            category_id=999,
            db=mock_db
        )

        # Verify
        assert response["status"] == ResponseStatus.S.value
        products = response["message"][f"products with category id: 999"]
        assert len(products) == 0


class TestDeleteProduct:
    """Test delete_product function"""

    @pytest.mark.asyncio
    async def test_delete_existing_product(self):
        """Test deleting an existing product"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock existing product
        mock_product = Product(id=1, name="Product to Delete", price=100, quantity=10, category_id=1)

        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_product
        mock_db.execute = AsyncMock(return_value=mock_result)

        # Mock delete operations
        mock_db.delete = AsyncMock()
        mock_db.commit = AsyncMock()

        # Execute
        response = await delete_product(
            current_user_email="test@test.com",
            product_id=1,
            db=mock_db
        )

        # Verify
        assert response["status"] == ResponseStatus.S.value
        deleted_product = response["message"]["deleted product"]
        assert deleted_product.id == 1

    @pytest.mark.asyncio
    async def test_delete_nonexistent_product(self):
        """Test deleting a non-existent product"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock no product found
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute.return_value = mock_result

        # Execute
        response = await delete_product(
            current_user_email="test@test.com",
            product_id=999,
            db=mock_db
        )

        # Verify
        assert response["status"] == ResponseStatus.E.value
        assert "not found" in response["message"]["response"].lower()


class TestProductServiceIntegration:
    """Integration tests for product service functions"""

    @pytest.mark.asyncio
    async def test_product_lifecycle_workflow(self):
        """Test complete product lifecycle workflow"""
        mock_db = AsyncMock(spec=AsyncSession)

        # 1. Create product
        product_data = ProductCreate(
            name="Lifecycle Product",
            price=100.0,
            quantity=10,
            category_id=1,
        )

        # Mock checks and category
        mock_result_checks = Mock()
        mock_result_checks.scalars.return_value.first.return_value = None

        mock_category = Category(id=1, name="electronics")
        mock_result_category = Mock()
        mock_result_category.scalars.return_value.first.return_value = mock_category

        mock_db.execute = AsyncMock(side_effect=[
            mock_result_checks,  # Name check
            mock_result_checks,  # ID check
            mock_result_category  # Category check
        ])

        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        create_response = await post_product(
            user_email="test@test.com",
            product=product_data,
            db=mock_db
        )

        assert create_response["status"] == ResponseStatus.S.value
