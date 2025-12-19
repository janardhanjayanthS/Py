from typing import Callable

from graph_utility import AgentState
from langchain_core.messages import ToolMessage


def update_system_prompt_with_state_variables(system_prompt: str, state: AgentState):
    system_prompt_with_state_variables = f"""
    {system_prompt}

    CURRENT USER DATA:
    - favorite authors: {state.get("favorite_authors", [])}
    - favorite genres: {state.get("favorite_genres", [])}
    - reading list: {state.get("reading_list", [])}
    """
    return system_prompt_with_state_variables


def get_tool_message_for_skipped_tool_call(tool_name: str, tool_id: str) -> ToolMessage:
    print(f"TOOL SKIPPED: {tool_name}")
    tool_msg = ToolMessage(
        content="User denied permission to execute this tool.",
        tool_call_id=tool_id,
        name=tool_name,
    )
    return tool_msg


def get_tool_message_for_unknown_tool(tool_name: str, tool_id: str) -> ToolMessage:
    print(f"Tool {tool_name} not found in TOOL_LIST")
    tool_msg = ToolMessage(
        content=f"Error: Tool {tool_name} not found",
        tool_call_id=tool_id,
        name=tool_name,
    )
    return tool_msg


def invoke_tools(
    tool_function: Callable, tool_call: dict, tool_name: str, state: AgentState
) -> str:
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
