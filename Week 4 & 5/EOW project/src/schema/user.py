from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    """
    Base model for user
    """

    name: str = Field(min_length=5, max_length=100)
    email: EmailStr
    password: str


class UserRegister(BaseUser):
    """
    Pydantic model for validating user's data when registering
    """


class UserLogin(BaseUser):
    """
    Pydantic model for validating user's data when log in
    """

    name: Optional[str]
