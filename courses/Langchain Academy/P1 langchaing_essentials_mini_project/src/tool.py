from langchain.tools import tool
from utility import load_json


books: list[dict[str, str]] | None = load_json("../data/books.json")


@tool(
        'search for book info',
        parse_docstring=True,
        description=(
            "this tool is for searching books from available books"
            "use this whenever there is a query about book details -> title, author, year"
        )
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
