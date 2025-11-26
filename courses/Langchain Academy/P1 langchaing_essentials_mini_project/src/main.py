from dotenv import load_dotenv
from langchain.agents import create_agent
from tool import search_book, get_books, add_to_reading_list, add_to_favorite_authors, add_to_favorite_genre
from prompt import SYSTEM_PROMPT
from schema import RuntimeContext
from utility import load_json
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import BaseTool

load_dotenv()

TOOL_LIST: list[BaseTool] = [
    search_book, 
    get_books, 
    add_to_reading_list,
    add_to_favorite_genre,
    add_to_favorite_authors
]


def mainloop():
    """
    mainloop for using agent
    """
    question: str = input("Prompt to LLM/e to exit: ").lower()
    while question not in ['e']:
        for step in agent.stream(
            {"messages": question},
            {"configurable": {"thread_id": "1"}},
            context=context,
            stream_mode="values",
        ):
            step["messages"][-1].pretty_print()
        question: str = input("Prompt to LLM [or] 'e' to exit: ").lower()
    


if __name__ == "__main__":
    books: list[dict[str, str]] | None = load_json("../data/books.json")
    # create agent
    agent = create_agent(
        model="openai:gpt-4o-mini",
        system_prompt=SYSTEM_PROMPT,
        tools=TOOL_LIST,
        context_schema=RuntimeContext,
        checkpointer=InMemorySaver(),
    )

    # define context
    context = RuntimeContext(
        data=books,  # type: ignore
        description="Books inventory data",
    )

    mainloop()