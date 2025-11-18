from typing import Any
from model import AddTaskInput, ListTasksInput, MarkDoneInput
from tool_functions import add_task, list_tasks, mark_done

tool_definition: list[Any] = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "adds a new task to tasks list",
            "parameters": AddTaskInput.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "lists all stored tasks to the CLI",
            "parameters": None,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mark_done",
            "description": "marks a task completed",
            "parameters": MarkDoneInput.model_json_schema(),
        },
    },
]

