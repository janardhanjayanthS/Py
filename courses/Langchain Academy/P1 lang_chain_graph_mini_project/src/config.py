from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")


BOOK_MCP_PATH = str(Path(__file__).parent / "book_mcp.py")
