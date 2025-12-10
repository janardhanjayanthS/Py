from json import dumps
from typing import Literal

from config import BOOK_MCP_PATH
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.types import Command, interrupt
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


async def check_approval_node(
    state: AgentState,
) -> Command[Literal["request_approval", "execute_tools"]]:
    sensitive_tools = {
        "add_to_reading_list",
        "add_to_favorite_authors",
        "add_to_favorite_genre",
    }
    needs_approval = any(
        tc["name"] in sensitive_tools for tc in state["pending_tool_calls"]
    )

    if needs_approval:
        print("SENSITIVE action")
        return Command(goto="request_approval", update={"awaiting_approval": True})
    else:
        print("INSENSITIVE action")
        return Command(goto="execute_tools", update={"awaiting_approval": False})


def request_approval_node(state: AgentState) -> AgentState:
    print("🚨 APPROVAL REQUIRED")
    for tc in state["pending_tool_calls"]:
        print(f"Tool name: {tc['name']}")
        print(f"Tool args: {dumps(tc['args'], indent=2)}")

    approval = interrupt(
        value={"type": "approval_request", "actions": state["pending_tool_calls"]}
    )
    print("\nApprove? (y/n): ", end="")
    user_approval = input().lower().strip() == "y"

    return {"approval_granted": user_approval, "awaiting_approval": False}


async def execute_tools_node(
    state: AgentState,
) -> Command[Literal["agent_node", "end"]]:
    print("\n⚙️  Executing tools...")
    tool_messages = []

    for tool_call in state["pending_tool_calls"]:
        tool_name = tool_call["name"]
        tool_func = next((t for t in TOOL_LIST if t.name == tool_name), None)

        try:
            result = tool_func.invoke(tool_call["args"])

            tool_msg = ToolMessage(
                content=str(result), tool_call_id=tool_call["id"], name=tool_name
            )
            tool_messages.append(tool_msg)
            print(f"{tool_name} completed")
        except Exception as e:
            error_msg = f"Error: {e}"
            tool_msg = ToolMessage(
                content=error_msg, tool_call_id=tool_call["id"], name=tool_name
            )
            tool_messages.append(tool_msg)
            print(f"{tool_name} failed to execute, error msg: {error_msg}")

    return Command(
        goto="agent_node", update={"messages": tool_messages, "pending_tool_calls": []}
    )
