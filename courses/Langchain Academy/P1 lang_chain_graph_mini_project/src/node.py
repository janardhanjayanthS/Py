from langchain_core.messages import SystemMessage
from lg_utility import AgentState
from prompt import SYSTEM_PROMPT


def agent_reasoning_node(state: AgentState) -> AgentState:
    messages = state["messages"]
    system_message = SystemMessage(content=SYSTEM_PROMPT)
