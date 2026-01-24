from datetime import timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.jwt import create_access_token
from src.core.log import get_logger
from src.interfaces.user_repo import AbstractUserRepository
from src.interfaces.user_service import AbstractUserService
from src.models.user import User
from src.repository.database import hash_password, verify_password
from src.schema.user import UserEdit, UserLogin, UserRegister, UserRole
from src.services.models import ResponseStatus

logger = get_logger(__name__)


class UserService(AbstractUserService):
    def __init__(self, repo: AbstractUserRepository) -> None:
        self.repo = repo

    async def register_user(self, user: UserRegister) -> User:
        logger.debug(f"Registration attempt for email: {user.email}")

        await self.repo.check_existing_user_using_email(user=user)

        created_user = await self.repo.create_user(user=user)

        return created_user

    async def login_user(self, user: UserLogin) -> User:
        logger.debug(f"Login attempt for email: {user.email}")
        user = await self.repo.authenticate_user(
            email=user.email, password=user.password
        )
        if not user:
            self.repo.handle_missing_user(email_id=user.email)

        access_token = self._get_new_user_jwt_token(role=user.role, email=user.email)

        logger.info(f"User {user.email} logged in successfully")
        return access_token

    def _get_new_user_jwt_token(self, role: UserRole, email: str) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": email, "role": role},
            expires_delta=access_token_expires,
        )

    async def update_user(self, current_user_email: str, user: UserEdit) -> User:
        logger.debug(f"User update request from: {current_user_email}")
        current_user = await self.repo.fetch_user_by_email(email_id=current_user_email)

        message = await self.repo.get_update_user_message(
            current_user=current_user, update_details=user
        )

        logger.info(f"User {current_user.email} details updated successfully")
        return message, current_user


async def check_existing_user_using_email(self, user: UserRegister) -> bool:
    """
    Checks if user's email address already exists in db
    Args:
        user: User object containing user details
        db: sqlalchemy db object

    Returns:
        bool: true if user already exists, false otherwise
    """
    existing_user = await self.fetch_user_by_email(email_id=user.email)
    return True if existing_user else False


async def fetch_user_by_email(self, email_id: str) -> User | None:
    """
    gets User object with specific email from db

    Args:
        email_id: email id of user to search
        db: sqlalchemy db object

    Returns:
        User | None: user object if user exists else None
    """
    logger.debug(f"Fetching user by email: {email_id}")
    stmt = select(User).filter_by(email=email_id)
    result = await self.session.execute(stmt)
    return result.scalars().first()


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Optional[User]:
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

    # REPO
    stmt = select(User).filter_by(email=email)
    result = await db.execute(stmt)
    user = result.scalars().first()

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
    logger.error(message)
    return {
        "status": ResponseStatus.E.value,
        "message": {"response": message},
    }
