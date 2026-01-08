from constants import llm
from langchain.agents import create_agent
from prompts import MAIN_AGENT_SYSTEM_PROMPT
from tools import number_calculation, process_medical_query

agent = create_agent(llm, system_prompt=MAIN_AGENT_SYSTEM_PROMPT)
response = agent.invoke(tools=[number_calculation, process_medical_query])

print(response)
