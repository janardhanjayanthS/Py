from typing import Optional

from sqlalchemy.orm import Session

from src.core.log import get_logger, log_error
from src.models.user import User
from src.repository.database import (
    hash_password,
    verify_password,
)
from src.schema.user import UserEdit, UserRegister
from src.services.models import ResponseStatus

logger = get_logger(__name__)


def check_existing_user_using_email(user: UserRegister, db: Session) -> bool:
    """
    Checks if user's email address already exists in db
    Args:
        user: User object containing user details
        db: sqlalchemy db object

    Returns:
        bool: true if user already exists, false otherwise
    """
    existing_user = fetch_user_by_email(email_id=user.email, db=db)
    return True if existing_user else False


def fetch_user_by_email(email_id: str, db: Session) -> User | None:
    """
    gets User object with specific email from db

    Args:
        email_id: email id of user to search
        db: sqlalchemy db object

    Returns:
        User | None: user object if user exists else None
    """
    logger.debug(f"Fetching user by email: {email_id}")
    return db.query(User).filter_by(email=email_id).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Verify user credentials,
    return user if authenticate

    Args:
        db: sqlalchemy db object
        email: user's email id
        password: user's passowrd

    Returns:
        User: valid user object with user data
    """
    logger.debug(f"Authenticating user: {email}")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Authentication failed: user not found for email: {email}")
        return None

    if not verify_password(plain_password=password, hashed_password=str(user.password)):
        logger.warning(f"Authentication failed: invalid password for email: {email}")
        return None

    logger.info(f"User authenticated successfully: {email}")
    return user


def update_user_name(current_user: User, update_details: UserEdit) -> str:
    """
    Update user's name to a new name

    Args:
        current_user: current logged in user's db instance
        update_details: user details to update

    Returns:
        str: update message if name is updated or empty string
    """
    if (
        update_details.new_name is not None
        and current_user.name != update_details.new_name
    ):
        logger.info(
            f"Updating user name from '{current_user.name}' to '{update_details.new_name}'"
        )
        current_user.name = update_details.new_name
        return f"updated user's name to {update_details.new_name}. "
    logger.debug("No name update required - names are identical")
    return "existing name and new name are same. "


def update_user_password(current_user: User, update_details: UserEdit) -> str:
    """
    Update user's password to a new password

    Args:
        current_user: current logged in user's db instance tf
        update_details: user details to update

    Returns:
        str: update message if name is updated or empty string
    """
    if (
        update_details.new_password is not None
        and current_user.password != hash_password(update_details.new_password)
    ):
        current_user.password = hash_password(update_details.new_password)
        logger.info(f"Password updated for user: {current_user.email}")
        return "password updated"
    logger.debug("No password update required")
    return "same password"


def handle_missing_user(user_id: int) -> dict:
    """
    Log and return response for missing user

    Args:
        user_id: missing user's id

    Returns:
        dict: response describing missing user
    """
    message = f"Unable to find user with id: {user_id}"
    log_error(message)
    return {
        "status": ResponseStatus.E.value,
        "message": {"response": message},
    }
