from abc import ABC, abstractmethod

from src.schema.user import UserRegister, UserResponse


class AbstractUserService(ABC):
    @abstractmethod
    def register_user(self, user: UserRegister) -> UserResponse:
        pass
