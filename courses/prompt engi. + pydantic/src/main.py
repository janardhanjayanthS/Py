from openai import OpenAI
from typing import Any
from prompts import system_prompt
from utility import validate_user_input, get_json_from_user_input
from tools import tool_definition
from model import Task

# client = OpenAI()

tasks: list = []


user_input_json: Task = get_json_from_user_input("string")
valid_user_input: Task | None = validate_user_input(user_json=user_input_json)
print(valid_user_input)

# messages: list = [
#     {"role": "system", "content": system_prompt},
#     {"role": "user", "content": valid_user_input},
# ]

# response = client.chat.completions.create(
#     model="chatgpt-4o-latest",
#     messages=messages,
#     tools=tool_definition,
#     tool_choice='auto'
# )


# waiting for openAI api key
# then implement this project based on req.txt
