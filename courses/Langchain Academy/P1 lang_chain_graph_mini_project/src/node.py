from json import dumps

from config import BOOK_MCP_PATH, OPENAI_API_KEY
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.types import Command, interrupt
from langgraph_utility import AgentState
from prompt import SYSTEM_PROMPT
from tool import (
    add_to_favorite_authors,
    add_to_favorite_genre,
    add_to_reading_list,
    get_books,
    search_book,
)

TOOL_LIST: list = [
    search_book,
    get_books,
    add_to_reading_list,
    add_to_favorite_genre,
    add_to_favorite_authors,
]

client = MultiServerMCPClient(
    {"book": {"transport": "stdio", "command": "python", "args": [BOOK_MCP_PATH]}}
)


async def agent_reasoning_node(state: AgentState):
    # Dictionary access
    messages = state["message"]
    system_message = SystemMessage(content=SYSTEM_PROMPT)
    open_book_tool = await client.get_tools()

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)
    agent = llm.bind_tools(TOOL_LIST + open_book_tool)

    response = await agent.ainvoke([system_message] + messages)

    last_input = (
        state["last_user_input"].strip().lower() if state["last_user_input"] else ""
    )
    should_exit = last_input == "e" or any(x in last_input for x in ["exit", "quit"])

    pending_tools = []
    if response.tool_calls:
        for tc in response.tool_calls:
            pending_tools.append(
                {"id": tc["id"], "name": tc["name"], "args": tc["args"]}
            )

    # Return a dictionary to update the state
    return {
        "message": [response],
        "pending_tool_calls": pending_tools,
        "iteration_count": state["iteration_count"] + 1,
        "should_exit": should_exit,
    }


async def check_approval_node(state: AgentState) -> Command:
    sensitive_tools = {
        "add_to_reading_list",
        "add_to_favorite_authors",
        "add_to_favorite_genre",
    }
    # Dictionary access
    needs_approval = any(
        tc["name"] in sensitive_tools for tc in state["pending_tool_calls"]
    )

    if needs_approval:
        return Command(goto="request_approval", update={"awaiting_approval": True})

    return Command(goto="execute_tools", update={"awaiting_approval": False})


def request_approval_node(state: AgentState):
    print("🚨 APPROVAL REQUIRED")
    for tc in state["pending_tool_calls"]:
        print(f"Tool name: {tc['name']}")
        print(f"Tool args: {dumps(tc['args'], indent=2)}")

    # Correct dictionary-based interrupt
    interrupt(
        value={"type": "approval_request", "actions": state["pending_tool_calls"]}
    )

    print("\nApprove? (y/n): ", end="")
    user_approval = input().lower().strip() == "y"

    return {"approval_granted": user_approval, "awaiting_approval": False}


async def execute_tools_node(state: AgentState) -> Command:
    print("\n⚙️ Executing tools...")
    tool_messages = []

    for tool_call in state["pending_tool_calls"]:
        tool_name = tool_call["name"]
        tool_func = next((t for t in TOOL_LIST if t.name == tool_name), None)

        try:
            # Note: You might need to handle MCP tools differently if they aren't in TOOL_LIST
            result = tool_func.invoke(tool_call["args"])
            tool_msg = ToolMessage(
                content=str(result), tool_call_id=tool_call["id"], name=tool_name
            )
            tool_messages.append(tool_msg)
        except Exception as e:
            tool_msg = ToolMessage(
                content=f"Error: {e}", tool_call_id=tool_call["id"], name=tool_name
            )
            tool_messages.append(tool_msg)

    return Command(
        goto="agent_node", update={"message": tool_messages, "pending_tool_calls": []}
    )


def finalize_node(state: AgentState):
    return {"iteration_count": 0}
