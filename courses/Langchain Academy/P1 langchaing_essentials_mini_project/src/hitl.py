from json import dumps


def get_human_approval(tool_name: str, tool_args: dict) -> str:
    """
    This function pauses execution and asks human for approval before executing a tool.

    Args:
        tool_name: Name of the tool the agent wants to call (e.g., "add_to_reading_list")
        tool_args: Arguments the agent wants to pass to the tool

    Returns:
        Human decision: "approve", "reject", or "modify"
    """
    print(f"Agent wants to call tool: {tool_name}")
    print(f"With arguments: {dumps(tool_args, indent=2)}")
    print("=" * 80)

    while True:
        decision = (
            input(
                "\n👤 Your decision:\n"
                "  [a] Approve - Let the agent proceed\n"
                "  [r] Reject - Stop this action\n"
                "  [m] Modify - Change the arguments\n"
                "Choice: "
            )
            .lower()
            .strip()
        )

        if decision in ["a", "approve"]:
            print("Approved! Agent will proceed...")
            return "approve"
        elif decision in ["r", "reject"]:
            print("Rejected! Agent will skip this action...")
            return "reject"
        elif decision in ["m", "modify"]:
            print("Modify mode - You can change the arguments")
            # In a real implementation, you'd allow modifying tool_args here
            return "modify"
        else:
            print("⚠️  Invalid choice. Please enter 'a', 'r', or 'm'")
