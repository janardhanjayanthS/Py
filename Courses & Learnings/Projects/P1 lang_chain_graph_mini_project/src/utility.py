from dataclasses import dataclass
from json import load

from langgraph.types import Command


@dataclass
class ToolInfo:
    name: str
    id: str


def is_valid_output(final_output: dict) -> bool:
    """Validates the structure and content of the graph's final output.

    This helper function ensures that the output dictionary is not empty,
    contains the 'message' key, and that the value associated with that
    key is not an empty list or None.

    Args:
        final_output: The dictionary returned by the compiled graph
            after execution.

    Returns:
        bool: True if the output is valid and contains message data;
            False otherwise.
    """
    return final_output and "message" in final_output and final_output["message"]


def interrupt_handler():
    """Handles user interaction during a graph interrupt for approval.

    This function is designed to be called when the graph execution is suspended.
    It prompts the user via the terminal to approve or deny pending actions,
    captures the input, and packages it into a LangGraph `Command` to resume
    the workflow.

    Returns:
        tuple: A tuple containing:
            - current_input (Command): A LangGraph Command object with the
                `resume` value set to the user's decision (True/False).
            - approval_granted (bool): A boolean flag representing the
                user's choice for immediate local logic handling.
    """
    print("IN-IN-shapshot tasks")
    print("---APPROVAL REQUIRED---")
    choice = input("Approve these actions (y/n): ").lower().strip()
    approval_granted = choice == "y"
    current_input = Command(resume=approval_granted)
    return current_input, approval_granted


def user_wants_to_exit(user_input: str) -> bool:
    """Checks if the user has provided the specific exit command.

    This function evaluates the user's input to determine if the conversation
    should be terminated. It specifically looks for the character 'e'.

    Args:
        user_input: The raw string input provided by the user.

    Returns:
        bool: True if the input matches the exit criteria and prints a
            farewell message; False otherwise.
    """
    if user_input.lower() == "e":
        print("Tata")
        return True
    return False


def no_user_input(user_input: str) -> bool:
    """Validates whether the user input is empty or null.

    This helper function ensures that the system does not attempt to process
    blank entries, prompting the user for a valid string if none is found.

    Args:
        user_input: The raw string input to validate.

    Returns:
        bool: True if the input is empty or evaluates to False; False if
            the input contains content.
    """
    if not user_input:
        print("please provide a prompt")
        return True
    return False


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
