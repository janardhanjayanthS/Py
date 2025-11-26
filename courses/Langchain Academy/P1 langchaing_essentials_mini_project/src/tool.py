from langchain.tools import tool
from schema import RuntimeContext
from langgraph.runtime import get_runtime
from prompt import (
    SEARCH_BOOK_PORMPT,
    GET_BOOKS_PROMPT,
    ADD_TO_READING_LIST_PROMPT,
    ADD_TO_FAVORITE_AUTHORS_PROMPT,
    ADD_TO_FAVORITE_GENRES_PROMPT,
)
from utility import get_books_from_runtime, search_book_using_title


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
    books = get_books_from_runtime()
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
    books = get_books_from_runtime()
    result = [book for book in books if book]

    return result


@tool(
    "add_to_reading_list", parse_docstring=True, description=ADD_TO_READING_LIST_PROMPT
)
def add_to_reading_list(book_title: str) -> str:
    """
    To add a particular book to user's reading list, which is in RuntimeContext

    Args:
        book_title: title of the book to add

    Returns:
        str: details about this process (success/fail)
    """
    books: list = get_books_from_runtime()
    reading_list = get_runtime(RuntimeContext).context.reading_list
    book_details = search_book_using_title(book_title=book_title, books=books)

    if book_details:
        reading_list.append(book_details)
        return f"Successfully appended book: {book_details} to reading list"
    else:
        return f"Cannot find requested book ({book_title}), try again"


@tool(
    "add_to_favorite_authors",
    parse_docstring=True,
    description=ADD_TO_FAVORITE_AUTHORS_PROMPT,
)
def add_to_favorite_authors(author_name: str) -> str:
    """
    To add an author's name to favorite_authors (list)
    in memory

    Args:
        author_name: name of the author

    Returns:
        str: result of this tool call (success/fail)
    """
    favorite_authors = get_runtime(RuntimeContext).context.favorite_authors
    favorite_authors.append(author_name)
    return f"Successfully added {author_name} to your favorites"


@tool(
    "add_to_favorite_genres",
    parse_docstring=True,
    description=ADD_TO_FAVORITE_GENRES_PROMPT,
)
def add_to_favorite_genre(genre_type: str) -> str:
    """
    To add a genre to favorite_genres (list)
    in memory

    Args:
        author_name: name of the author

    Returns:
        str: result of this tool call (success/fail)
    """
    favorite_authors = get_runtime(RuntimeContext).context.favorite_genres
    favorite_authors.append(genre_type)
    return f"Successfully added {genre_type} to your favorites"


