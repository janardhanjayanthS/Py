from abc import ABC, abstractmethod
from typing import Any

from src.models.user import User
from src.schema.user import UserRegister, UserResponse


class AbstractUserService(ABC):
    @abstractmethod
    def register_user(self, user: UserRegister) -> UserResponse:
        pass

    @abstractmethod
    def login_user(self, user: UserRegister) -> User:
        pass

    @abstractmethod
    def update_user(self, user_email: str) -> list:
        pass

    @abstractmethod
    def delete_user(self, user_id: int, user_email: str) -> Any:
        pass
