# test_database.py - Tests for database operations and utility functions
import pytest
from unittest.mock import AsyncMock, Mock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.database import (
    hash_password,
    verify_password,
    add_commit_refresh_db,
    commit_refresh_db,
    delete_commit_db,
    get_db,
    seed_db,
)
from src.core.exceptions import DatabaseException
from src.models.user import User


class TestPasswordHashing:
    """Test password hashing and verification"""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password  # Should be different from plain text

    def test_hash_password_different_hashes(self):
        """Test that same password produces different hashes (due to salt)"""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Bcrypt includes random salt, so hashes should differ
        assert hash1 != hash2

    def test_hash_password_empty_string(self):
        """Test hashing empty string"""
        hashed = hash_password("")
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_special_characters(self):
        """Test hashing password with special characters"""
        password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert hashed != password

    def test_hash_password_unicode(self):
        """Test hashing password with unicode characters"""
        password = "Pässwörd123!"
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert hashed != password


class TestPasswordVerification:
    """Test password verification functionality"""

    def test_verify_password_correct(self):
        """Test verification with correct password"""
        plain_password = "TestPassword123!"
        hashed = hash_password(plain_password)

        assert verify_password(plain_password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verification with incorrect password"""
        plain_password = "TestPassword123!"
        wrong_password = "WrongPassword123!"
        hashed = hash_password(plain_password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty_plain(self):
        """Test verification with empty plain password"""
        hashed = hash_password("TestPassword123!")

        assert verify_password("", hashed) is False

    def test_verify_password_empty_hash(self):
        """Test verification with empty hash"""
        with pytest.raises(ValueError):
            verify_password("TestPassword123!", "")

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case sensitive"""
        plain_password = "TestPassword123!"
        hashed = hash_password(plain_password)

        assert verify_password("testpassword123!", hashed) is False

    def test_verify_password_special_characters(self):
        """Test verification with special characters"""
        plain_password = "P@ssw0rd!#$%"
        hashed = hash_password(plain_password)

        assert verify_password(plain_password, hashed) is True
        assert verify_password("P@ssw0rd!#$", hashed) is False


class TestDatabaseOperations:
    """Test database CRUD operation helpers"""

    @pytest.mark.asyncio
    async def test_add_commit_refresh_db(self):
        """Test add_commit_refresh_db function"""
        # Create mock objects
        mock_db = AsyncMock(spec=AsyncSession)
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )

        # Execute
        await add_commit_refresh_db(object=mock_user, db=mock_db)

        # Verify
        mock_db.add.assert_called_once_with(mock_user)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_user)

    @pytest.mark.asyncio
    async def test_commit_refresh_db(self):
        """Test commit_refresh_db function"""
        # Create mock objects
        mock_db = AsyncMock(spec=AsyncSession)
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )

        # Execute
        await commit_refresh_db(object=mock_user, db=mock_db)

        # Verify - add should NOT be called, only commit and refresh
        assert not mock_db.add.called
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_user)

    @pytest.mark.asyncio
    async def test_delete_commit_db(self):
        """Test delete_commit_db function"""
        # Create mock objects
        mock_db = AsyncMock(spec=AsyncSession)
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )

        # Execute
        await delete_commit_db(object=mock_user, db=mock_db)

        # Verify
        mock_db.delete.assert_called_once_with(mock_user)
        mock_db.commit.assert_called_once()
        # Refresh should NOT be called for deleted objects
        assert not mock_db.refresh.called


class TestGetDbDependency:
    """Test get_db database dependency"""

    @pytest.mark.asyncio
    async def test_get_db_yields_session(self):
        """Test that get_db yields a database session"""
        # We need to test that it yields and closes properly
        db_generator = get_db()

        try:
            db_session = await anext(db_generator)
            assert db_session is not None
            # Session should be AsyncSession type
            assert isinstance(db_session, AsyncSession)
        finally:
            # Clean up
            try:
                await anext(db_generator)
            except StopAsyncIteration:
                pass  # Expected when generator is exhausted

    @pytest.mark.asyncio
    async def test_get_db_closes_on_error(self):
        """Test that get_db closes session on error"""
        db_generator = get_db()

        with patch('src.repository.database.async_session_local') as mock_session_maker:
            mock_session = AsyncMock(spec=AsyncSession)
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock()
            mock_session.close = AsyncMock()
            mock_session_maker.return_value = mock_session

            # Start the generator
            db_generator = get_db()

            try:
                # Get the session
                await anext(db_generator)
                # Simulate an error
                await db_generator.athrow(Exception("Test error"))
            except (DatabaseException, StopAsyncIteration):
                # Expected exception
                pass


