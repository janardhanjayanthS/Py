from typing import Any
from model import Task


system_prompt = f"""
Your are a helpful to-do manager agent,
your job is to determine which action to perfrom
based on user's interaction. Based on the user's 
prompts and the pre-defined tools assist the user to 
manage their to do work.

Ask for clarification if any user input is
is unclear

Here is the json for creating a new task
from users prompt: {Task.model_json_schema()}
"""

messages: list[dict[str, Any]] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": },
]
