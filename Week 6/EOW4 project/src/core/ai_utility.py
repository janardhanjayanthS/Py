from decimal import Decimal

from langchain_openai import ChatOpenAI
from src.core.constants import MODEL_COST_PER_MILLION_TOKENS, OPENAI_API_KEY, AIModels


def get_agent(ai_model: AIModels):
    """Initializes and returns an instance of the ChatOpenAI client.

    The client is configured to use the specified model, a temperature of 0
    (for deterministic responses), and enables streaming usage tracking.

    Args:
        ai_model: An enum member (AIModels) specifying the desired OpenAI model (e.g., GPT-4, GPT-3.5-turbo).

    Returns:
        A configured instance of the ChatOpenAI client.
    """
    agent = ChatOpenAI(
        model=ai_model.value, temperature=0, api_key=OPENAI_API_KEY, stream_usage=True
    )
    return agent


def calculate_token_cost(token_usage: dict, ai_model=AIModels) -> str:
    """Calculates the total monetary cost incurred for a given prompt-response pair based on token usage.

    The cost is calculated by summing the input token cost and the output token cost
    using the predefined cost rates for the specified model.

    Args:
        token_usage: A dictionary containing the token counts, expected to have keys "input_tokens" and "output_tokens".
        ai_model: An enum member (AIModels) specifying the model used for the operation.

    Returns:
        A string representation of the total calculated cost (e.g., "0.00015").
    """
    input_tokens = token_usage.get("input_tokens", 0)
    output_tokens = token_usage.get("output_tokens", 0)
    return str(
        Decimal(
            get_input_token_cost(input_tokens=input_tokens, ai_model=ai_model)
            + get_output_token_cost(output_tokens=output_tokens, ai_model=ai_model)
        )
    )


def get_output_token_cost(output_tokens: int, ai_model: AIModels) -> float:
    """Calculates the monetary cost specifically for the output (response) tokens.

    The cost is based on the model's defined cost per million output tokens.

    Args:
        output_tokens: The number of tokens generated in the LLM's response.
        ai_model: An enum member (AIModels) specifying the model used.

    Returns:
        The total cost of the output tokens as a float.
    """
    output_token_cost = output_tokens * (
        MODEL_COST_PER_MILLION_TOKENS[ai_model.value]["o"] / 1_000_000
    )
    return output_token_cost


def get_input_token_cost(input_tokens: int, ai_model: AIModels) -> float:
    """Calculates the monetary cost specifically for the input (prompt/context) tokens.

    The cost is based on the model's defined cost per million input tokens.

    Args:
        input_tokens: The number of tokens sent to the LLM in the prompt and context.
        ai_model: An enum member (AIModels) specifying the model used.

    Returns:
        The total cost of the input tokens as a float.
    """
    input_token_cost = input_tokens * (
        MODEL_COST_PER_MILLION_TOKENS[ai_model.value]["i"] / 1_000_000
    )
    return input_token_cost