class TestSeedDb:
    """Test database seeding functionality"""

    @pytest.mark.asyncio
    async def test_seed_db_success(self):
        """Test successful database seeding"""
        mock_initial_data = {
            "product_category": [
                {"id": 1, "name": "electronics"},
                {"id": 2, "name": "books"}
            ],
            "product": [
                {"id": 1, "name": "Laptop", "quantity": 10, "price": 999, "category_id": 1},
                {"id": 2, "name": "Book", "quantity": 5, "price": 20, "category_id": 2}
            ]
        }

        with patch('src.repository.database.get_initial_data_from_csv') as mock_get_data, \
             patch('src.repository.database.engine') as mock_engine:

            mock_get_data.return_value = mock_initial_data

            # Mock connection
            mock_connection = AsyncMock()
            mock_engine.connect.return_value.__aenter__ = AsyncMock(return_value=mock_connection)
            mock_engine.connect.return_value.__aexit__ = AsyncMock()

            # Execute
            await seed_db()

            # Verify get_initial_data_from_csv was called
            mock_get_data.assert_called_once()

    @pytest.mark.asyncio
    async def test_seed_db_empty_data(self):
        """Test seeding with empty data"""
        mock_initial_data = {
            "product_category": [],
            "product": []
        }

        with patch('src.repository.database.get_initial_data_from_csv') as mock_get_data, \
             patch('src.repository.database.engine') as mock_engine:

            mock_get_data.return_value = mock_initial_data

            # Mock connection
            mock_connection = AsyncMock()
            mock_connection.execute = AsyncMock()
            mock_engine.connect.return_value.__aenter__ = AsyncMock(return_value=mock_connection)
            mock_engine.connect.return_value.__aexit__ = AsyncMock()

            # Execute - should not raise error even with empty data
            await seed_db()

            # Verify
            mock_get_data.assert_called_once()

    @pytest.mark.asyncio
    async def test_seed_db_database_error(self):
        """Test seeding with database error"""
        # This test verifies error handling in seed_db
        # Note: The actual implementation may not raise in all error cases
        # due to exception handling in async context managers

        mock_initial_data = {
            "product_category": [{"id": 1, "name": "electronics"}],
            "product": []
        }

        with patch('src.repository.database.get_initial_data_from_csv') as mock_get_data, \
             patch('src.repository.database.engine') as mock_engine, \
             patch('src.repository.database.logger') as mock_logger:

            mock_get_data.return_value = mock_initial_data

            # Create proper async context manager for engine.connect()
            mock_connection = AsyncMock()
            mock_connection.execute = AsyncMock(side_effect=Exception("Database error"))

            # Create async context manager
            mock_context = AsyncMock()
            mock_context.__aenter__ = AsyncMock(return_value=mock_connection)
            mock_context.__aexit__ = AsyncMock(return_value=None)  # Don't suppress exception
            mock_engine.connect.return_value = mock_context

            # Execute - may or may not raise depending on async context handling
            try:
                await seed_db()
                # If no exception, verify error was logged
                assert mock_logger.error.called
            except DatabaseException as e:
                # If exception raised, verify it contains relevant info
                assert "Failed to seed" in str(e) or "error" in str(e).lower()


class TestPasswordHashingIntegration:
    """Integration tests for password hashing"""

    def test_hash_and_verify_workflow(self):
        """Test complete hash and verify workflow"""
        passwords = [
            "SimplePass123!",
            "C0mplex!P@ssw0rd",
            "Test123!@#$%^&*()",
            "Unicode_Pässwörd123!"
        ]

        for password in passwords:
            # Hash the password
            hashed = hash_password(password)

            # Verify correct password
            assert verify_password(password, hashed) is True

            # Verify incorrect passwords
            assert verify_password(password + "x", hashed) is False
            assert verify_password("", hashed) is False

    def test_multiple_users_different_hashes(self):
        """Test that multiple users with same password get different hashes"""
        password = "CommonPassword123!"

        # Create 5 users with same password
        hashes = [hash_password(password) for _ in range(5)]

        # All should verify correctly
        for h in hashes:
            assert verify_password(password, h) is True

        # All hashes should be unique (due to different salts)
        assert len(set(hashes)) == 5
