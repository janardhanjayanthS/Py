from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.log import get_logger
from src.interfaces.user_repo import AbstractUserRepository
from src.models.user import User
from src.repository.database import add_commit_refresh_db, hash_password
from src.schema.user import UserRegister

logger = get_logger(__name__)


class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

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
