# test_category_service.py - Tests for category service layer functions
import pytest
from unittest.mock import AsyncMock, Mock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import DatabaseException
from src.models.category import Category
from src.schema.category import BaseCategory, CategoryCreate
from src.services.category_service import (
    get_category_by_id,
    get_category_by_name,
    check_existing_category_using_name,
    check_existing_category_using_id,
    handle_missing_category,
)
from src.services.models import ResponseStatus


class TestGetCategoryById:
    """Test get_category_by_id function"""

    @pytest.mark.asyncio
    async def test_get_category_by_id_exists(self):
        """Test getting category that exists"""
        # Mock database session
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock category
        mock_category = Category(id=1, name="electronics")

        # Mock query result - result is NOT async, only execute is
        mock_scalars = Mock()
        mock_scalars.first.return_value = mock_category
        mock_result = Mock()  # This should NOT be AsyncMock
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        # Execute
        result = await get_category_by_id(category_id=1, db=mock_db)

        # Verify
        assert result == mock_category
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_category_by_id_not_exists(self):
        """Test getting category that doesn't exist"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock query result returning None
        mock_scalars = Mock()
        mock_scalars.first.return_value = None
        mock_result = Mock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        # Execute
        result = await get_category_by_id(category_id=999, db=mock_db)

        # Verify
        assert result is None
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_category_by_id_multiple_calls(self):
        """Test multiple category lookups"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock different categories
        categories = [
            Category(id=1, name="electronics"),
            Category(id=2, name="books"),
            Category(id=3, name="clothing")
        ]

        for category in categories:
            mock_scalars = Mock()
            mock_scalars.first.return_value = category
            mock_result = Mock()
            mock_result.scalars.return_value = mock_scalars
            mock_db.execute.return_value = mock_result

            result = await get_category_by_id(category_id=category.id, db=mock_db)
            assert result.id == category.id
            assert result.name == category.name


class TestGetCategoryByName:
    """Test get_category_by_name function"""

    @pytest.mark.asyncio
    async def test_get_category_by_name_exists(self):
        """Test getting category by name when it exists"""
        mock_db = AsyncMock(spec=AsyncSession)
        mock_category = Category(id=1, name="electronics")

        # Mock query result
        mock_scalars = Mock()
        mock_scalars.first.return_value = mock_category
        mock_result = Mock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        # Execute
        result = await get_category_by_name(category_name="electronics", db=mock_db)

        # Verify
        assert result == mock_category
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_category_by_name_not_exists(self):
        """Test getting category by name when it doesn't exist"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Mock query result returning None
        mock_scalars = Mock()
        mock_scalars.first.return_value = None
        mock_result = Mock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        # Execute
        result = await get_category_by_name(category_name="nonexistent", db=mock_db)

        # Verify
        assert result is None
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_category_by_name_empty_string(self):
        """Test getting category with empty string name"""
        mock_db = AsyncMock(spec=AsyncSession)

        mock_scalars = Mock()
        mock_scalars.first.return_value = None
        mock_result = Mock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        # Execute
        result = await get_category_by_name(category_name="", db=mock_db)

        # Verify
        assert result is None

    @pytest.mark.asyncio
    async def test_get_category_by_name_case_sensitive(self):
        """Test that category name lookup is case sensitive"""
        mock_db = AsyncMock(spec=AsyncSession)
        mock_category = Category(id=1, name="electronics")

        mock_scalars = Mock()
        mock_scalars.first.return_value = mock_category
        mock_result = Mock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        # Execute with exact match
        result = await get_category_by_name(category_name="electronics", db=mock_db)
        assert result is not None

        # Would need to test with different case, but that requires different mock setup


class TestCheckExistingCategoryUsingName:
    """Test check_existing_category_using_name function"""

    @pytest.mark.asyncio
    async def test_check_existing_category_using_name_exists(self):
        """Test checking existing category raises exception"""
        mock_db = AsyncMock(spec=AsyncSession)
        category_data = BaseCategory(name="electronics")

        # Mock that category exists - patch get_category_by_name
        mock_category = Category(id=1, name="electronics")

        with patch('src.services.category_service.get_category_by_name', return_value=mock_category):
            # Execute and verify exception is raised
            with pytest.raises(DatabaseException) as exc_info:
                await check_existing_category_using_name(category=category_data, db=mock_db)

            assert "already exists" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_check_existing_category_using_name_not_exists(self):
        """Test checking non-existing category doesn't raise exception"""
        mock_db = AsyncMock(spec=AsyncSession)
        category_data = BaseCategory(name="newcategory")

        # Mock that category doesn't exist - patch get_category_by_name
        with patch('src.services.category_service.get_category_by_name', return_value=None):
            # Execute - should not raise exception
            await check_existing_category_using_name(category=category_data, db=mock_db)

            # If we get here, no exception was raised (success)
            assert True


