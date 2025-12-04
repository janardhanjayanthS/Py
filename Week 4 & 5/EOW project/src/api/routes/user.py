from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from src.core.api_utility import (
    authenticate_user,
    check_existing_user_using_email,
    fetch_user_by_email,
    handle_missing_user,
    update_user_name,
    update_user_password,
)
from src.core.constants import ResponseStatus
from src.core.database import (
    add_commit_refresh_db,
    get_db,
    hash_password,
)
from src.core.decorators import authorize_admin, authorize_manager, authorize_staff
from src.core.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.models.models import User
from src.schema.user import UserEdit, UserLogin, UserRegister, WrapperUserResponse

user = APIRouter()


@user.post("/user/register", response_model=WrapperUserResponse)
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
        role=create_user.role.value,
    )

    add_commit_refresh_db(object=db_user, db=db)

    return {"status": "success", "message": {"registered user": db_user}}


@user.post("/user/login")
async def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(
        db=db, email=user_login.email, password=user_login.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires,
    )

    # cannot copy from postman
    print(access_token)
    return {"access_tokem": access_token, "token_type": "Bearer"}


@user.get("/user/all", response_model=WrapperUserResponse)
@authorize_admin
@authorize_manager
@authorize_staff
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    current_user_email = request.state.email
    all_users = db.query(User).all()
    return {
        "response": ResponseStatus.S.value,
        "message": {"user email": current_user_email, "users": all_users},
    }


@user.patch("/user/update", response_model=WrapperUserResponse)
@authorize_admin
@authorize_manager
async def update_user_detail(
    request: Request,
    update_details: UserEdit,
    db: Session = Depends(get_db),
):
    current_user = fetch_user_by_email(email_id=request.state.email)

    message = update_user_name(
        current_user=current_user, update_details=update_details
    ) + update_user_password(current_user=current_user, update_details=update_details)
    db.commit()
    db.refresh(current_user)

    return {
        "status": ResponseStatus.S.value,
        "message": {"update status": message, "updated user detail": current_user},
    }


@user.delete("/user/delete", response_model=WrapperUserResponse)
@authorize_admin
async def remove_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
):
    current_user_email = request.state.email
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return handle_missing_user(user_id=user_id)

    db.delete(user)
    db.commit()

    return {
        "status": ResponseStatus.S.value,
        "message": {"user email": current_user_email, "deleted account": user},
    }
