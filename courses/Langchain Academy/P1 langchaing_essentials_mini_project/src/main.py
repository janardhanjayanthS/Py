from dotenv import load_dotenv
from langchain.agents import create_agent
from tool import search_book
from prompt import SYSTEM_PROMPT

load_dotenv()








if __name__ == '__main__':
    agent = create_agent(
        model='openai:gpt-4o-mini',
        system_prompt=SYSTEM_PROMPT
    )
    
    
    question = "List all the book titles"
    
    for step in agent.stream(
        {"messages": question},
        stream_mode="values"
    ):
        step["messages"][-1].pretty_print()
