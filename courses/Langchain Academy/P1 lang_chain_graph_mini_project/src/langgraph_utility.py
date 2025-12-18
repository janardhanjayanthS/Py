import operator
from typing import Annotated, Any, TypedDict


# We use TypedDict for seamless compatibility with LangGraph's update logic
class AgentState(TypedDict):
    message: Annotated[list[Any], operator.add]
    pending_tool_calls: list[dict]
    awaiting_approval: bool
    approval_granted: bool
    iteration_count: int
    should_exit: bool
    last_user_input: str
    favorite_authors: list[str]
    favorite_genres: list[str]
    reading_list: list[str]
    books: list[dict[str, Any]]
