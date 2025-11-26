from config import BOOK_MCP_PATH
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from prompt import SYSTEM_PROMPT
from schema import RuntimeContext
from tool import (
    add_to_favorite_authors,
    add_to_favorite_genre,
    add_to_reading_list,
    get_books,
    search_book,
)
from utility import load_json

load_dotenv()

TOOL_LIST: list[BaseTool] = [
    search_book,
    get_books,
    add_to_reading_list,
    add_to_favorite_genre,
    add_to_favorite_authors,
]

client = MultiServerMCPClient(
    {"book": {"transport": "stdio", "command": "python", "args": [BOOK_MCP_PATH]}}
)

books: list[dict[str, str]] | None = load_json("../data/books.json")

# define context
context = RuntimeContext(
    data=books,  # type: ignore
    description="Books inventory data",
)


async def mainloop():
    """
    mainloop for using agent
    """

    open_book_tool = await client.get_tools()

    # create agent
    agent = create_agent(
        model="openai:gpt-4o-mini",
        system_prompt=SYSTEM_PROMPT,
        tools=TOOL_LIST + open_book_tool,
        context_schema=RuntimeContext,
        checkpointer=InMemorySaver(),
    )

    question: str = input("Prompt to LLM/e to exit: ").lower()

    while question not in ["e"]:
        for step in agent.stream(
            {"messages": question},  # type: ignore
            {"configurable": {"thread_id": "1"}},
            context=context,
            stream_mode="values",
        ):
            step["messages"][-1].pretty_print()

        question: str = input("Prompt to LLM [or] 'e' to exit: ").lower()


if __name__ == "__main__":
    await mainloop()
