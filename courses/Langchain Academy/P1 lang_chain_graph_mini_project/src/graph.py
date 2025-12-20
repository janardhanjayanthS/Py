from typing import Literal

from constants import SENSITIVE_TOOLS
from graph_utility import AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from node import (
    agent_reasoning_node,
    check_approval_node,
    execute_tools_node,
    finalize_node,
    request_approval_node,
)


def get_compiled_graph():
    """Initializes, builds, and compiles the state graph with memory.

    This function serves as the high-level entry point to create the agentic
    workflow. It initializes a StateGraph, builds the internal architecture,
    and attaches an in-memory checkpointer for state persistence.

    Returns:
        CompiledGraph: A compiled LangGraph instance ready for invocation.
    """
    builder = StateGraph(AgentState)
    build_graph(builder=builder)
    memory = InMemorySaver()
    compiled_graph = builder.compile(checkpointer=memory)
    # Run once to get graph image
    # create_graph_image(graph=compiled_graph)
    return compiled_graph


def create_graph_image(graph) -> None:
    """Generates and saves a Mermaid visual representation of the graph.

    This helper function renders the graph architecture into a PNG file
    using Mermaid syntax, saving it to a local data directory.

    Args:
        graph (CompiledGraph): The compiled graph instance to visualize.

    Returns:
        None
    """
    with open("../data/graph_img_new_new.png", "wb+") as file:
        file.write(graph.get_graph().draw_mermaid_png())


def build_graph(builder: StateGraph) -> None:
    """Defines the nodes, edges, and routing logic for the agent graph.

    This function constructs the workflow topology, including:
    1. Adding functional nodes (reasoning, approval, execution, etc.).
    2. Setting the entry point.
    3. Defining conditional routing based on tool calls and tool sensitivity.
    4. Mapping edges to handle the iterative loop between reasoning and execution.

    Args:
        builder (StateGraph): The graph builder instance to be configured.

    Returns:
        None
    """
    builder.add_node("agent_node", agent_reasoning_node)
    builder.add_node("check_approval", check_approval_node)
    builder.add_node("request_approval", request_approval_node)
    builder.add_node("execute_tools", execute_tools_node)
    builder.add_node("finalize", finalize_node)

    builder.add_edge(START, "agent_node")

    def route_after_agent(state: AgentState) -> Literal["check_approval", "finalize"]:
        """Determines if the agent should move to tool checking or finalization."""
        if state["pending_tool_calls"]:
            return "check_approval"
        return "finalize"

    builder.add_conditional_edges(
        "agent_node",
        route_after_agent,
        {"check_approval": "check_approval", "finalize": "finalize"},
    )

    def route_after_check(
        state: AgentState,
    ) -> Literal["request_approval", "execute_tools"]:
        """Routes to approval request if sensitive tools are detected."""
        needs_approval = any(
            tc["name"] in SENSITIVE_TOOLS for tc in state["pending_tool_calls"]
        )
        return "request_approval" if needs_approval else "execute_tools"

    builder.add_conditional_edges(
        "check_approval",
        route_after_check,
        {"request_approval": "request_approval", "execute_tools": "execute_tools"},
    )

    builder.add_edge("request_approval", "execute_tools")
    builder.add_edge("execute_tools", "agent_node")
    builder.add_edge("finalize", END)
