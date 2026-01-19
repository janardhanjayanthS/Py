# test_user_service.py - Tests for user service layer functions
import pytest
from sqlalchemy.orm import Session
from src.models.user import User
from src.repository.database import hash_password
from src.schema.user import UserEdit, UserRegister
from src.services.user_service import (
    authenticate_user,
    check_existing_user_using_email,
    fetch_user_by_email,
    update_user_name,
    update_user_password,
)


class TestCheckExistingUserUsingEmail:
    """Test suite for check_existing_user_using_email function"""

    def test_user_exists_returns_true(self, db_session: Session, staff_user: User):
        """Test that function returns True when user exists"""
        user_data = UserRegister(
            name="Test User",
            email=staff_user.email,
            password="TestPass123!",
            role="staff",
        )
        result = check_existing_user_using_email(user=user_data, db=db_session)
        assert result is True

    def test_user_not_exists_returns_false(self, db_session: Session):
        """Test that function returns False when user doesn't exist"""
        user_data = UserRegister(
            name="Test User",
            email="nonexistent@test.com",
            password="TestPass123!",
            role="staff",
        )
        result = check_existing_user_using_email(user=user_data, db=db_session)
        assert result is False


class TestFetchUserByEmail:
    """Test suite for fetch_user_by_email function"""

    def test_fetch_existing_user(self, db_session: Session, staff_user: User):
        """Test fetching an existing user by email"""
        user = fetch_user_by_email(email_id=staff_user.email, db=db_session)
        assert user is not None
        assert user.email == staff_user.email
        assert user.name == staff_user.name

    def test_fetch_nonexistent_user(self, db_session: Session):
        """Test fetching a non-existent user by email"""
        user = fetch_user_by_email(email_id="nonexistent@test.com", db=db_session)
        assert user is None

    def test_fetch_user_case_insensitive(self, db_session: Session, staff_user: User):
        """Test that email lookup is case insensitive"""
        user = fetch_user_by_email(email_id=staff_user.email.upper(), db=db_session)
        assert user is not None
        assert user.email == staff_user.email


class TestAuthenticateUser:
    """Test suite for authenticate_user function"""

    def test_authenticate_valid_credentials(
        self, db_session: Session, staff_user: User
    ):
        """Test authentication with valid credentials"""
        user = authenticate_user(
            db=db_session, email=staff_user.email, password="staffpass123"
        )
        assert user is not None
        assert user.email == staff_user.email

    def test_authenticate_invalid_email(self, db_session: Session):
        """Test authentication with invalid email"""
        user = authenticate_user(
            db=db_session, email="nonexistent@test.com", password="anypassword"
        )
        assert user is None

    def test_authenticate_invalid_password(self, db_session: Session, staff_user: User):
        """Test authentication with invalid password"""
        user = authenticate_user(
            db=db_session, email=staff_user.email, password="wrongpassword"
        )
        assert user is None

    def test_authenticate_empty_password(self, db_session: Session, staff_user: User):
        """Test authentication with empty password"""
        user = authenticate_user(db=db_session, email=staff_user.email, password="")
        assert user is None


class TestUpdateUserName:
    """Test suite for update_user_name function"""

    def test_update_user_name_success(self, db_session: Session, staff_user: User):
        """Test successful user name update"""
        update_details = UserEdit(new_name="Updated Name")
        message = update_user_name(
            current_user=staff_user, update_details=update_details
        )
        assert "updated" in message.lower()
        assert staff_user.name == "Updated Name"

    def test_update_user_name_same_name(self, db_session: Session, staff_user: User):
        """Test updating user name to same value"""
        original_name = staff_user.name
        update_details = UserEdit(new_name=original_name)
        message = update_user_name(
            current_user=staff_user, update_details=update_details
        )
        assert "same" in message.lower()
        assert staff_user.name == original_name

    def test_update_user_name_empty_name(self, db_session: Session, staff_user: User):
        """Test updating user name with empty string"""
        original_name = staff_user.name
        update_details = UserEdit(new_name="")
        message = update_user_name(
            current_user=staff_user, update_details=update_details
        )
        assert "same" in message.lower()
        assert staff_user.name == original_name


class TestUpdateUserPassword:
    """Test suite for update_user_password function"""

    def test_update_user_password_success(self, db_session: Session, staff_user: User):
        """Test successful user password update"""
        old_password_hash = staff_user.password
        update_details = UserEdit(new_password="NewPass123!")
        message = update_user_password(
            current_user=staff_user, update_details=update_details
        )
        assert "password updated" in message.lower()
        assert staff_user.password != old_password_hash

    def test_update_user_password_same_password(
        self, db_session: Session, staff_user: User
    ):
        """Test updating password to same value"""
        update_details = UserEdit(new_password="staffpass123")
        message = update_user_password(
            current_user=staff_user, update_details=update_details
        )
        assert "same" in message.lower()

    def test_update_user_password_weak_password(
        self, db_session: Session, staff_user: User
    ):
        """Test updating password with weak password"""
        update_details = UserEdit(new_password="weak")
        message = update_user_password(
            current_user=staff_user, update_details=update_details
        )
        assert "same" in message.lower()

    def test_update_user_password_empty_password(
        self, db_session: Session, staff_user: User
    ):
        """Test updating password with empty string"""
        update_details = UserEdit(new_password="")
        message = update_user_password(
            current_user=staff_user, update_details=update_details
        )
        assert "same" in message.lower()


class TestUserServiceIntegration:
    """Integration tests for user service functions"""

    def test_user_registration_flow(self, db_session: Session):
        """Test complete user registration flow"""
        user_data = UserRegister(
            name="Integration User",
            email="integration@test.com",
            password="IntegrationPass123!",
            role="staff",
        )

        # Check user doesn't exist
        assert not check_existing_user_using_email(user=user_data, db=db_session)

        # Create user
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hash_password(user_data.password),
            role=user_data.role.value,
        )
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        # Verify user exists
        assert check_existing_user_using_email(user=user_data, db=db_session)

        # Test authentication
        authenticated_user = authenticate_user(
            db=db_session, email=user_data.email, password=user_data.password
        )
        assert authenticated_user is not None
        assert authenticated_user.email == user_data.email

    def test_user_update_flow(self, db_session: Session, staff_user: User):
        """Test complete user update flow"""
        # Fetch user
        user = fetch_user_by_email(email_id=staff_user.email, db=db_session)
        assert user is not None

        # Update name and password
        update_details = UserEdit(
            new_name="Updated Integration User", new_password="UpdatedPass123!"
        )

        name_message = update_user_name(
            current_user=user, update_details=update_details
        )
        password_message = update_user_password(
            current_user=user, update_details=update_details
        )

        assert "updated" in name_message.lower()
        assert "password updated" in password_message.lower()

        # Verify updates
        assert user.name == "Updated Integration User"

        # Test authentication with new password
        authenticated_user = authenticate_user(
            db=db_session, email=user.email, password="UpdatedPass123!"
        )
        assert authenticated_user is not None
        assert authenticated_user.email == user.email
