from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session


def add_commit_refresh_db(object: BaseModel, db: Session):
    """
    add, commit and refresh db after adding a row

    Args:
        object: to insert to db (pydantic model instance)
        db: database instance in session
    """
    db.add(object)
    db.commit()
    db.refresh(object)


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
