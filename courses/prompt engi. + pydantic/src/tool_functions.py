from model import AddTaskInput, ListTasksInput, MarkDoneInput

tasks: list = []


def add_task(add_args: AddTaskInput):
    """
    adds a new task to tasks list

    Args:
        add_args: contains infromation about task
    """
    tasks.append(add_args)
    print(f"Added new task: {add_args.task}")


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
            print(f"Marked task with id {mark_done_args.id} as completed")
            return
    print(f"Unable to find the requested task with id: {mark_done_args.task_id}")


def perform_tool_call(tool_calls: list):
    """
    For each call in tool_calls generates corresponding
    model and calls corresponding fucntion with it

    Args:
        tool_calls: list containing tool_calls (from LLM)
    """
    if tool_calls:
        for tool_call in tool_calls:
            if tool_call.function.name == "add_task":
                call_add_task(tool_call=tool_call)
            elif tool_call.function.name == "list_tasks":
                list_tasks()
            elif tool_call.function.name == "mark_done":
                call_mark_done(tool_call=tool_call)


def call_add_task(tool_call) -> None:
    """
    Calls the add_task function with args from tool_call

    Args:
        tool_call: LLM generated tool call object containing args for add_task function
    """
    add_args: AddTaskInput = AddTaskInput.model_validate_json(
        tool_call.function.arguments
    )
    add_task(add_args=add_args)


def call_mark_done(tool_call) -> None:
    """
    Calls the mark_done function with args from tool_call

    Args:
        tool_call: LLM generated tool call object containing args for mark_done function
    """
    args: MarkDoneInput = MarkDoneInput.model_validate_json(
        tool_call.function.arguments
    )
    mark_done(mark_done_args=args)
