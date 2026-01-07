from constants import llm
from langchain.agents import create_agent
from langchain.tools import tool
from prompts import MEDICAL_AGENT_SYSTEM_PROMT


@tool(
    parse_docstring=True,
    description="Performs basic arithmetic operations (sum, subtract, multiply, divide) on two numbers.",
)
def number_calculation(
    number1: int | float, number2: int | float, operation: str
) -> int:
    """Performs a specified arithmetic operation on two numeric inputs.

    This tool handles addition, subtraction, multiplication, and integer division.
    Note: Division uses floor division (//) and returns an integer.

    Args:
        number1 (int | float): The first number in the operation.
        number2 (int | float): The second number in the operation.
            For subtraction (number2 - number1) and division (number2 // number1),
            this acts as the starting value or dividend.
        operation (str): The arithmetic operation to perform.
            Supported values: 'sum', 'add', 'multiply', 'subtract', 'divide'.

    Returns:
        int: The result of the arithmetic operation.

    Raises:
        Exception: If the provided operation string is not supported.
        ZeroDivisionError: If operation is 'divide' and number1 is 0.
    """
    if operation in ["sum", "add"]:
        return number1 + number2
    elif operation == "multiply":
        return number2 * number1
    elif operation == "subtract":
        return number2 - number1
    elif operation == "divide":
        return number2 // number1
    else:
        raise Exception(f"Unknown operation: {operation}")


@tool()
def process_medical_query(query: str) -> str:
    medical_agent = create_agent(llm, system_prompt=MEDICAL_AGENT_SYSTEM_PROMT)
    medical_agent.invoke()

