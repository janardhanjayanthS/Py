from pathlib import Path

from langchain.tools import tool
from prompt import (
    ADD_TO_FAVORITE_AUTHORS_PROMPT,
    ADD_TO_FAVORITE_GENRES_PROMPT,
    ADD_TO_READING_LIST_PROMPT,
    GET_BOOKS_PROMPT,
    SEARCH_BOOK_PORMPT,
)
from utility import load_json

# Circular imports
JSON_FILEPATH = str(Path(__file__).parent.parent) + "/data/books.json"


@tool(
    "search_for_book_info",
    parse_docstring=True,
    description=SEARCH_BOOK_PORMPT,
)
def search_book(query: str, books: list) -> list:
    """
    Searches for book from qurey

    Args:
        query: query used for searching book
        books: list of all available books from .json file

    Returns:
        list[dict]: list containing books as dict
    """
    query = query.lower()
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
def get_books() -> str:
    """
    get books from available books (context)

    Returns:
        list: of dict containing book detail
    """
    data = load_json(filepath=JSON_FILEPATH)
    return str(data) if data else "Unable to load books data"


@tool(
    "add_to_reading_list", parse_docstring=True, description=ADD_TO_READING_LIST_PROMPT
)
def add_to_reading_list(book_title: str, existing_reading_list: list) -> str:
    """
    To add a particular book to user's reading list, which is in RuntimeContext

    Args:
        book_title: title of the book to add
        existing_reading_list: user's current reading list

    Returns:
        str: details about this process (success/fail)
    """
    existing_reading_list.append(book_title)
    return f"Successfully appended book: {book_title} to reading list"


@tool(
    "add_to_favorite_authors",
    parse_docstring=True,
    description=ADD_TO_FAVORITE_AUTHORS_PROMPT,
)
def add_to_favorite_authors(author_name: str, existing_favorite_authors: list) -> str:
    """
    To add an author's name to favorite_authors (list)
    in memory

    Args:
        author_name: name of the author

    Returns:
        str: result of this tool call (success/fail)
    """
    existing_favorite_authors.append(author_name)
    return f"Successfully added {author_name} to your favorites"


@tool(
    "add_to_favorite_genres",
    parse_docstring=True,
    description=ADD_TO_FAVORITE_GENRES_PROMPT,
)
def add_to_favorite_genre(genre_type: str, existing_favorite_genres: list) -> str:
    """
    To add a genre to favorite_genres (list)
    in memory

    Args:
        genre_type: name of the author
        existing_favorite_genres: user's current favorite genre list

    Returns:
        str: result of this tool call (success/fail)
    """
    existing_favorite_genres.append(genre_type)
    return f"Successfully added {genre_type} to your favorites"
