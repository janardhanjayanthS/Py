from constants import llm
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from prompts import MAIN_AGENT_SYSTEM_PROMPT
from tools import number_calculation, process_medical_query

agent = create_agent(
    llm,
    tools=[number_calculation, process_medical_query],
    system_prompt=MAIN_AGENT_SYSTEM_PROMPT,
)


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "one"}}

    print("AI that answers basic arithmentic questions and medical qeueries")
    while True:
        user_input = input("user query: (or) 'e' to exit: ")
        if user_input.lower() in ["e", "exit"]:
            break
        messages = [HumanMessage(content=user_input)]
        response = agent.invoke({"messages": messages}, config=config)
        print(f"AI: {response['messages'][-1].content}")

    print("EXIT")
