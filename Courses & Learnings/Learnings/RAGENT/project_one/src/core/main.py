from src.core.constants import llm
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from src.core.prompts import MAIN_AGENT_SYSTEM_PROMPT
from src.core.tools import number_calculation, process_medical_query

agent = create_agent(
    llm,
    tools=[number_calculation, process_medical_query],
    system_prompt=MAIN_AGENT_SYSTEM_PROMPT,
)

config = {"configurable": {"thread_id": "one"}}

def mainloop(human_message: str) -> str:
    messages = [HumanMessage(content=human_message)]
    response = agent.invoke({'messages': messages}, config=config)
    return response['messages'][-1].content



# FOR LOCAL EXEC.
# if __name__ == "__main__":

#     print("AI that answers basic arithmentic questions and medical qeueries")
#     while True:
#         user_input = input("user query: (or) 'e' to exit: ")
#         if user_input.lower() in ["e", "exit"]:
#             break
#         messages = [HumanMessage(content=user_input)]
#         response = agent.invoke({"messages": messages}, config=config)
#         print(f"AI: {response['messages'][-1].content}")

#     print("EXIT")