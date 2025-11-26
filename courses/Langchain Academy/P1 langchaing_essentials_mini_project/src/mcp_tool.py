from langchain_mcp_adapters.client import MultiServerMCPClient
from pathlib import Path

BOOK_MCP_PATH = str(Path(__file__).parent / "book_mcp.py")

client = MultiServerMCPClient(
    {"book": {"transport": "stdio", "command": "python", "args": [BOOK_MCP_PATH]}}
)

open_book_tool = await client.get_tools()
