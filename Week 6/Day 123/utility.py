from constants import MODEL_COST_PER_MILLION_TOKENS
from openai.types.responses import Response


def get_input_and_output_tokens_from_response(response: Response) -> tuple[int, int]:
    return response.usage.prompt_tokens, response.usage.completion_tokens


def calculate_token_cost(response: Response, model_name: str) -> float:
    input_tokens, output_token = get_input_and_output_tokens_from_response(
        response=response
    )
    input_cost = input_tokens * (
        get_input_cost_for_model(model_name=model_name) / 1_000_000
    )
    output_cost = output_token * (
        get_output_cost_for_model(model_name=model_name) / 1_000_000
    )
    return input_cost + output_cost


def get_input_cost_for_model(model_name: str) -> float | None:
    try:
        model_cost = MODEL_COST_PER_MILLION_TOKENS[model_name]["i"]
        return model_cost
    except AttributeError as e:
        print(f"Error: {e}")


def get_output_cost_for_model(model_name: str) -> float | None:
    try:
        model_cost = MODEL_COST_PER_MILLION_TOKENS[model_name]["o"]
        return model_cost
    except AttributeError as e:
        print(f"Error: {e}")
