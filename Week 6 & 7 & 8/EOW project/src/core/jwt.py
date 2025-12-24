from datetime import datetime, timedelta
from os import getenv
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException, status
from jose import JWTError, jwt

from src.core.constants import logger
from src.schema.token import TokenData

load_dotenv()

JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")

if not JWT_SECRET_KEY:
    message = "Cannot find JSON_SECRET_KEY from .env"
    logger.error(message)
    raise ValueError(message)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT token with user data

    Args:
        data: user's data (eg: name, id)
        expires_delta: token expiry time. Defaults to None.
    """
    to_encode = data.copy()

    to_encode["exp"] = get_expiration_time(expires_delta=expires_delta)

    logger.info(f"To encode: {to_encode}")
    encode_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encode_jwt


def get_expiration_time(expires_delta: Optional[timedelta]) -> datetime:
    """
    gets expiration time for jwt token,
    calcualted based on param or set to 30 from current time

    Args:
        expires_delta: expiration duration for jwt

    Returns:
        datetime: result jwt expiration timestamp
    """
    if expires_delta:
        return datetime.now() + expires_delta
    else:
        return datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


def decode_access_token(token: str) -> TokenData:
    """
    Decodes incoming jwt token

    Args:
        token: JWT token

    Returns:
        TokenData: pydantic model containing token details

    Raises:
        HTTPException: if invalid/expired token
    """
    try:
        payload: dict = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub", "")
        id: str = payload.get("id", "")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        if id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        return TokenData(email=email, id=id)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
