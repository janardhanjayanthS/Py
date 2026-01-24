from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.jwt import required_roles
from src.core.log import get_logger
from src.interfaces.user_service import AbstractUserService
from src.repository.database import (
    get_db,
)
from src.repository.user_repo import UserRepository
from src.schema.user import (
    UserEdit,
    UserLogin,
    UserRegister,
    UserRole,
    WrapperUserResponse,
)
from src.services.models import ResponseStatus
from src.services.user_service import (
    UserService,
)

logger = get_logger(__name__)

user = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(repo=UserRepository(session=db))


@user.post("/user/register", response_model=WrapperUserResponse)
async def register_user(
    create_user: UserRegister,
    user_service: AbstractUserService = Depends(get_user_service),
):
    """Register a new user account.

    Args:
        create_user: User registration data.
        db: Database session dependency.

    Returns:
        WrapperUserResponse containing the created user.

    Raises:
        AuthenticationException: If user email already exists.
    """

    db_user = await user_service.register_user(user=create_user)
    return {"status": "success", "message": {"registered user": db_user}}


@user.post("/user/login")
async def login_user(
    user_login: UserLogin, user_service: AbstractUserService = Depends(get_user_service)
):
    """Authenticate user and return access token.

    Args:
        user_login: User login credentials.
        db: Database session dependency.

    Returns:
        Access token response.tf

    Raises:
        AuthenticationException: If credentials are invalid.
    """
    access_token = await user_service.login_user(user=user_login)
    return {"access_tokem": access_token, "token_type": "Bearer"}


@user.get("/user/all", response_model=WrapperUserResponse)
@required_roles(UserRole.MANAGER, UserRole.ADMIN, UserRole.STAFF)
async def get_all_users(
    request: Request, user_service: AbstractUserService = Depends(get_user_service)
):
    """Retrieve all users from the database.

    Args:
        request: HTTP request object.
        db: Database session dependency.

    Returns:
        WrapperUserResponse containing all users.
    """
    current_user_email = request.state.email
    all_users = await user_service.get_users(user_email=current_user_email)

    logger.info(f"Retrieved {len(all_users)} users")
    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": current_user_email, "users": all_users},
    }


@user.patch("/user/update", response_model=WrapperUserResponse)
@required_roles(UserRole.MANAGER, UserRole.ADMIN)
async def update_user_detail(
    request: Request,
    update_details: UserEdit,
    user_service: AbstractUserService = Depends(get_user_service),
):
    """Update user details (name and/or password).

    Args:
        request: HTTP request object.
        update_details: User details to update.
        db: Database session dependency.

    Returns:
        WrapperUserResponse containing updated user details.
    """

    message, current_user = await user_service.update_user(
        current_user_email=request.state.email, user=update_details
    )

    return {
        "status": ResponseStatus.S.value,
        "message": {"update status": message, "updated user detail": current_user},
    }


@user.delete("/user/delete", response_model=WrapperUserResponse)
@required_roles(UserRole.ADMIN)
async def remove_user(
    request: Request,
    user_id: int,
    user_service: AbstractUserService = Depends(get_user_service),
):
    """Delete a user by ID.

    Args:
        request: HTTP request object.
        user_id: ID of the user to delete.
        db: Database session dependency.

    Returns:
        WrapperUserResponse containing deletion confirmation.
    """
    current_user_email = request.state.email
    deleted_account = await user_service.delete_user(
        user_id=user_id, user_email=current_user_email
    )

    return {
        "status": ResponseStatus.S.value,
        "message": {
            "user email": current_user_email,
            "deleted account": deleted_account,
        },
    }
