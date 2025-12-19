from typing import Literal

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph_utility import AgentState
from node import (
    agent_reasoning_node,
    check_approval_node,
    execute_tools_node,
    finalize_node,
    request_approval_node,
)


def get_compiled_graph():
    builder = StateGraph(AgentState)
    build_graph(builder=builder)
    memory = InMemorySaver()
    compiled_graph = builder.compile(checkpointer=memory)
    # Run once to get graph image
    # create_graph_image(graph=compiled_graph)
    return compiled_graph


def create_graph_image(graph) -> None:
    with open("../data/graph_img_new_new.png", "wb+") as file:
        file.write(graph.get_graph().draw_mermaid_png())


def build_graph(builder: StateGraph) -> None:
    # Add all nodes
    builder.add_node("agent_node", agent_reasoning_node)
    builder.add_node("check_approval", check_approval_node)
    builder.add_node("request_approval", request_approval_node)
    builder.add_node("execute_tools", execute_tools_node)
    builder.add_node("finalize", finalize_node)

    # Start edge
    builder.add_edge(START, "agent_node")

    # Route after agent: either check approval or finalize
    def route_after_agent(state: AgentState) -> Literal["check_approval", "finalize"]:
        if state["pending_tool_calls"]:
            return "check_approval"
        return "finalize"

    builder.add_conditional_edges(
        "agent_node",
        route_after_agent,
        {"check_approval": "check_approval", "finalize": "finalize"},
    )

    # Route after check_approval: either request approval or execute directly
    def route_after_check(
        state: AgentState,
    ) -> Literal["request_approval", "execute_tools"]:
        # Check if any pending tools need approval
        from tool import SENSITIVE_TOOLS

        needs_approval = any(
            tc["name"] in SENSITIVE_TOOLS for tc in state["pending_tool_calls"]
        )
        return "request_approval" if needs_approval else "execute_tools"

    builder.add_conditional_edges(
        "check_approval",
        route_after_check,
        {"request_approval": "request_approval", "execute_tools": "execute_tools"},
    )

    # After approval, always go to execute_tools
    builder.add_edge("request_approval", "execute_tools")

    # After executing tools, go back to agent
    builder.add_edge("execute_tools", "agent_node")

    # Finalize ends the conversation
    builder.add_edge("finalize", END)
