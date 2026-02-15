from abc import ABC, abstractmethod

from src.models.user import User
from src.schema.user import UserRegister, UserResponse


class AbstractUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserRegister) -> UserResponse:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> User | dict:
        pass

    @abstractmethod
    def fetch_all_users(self) -> list:
        pass
