from openai import OpenAI
from typing import Any
from prompts import system_prompt
from utility import validate_user_input
from tools import tool_definition

client = OpenAI()

tasks: list = []


user_input_json = """
{
    "id": 1,
    "task": "buy grocery",
    "done": False
}
"""

valid_user_input = validate_user_input(user_json=user_input_json)

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
