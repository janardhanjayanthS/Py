from typing import Literal

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from lg_utility import AgentState
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
    with open("../data/graph_img.png", "wb+") as file:
        file.write(graph.get_graph().draw_mermaid_png())


def build_graph(builder: StateGraph) -> None:
    builder.add_node("agent_node", agent_reasoning_node)
    builder.add_node("check_approval", check_approval_node)
    builder.add_node("request_approval", request_approval_node)
    builder.add_node("execute_tools", execute_tools_node)
    builder.add_node("finalize", finalize_node)

    builder.add_edge(START, "agent_node")

    def route_after_agent(state: AgentState) -> Literal["check_approval", "finalize"]:
        if state["pending_tool_calls"]:
            return "check_approval"
        return "finalize"

    def route_after_approval(
        state: AgentState,
    ) -> Literal["execute_tools", "agent_node"]:
        return "execute_tools" if state["approval_granted"] else "agent_node"

    builder.add_conditional_edges(
        "agent_node",
        route_after_agent,
        {"check_approval": "check_approval", "finalize": "finalize"},
    )

    builder.add_conditional_edges(
        "request_approval",
        route_after_approval,
        {"execute_tools": "execute_tools", "agent_node": "agent_node"},
    )

    builder.add_edge("finalize", END)
