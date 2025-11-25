from dotenv import load_dotenv
from langchain.agents import create_agent
from tool import search_book, get_books
from prompt import SYSTEM_PROMPT
from schema import RuntimeContext
from utility import load_json
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


if __name__ == "__main__":
    books: list[dict[str, str]] | None = load_json("../data/books.json")
    # create agent
    agent = create_agent(
        model="openai:gpt-4o-mini",
        system_prompt=SYSTEM_PROMPT,
        tools=[search_book, get_books],
        context_schema=RuntimeContext,
        checkpointer=InMemorySaver(),
    )

    # define context
    context = RuntimeContext(
        data=books,  # type: ignore
        description="Books inventory data",
    )

    question = "List all the available book titles from finance genre"

    for step in agent.stream(
        {"messages": question},
        {"configurable": {"thread_id": "1"}}, 
        context=context, stream_mode="values"
    ):
        step["messages"][-1].pretty_print()

    question = "what is the total price of those books"

    for step in agent.stream(
        {"messages": question},
        {"configurable": {"thread_id": "1"}}, 
        context=context, stream_mode="values"
    ):
        step["messages"][-1].pretty_print()
