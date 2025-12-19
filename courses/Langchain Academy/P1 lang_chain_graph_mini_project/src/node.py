from json import dumps

from constants import OPENAI_API_KEY, SENSITIVE_TOOLS, TOOL_LIST, client
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.types import Command, interrupt
from langgraph_utility import AgentState
from node_utility import (
    get_tool_message_for_skipped_tool_call,
    get_tool_message_for_unknown_tool,
    invoke_tools,
    update_system_prompt_with_state_variables,
)
from prompt import SYSTEM_PROMPT


async def agent_reasoning_node(state: AgentState):
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
    print("INSIDE check_approval_node!")

    needs_approval = any(
        tc["name"] in SENSITIVE_TOOLS for tc in state["pending_tool_calls"]
    )
    print(f"NEEDS APPROVAL {needs_approval}")

    if needs_approval:
        return Command(goto="request_approval", update={"awaiting_approval": True})

    return Command(goto="execute_tools")


async def execute_tools_node(state: AgentState) -> Command:
    print("\n⚙️ Executing tools...")

    tool_messages = []
    approval_granted = state.get("approval_granted", False)

    for tool_call in state["pending_tool_calls"]:
        tool_id = tool_call["id"]
        tool_name = tool_call["name"]

        if not approval_granted and tool_name in SENSITIVE_TOOLS:
            tool_messages.append(
                get_tool_message_for_skipped_tool_call(
                    tool_name=tool_name, tool_id=tool_id
                )
            )
            continue

        tool_func = next((t for t in TOOL_LIST if t.name == tool_name), None)

        if not tool_func:
            tool_messages.append(
                get_tool_message_for_unknown_tool(tool_name=tool_name, tool_id=tool_id)
            )
            continue

        try:
            result = invoke_tools(
                tool_function=tool_func,
                tool_call=tool_call,
                tool_name=tool_name,
                state=state,
            )

            tool_messages.append(
                ToolMessage(content=str(result), tool_call_id=tool_id, name=tool_name)
            )

        except Exception as e:
            print(f"Error executing tool {tool_name}: {e}")
            tool_messages.append(
                ToolMessage(content=f"Error: {e}", tool_call_id=tool_id, name=tool_name)
            )

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
    return {"iteration_count": 0}
