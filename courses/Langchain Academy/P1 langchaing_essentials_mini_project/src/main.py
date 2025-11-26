import asyncio

from config import BOOK_MCP_PATH
from dotenv import load_dotenv
from hitl import get_human_approval
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
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
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "add_to_reading_list": {"allowed_decisions": ["approve", "reject"]},
                },
            ),  # type: ignore
        ],
    )

    question: str = input("Prompt to LLM [or] 'e' to exit: ").lower()

    while question not in ["e"]:
        async for step in agent.astream(
            {"messages": question},  # type: ignore
            {"configurable": {"thread_id": "1"}},
            context=context,
            stream_mode="values",
        ):
            if "messages" in step:
                last_message = step["messages"][-1]
                last_message.pretty_print()

                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                    for tool_call in last_message.tool_calls:
                        tool_name = tool_call.get("name", "unknown")
                        tool_args = tool_call.get("args", {})

                        if tool_name == "add_to_reading_list":
                            called_add_to_reading_list_tool(agent, tool_name, tool_args)
                        else:
                            print(f"Auto executing tool: {tool_name}")

            if hasattr(step, "interrupt") and step.interrupts:
                print("\n waiting for human response...")

        print("\n", "=" * 80)
        question: str = input("Prompt to LLM [or] 'e' to exit: ").lower()


def called_add_to_reading_list_tool(agent, tool_name, tool_args):
    """
    processes human decision after calling add_to_reading list tool

    Args:
        agent: ai agent
        tool_name: name of the tool
        tool_args: arguments passed to that tool
    """
    human_decision = get_human_approval(tool_name, tool_args)

    if human_decision == "approval":
        print("\nHuman approved!")
    elif human_decision == "reject":
        print("\nHuman Rejected!")
        agent.invoke(
            Command(
                resume={
                    "decisions": [
                        {
                            "type": "reject",
                            "message": "Human interviened while adding data to reading list",
                        }
                    ]
                }
            ),
            config={"configurable": {"thread_id": "1"}},
            context=context,
        )
    elif human_decision == "modify":
        print("\nModification required!")


if __name__ == "__main__":
    asyncio.run(mainloop())
