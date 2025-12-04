from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from src.core.excptions import WeakPasswordException
from src.core.utility import check_password_strength


def validate_password(password: str) -> str:
    pwd_strength = check_password_strength(password=password)
    if not pwd_strength:
        raise WeakPasswordException(
            f"Your password must include a digit, a lowercase letter, an uppercase letter, and a special character. You entered: {password}"
        )
    return password


class UserRole(Enum):
    """
    Enum for user roles - RBAC

    Attributes:
        ADMIN: admin role - GET/POST/PUT/PATCH/DELETE
        MANAGER: manager role - GET/POST/PUT/PATCH
        STAFF: staff role - GET
    """

    ADMIN: str = "admin"
    MANAGER: str = "manager"
    STAFF: str = "staff"

    @staticmethod
    def get_values() -> list[str]:
        return [role.value for role in UserRole]


class BaseUser(BaseModel):
    """
    Base model for user
    """

    name: str = Field(min_length=5, max_length=100)
    email: EmailStr
    password: str
    role: UserRole


class UserRegister(BaseUser):
    """
    Pydantic model for validating user's data when registering
    """

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, pwd: str) -> str:
        return validate_password(password=pwd)


class UserLogin(BaseModel):
    """
    Pydantic model for validating user's data when log in
    """

    email: EmailStr
    password: str


class UserEdit(BaseModel):
    """
    Pydantic model for editing user information

    Attributes:
        new_name: name to update
        new_password: password to update
    """

    new_name: Optional[str] = None
    new_password: Optional[str] = None

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, pwd: str) -> str:
        return validate_password(password=pwd)


class UserResponse(BaseModel):
    """
    Pydantic model for user response (json) to hide password hash
    """

    id: int
    name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class WrapperUserResponse(BaseModel):
    """
    Wrapper model around UserResponse to match the response json format
    """

    status: str
    message: dict[str, str | list[UserResponse] | UserResponse]
