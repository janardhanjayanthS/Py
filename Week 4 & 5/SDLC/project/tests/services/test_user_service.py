# test_user_service.py - Tests for user service layer with new async architecture
from unittest.mock import AsyncMock, Mock

import pytest
from src.core.exceptions import AuthenticationException
from src.models.user import User

# Legacy imports for backward compatibility tests
from src.repository.user_repo import UserRepository
from src.schema.user import UserEdit, UserLogin, UserRegister, UserRole
from src.services.user_service import UserService


@pytest.fixture
def mock_repo():
    """Create a mock repository for testing"""
    repo = AsyncMock(spec=UserRepository)
    return repo


@pytest.fixture
def user_service(mock_repo):
    """Create UserService instance with mock repository"""
    return UserService(repo=mock_repo)


@pytest.fixture
def sample_user_register():
    """Sample user registration data"""
    return UserRegister(
        name="Test User",
        email="test@example.com",
        password="TestPass123!",
        role=UserRole.STAFF,
    )


@pytest.fixture
def sample_user_login():
    """Sample user login data"""
    return UserLogin(email="test@example.com", password="TestPass123!")


@pytest.fixture
def sample_user_edit():
    """Sample user edit data"""
    return UserEdit(new_name="Updated Name", new_password="UpdatedPass123!")


class TestUserService:
    """Test suite for UserService class with async operations"""

    pass


class TestUserServiceRegister:
    """Test user registration functionality"""

    @pytest.mark.asyncio
    async def test_register_user_success(
        self, user_service, mock_repo, sample_user_register
    ):
        """Test successful user registration"""
        # Setup mock
        mock_repo.check_existing_user_using_email.return_value = None
        mock_user = User(
            id=1,
            name=sample_user_register.name,
            email=sample_user_register.email,
            password="hashed_password",
            role=sample_user_register.role.value,
        )
        mock_repo.create_user.return_value = mock_user

        # Execute
        result = await user_service.register_user(sample_user_register)

        # Verify
        assert result == mock_user
        mock_repo.check_existing_user_using_email.assert_called_once_with(
            user=sample_user_register
        )
        mock_repo.create_user.assert_called_once_with(user=sample_user_register)

    @pytest.mark.asyncio
    async def test_register_user_existing_email(
        self, user_service, mock_repo, sample_user_register
    ):
        """Test registration with existing email raises exception"""
        # Setup mock to raise exception for existing user
        mock_repo.check_existing_user_using_email.side_effect = AuthenticationException(
            message="User with this email already exists"
        )

        # Execute and verify
        with pytest.raises(AuthenticationException) as exc_info:
            await user_service.register_user(sample_user_register)

        assert "already exists" in str(exc_info.value)
        mock_repo.check_existing_user_using_email.assert_called_once_with(
            user=sample_user_register
        )
        mock_repo.create_user.assert_not_called()


class TestUserServiceLogin:
    """Test user login functionality"""

    @pytest.mark.asyncio
    async def test_login_user_success(self, user_service, mock_repo, sample_user_login):
        """Test successful user login"""
        # Setup mock
        mock_user = User(
            id=1,
            name="Test User",
            email=sample_user_login.email,
            password="hashed_password",
            role=UserRole.STAFF.value,
        )
        mock_repo.authenticate_user.return_value = mock_user

        # Execute
        result = await user_service.login_user(sample_user_login)

        # Verify
        assert isinstance(result, str)  # JWT token should be a string
        assert len(result) > 0  # Token should not be empty
        mock_repo.authenticate_user.assert_called_once_with(
            email=sample_user_login.email, password=sample_user_login.password
        )

    @pytest.mark.asyncio
    async def test_login_user_invalid_credentials(
        self, user_service, mock_repo, sample_user_login
    ):
        """Test login with invalid credentials raises exception"""
        # Setup mock to return None (authentication failed)
        mock_repo.authenticate_user.return_value = None
        mock_repo.handle_unknown_user = Mock(
            side_effect=AuthenticationException(message="Incorrect email or password")
        )

        # Execute and verify
        with pytest.raises(AuthenticationException) as exc_info:
            await user_service.login_user(sample_user_login)

        assert "Incorrect email or password" in str(exc_info.value)
        mock_repo.authenticate_user.assert_called_once_with(
            email=sample_user_login.email, password=sample_user_login.password
        )
        mock_repo.handle_unknown_user.assert_called_once_with(
            email_id=sample_user_login.email
        )


class TestUserServiceUpdate:
    """Test user update functionality"""

    @pytest.mark.asyncio
    async def test_update_user_success(self, user_service, mock_repo, sample_user_edit):
        """Test successful user update"""
        # Setup mock
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role=UserRole.STAFF.value,
        )
        mock_repo.fetch_user_by_email.return_value = mock_user
        mock_repo.get_update_user_message.return_value = "User updated successfully"

        # Execute
        message, updated_user = await user_service.update_user(
            "test@example.com", sample_user_edit
        )

        # Verify
        assert message == "User updated successfully"
        assert updated_user == mock_user
        mock_repo.fetch_user_by_email.assert_called_once_with(
            email_id="test@example.com"
        )
        mock_repo.get_update_user_message.assert_called_once_with(
            current_user=mock_user, update_details=sample_user_edit
        )


class TestUserServiceGetUsers:
    """Test get all users functionality"""

    @pytest.mark.asyncio
    async def test_get_users_success(self, user_service, mock_repo):
        """Test successful retrieval of all users"""
        # Setup mock
        mock_users = [
            User(
                id=1,
                name="User 1",
                email="user1@example.com",
                password="hash1",
                role="staff",
            ),
            User(
                id=2,
                name="User 2",
                email="user2@example.com",
                password="hash2",
                role="admin",
            ),
        ]
        mock_repo.fetch_all_users.return_value = mock_users

        # Execute
        result = await user_service.get_users("admin@example.com")

        # Verify
        assert len(result) == 2
        assert result == mock_users
        mock_repo.fetch_all_users.assert_called_once()


class TestUserServiceDelete:
    """Test user deletion functionality"""

    @pytest.mark.asyncio
    async def test_delete_user_success(self, user_service, mock_repo):
        """Test successful user deletion"""
        # Setup mock
        mock_user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            role=UserRole.STAFF.value,
        )
        mock_repo.delete_user.return_value = mock_user

        # Execute
        result = await user_service.delete_user(1, "admin@example.com")

        # Verify
        assert result == mock_user
        mock_repo.delete_user.assert_called_once_with(user_id=1)
