from langgraph.runtime import get_runtime
from json import load
from typing import Optional
from schema import RuntimeContext


def load_json(filepath: str) -> list[dict]:
    """
    loads books data from .json file if book exists
    else raises FileNotFoundError

    Args:
        filepath: filepath for json file

    Returns:
        Optional[list[dict]]: book data in list containing dict if book json exists

    Raises:
        FileNotFoundError: if .json is not existing in given filepath
    """
    try:
        with open(filepath, "r") as json_file:
            return load(json_file)
    except FileNotFoundError as e:
        print(f"Unable to find {filepath}, error: {e}")
        return []


def get_books_from_runtime() -> list[dict]:
    """
    returns the books from runtime context

    Returns:
        Optional[list[dict]]: list contining book dictionary
    """
    runtime = get_runtime(RuntimeContext)
    books = runtime.context.data
    return books if books else []


def search_book_using_title(book_title: str, books: list[dict]) -> dict:
    """
    searches book using a param title

    Args:
        book_title: title of the book to search
        books: list of books to search from

    Returns:
        dict: result book details
    """
    for book in books:
        if book["title"].lower() == book_title.lower():
            return book
    return {}
