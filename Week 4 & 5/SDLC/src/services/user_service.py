from datetime import timedelta

from src.core.config import settings
from src.core.jwt import create_access_token
from src.core.log import get_logger
from src.interfaces.user_repo import AbstractUserRepository
from src.interfaces.user_service import AbstractUserService
from src.models.user import User
from src.schema.user import UserEdit, UserLogin, UserRegister, UserRole

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

    async def update_user(self, current_user_email: str, user: UserEdit) -> str | User:
        logger.debug(f"User update request from: {current_user_email}")
        current_user = await self.repo.fetch_user_by_email(email_id=current_user_email)

        message = await self.repo.get_update_user_message(
            current_user=current_user, update_details=user
        )

        logger.info(f"User {current_user.email} details updated successfully")
        return message, current_user

    async def get_users(self, user_email: str) -> list[User]:
        logger.debug(f"Fetching all users, requested by: {user_email}")
        return await self.repo.fetch_all_users()

    async def delete_user(self, user_id: int, user_email: str) -> None:
        logger.debug(f"Delete user request for user_id: {user_id} by: {user_email}")

        deleted_user = await self.repo.delete_user(user_id=user_id)

        logger.info(f"User {user_email} (id: {user_id}) deleted by {user_email}")
        return deleted_user
