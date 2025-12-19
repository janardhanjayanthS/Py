from dataclasses import dataclass
from json import load
from typing import Callable, Optional


@dataclass
class ToolInfo:
    name: str
    id: str
    tool_call: Optional[dict] = None
    mcp_tool: Optional[Callable] = None
    tool_messages: Optional[list] = None


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
            data = load(json_file)
            return data
    except FileNotFoundError as e:
        print(f"Unable to find {filepath}, error: {e}")
        return []


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


def get_book_details(book_data: dict):
    """
    Generates books as a string from data recieved from
    openbooks api

    Args:
        book_data: json response from openbooks api

    Returns:
        string: containing top 5 book details
    """
    result = ""
    for book in book_data["docs"][:5]:
        result += format_book_details(book=book)
    return result


def format_book_details(book: dict) -> str:
    """
    Format the book details received from openbook api,
    used in mcp server

    Args:
        book: response book data

    Returns:
        str: book details as string
    """
    return f"Book Title: {book['title']}, Author: {book['author_name']}, first publish year: {book['first_publish_year']}\n"
