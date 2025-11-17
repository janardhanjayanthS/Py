from openai import OpenAI
from typing import Any
from prompts import system_prompt

client = OpenAI()

tasks: list = []


messages: list[dict[str, Any]] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": ""},
]
