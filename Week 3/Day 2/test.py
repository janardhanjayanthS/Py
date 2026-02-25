from pydantic import BaseModel
import pytest


class User(BaseModel):
    name: str
    age: int


# tests
@pytest.fixture
def user() -> User:
    """
    Returns a valid user object

    Returns:
        User object
    """
    return User(name="Alice", age=18)


def test_valid_user(user: User):
    """
    test for valid user objec

    Args:
        user: object to test
    """
    assert user.name == "Alice"
    assert user.age == 18
