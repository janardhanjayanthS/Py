from json import dumps

from constants import OPENAI_API_KEY, SENSITIVE_TOOLS, TOOL_LIST, client
from graph_utility import AgentState
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.types import Command, interrupt
from node_utility import (
    process_single_tool_call,
    update_system_prompt_with_state_variables,
)
from prompt import SYSTEM_PROMPT


async def agent_reasoning_node(state: AgentState):
    """Processes the current state to generate agent reasoning and tool calls.

    This node prepares the dynamic system prompt, binds available tools
    (including dynamic tools from the client), and invokes the LLM. It also
    detects exit intent from the user and tracks the loop iteration count.

    Args:
        state (AgentState): The current global state of the agent.

    Returns:
        dict: A state update containing the LLM response message, any extracted
            pending tool calls, the incremented iteration count, and the exit flag.
    """
    messages = state["message"]
    open_book_tool = await client.get_tools()

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)
    agent = llm.bind_tools(TOOL_LIST + open_book_tool)

    updated_sys_prompt = update_system_prompt_with_state_variables(
        system_prompt=SYSTEM_PROMPT, state=state
    )
    system_message = SystemMessage(content=updated_sys_prompt)

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
    """Triggers a human-in-the-loop interrupt to request tool execution approval.

    This node pauses the graph execution using an interrupt. It displays the
    pending tool calls and their arguments to the user and waits for a
    boolean approval signal.

    Args:
        state (AgentState): The current global state of the agent.

    Returns:
        dict: A state update reflecting the user's decision in `approval_granted`
            and resetting the `awaiting_approval` flag.
    """
    already_denied = "approval_granted" in state and not state.get("awaiting_approval")
    if already_denied:
        print(f"Already denied tool execution - {already_denied}")
        return {}

    print("🚨 APPROVAL REQUIRED")
    for tc in state["pending_tool_calls"]:
        print(f"Tool name: {tc['name']}")
        print(f"Tool args: {dumps(tc['args'], indent=2)}")

    user_approval = interrupt(
        value={"type": "approval_request", "actions": state["pending_tool_calls"]}
    )

    print(f"Approval received: {user_approval}")

    return {
        "approval_granted": user_approval,
        "awaiting_approval": False,
    }


async def check_approval_node(state: AgentState) -> Command:
    """Evaluates if any pending tool calls require explicit user authorization.

    Checks the tool names in the state against a predefined list of sensitive
    tools. Based on this check, it routes the workflow either to the approval
    request node or directly to execution.

    Args:
        state (AgentState): The current global state of the agent.

    Returns:
        Command: A LangGraph Command directing the flow to 'request_approval'
            or 'execute_tools'.
    """
    print("INSIDE check_approval_node!")

    needs_approval = any(
        tc["name"] in SENSITIVE_TOOLS for tc in state["pending_tool_calls"]
    )
    print(f"NEEDS APPROVAL {needs_approval}")

    if needs_approval:
        return Command(goto="request_approval", update={"awaiting_approval": True})

    return Command(goto="execute_tools")


async def execute_tools_node(state: AgentState) -> Command:
    """Executes all pending tool calls and handles the results.

    Iterates through tool calls in the state, processes them (respecting
    whether approval was granted), and generates tool messages to be
    added to the conversation history.

    Args:
        state (AgentState): The current global state of the agent.

    Returns:
        Command: A LangGraph Command that routes back to 'agent_node' with
            updated messages and cleared tool-related state flags.
    """
    print("\n⚙️ Executing tools...")

    tool_messages = []
    approval_granted = state.get("approval_granted", False)

    for tool_call in state["pending_tool_calls"]:
        tool_message = await process_single_tool_call(
            tool_call=tool_call, approval_granted=approval_granted, state=state
        )
        tool_messages.append(tool_message)

    return Command(
        goto="agent_node",
        update={
            "message": tool_messages,
            "pending_tool_calls": [],
            "approval_granted": False,
            "awaiting_approval": False,
        },
    )


def finalize_node(state: AgentState):
    """Performs cleanup and resets counters at the end of a conversation turn.

    Args:
        state (AgentState): The current global state of the agent.

    Returns:
        dict: A state update resetting the `iteration_count` to zero.
    """
    return {"iteration_count": 0}
