from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.api_utility import check_if_user_email_exists
from src.core.db_config import get_db
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

    return {"register": "user"}
