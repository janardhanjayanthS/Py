# test_user_repo.py - Tests for UserRepository with async operations
import pytest
from unittest.mock import AsyncMock, Mock
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AuthenticationException
from src.models.user import User
from src.repository.user_repo import UserRepository
from src.schema.user import UserEdit, UserRegister, UserRole
from src.services.models import ResponseStatus


class TestUserRepository:
    """Test suite for UserRepository class"""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session"""
        session = AsyncMock(spec=AsyncSession)
        return session

    @pytest.fixture
    def user_repo(self, mock_session):
        """Create UserRepository instance with mock session"""
        return UserRepository(session=mock_session)

    @pytest.fixture
    def sample_user_register(self):
        """Sample user registration data"""
        return UserRegister(
            name="Test User",
            email="test@example.com",
            password="TestPass123!",
            role=UserRole.STAFF
        )

    @pytest.fixture
    def sample_user_edit(self):
        """Sample user edit data"""
        return UserEdit(
            new_name="Updated Name",
            new_password="UpdatedPass123!"
        )


class TestUserRepositoryCreate:
    """Test user creation functionality"""

    @pytest.mark.asyncio
    async def test_create_user_success(self, user_repo, mock_session, sample_user_register):
        """Test successful user creation"""
        # Mock the database operations
        mock_session.add = Mock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()

        # Execute
        result = await user_repo.create_user(sample_user_register)

        # Verify
        assert isinstance(result, User)
        assert result.name == sample_user_register.name
        assert result.email == sample_user_register.email
        assert result.role == sample_user_register.role.value
        assert result.password != sample_user_register.password  # Should be hashed
        
        # Verify database operations were called
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(result)

    @pytest.mark.asyncio
    async def test_create_user_with_different_roles(self, user_repo, mock_session):
        """Test creating users with different roles"""
        mock_session.add = Mock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()

        roles = [UserRole.STAFF, UserRole.MANAGER, UserRole.ADMIN]
        
        for role in roles:
            user_data = UserRegister(
                name=f"Test {role.value}",
                email=f"test{role.value}@example.com",
                password="TestPass123!",
                role=role
            )
            
            result = await user_repo.create_user(user_data)
            
            assert result.role == role.value
            assert result.name == f"Test {role.value}"


class TestUserRepositoryAuthenticate:
    """Test user authentication functionality"""

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, user_repo, mock_session):
        """Test successful user authentication"""
        # Setup mock user
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )
        
        # Mock database query
        mock_result = AsyncMock()
        mock_result.scalars.return_value.first.return_value = mock_user
        mock_session.execute.return_value = mock_result
        
        # Mock password verification
        user_repo.verify_password = Mock(return_value=True)
        
        # Execute
        result = await user_repo.authenticate_user("test@example.com", "password123")
        
        # Verify
        assert result == mock_user
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(self, user_repo, mock_session):
        """Test authentication with non-existent user"""
        # Mock database query to return None
        mock_result = AsyncMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_session.execute.return_value = mock_result
        
        # Execute
        result = await user_repo.authenticate_user("nonexistent@example.com", "password123")
        
        # Verify
        assert result is None

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self, user_repo, mock_session):
        """Test authentication with wrong password"""
        # Setup mock user
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )
        
        # Mock database query
        mock_result = AsyncMock()
        mock_result.scalars.return_value.first.return_value = mock_user
        mock_session.execute.return_value = mock_result
        
        # Mock password verification to fail
        user_repo.verify_password = Mock(return_value=False)
        
        # Execute
        result = await user_repo.authenticate_user("test@example.com", "wrongpassword")
        
        # Verify
        assert result is None


class TestUserRepositoryFetch:
    """Test user fetching functionality"""

    @pytest.mark.asyncio
    async def test_fetch_user_by_email_success(self, user_repo, mock_session):
        """Test successful user fetch by email"""
        # Setup mock user
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )
        
        # Mock database query
        mock_result = AsyncMock()
        mock_result.scalars.return_value.first.return_value = mock_user
        mock_session.execute.return_value = mock_result
        
        # Execute
        result = await user_repo.fetch_user_by_email("test@example.com")
        
        # Verify
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_fetch_user_by_email_not_found(self, user_repo, mock_session):
        """Test fetching non-existent user by email"""
        # Mock database query to return None
        mock_result = AsyncMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_session.execute.return_value = mock_result
        
        # Execute
        result = await user_repo.fetch_user_by_email("nonexistent@example.com")
        
        # Verify
        assert result is None

    @pytest.mark.asyncio
    async def test_fetch_all_users_success(self, user_repo, mock_session):
        """Test successful fetch of all users"""
        # Setup mock users
        mock_users = [
            User(id=1, name="User 1", email="user1@example.com", password="hash1", role="staff"),
            User(id=2, name="User 2", email="user2@example.com", password="hash2", role="admin")
        ]
        
        # Mock database query
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = mock_users
        mock_session.execute.return_value = mock_result
        
        # Execute
        result = await user_repo.fetch_all_users()
        
        # Verify
        assert len(result) == 2
        assert result == mock_users


class TestUserRepositoryUpdate:
    """Test user update functionality"""

    @pytest.mark.asyncio
    async def test_update_user_name_success(self, user_repo, mock_session, sample_user_edit):
        """Test successful user name update"""
        # Setup mock user
        mock_user = User(
            id=1,
            name="Old Name",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )
        
        # Execute
        result = user_repo.update_user_name(mock_user, sample_user_edit)
        
        # Verify
        assert "updated" in result.lower()
        assert mock_user.name == sample_user_edit.new_name

    @pytest.mark.asyncio
    async def test_update_user_name_same_name(self, user_repo, mock_session):
        """Test updating user name to same value"""
        # Setup mock user
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )
        
        # Edit with same name
        edit_data = UserEdit(new_name="Test User")
        
        # Execute
        result = user_repo.update_user_name(mock_user, edit_data)
        
        # Verify
        assert "same" in result.lower()
        assert mock_user.name == "Test User"

    @pytest.mark.asyncio
    async def test_update_user_password_success(self, user_repo, mock_session, sample_user_edit):
        """Test successful user password update"""
        # Setup mock user
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="old_hashed_password",
            role="staff"
        )
        
        # Mock hash_password function
        user_repo.hash_password = Mock(return_value="new_hashed_password")
        
        # Execute
        result = user_repo.update_user_password(mock_user, sample_user_edit)
        
        # Verify
        assert "password updated" in result.lower()
        assert mock_user.password == "new_hashed_password"

    @pytest.mark.asyncio
    async def test_get_update_user_message(self, user_repo, mock_session, sample_user_edit):
        """Test getting update user message"""
        # Setup mock user
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )
        
        # Mock database operations
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        # Mock the individual update methods
        user_repo.update_user_name = Mock(return_value="Name updated. ")
        user_repo.update_user_password = Mock(return_value="Password updated")
        
        # Execute
        result = await user_repo.get_update_user_message(mock_user, sample_user_edit)
        
        # Verify
        assert "Name updated." in result
        assert "Password updated" in result
        mock_session.commit.assert_called_once()


class TestUserRepositoryDelete:
    """Test user deletion functionality"""

    @pytest.mark.asyncio
    async def test_delete_user_success(self, user_repo, mock_session):
        """Test successful user deletion"""
        # Setup mock user
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )
        
        # Mock database query to find user
        mock_result = AsyncMock()
        mock_result.scalars.return_value.first.return_value = mock_user
        mock_session.execute.return_value = mock_result
        
        # Mock delete operations
        mock_session.delete = Mock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        # Execute
        result = await user_repo.delete_user(1)
        
        # Verify
        assert result == mock_user
        mock_session.delete.assert_called_once_with(mock_user)
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, user_repo, mock_session):
        """Test deleting non-existent user"""
        # Mock database query to return None
        mock_result = AsyncMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_session.execute.return_value = mock_result
        
        # Mock handle_missing_user method
        expected_response = {
            "status": ResponseStatus.E.value,
            "message": {"response": "Unable to find user with id: 999"}
        }
        user_repo.handle_missing_user = Mock(return_value=expected_response)
        
        # Execute
        result = await user_repo.delete_user(999)
        
        # Verify
        assert result == expected_response
        user_repo.handle_missing_user.assert_called_once_with(user_id=999)


class TestUserRepositoryHelpers:
    """Test helper methods"""

    def test_handle_missing_user(self, user_repo):
        """Test handle_missing_user method"""
        result = user_repo.handle_missing_user(999)
        
        expected = {
            "status": ResponseStatus.E.value,
            "message": {"response": "Unable to find user with id: 999"}
        }
        
        assert result == expected

    def test_handle_unknown_user(self, user_repo):
        """Test handle_unknown_user method raises exception"""
        with pytest.raises(AuthenticationException) as exc_info:
            user_repo.handle_unknown_user("test@example.com")
        
        assert "Incorrect email or password" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_check_existing_user_using_email_true(self, user_repo, mock_session):
        """Test checking existing user returns True when user exists"""
        # Setup mock user
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role="staff"
        )
        
        # Mock fetch_user_by_email to return user
        user_repo.fetch_user_by_email = AsyncMock(return_value=mock_user)
        
        # Execute
        user_data = UserRegister(
            name="Test User",
            email="test@example.com",
            password="TestPass123!",
            role=UserRole.STAFF
        )
        result = await user_repo.check_existing_user_using_email(user_data)
        
        # Verify
        assert result is True

    @pytest.mark.asyncio
    async def test_check_existing_user_using_email_false(self, user_repo, mock_session):
        """Test checking existing user returns False when user doesn't exist"""
        # Mock fetch_user_by_email to return None
        user_repo.fetch_user_by_email = AsyncMock(return_value=None)
        
        # Execute
        user_data = UserRegister(
            name="Test User",
            email="nonexistent@example.com",
            password="TestPass123!",
            role=UserRole.STAFF
        )
        result = await user_repo.check_existing_user_using_email(user_data)
        
        # Verify
        assert result is False


