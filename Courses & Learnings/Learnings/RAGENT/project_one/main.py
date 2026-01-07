from constants import llm
from langchain.agents import create_agent
from prompts import MAIN_AGENT_SYSTEM_PROMPT

agent = create_agent(llm, system_prompt=MAIN_AGENT_SYSTEM_PROMPT)
