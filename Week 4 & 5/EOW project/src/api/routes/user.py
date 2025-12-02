from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.api_utility import authenticate_user, check_existing_user_using_email
from src.core.constants import ResponseStatus
from src.core.database import add_commit_refresh_db, get_db, hash_password
from src.core.decorators import get_current_user
from src.core.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.models.models import User
from src.schema.user import UserLogin, UserRegister

user = APIRouter()


@user.post("/user/register")
async def register_user(create_user: UserRegister, db: Session = Depends(get_db)):
    if check_existing_user_using_email(user=create_user, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {create_user.email} already exists",
        )

    db_user = User(
        name=create_user.name,
        email=create_user.email,
        password=hash_password(create_user.password),
    )

    add_commit_refresh_db(object=db_user, db=db)

    return {"status": "success", "message": {"registered user": db_user}}


@user.post("/user/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db=db, email=user.email, password=user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # cannot copy from postman
    print(access_token)
    return {"access_tokem": access_token, "token_type": "Bearer"}


@user.get("/user/all")
async def get_all_users(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    all_users = db.query(User).all()
    return {
        "response": ResponseStatus.S.value,
        "message": {"user email": current_user.email, "users": all_users},
    }
