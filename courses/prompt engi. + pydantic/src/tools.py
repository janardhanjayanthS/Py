from typing import Any
from model import AddTaskInput, ListTasksInput, MarkDoneInput
from main import tasks

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


def add_task(add_args: AddTaskInput):
    """
    adds a new task to tasks list

    Args:
        add_args: contains infromation about task
    """
    tasks.append(add_args)


def list_tasks():
    """
    Lists all existing tasks from tasks list
    """
    if tasks:
        print_tasks()
    else:
        print("Tasks list is empty")


def print_tasks() -> None:
    """
    Prints each task line by line
    """
    for task in tasks:
        print(f"id: {task.id} | work: {task.task} | is done: {task.done}")


def mark_done(mark_done_args: MarkDoneInput):
    """
    Marks a task done/compeleted if it exists or
    prints unable to find task.

    Args:
        mark_done_args: contains the id of the ask to update
    """
    for task in tasks:
        if task.id == mark_done_args.task_id:
            task.done = True
            return
    print(f"Unable to find the requested task with id: {mark_done_args.task_id}")
