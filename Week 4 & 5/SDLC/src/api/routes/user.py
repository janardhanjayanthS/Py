from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.jwt import required_roles
from src.core.log import get_logger
from src.interfaces.user_service import AbstractUserService
from src.repository.database import get_db
from src.repository.user_repo import UserRepository
from src.schema.user import (
    UserEdit,
    UserLogin,
    UserRegister,
    UserRole,
    WrapperUserResponse,
)
from src.services.models import ResponseStatus
from src.services.user_service import UserService

logger = get_logger(__name__)

user = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Dependency provider for UserService.

    Args:
        db: The asynchronous database session.

    Returns:
        An instance of UserService initialized with a UserRepository.
    """
    return UserService(repo=UserRepository(session=db))


@user.post("/user/register", response_model=WrapperUserResponse)
async def register_user(
    create_user: UserRegister,
    user_service: AbstractUserService = Depends(get_user_service),
):
    """Registers a new user account in the system.

    Args:
        create_user: Data transfer object containing registration details.
        user_service: The user service business logic layer.

    Returns:
        A dictionary containing the success status and the registered user data.

    Raises:
        AuthenticationException: If the user email is already registered.
    """
    db_user = await user_service.register_user(user=create_user)
    return {"status": "success", "message": {"registered user": db_user}}


@user.post("/user/login")
async def login_user(
    user_login: UserLogin, user_service: AbstractUserService = Depends(get_user_service)
):
    """Authenticates a user and returns a Bearer access token.

    Args:
        user_login: User credentials (email and password).
        user_service: The user service business logic layer.

    Returns:
        A dictionary containing the JWT access token and token type.

    Raises:
        AuthenticationException: If the credentials provided are invalid.
    """
    access_token = await user_service.login_user(user=user_login)
    return {"access_token": access_token, "token_type": "Bearer"}


@user.get("/user/all", response_model=WrapperUserResponse)
@required_roles(UserRole.MANAGER, UserRole.ADMIN, UserRole.STAFF)
async def get_all_users(
    request: Request, user_service: AbstractUserService = Depends(get_user_service)
):
    """Retrieves a list of all users from the database.

    Requires MANAGER, ADMIN, or STAFF roles.

    Args:
        request: The FastAPI request object (used to extract current user email).
        user_service: The user service business logic layer.

    Returns:
        A dictionary containing the list of all users and the requester's email.
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
    """Updates the details of the currently authenticated user.

    Requires MANAGER or ADMIN roles.

    Args:
        request: The FastAPI request object.
        update_details: The user fields to be updated.
        user_service: The user service business logic layer.

    Returns:
        A dictionary containing the update status message and updated user object.
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
    """Deletes a specific user from the system by their ID.

    Requires ADMIN role.

    Args:
        request: The FastAPI request object.
        user_id: The unique identifier of the user to delete.
        user_service: The user service business logic layer.

    Returns:
        A dictionary confirming the deletion and the email of the requester.
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
