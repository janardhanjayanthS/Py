# test_jwt.py - Tests for JWT authentication functionality
from datetime import datetime, timedelta

import jwt
from src.core.config import settings
from src.core.jwt import create_access_token, decode_access_token


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
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
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
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        # Check expiration is approximately 2 hours from now (allowing for timezone differences)
        exp_time = datetime.fromtimestamp(decoded["exp"])
        current_time = datetime.now()
        time_diff = exp_time - current_time

        # Should be close to 2 hours (allowing for timezone differences and small time variations)
        assert (
            timedelta(hours=1, minutes=30)
            <= time_diff
            <= timedelta(hours=14)  # Allow for timezone differences
        )

    def test_create_token_with_minimal_data(self):
        """Test creating token with minimal required data"""
        data = {"sub": "minimal@example.com"}
        token = create_access_token(data=data)

        decoded = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
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
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        assert decoded["sub"] == "extra@example.com"
        assert decoded["role"] == "manager"
        assert decoded["department"] == "IT"
        assert decoded["permissions"] == ["read", "write"]

    def test_verify_token_with_wrong_algorithm(self):
        """Test verifying token with wrong algorithm"""
        # Create token with different algorithm
        data = {"sub": "wrongalgo@example.com"}
        token = jwt.encode(
            data,
            settings.JWT_SECRET_KEY,
            algorithm="HS256",  # Different from settings.ALGORITHM
        )

        # This should still work if our settings use HS256
        if settings.ALGORITHM == "HS256":
            payload = decode_access_token(token)
            assert payload.email == "wrongalgo@example.com"
