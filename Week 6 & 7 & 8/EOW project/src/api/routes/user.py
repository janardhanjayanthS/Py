from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.constants import ResponseType, logger
from src.core.database import get_db
from src.core.database_utility import (
    add_commit_refresh_db,
    authenticate_user,
    check_existing_user_using_email,
)
from src.core.jwt import create_access_token
from src.core.utility import hash_password
from src.models.user import User
from src.schema.response import APIResponse
from src.schema.user import UserCreate, UserLogin, UserResponse

user = APIRouter()


@user.post("/user/register", response_model=APIResponse)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    try:
        if check_existing_user_using_email(db=db, user=user_create):
            logger.info("Existing user!")
            return APIResponse(
                response=ResponseType.ERROR,
                message={
                    "result": f"User already exists with {user_create.email} email id"
                },
            )

        new_user = User(
            name=user_create.name,
            email=user_create.email,
            password_hash=hash_password(password=user_create.password),
        )

        add_commit_refresh_db(object=new_user, db=db)

        return APIResponse(
            response=ResponseType.SUCCESS,
            message={
                "result": "Successfully added user to database",
                "user details": UserResponse(
                    name=user_create.name, email=user_create.email
                ),
            },
        )
    except Exception as e:
        message = f"Error occured: {e}"
        logger.error(message)
        raise HTTPException(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details="Internal server error occured try again later",
        )


@user.post("/user/login", response_model=APIResponse)
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    try:
        logger.info(f"user login: {user_login}")
        user = authenticate_user(user=user_login, db=db)
        token = create_access_token(
            data={"email": user.email, "id": user.id}, expires_delta=None
        )
        logger.info(f"JWT TOKEN: {token}")
        return APIResponse(response=ResponseType.SUCCESS, message={"token": token})
    except HTTPException:
        raise
    except Exception as e:
        message = f"Error occured: {e}"
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occured try again later",
        )

