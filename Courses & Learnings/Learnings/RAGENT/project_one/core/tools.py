from api import access_medical_api
from api_utility import disease_to_code
from constants import llm
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from prompts import DATA_CLEANER_SYSTEM_PROMPT, MEDICAL_AGENT_SYSTEM_PROMT


@tool(parse_docstring=True)
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
            Acceptable values are 'sum', 'add', 'multiply', 'subtract', or 'divide'.

    Returns:
        int: The result of the arithmetic operation.
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


@tool(parse_docstring=True)
async def get_medical_information(disease: str) -> str:
    """Fetches and cleans medical data for a specific disease from an external API.

    This tool acts as a bridge between raw medical API data and the agent,
    using a secondary 'cleaner' agent to summarize and format the information.

    Args:
        disease (str): The common name of the disease (e.g., 'Diabetes', 'Asthma').

    Returns:
        str: A cleaned, human-readable summary of medical information about the disease.
    """
    code = disease_to_code.get(disease, "Unknown disease")
    print(f"D code: {code}")
    if code == 'Unknown disease':
        return f'Cannont give assistance for this {disease} disease'
    medical_response = await access_medical_api(disease_code=code)
    api_data_cleaner = create_agent(
        llm, system_prompt=SystemMessage(content=DATA_CLEANER_SYSTEM_PROMPT)
    )
    cleaned_api_response = api_data_cleaner.invoke(medical_response)
    cleaned_content = cleaned_api_response.content
    print(f"CLEANED API RESPONSE: {cleaned_content}")
    return cleaned_content


@tool(parse_docstring=True)
def process_medical_query(query: str) -> str:
    """Delegates a complex medical user query to a specialized medical agent.

    Use this tool when a user's question requires multi-step reasoning,
    accessing medical databases, or clinical interpretation.

    Args:
        query (str): The full natural language medical question from the user.

    Returns:
        str: The final interpreted answer from the medical expert agent.
    """
    medical_agent = create_agent(llm, system_prompt=MEDICAL_AGENT_SYSTEM_PROMT)

    result = medical_agent.invoke(
        {"messages": [HumanMessage(content=query)]}, tools=[get_medical_information]
    )
    return result["messages"][-1].content
