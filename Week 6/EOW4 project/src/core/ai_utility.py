from decimal import Decimal

from langchain_openai import ChatOpenAI
from src.core.constants import MODEL_COST_PER_MILLION_TOKENS, OPENAI_API_KEY, AIModels


def get_agent(ai_model: AIModels):
    agent = ChatOpenAI(
        model=ai_model.value, temperature=0, api_key=OPENAI_API_KEY, stream_usage=True
    )
    return agent


def calculate_token_cost(token_usage: dict, ai_model=AIModels) -> str:
    input_tokens = token_usage.get("input_tokens", 0)
    output_tokens = token_usage.get("output_tokens", 0)
    return str(
        Decimal(
            get_input_token_cost(input_tokens=input_tokens, ai_model=ai_model)
            + get_output_token_cost(output_tokens=output_tokens, ai_model=ai_model)
        )
    )


def get_output_token_cost(output_tokens: int, ai_model: AIModels) -> float:
    output_token_cost = output_tokens * (
        MODEL_COST_PER_MILLION_TOKENS[ai_model.value]["o"] / 1_000_000
    )
    return output_token_cost


def get_input_token_cost(input_tokens: int, ai_model: AIModels) -> float:
    input_token_cost = input_tokens * (
        MODEL_COST_PER_MILLION_TOKENS[ai_model.value]["i"] / 1_000_000
    )
    return input_token_cost
