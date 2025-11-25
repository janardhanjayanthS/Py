from dotenv import load_dotenv
from langchain.agents import create_agent
from tool import search_book
from prompt import SYSTEM_PROMPT
from schema import RuntimeContext
from utility import load_json

load_dotenv()


if __name__ == "__main__":
    books: list[dict[str, str]] | None = load_json("../data/books.json")   

    # create agent
    agent = create_agent(
        model="openai:gpt-4o-mini",
        system_prompt=SYSTEM_PROMPT,
        tools=[search_book],
        context_schema=RuntimeContext,
    )

    # define context
    context = RuntimeContext(
        data=books # type: ignore
    )

    question = "List all the book titles"

    for step in agent.stream({"messages": question}, stream_mode="values"):
        step["messages"][-1].pretty_print()
