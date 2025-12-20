from typing import Callable

from constants import SENSITIVE_TOOLS, TOOL_LIST, client
from graph_utility import AgentState
from langchain_core.messages import ToolMessage
from utility import ToolInfo


async def process_single_tool_call(
    tool_call: dict, approval_granted: bool, state: AgentState
) -> ToolMessage:
    """Orchestrates the lifecycle of a single tool execution.

    This function determines if a tool is local or remote (MCP), checks for
    necessary user permissions for sensitive operations, and routes the call
    to the appropriate execution handler.

    Args:
        tool_call: A dictionary containing 'id', 'name', and 'args' for the call.
        approval_granted: Boolean indicating if the user authorized this action.
        state: The current global AgentState.

    Returns:
        ToolMessage: The resulting message containing the tool output or error.
    """
    tool_id = tool_call["id"]
    tool_name = tool_call["name"]

    if not approval_granted and tool_name in SENSITIVE_TOOLS:
        return get_tool_message_for_skipped_tool_call(
            ToolInfo(name=tool_name, id=tool_id)
        )

    tool_func = next((t for t in TOOL_LIST if t.name == tool_name), None)

    if tool_func:
        return await execute_local_tool_call(
            tool_func=tool_func,
            tool_call=tool_call,
            tool=ToolInfo(name=tool_name, id=tool_id),
            state=state,
        )
    else:
        return await execute_mcp_tool_call(
            tool_call=tool_call, tool=ToolInfo(name=tool_name, id=tool_id)
        )


async def execute_local_tool_call(
    tool_func: Callable, tool_call: dict, tool: ToolInfo, state: AgentState
):
    """Executes a tool defined within the local environment.

    Args:
        tool_func: The callable Python function associated with the tool.
        tool_call: The raw tool call data from the LLM.
        tool: Metadata object containing tool name and ID.
        state: The current AgentState.

    Returns:
        ToolMessage: The outcome of the local function execution.
    """
    try:
        result = invoke_tools(
            tool_function=tool_func,
            tool_call=tool_call,
            tool_name=tool.name,
            state=state,
        )
        return ToolMessage(content=str(result), tool_call_id=tool.id, name=tool.name)

    except Exception as e:
        print(f"Error executing tool {tool.name}: {e}")
        return ToolMessage(content=f"Error: {e}", tool_call_id=tool.id, name=tool.name)


async def execute_mcp_tool_call(tool_call: dict, tool: ToolInfo):
    """Fetches and executes a tool via the Model Context Protocol (MCP) client.

    This is used for dynamic tools not hardcoded in the primary TOOL_LIST.

    Args:
        tool_call: The raw tool call data from the LLM.
        tool: Metadata object containing tool name and ID.

    Returns:
        ToolMessage: The result returned from the MCP server or an error message.
    """
    print("Tool not found in existing tool list, checking MCP tools")
    try:
        mcp_tools = await client.get_tools()
        mcp_tool = next((t for t in mcp_tools if t.name == tool.name), None)

        if mcp_tool:
            print(f"Found mcp tool: {mcp_tool.name}")
            print(f"mcp tool args: {tool_call['args']}")
            result = await mcp_tool.ainvoke(tool_call["args"])
            return ToolMessage(
                content=str(result), tool_call_id=tool.id, name=tool.name
            )
        else:
            return get_tool_message_for_unknown_tool(tool=tool)
    except Exception as e:
        message = f"Error with MCP tool exec. {e}"
        print(message)
        return ToolMessage(content=message, tool_call_id=tool.id, name=tool.name)


def update_system_prompt_with_state_variables(system_prompt: str, state: AgentState):
    """Injects current user preferences and state into the base system prompt.

    Args:
        system_prompt: The static base instructions for the agent.
        state: The current AgentState containing user data.

    Returns:
        str: An augmented system prompt with the user's favorite authors,
            genres, and reading list context.
    """
    system_prompt_with_state_variables = f"""
    {system_prompt}

    CURRENT USER DATA:
    - favorite authors: {state.get("favorite_authors", [])}
    - favorite genres: {state.get("favorite_genres", [])}
    - reading list: {state.get("reading_list", [])}
    """
    return system_prompt_with_state_variables


def get_tool_message_for_skipped_tool_call(tool: ToolInfo) -> ToolMessage:
    """Generates a ToolMessage for instances where the user denied execution.

    Args:
        tool: Metadata object for the skipped tool.

    Returns:
        ToolMessage: A message indicating permission was denied.
    """
    print(f"TOOL SKIPPED: {tool.name}")
    tool_msg = ToolMessage(
        content="User denied permission to execute this tool.",
        tool_call_id=tool.id,
        name=tool.name,
    )
    return tool_msg


def get_tool_message_for_unknown_tool(tool: ToolInfo) -> ToolMessage:
    """Generates an error ToolMessage for a tool that cannot be found.

    Args:
        tool: Metadata object for the missing tool.

    Returns:
        ToolMessage: A message reporting that the tool is unrecognized.
    """
    print(f"Tool {tool.name} not found in TOOL_LIST")
    tool_msg = ToolMessage(
        content=f"Error: Tool {tool.name} not found",
        tool_call_id=tool.id,
        name=tool.name,
    )
    return tool_msg


def invoke_tools(
    tool_function: Callable, tool_call: dict, tool_name: str, state: AgentState
) -> str:
    """Invokes local tool functions with context-aware argument injection.

    This function acts as a dispatcher that adds relevant state information
    (like the current reading list or last message content) to tool
    arguments before execution.

    Args:
        tool_function: The tool logic to be invoked.
        tool_call: The dictionary containing arguments from the LLM.
        tool_name: The identifier of the tool being called.
        state: The current AgentState used to hydrate tool arguments.

    Returns:
        str: The result of the tool invocation.
    """
    if tool_name == "get_all_available_books":
        print("calling get all available books tool")
        result = tool_function.invoke(tool_call["args"])
    elif tool_name == "search_for_book_info":
        print("calling search for book info")
        query = state["message"][-1].content if state["message"] else ""
        tool_call["args"]["query"] = query
        result = tool_function.invoke(tool_call["args"])
    elif tool_name == "add_to_reading_list":
        print("calling add to reading list")
        tool_call["args"]["existing_reading_list"] = state["reading_list"]
        result = tool_function.invoke(tool_call["args"])
    elif tool_name == "add_to_favorite_authors":
        print("calling add to favorite authors")
        tool_call["args"]["existing_favorite_authors"] = state["favorite_authors"]
        result = tool_function.invoke(tool_call["args"])
    elif tool_name == "add_to_favorite_genres":
        print("calling add to favorite genres")
        tool_call["args"]["existing_favorite_genres"] = state["favorite_genres"]
        result = tool_function.invoke(tool_call["args"])
    else:
        print(f"calling {tool_name}!")
        result = tool_function.invoke(tool_call["args"])

    return result
