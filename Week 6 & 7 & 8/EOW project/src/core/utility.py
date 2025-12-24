from hashlib import sha256

from passlib.context import CryptContext

from src.core.constants import logger

pwt_context = CryptContext(schemes=["argon2"], deprecated="auto")


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


def hash_bytes(data: bytes) -> str:
    """Computes the SHA-256 hash of a bytes object.

    Checks if the input is of type bytes, generates a SHA-256 hash, and
    returns the hexadecimal representation. If the input type is invalid,
    triggers an error logging sequence.

    Args:
        data: The bytes data to be hashed.

    Returns:
        str: The hexadecimal string representation of the hash.

    Raises:
        Note: If 'data' is not bytes, it calls unknown_type_while_hashing,
        which logs an error but does not explicitly raise a Python exception.
    """
    if isinstance(data, bytes):
        hash = sha256(data)
        return hash.hexdigest()
    unknown_type_while_hashing(_type=type(data))


def hash_str(data: str) -> str:
    """Computes the SHA-256 hash of a string.

    Encodes the input string into UTF-8 before generating a SHA-256 hash
    and returning the hexadecimal representation. If the input type is
    invalid, triggers an error logging sequence.

    Args:
        data: The string to be hashed.

    Returns:
        str: The hexadecimal string representation of the hash.

    Raises:
        Note: If 'data' is not a string, it calls unknown_type_while_hashing,
        which logs an error.
    """
    if isinstance(data, str):
        hash = sha256(data.encode("utf-8"))
        return hash.hexdigest()
    unknown_type_while_hashing(_type=type(data))


def unknown_type_while_hashing(_type: type) -> None:
    """Logs an error message when an unsupported data type is provided for hashing.

    This utility is called by hashing functions to provide consistent error
    reporting when type validation fails.

    Args:
        _type: The Python type class that was found to be incompatible.

    Returns:
        None
    """
    logger.error(f"Cannot encrypt {_type}")
    return
