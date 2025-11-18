from openai import OpenAI
from prompts import system_prompt
from utility import validate_user_input, get_json_from_user_input
from tools import tool_definition
from tool_functions import perform_tool_call
from model import Task
from dotenv import load_dotenv
import os
from tool_functions import tasks

load_dotenv()

opne_ai_api_key = os.getenv("OPEN_AI_API_KEY")

client = OpenAI(api_key=opne_ai_api_key)


def main_loop() -> None:
    """
    Mainloop containing the to-chat bot logic
    """
    while True:
        user_ip = input("Enter a prompt for to-do manager chat bot (or) 'e' to exit: ")
        if user_ip in {"e", "E"}:
            break
        else:
            # task_object_from_user_input: Task = get_json_from_user_input(
            #     user_input=user_ip
            # )
            # valid_user_input: Task | None = validate_user_input(
            #     model=task_object_from_user_input
            # )
            # print(f"Validated user ip: {valid_user_input}, {type(valid_user_input)}")

            messages: list = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_ip},
            ]

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tool_definition,
                tool_choice="auto",
            )

            response_message = response.choices[0].message
            tool_calls: list = getattr(response_message, "tool_calls", [])
            perform_tool_call(tool_calls=tool_calls)
            bot_message = response_message.content
            if bot_message:
                messages.append({'assistant': bot_message})
            print(f"Bot: {response_message.content}")
            # print(f"Response from llm with tool calling: {response}, {type(response)}")
            # print(f"Response message: {response_message}, {type(response_message)}")
            # print(f"Response tool calls: {tool_calls}, {type(tool_calls)}")
            # print(f"Tasks list: {tasks}")


if __name__ == "__main__":
    main_loop()
