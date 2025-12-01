from jose import JWTError, jwt
from passlib.context import CryptContext

pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt

    Args:
        password: plain text password

    Returns:
        str: hash of the password
    """
    return pwt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if plain text matches a hash

    Args:
        plain_password: plain text password
        hashed_password: hashed password

    Returns:
        bool: True if match, False otherwise
    """
    return pwt_context.verify(plain_password, hashed_password)