# Integration Tests

class TestUserRepositoryIntegration:
    """Integration tests for UserRepository with real async session"""

    @pytest.mark.asyncio
    async def test_user_repository_integration(self, async_test_db):
        """Test UserRepository with real async session"""
        # Create real repository
        repo = UserRepository(session=async_test_db)

        # Test data
        user_data = UserRegister(
            name="Integration User",
            email="integration@example.com",
            password="IntegrationPass123!",
            role=UserRole.STAFF
        )

        # Test create user
        created_user = await repo.create_user(user_data)
        assert created_user.email == user_data.email
        assert created_user.name == user_data.name

        # Test fetch user by email
        fetched_user = await repo.fetch_user_by_email(user_data.email)
        assert fetched_user is not None
        assert fetched_user.id == created_user.id

        # Test authenticate user
        auth_user = await repo.authenticate_user(user_data.email, user_data.password)
        assert auth_user is not None
        assert auth_user.email == user_data.email

        # Test update user
        edit_data = UserEdit(new_name="Updated Integration User")
        message = await repo.get_update_user_message(fetched_user, edit_data)
        assert "updated" in message.lower()

        # Test fetch all users
        all_users = await repo.fetch_all_users()
        assert len(all_users) >= 1
        assert any(u.email == user_data.email for u in all_users)

        # Test delete user
        deleted_user = await repo.delete_user(created_user.id)
        assert deleted_user.id == created_user.id

        # Verify user is deleted
        deleted_check = await repo.fetch_user_by_email(user_data.email)
        assert deleted_check is None
