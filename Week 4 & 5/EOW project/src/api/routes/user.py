from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.api_utility import check_if_user_email_exists
from src.core.database import add_commit_refresh_db, get_db, hash_password
from src.models.models import User
from src.schema.user import UserRegister

user = APIRouter()


@user.post("/user/register")
async def register_user(create_user: UserRegister, db: Session = Depends(get_db)):
    print(f"register user details: {create_user}")

    if check_if_user_email_exists(user=create_user, db=db):
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