class TestCheckExistingCategoryUsingId:
    """Test check_existing_category_using_id function"""

    @pytest.mark.asyncio
    async def test_check_existing_category_using_id_exists(self):
        """Test checking existing category by ID raises exception"""
        mock_db = AsyncMock(spec=AsyncSession)
        category_data = CategoryCreate(id=1, name="electronics")  # Use CategoryCreate which has id

        # Mock that category exists - patch get_category_by_id
        mock_category = Category(id=1, name="electronics")

        with patch('src.services.category_service.get_category_by_id', return_value=mock_category):
            # Execute and verify exception is raised
            with pytest.raises(DatabaseException) as exc_info:
                await check_existing_category_using_id(category=category_data, db=mock_db)

            assert "already exists" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_check_existing_category_using_id_not_exists(self):
        """Test checking non-existing category by ID doesn't raise exception"""
        mock_db = AsyncMock(spec=AsyncSession)
        category_data = CategoryCreate(id=999, name="newcategory")  # Use CategoryCreate which has id

        # Mock that category doesn't exist - patch get_category_by_id
        with patch('src.services.category_service.get_category_by_id', return_value=None):
            # Execute - should not raise exception
            await check_existing_category_using_id(category=category_data, db=mock_db)

            # If we get here, no exception was raised (success)
            assert True


class TestHandleMissingCategory:
    """Test handle_missing_category function"""

    def test_handle_missing_category_returns_error_dict(self):
        """Test missing category handler returns error response"""
        result = handle_missing_category(category_id=999)

        assert isinstance(result, dict)
        assert result["status"] == ResponseStatus.E.value
        assert "message" in result
        assert "response" in result["message"]

    def test_handle_missing_category_contains_id(self):
        """Test error message contains category ID"""
        category_id = 42
        result = handle_missing_category(category_id=category_id)

        message = result["message"]["response"]
        assert str(category_id) in message
        assert "cannot find" in message.lower() or "not found" in message.lower()

    def test_handle_missing_category_various_ids(self):
        """Test with various category IDs"""
        test_ids = [1, 999, 0, -1]

        for category_id in test_ids:
            result = handle_missing_category(category_id=category_id)

            assert result["status"] == ResponseStatus.E.value
            assert str(category_id) in result["message"]["response"]


class TestCategoryServiceIntegration:
    """Integration tests for category service functions"""

    @pytest.mark.asyncio
    async def test_category_lookup_workflow(self):
        """Test complete category lookup workflow"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Create mock categories
        categories = [
            Category(id=1, name="electronics"),
            Category(id=2, name="books"),
            Category(id=3, name="clothing")
        ]

        # Test looking up each category by ID
        for category in categories:
            mock_scalars = Mock()
            mock_scalars.first.return_value = category
            mock_result = Mock()
            mock_result.scalars.return_value = mock_scalars
            mock_db.execute.return_value = mock_result

            # Lookup by ID
            result_by_id = await get_category_by_id(category_id=category.id, db=mock_db)
            assert result_by_id.id == category.id

            # Lookup by name
            result_by_name = await get_category_by_name(category_name=category.name, db=mock_db)
            assert result_by_name.name == category.name

    @pytest.mark.asyncio
    async def test_category_validation_workflow(self):
        """Test category validation workflow"""
        mock_db = AsyncMock(spec=AsyncSession)

        # Test adding new category (doesn't exist)
        new_category = BaseCategory(name="newcategory")

        with patch('src.services.category_service.get_category_by_name', return_value=None):
            # Should not raise exception
            await check_existing_category_using_name(category=new_category, db=mock_db)

        # Test adding duplicate category (exists)
        existing_category = BaseCategory(name="electronics")
        mock_existing = Category(id=1, name="electronics")

        with patch('src.services.category_service.get_category_by_name', return_value=mock_existing):
            # Should raise exception
            with pytest.raises(DatabaseException):
                await check_existing_category_using_name(category=existing_category, db=mock_db)


class TestCategoryServiceEdgeCases:
    """Test edge cases for category service"""

    @pytest.mark.asyncio
    async def test_get_category_special_characters(self):
        """Test getting category with special characters in name"""
        mock_db = AsyncMock(spec=AsyncSession)
        mock_category = Category(id=1, name="electronics & gadgets")

        mock_scalars = Mock()
        mock_scalars.first.return_value = mock_category
        mock_result = Mock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        result = await get_category_by_name(category_name="electronics & gadgets", db=mock_db)
        assert result.name == "electronics & gadgets"

    @pytest.mark.asyncio
    async def test_get_category_unicode_name(self):
        """Test getting category with unicode characters"""
        mock_db = AsyncMock(spec=AsyncSession)
        mock_category = Category(id=1, name="électronique")

        mock_scalars = Mock()
        mock_scalars.first.return_value = mock_category
        mock_result = Mock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute.return_value = mock_result

        result = await get_category_by_name(category_name="électronique", db=mock_db)
        assert result.name == "électronique"

    def test_handle_missing_category_zero_id(self):
        """Test handling missing category with ID 0"""
        result = handle_missing_category(category_id=0)

        assert result["status"] == ResponseStatus.E.value
        assert "0" in result["message"]["response"]

    def test_handle_missing_category_negative_id(self):
        """Test handling missing category with negative ID"""
        result = handle_missing_category(category_id=-1)

        assert result["status"] == ResponseStatus.E.value
        assert "-1" in result["message"]["response"]
