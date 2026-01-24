from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AuthenticationException
from src.core.log import get_logger
from src.interfaces.user_repo import AbstractUserRepository
from src.models.user import User
from src.repository.database import (
    add_commit_refresh_db,
    commit_refresh_db,
    delete_commit_db,
    hash_password,
    verify_password,
)
from src.schema.user import UserEdit, UserRegister
from src.services.models import ResponseStatus

logger = get_logger(__name__)


class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def delete_user(self, user_id: int):
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()

        if not user:
            logger.warning(f"Attempted to delete non-existent user with id: {user_id}")
            return self.handle_missing_user(user_id=user_id)

        await delete_commit_db(object=user, db=self.session)
        return user

    async def fetch_all_users(self) -> list[User]:
        stmt = select(User)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_user(self, user: UserRegister) -> User:
        db_user = User(
            name=user.name,
            email=user.email,
            password=hash_password(user.password),
            role=user.role.value,
        )

        await add_commit_refresh_db(object=db_user, db=self.session)
        logger.debug(f"Created new user with- {db_user.email} - email")
        logger.warning(f"Created new user with - {db_user.email} - email")
        return db_user

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

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
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
        result = await self.session.execute(stmt)
        user = result.scalars().first()

        if not user:
            logger.warning(f"Authentication failed: user not found for email: {email}")
            return None

        if not verify_password(
            plain_password=password, hashed_password=str(user.password)
        ):
            logger.warning(
                f"Authentication failed: invalid password for email: {email}"
            )
            return None

        logger.info(f"User authenticated successfully: {email}")
        return user

    def handle_unknown_user(self, email_id: str) -> None:
        logger.warning(f"Failed login attempt for email: {email_id}")
        raise AuthenticationException(
            message="Incorrect email or password",
            field_errors=[
                {"field": "email", "message": "Email or password is incorrect"}
            ],
        )

    async def get_update_user_message(
        self, current_user: User, update_details: UserEdit
    ) -> str:
        message = self.update_user_name(
            current_user=current_user, update_details=update_details
        ) + self.update_user_password(
            current_user=current_user, update_details=update_details
        )
        await commit_refresh_db(object=current_user, db=self.session)
        return message

    def update_user_name(self, current_user: User, update_details: UserEdit) -> str:
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

    def update_user_password(self, current_user: User, update_details: UserEdit) -> str:
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

    def handle_missing_user(self, user_id: int) -> dict:
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
