import asyncio

from config import BOOK_MCP_PATH
from dotenv import load_dotenv
from hitl import get_human_approval
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import BaseTool
from langchain_core.messages import ToolMessage
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
    # NOTE: HumanInTheLoopMiddleware has a bug with interrupt() context
    # Using manual HITL instead - intercepting tool calls before execution
    agent = create_agent(
        model="openai:gpt-4o-mini",
        system_prompt=SYSTEM_PROMPT,
        tools=TOOL_LIST + open_book_tool,
        context_schema=RuntimeContext,
        checkpointer=InMemorySaver(),
        # Removed middleware - implementing manual HITL below
    )

    question: str = input("Prompt to LLM [or] 'e' to exit: ").lower()

    while question not in ["e"]:
        config = {"configurable": {"thread_id": "1"}}
        pending_tool_calls = []
        last_ai_message = None

        async for step in agent.astream(
            {"messages": question},  # type: ignore
            config,
            context=context,
            stream_mode="values",
        ):
            if "messages" in step:
                last_message = step["messages"][-1]
                last_message.pretty_print()

                # Manual HITL: Intercept tool calls before execution
                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                    last_ai_message = last_message
                    for tool_call in last_message.tool_calls:
                        tool_name = tool_call.get("name", "unknown")
                        tool_args = tool_call.get("args", {})
                        tool_call_id = tool_call.get("id", "")

                        if tool_name == "add_to_reading_list":
                            # Intercept and ask for approval
                            pending_tool_calls.append(
                                {
                                    "name": tool_name,
                                    "args": tool_args,
                                    "id": tool_call_id,
                                }
                            )
                        else:
                            print(f"Auto executing tool: {tool_name}")

        # Handle human-in-the-loop approval for intercepted tool calls
        if pending_tool_calls:
            tool_messages = []
            for pending_tool_call in pending_tool_calls:
                human_decision = get_human_approval(
                    pending_tool_call["name"], pending_tool_call["args"]
                )

                if human_decision == "approve":
                    print("\nHuman approved! Executing tool...")
                    # Execute the tool and create a ToolMessage with the result
                    try:
                        result = add_to_reading_list.invoke(pending_tool_call["args"])
                        tool_message = ToolMessage(
                            content=str(result), tool_call_id=pending_tool_call["id"]
                        )
                        tool_messages.append(tool_message)
                    except Exception as e:
                        tool_message = ToolMessage(
                            content=f"Error executing tool: {str(e)}",
                            tool_call_id=pending_tool_call["id"],
                            status="error",
                        )
                        tool_messages.append(tool_message)
                elif human_decision == "reject":
                    print("\nHuman Rejected! Tool execution cancelled.")
                    # Create a ToolMessage indicating rejection
                    tool_message = ToolMessage(
                        content="User rejected adding the book to reading list",
                        tool_call_id=pending_tool_call["id"],
                    )
                    tool_messages.append(tool_message)
                elif human_decision == "modify":
                    print("\nModification required!")
                    # In a full implementation, modify tool_args here
                    # For now, treat as rejection
                    tool_message = ToolMessage(
                        content="User requested modification but not implemented yet. Tool call cancelled.",
                        tool_call_id=pending_tool_call["id"],
                    )
                    tool_messages.append(tool_message)

            # Send tool messages back to the agent to continue the conversation
            if tool_messages:
                await agent.ainvoke(
                    {"messages": tool_messages},
                    config=config,
                    context=context,
                )

        print("\n", "=" * 80)
        question: str = input("Prompt to LLM [or] 'e' to exit: ").lower()


if __name__ == "__main__":
    asyncio.run(mainloop())
