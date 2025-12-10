from config import BOOK_MCP_PATH
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from lg_utility import AgentState
from prompt import SYSTEM_PROMPT
from schema import BaseTool
from tool import (
    add_to_favorite_authors,
    add_to_favorite_genre,
    add_to_reading_list,
    get_books,
    search_book,
)

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


async def agent_reasoning_node(state: AgentState) -> AgentState:
    messages = state["messages"]
    system_message = SystemMessage(content=SYSTEM_PROMPT)
    open_book_tool = await client.get_tools()

    agent = create_agent(
        model="openai:gpt-4o-mini",
        system_prompt=SYSTEM_PROMPT,
        tools=TOOL_LIST + open_book_tool,
    )

    response = await agent.ainvoke([system_message] + messages)

    last_input = state.get("last_user_input", "").strip().lower()
    should_exit = last_input == "e" or "exit" in last_input or "quit" in last_input

    pending_tools = []
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tc in response.tool_calls:
            pending_tools.append(
                {"id": tc["id"], "name": tc["name"], "args": tc["args"]}
            )

    return AgentState(
        messages=[response],
        pending_tools_calls=pending_tools,
        iteration_count=state["iteration_count"] + 1,
        should_exit=should_exit,
    )
