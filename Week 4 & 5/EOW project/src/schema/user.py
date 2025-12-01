from pydantic import BaseModel, EmailStr, Field, field_validator

from src.core.excptions import WeakPasswordException
from src.core.utility import password_strength


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

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, pwd: str) -> str:
        pwt_strength = password_strength(password=pwd)
        if pwt_strength != "Strong password":
            raise WeakPasswordException(
                f"Your password must include a digit, a lowercase letter, an uppercase letter, and a special character. You entered: {pwd}"
            )
        return pwd


class UserLogin(BaseModel):
    """
    Pydantic model for validating user's data when log in
    """

    email: EmailStr
    password: str
