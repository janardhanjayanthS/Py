from json import dumps

from config import BOOK_MCP_PATH, OPENAI_API_KEY
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.types import Command, interrupt
from langgraph_utility import AgentState
from prompt import SYSTEM_PROMPT
from tool import (
    SENSITIVE_TOOLS,
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

    return {
        "message": [response],
        "pending_tool_calls": pending_tools,
        "iteration_count": state["iteration_count"] + 1,
        "should_exit": should_exit,
    }


def request_approval_node(state: AgentState):
    print("🚨 APPROVAL REQUIRED")
    for tc in state["pending_tool_calls"]:
        print(f"Tool name: {tc['name']}")
        print(f"Tool args: {dumps(tc['args'], indent=2)}")

    user_approval = interrupt(
        value={"type": "approval_request", "actions": state["pending_tool_calls"]}
    )

    return {"approval_granted": user_approval, "awaiting_approval": False}


async def check_approval_node(state: AgentState) -> Command:
    print("INSIDE check_approval_node!")

    needs_approval = any(
        tc["name"] in SENSITIVE_TOOLS for tc in state["pending_tool_calls"]
    )
    print(f"NEEDS APPROVAL {needs_approval}")

    if needs_approval:
        return Command(goto="request_approval")

    return Command(goto="execute_tools")


async def execute_tools_node(state: AgentState) -> Command:
    print("\n⚙️ Executing tools...")

    tool_messages = []

    approval_granted = state.get("approval_granted", False)

    for tool_call in state["pending_tool_calls"]:
        tool_id = tool_call["id"]
        tool_name = tool_call["name"]

        if not approval_granted and tool_name in SENSITIVE_TOOLS:
            print(f"TOOL SKIPPED: {tool_name}")
            tool_msg = ToolMessage(
                content="User denied permission to execute this tool.",
                tool_call_id=tool_id,
                name=tool_name,
            )
            tool_messages.append(tool_msg)
            continue

        tool_func = next((t for t in TOOL_LIST if t.name == tool_name), None)
        try:
            if tool_name == "get_all_available_books":
                print("calling get all available books tool")
                result = tool_func.invoke(tool_call["args"])
            elif tool_name == "search_for_book_info":
                print("calling search for book info")
                query = state["message"][-1].content if state["message"] else ""
                tool_call["args"]["query"] = query
                result = tool_func.invoke(tool_call["args"])
            elif tool_name == "add_to_reading_list":
                print("calling add to reading list")
                tool_call["args"]["existing_reading_list"] = state["reading_list"]
                result = tool_func.invoke(tool_call["args"])
            elif tool_name == "add_to_favorite_authors":
                print("calling add to reading list")
                print(f"ARGS: {tool_call['args']}")
                tool_call["args"]["existing_favorite_authors"] = state[
                    "favorite_authors"
                ]
                result = tool_func.invoke(tool_call["args"])

            else:
                print(f"calling {tool_name}!")
                result = tool_func.invoke(tool_call["args"])

            tool_messages.append(
                ToolMessage(content=str(result), tool_call_id=tool_id, name=tool_name)
            )

        except Exception as e:
            tool_messages.append(
                ToolMessage(content=f"Error: {e}", tool_call_id=tool_id, name=tool_name)
            )

    return Command(
        goto="agent_node", update={"message": tool_messages, "pending_tool_calls": []}
    )


def finalize_node(state: AgentState):
    return {"iteration_count": 0}
