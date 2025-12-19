from constants import BOOK_DATA
from langchain.tools import tool
from langgraph_utility import AgentState
from prompt import (
    ADD_TO_FAVORITE_AUTHORS_PROMPT,
    ADD_TO_FAVORITE_GENRES_PROMPT,
    ADD_TO_READING_LIST_PROMPT,
    GET_BOOKS_PROMPT,
    SEARCH_BOOK_PORMPT,
)

SENSITIVE_TOOLS = {
    "add_to_reading_list",
    "add_to_favorite_authors",
    "add_to_favorite_genres",
}

DATA: list


@tool(
    "search_for_book_info",
    parse_docstring=True,
    description=SEARCH_BOOK_PORMPT,
)
def search_book(state: AgentState) -> list:
    """
    Searches for book from qurey

    Args:
        state: agent state with all data

    Returns:
        list[dict]: list containing books as dict
    """
    query = state["message"][-1].content if state["message"] else ""
    result = []

    for book in BOOK_DATA:
        if (
            query in book["title"].lower()
            or query in book["author"].lower()
            or query in book["genre"].lower()
            or str(book["year"]) == query
        ):
            result.append(book)

    return result


@tool("get_all_available_books", parse_docstring=True, description=GET_BOOKS_PROMPT)
def get_books() -> str:
    """
    get books from available books (context)

    Returns:
        list: of dict containing book detail
    """
    return str(BOOK_DATA) if BOOK_DATA else "Unable to load books data"


@tool(
    "add_to_reading_list", parse_docstring=True, description=ADD_TO_READING_LIST_PROMPT
)
def add_to_reading_list(book_title: str, state: AgentState) -> str:
    """
    To add a particular book to user's reading list, which is in RuntimeContext

    Args:
        book_title: title of the book to add
        state: agent state with all data

    Returns:
        str: details about this process (success/fail)
    """
    state["reading_list"].append(book_title)
    return f"Successfully appended book: {book_title} to reading list"


@tool(
    "add_to_favorite_authors",
    parse_docstring=True,
    description=ADD_TO_FAVORITE_AUTHORS_PROMPT,
)
def add_to_favorite_authors(author_name: str, state: AgentState) -> str:
    """
    To add an author's name to favorite_authors (list)
    in memory

    Args:
        author_name: name of the author
        state: agent state with all data

    Returns:
        str: result of this tool call (success/fail)
    """
    state["favorite_authors"].append(author_name)
    return f"Successfully added {author_name} to your favorites"


@tool(
    "add_to_favorite_genres",
    parse_docstring=True,
    description=ADD_TO_FAVORITE_GENRES_PROMPT,
)
def add_to_favorite_genre(genre_type: str, state: AgentState) -> str:
    """
    To add a genre to favorite_genres (list)
    in memory

    Args:
        genre_type: name of the author
        state: agent state with all data

    Returns:
        str: result of this tool call (success/fail)
    """
    state["favorite_genres"].append(genre_type)
    return f"Successfully added {genre_type} to your favorites"
