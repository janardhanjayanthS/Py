import asyncio

from graph import get_compiled_graph
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from utility import load_json


async def mainloop():
    print("Book Manager Agent Welcomes you!")

    agent = get_compiled_graph()
    config = {"configurable": {"thread_id": "1"}}

    turn_count = 1
    while True:
        turn_count += 1
        user_input = input("Prompt to llm [or] 'e' to exit: ")

        if user_input.lower() == "e":
            print("Tata")
            break

        if not user_input:
            print("please enter a message")
            continue

        initial_state = {
            "message": [HumanMessage(content=user_input)],
            "pending_tool_calls": [],
            "awaiting_approval": False,
            "approval_granted": False,
            "iteration_count": 0,
            "should_exit": False,
            "last_user_input": user_input,
            "favorite_authors": [],
            "favorite_genres": [],
            "reading_list": [],
            "books": load_json(filepath="../data/books.json"),
        }

        try:
            async for event in agent.astream(
                initial_state, config, stream_mode="values"
            ):
                final_output = event

            if final_output and final_output["message"]:
                last_msg = final_output["message"][-1]

                if isinstance(last_msg, AIMessage) and last_msg.content:
                    if not last_msg.tool_calls:
                        print(f"\nAssistant: {last_msg.content}")
                        print("-" * 100)
                elif isinstance(last_msg, ToolMessage):
                    pass

            if (
                final_output
                and hasattr(final_output, "should_exit")
                and final_output["should_exit"]
            ):
                print("detected exit request, type 'e' to confirm")

        except Exception as e:
            print("MAINLOOP ERROR")
            print(f"Error: {e}")

    print("Conversation ended")
    print(f"Total turns: {turn_count}")


if __name__ == "__main__":
    asyncio.run(mainloop())
    # TOFIX:
    # - list all books tool is not working!
