import operator
from typing import Annotated, Optional, TypedDict


class AgentState(TypedDict):
    messages: Annotated[list[str], operator.add]
    pending_tool_calls: list[dict]
    awaiting_approval: bool
    approval_granted: bool
    iteration_count: int
    should_exit: bool  # Flag to exit conversation
    last_user_input: str

    favorite_authors: Optional[str]
    favorite_genres: Optional[str]
    reading_list: Optional[list[str]]
