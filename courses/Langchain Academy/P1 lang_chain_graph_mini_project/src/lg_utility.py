import operator
from dataclasses import dataclass, field
from typing import Annotated, Any, Optional

from utility import load_json


@dataclass
class AgentState:
    message: Annotated[list[str], operator.add]

    pending_tool_calls: list[dict]
    awaiting_approval: bool
    approval_granted: bool = field(init=False)
    iteration_count: int
    should_exit: bool  # Flag to exit conversation
    last_user_input: str

    favorite_authors: Optional[str] = field(default_factory=list)
    favorite_genres: Optional[str] = field(default_factory=list)
    reading_list: Optional[list[str]] = field(default_factory=list)

    books: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        self.books = load_json(filepath="../data/books.json")
