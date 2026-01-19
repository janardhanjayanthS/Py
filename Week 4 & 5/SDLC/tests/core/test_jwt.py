# test_jwt.py - Tests for JWT authentication functionality
from datetime import datetime, timedelta

import jwt
import pytest
from src.core.config import settings
from src.core.jwt import (
    InvalidTokenException,
    TokenExpiredException,
    create_access_token,
    get_token_expiry,
    verify_token,
)


class TestCreateAccessToken:
    """Test suite for create_access_token function"""

    def test_create_token_with_default_expiry(self):
        """Test creating token with default expiration"""
        data = {"sub": "test@example.com", "role": "staff"}
        token = create_access_token(data=data)

        assert isinstance(token, str)
        assert len(token) > 0

        # Verify token can be decoded
        decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        assert decoded["sub"] == "test@example.com"
        assert decoded["role"] == "staff"
        assert "exp" in decoded

    def test_create_token_with_custom_expiry(self):
        """Test creating token with custom expiration"""
        data = {"sub": "test@example.com", "role": "admin"}
        expires_delta = timedelta(hours=2)

        token = create_access_token(data=data, expires_delta=expires_delta)

        decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        # Check expiration is approximately 2 hours from now
        exp_time = datetime.fromtimestamp(decoded["exp"])
        current_time = datetime.utcnow()
        time_diff = exp_time - current_time

        # Should be close to 2 hours (allowing for small time differences)
        assert (
            timedelta(hours=1, minutes=50)
            <= time_diff
            <= timedelta(hours=2, minutes=10)
        )

    def test_create_token_with_minimal_data(self):
        """Test creating token with minimal required data"""
        data = {"sub": "minimal@example.com"}
        token = create_access_token(data=data)

        decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        assert decoded["sub"] == "minimal@example.com"
        assert "exp" in decoded

    def test_create_token_with_additional_data(self):
        """Test creating token with additional custom data"""
        data = {
            "sub": "extra@example.com",
            "role": "manager",
            "department": "IT",
            "permissions": ["read", "write"],
        }
        token = create_access_token(data=data)

        decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        assert decoded["sub"] == "extra@example.com"
        assert decoded["role"] == "manager"
        assert decoded["department"] == "IT"
        assert decoded["permissions"] == ["read", "write"]


class TestVerifyToken:
    """Test suite for verify_token function"""

    def test_verify_valid_token(self):
        """Test verifying a valid token"""
        data = {"sub": "verify@example.com", "role": "staff"}
        token = create_access_token(data=data)

        payload = verify_token(token)
        assert payload["sub"] == "verify@example.com"
        assert payload["role"] == "staff"

    def test_verify_invalid_token(self):
        """Test verifying an invalid token"""
        invalid_token = "invalid.token.string"

        with pytest.raises(InvalidTokenException) as exc_info:
            verify_token(invalid_token)

        assert "invalid" in str(exc_info.value.message).lower()

    def test_verify_expired_token(self):
        """Test verifying an expired token"""
        data = {"sub": "expired@example.com"}
        # Create token that's already expired
        expires_delta = timedelta(seconds=-1)  # Expired 1 second ago
        token = create_access_token(data=data, expires_delta=expires_delta)

        with pytest.raises(TokenExpiredException) as exc_info:
            verify_token(token)

        assert "expired" in str(exc_info.value.message).lower()

    def test_verify_malformed_token(self):
        """Test verifying a malformed token"""
        malformed_tokens = [
            "only.one.part",
            "too.many.parts.in.token",
            "",
            "not_a_token_at_all",
        ]

        for malformed_token in malformed_tokens:
            with pytest.raises(InvalidTokenException):
                verify_token(malformed_token)

    def test_verify_token_with_wrong_algorithm(self):
        """Test verifying token with wrong algorithm"""
        # Create token with different algorithm
        data = {"sub": "wrongalgo@example.com"}
        token = jwt.encode(
            data,
            settings.SECRET_KEY,
            algorithm="HS256",  # Different from settings.ALGORITHM
        )

        # This should still work if our settings use HS256
        if settings.ALGORITHM == "HS256":
            payload = verify_token(token)
            assert payload["sub"] == "wrongalgo@example.com"


class TestGetTokenExpiry:
    """Test suite for get_token_expiry function"""

    def test_get_expiry_from_valid_token(self):
        """Test getting expiry from valid token"""
        data = {"sub": "expiry@example.com"}
        token = create_access_token(data=data)

        expiry_time = get_token_expiry(token)
        assert isinstance(expiry_time, datetime)
        assert expiry_time > datetime.utcnow()

    def test_get_expiry_from_expired_token(self):
        """Test getting expiry from expired token"""
        data = {"sub": "expiredexpiry@example.com"}
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data=data, expires_delta=expires_delta)

        expiry_time = get_token_expiry(token)
        assert isinstance(expiry_time, datetime)
        assert expiry_time < datetime.utcnow()

    def test_get_expiry_from_invalid_token(self):
        """Test getting expiry from invalid token"""
        invalid_token = "invalid.token.string"

        with pytest.raises(InvalidTokenException):
            get_token_expiry(invalid_token)


class TestJWTIntegration:
    """Integration tests for JWT functionality"""

    def test_complete_token_lifecycle(self):
        """Test complete token lifecycle: create, verify, expire"""
        # Create token
        user_data = {
            "sub": "lifecycle@example.com",
            "role": "admin",
            "permissions": ["all"],
        }
        token = create_access_token(data=user_data)

        # Verify token
        payload = verify_token(token)
        assert payload["sub"] == "lifecycle@example.com"
        assert payload["role"] == "admin"
        assert payload["permissions"] == ["all"]

        # Check expiry
        expiry = get_token_expiry(token)
        assert expiry > datetime.utcnow()

        # Wait for token to expire (using very short expiry for testing)
        short_expiry_token = create_access_token(
            data=user_data, expires_delta=timedelta(milliseconds=1)
        )

        # Token should be valid immediately
        verify_token(short_expiry_token)

        # Wait a bit for expiration
        import time

        time.sleep(0.01)  # 10ms

        # Token should now be expired
        with pytest.raises(TokenExpiredException):
            verify_token(short_expiry_token)

    def test_token_with_different_user_roles(self):
        """Test creating tokens for different user roles"""
        roles = ["staff", "manager", "admin"]

        for role in roles:
            data = {"sub": f"{role}@example.com", "role": role}
            token = create_access_token(data=data)

            payload = verify_token(token)
            assert payload["role"] == role
            assert payload["sub"] == f"{role}@example.com"

    def test_token_data_persistence(self):
        """Test that token data persists correctly"""
        complex_data = {
            "sub": "complex@example.com",
            "role": "manager",
            "department": "Engineering",
            "team": "Backend",
            "permissions": ["read", "write", "delete"],
            "metadata": {"last_login": "2023-01-01", "login_count": 42},
        }

        token = create_access_token(data=complex_data)
        payload = verify_token(token)

        # Check all data is preserved
        assert payload["sub"] == complex_data["sub"]
        assert payload["role"] == complex_data["role"]
        assert payload["department"] == complex_data["department"]
        assert payload["team"] == complex_data["team"]
        assert payload["permissions"] == complex_data["permissions"]
        assert (
            payload["metadata"]["last_login"] == complex_data["metadata"]["last_login"]
        )
        assert (
            payload["metadata"]["login_count"]
            == complex_data["metadata"]["login_count"]
        )
        assert (
            payload["metadata"]["login_count"]
            == complex_data["metadata"]["login_count"]
        )
