from model import Task
from pydantic import ValidationError


def validate_user_input(user_json: str) -> None | Task:
    """
    Validates user's input json with the Task mode
    raises validation error if any

    Args:
        user_intput: json task infromation in string format

    Returns:
        None | str: valid data or None
    """
    try:
        user_input = Task.model_validate_json(user_json)
        return user_input
    except ValidationError as e:
        print(f"Error occured: {e}")
        return None
