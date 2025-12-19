from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from tool import (
    add_to_favorite_authors,
    add_to_favorite_genre,
    add_to_reading_list,
    get_books,
    search_book,
)

load_dotenv()
OPENAI_API_KEY = getenv("OPENAI_API_KEY")

JSON_FILEPATH = str(Path(__file__).parent.parent) + "/data/books.json"

TOOL_LIST: list = [
    search_book,
    get_books,
    add_to_reading_list,
    add_to_favorite_genre,
    add_to_favorite_authors,
]

SENSITIVE_TOOLS = {
    "add_to_reading_list",
    "add_to_favorite_authors",
    "add_to_favorite_genres",
}

# MCP client
BOOK_MCP_PATH = str(Path(__file__).parent / "book_mcp.py")
client = MultiServerMCPClient(
    {"book": {"transport": "stdio", "command": "python", "args": [BOOK_MCP_PATH]}}
)
