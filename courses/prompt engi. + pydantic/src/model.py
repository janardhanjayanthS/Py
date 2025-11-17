from pydantic import BaseModel


class Task(BaseModel):
    """
    A task model
    """

    id: int
    task: str
    done: bool


class AddTaskInput(Task):
    """
    Add task model
    """

    task: str


class MarkDoneInput(Task):
    """
    Marks a particular task done
    """

    task_id: int


class ListTasksInput:
    """
    Lists all tasks
    """

