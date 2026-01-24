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
    """Repository for performing database operations on User entities.

    Attributes:
        session (AsyncSession): The SQLAlchemy async session for database interaction.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the repository with a database session.

        Args:
            session: An instance of SQLAlchemy AsyncSession.
        """
        self.session = session

    async def delete_user(self, user_id: int) -> User | dict:
        """Deletes a user from the database by their ID.

        Args:
            user_id: The unique identifier of the user to delete.

        Returns:
            The deleted User object if successful, or a error dictionary
            via handle_missing_user if not found.
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()

        if not user:
            logger.warning(f"Attempted to delete non-existent user with id: {user_id}")
            return self.handle_missing_user(user_id=user_id)

        await delete_commit_db(object=user, db=self.session)
        return user

    async def fetch_all_users(self) -> list[User]:
        """Retrieves all user records from the database.

        Returns:
            A list of all User objects.
        """
        stmt = select(User)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_user(self, user: UserRegister) -> User:
        """Hashes the password and persists a new user to the database.

        Args:
            user: The registration data transfer object.

        Returns:
            The created User database object.
        """
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
        """Checks if a user's email address already exists in the database.

        Args:
            user: User object containing the email to check.

        Returns:
            True if the email exists, False otherwise.
        """
        existing_user = await self.fetch_user_by_email(email_id=user.email)
        return True if existing_user else False

    async def fetch_user_by_email(self, email_id: str) -> User | None:
        """Retrieves a single user from the database by their email.

        Args:
            email_id: The email address to search for.

        Returns:
            The User object if found, otherwise None.
        """
        logger.debug(f"Fetching user by email: {email_id}")
        stmt = select(User).filter_by(email=email_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """Verifies user credentials against the database.

        Args:
            email: The user's email address.
            password: The plain-text password to verify.

        Returns:
            The authenticated User object if credentials are valid, else None.
        """
        logger.debug(f"Authenticating user: {email}")

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
        """Logs a failed login attempt and raises an authentication error.

        Args:
            email_id: The email address that failed authentication.

        Raises:
            AuthenticationException: Always raised to trigger a 401/403 response.
        """
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
        """Aggregates update operations for name and password.

        Args:
            current_user: The User database instance to update.
            update_details: The new details to be applied.

        Returns:
            A concatenated string of all changes made.
        """
        message = self.update_user_name(
            current_user=current_user, update_details=update_details
        ) + self.update_user_password(
            current_user=current_user, update_details=update_details
        )
        await commit_refresh_db(object=current_user, db=self.session)
        return message

    def update_user_name(self, current_user: User, update_details: UserEdit) -> str:
        """Updates the user's name if a new one is provided.

        Args:
            current_user: The current User database instance.
            update_details: Object containing the potential new name.

        Returns:
            A message indicating if the name was updated or remained the same.
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
        """Updates and hashes the user's password if a new one is provided.

        Args:
            current_user: The current User database instance.
            update_details: Object containing the potential new password.

        Returns:
            A message indicating if the password was updated or remained the same.
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
        """Logs an error and returns a formatted missing user response.

        Args:
            user_id: The ID of the user that could not be found.

        Returns:
            A dictionary containing the error status and message.
        """
        message = f"Unable to find user with id: {user_id}"
        logger.error(message)
        return {
            "status": ResponseStatus.E.value,
            "message": {"response": message},
        }
