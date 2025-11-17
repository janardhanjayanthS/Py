from model import Task
from prompts import system_prompt
from pydantic import ValidationError
from pydantic_ai import Agent


# def validate_user_input(user_json: Task) -> None | Task:
#     """
#     Validates user's input json with the Task mode
#     raises validation error if any

#     Args:
#         user_intput: json task infromation in string format

#     Returns:
#         None | str: valid data or None
#     """
#     try:
#         user_input = Task.model_validate_json(user_json)
#         return user_input
#     except ValidationError as e:
#         print(f"Error occured: {e}")
#         return None


def get_json_from_user_input(user_input: str) -> Task:
    """
    provides json data from user's input

    Args:
        user_input: prompt from the user
    """
    json_delivery_agent = Agent(
        model="", 
        output_type=Task, 
        output_retries=5, 
        system_prompt=system_prompt
    )
    response = json_delivery_agent.run_sync(user_input)
    print(response.output)
    return response.output
