from langchain.tools import tool
from langgraph.runtime import get_runtime
from schema import RuntimeContext
from prompt import SEARCH_BOOK_PORMPT, GET_BOOKS_PROMPT


@tool(
    "search_for_book_info",
    parse_docstring=True,
    description=SEARCH_BOOK_PORMPT,
)
def search_book(query: str) -> list:
    """
    Searches for book from qurey

    Args:
        query: query used for searching book

    Returns:
        list[dict]: list containing books as dict
    """
    query = query.lower()
    runtime = get_runtime(RuntimeContext)
    books = runtime.context.data
    result = []

    for book in books:
        if (
            query in book["title"].lower()
            or query in book["author"].lower()
            or query in book["genre"].lower()
            or str(book["year"]) == query
        ):
            result.append(book)

    return result


@tool("get_all_available_books", parse_docstring=True, description=GET_BOOKS_PROMPT)
def get_books() -> list:
    """
    get books from available books (context)

    Returns:
        list: of dict containing book detail
    """
    runtime = get_runtime(RuntimeContext)
    books = runtime.context.data
    result = [book for book in books if book]

    return result
