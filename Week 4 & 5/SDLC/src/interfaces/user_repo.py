from abc import ABC, abstractmethod

from src.schema.user import UserRegister, UserResponse


class AbstractUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserRegister) -> UserResponse:
        pass
