import operator
from typing import Annotated, Optional, TypedDict


class AgentState(TypedDict):
    messages: Annotated[list[str], operator.add]

    favorite_authors: Optional[str]
    favorite_genres: Optional[str]
    reading_list: Optional[list[str]]
