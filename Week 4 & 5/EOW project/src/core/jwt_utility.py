from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt, TokenData

from src.core.jwt_config import ALGORITHM, JWT_SECRET_KEY


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT token with user data

    Args:
        data: user's data (eg: name, email)
        expires_delta: token expiry time. Defaults to None.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=30)

    to_encode["exp"] = expire

    encode_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encode_jwt

def decode_access_token(token: str) -> 
