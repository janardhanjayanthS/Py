import asyncio

from graph import get_compiled_graph
from langchain_core.messages import AIMessage, HumanMessage
from utility import (
    interrupt_handler,
    is_valid_output,
    no_user_input,
    user_wants_to_exit,
)


async def mainloop():
    print("Book Manager Agent Welcomes you!")

    agent = get_compiled_graph()
    config = {"configurable": {"thread_id": "1"}}
    initial_state = {
        "message": [],
        "pending_tool_calls": [],
        "awaiting_approval": False,
        "approval_granted": False,
        "iteration_count": 0,
        "should_exit": False,
        "last_user_input": "",
        "favorite_authors": [],
        "favorite_genres": [],
        "reading_list": [],
    }

    turn_count = 1
    while True:
        turn_count += 1
        user_input = input("Prompt to llm [or] 'e' to exit: ")

        if user_wants_to_exit(user_input=user_input):
            break

        if no_user_input(user_input=user_input):
            continue

        initial_state["message"].append(HumanMessage(content=user_input))
        initial_state["last_user_input"] = user_input

        current_input = initial_state

        while True:
            try:
                final_output = None
                async for event in agent.astream(
                    current_input, config, stream_mode="values"
                ):
                    final_output = event

                # checking for interrupts
                snapshot = await agent.aget_state(config)
                if snapshot.tasks:
                    current_input, approval_granted = interrupt_handler()
                    continue

                if is_valid_output(final_output=final_output):
                    last_msg = final_output["message"][-1]

                    if isinstance(last_msg, AIMessage) and last_msg.content:
                        if not last_msg.tool_calls:
                            print(f"\nAssistant: {last_msg.content}")
                            print("-" * 100)

                        initial_state = final_output
                    break

                if (
                    final_output
                    and hasattr(final_output, "should_exit")
                    and final_output["should_exit"]
                ):
                    print("detected exit request, type 'e' to confirm")

            except Exception as e:
                print(f"MAINLOOP ERROR: {e}")
                import traceback

                traceback.print_exc()
                break

    print("Conversation ended")
    print(f"Total turns: {turn_count}")


if __name__ == "__main__":
    asyncio.run(mainloop())
