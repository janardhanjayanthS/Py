from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.jwt import create_access_token, required_roles
from src.core.log import get_logger
from src.models.user import User
from src.repository.database import add_commit_refresh_db, get_db, hash_password
from src.schema.user import (
    UserEdit,
    UserLogin,
    UserRegister,
    UserRole,
    WrapperUserResponse,
)
from src.services.api_utility import (
    authenticate_user,
    check_existing_user_using_email,
    fetch_user_by_email,
    handle_missing_user,
    update_user_name,
    update_user_password,
)
from src.services.models import ResponseStatus

logger = get_logger(__name__)

user = APIRouter()


@user.post("/user/register", response_model=WrapperUserResponse)
async def register_user(create_user: UserRegister, db: Session = Depends(get_db)):
    logger.debug(f"Registration attempt for email: {create_user.email}")
    if check_existing_user_using_email(user=create_user, db=db):
        message = f"User with email {create_user.email} already exists"
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    db_user = User(
        name=create_user.name,
        email=create_user.email,
        password=hash_password(create_user.password),
        role=create_user.role.value,
    )

    add_commit_refresh_db(object=db_user, db=db)
    logger.debug(f"Created new user with- {db_user.email} - email")
    logger.warning(f"Created new user with - {db_user.email} - email")

    return {"status": "success", "message": {"registered user": db_user}}


@user.post("/user/login")
async def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    logger.debug(f"Login attempt for email: {user_login.email}")
    user = authenticate_user(
        db=db, email=user_login.email, password=user_login.password
    )
    if not user:
        logger.warning(f"Failed login attempt for email: {user_login.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires,
    )

    logger.info(f"User {user.email} logged in successfully")
    return {"access_tokem": access_token, "token_type": "Bearer"}


@user.get("/user/all", response_model=WrapperUserResponse)
@required_roles(UserRole.MANAGER, UserRole.ADMIN, UserRole.STAFF)
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    current_user_email = request.state.email
    logger.debug(f"Fetching all users, requested by: {current_user_email}")
    all_users = db.query(User).all()
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
    db: Session = Depends(get_db),
):
    logger.debug(f"User update request from: {request.state.email}")
    current_user = fetch_user_by_email(email_id=request.state.email, db=db)

    message = update_user_name(
        current_user=current_user, update_details=update_details
    ) + update_user_password(current_user=current_user, update_details=update_details)
    db.commit()
    db.refresh(current_user)
    logger.info(f"User {current_user.email} details updated successfully")

    return {
        "status": ResponseStatus.S.value,
        "message": {"update status": message, "updated user detail": current_user},
    }


@user.delete("/user/delete", response_model=WrapperUserResponse)
@required_roles(UserRole.ADMIN)
async def remove_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
):
    current_user_email = request.state.email
    logger.debug(f"Delete user request for user_id: {user_id} by: {current_user_email}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"Attempted to delete non-existent user with id: {user_id}")
        return handle_missing_user(user_id=user_id)

    db.delete(user)
    db.commit()
    logger.info(f"User {user.email} (id: {user_id}) deleted by {current_user_email}")

    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": current_user_email, "deleted account": user},
    }
