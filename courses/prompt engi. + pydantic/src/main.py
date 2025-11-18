from openai import OpenAI
from typing import Any
from prompts import system_prompt
from utility import validate_user_input, get_json_from_user_input
from tools import tool_definition
from model import Task
from dotenv import load_dotenv
import os
from tool_functions import tasks

load_dotenv()

opne_ai_api_key = os.getenv('OPEN_AI_API_KEY')

client = OpenAI(api_key=opne_ai_api_key)

user_message = 'Add a new task to buy grocery'

task_object_from_user_input: Task = get_json_from_user_input(user_message)
valid_user_input: Task | None = validate_user_input(model=task_object_from_user_input)
print(f'Validated user ip: {valid_user_input}, {type(valid_user_input)}')

messages: list = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_message},
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tool_definition,
    tool_choice='auto'
)

print(f'Response from llm with tool calling: {response}')
print(f'Tasks list: {tasks}')