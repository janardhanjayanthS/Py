from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()








if __name__ == '__main__':
    agent = create_agent(
        model='openai:gpt-4o-mini',
        system_prompt='you are a helpful assistant'
    )


    question = "Which table has the largest number of entries?"

    for step in agent.stream(
        {"messages": question},
        stream_mode="values"
    ):
        step["messages"][-1].pretty_print()