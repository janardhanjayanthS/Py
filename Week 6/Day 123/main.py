from decimal import Decimal
from typing import Optional

from constants import GPT_4_MODELS, GPT_5_MODELS, client
from evaluation import evaluate_llm_response
from openai.types.responses import Response
from prompt import SYSTEM_PROMPT_FEW_SHOT
from utility import calculate_token_cost


def get_completion_from_messages(
    messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500
) -> Optional[Response]:
    print(f"Model called using: {model}")
    if model in GPT_4_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as e:
            print(f"Error: {e}")
    elif model in GPT_5_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                reasoning_effort="medium",
            )
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Model {model} not found")
        return

    llm_response = response.choices[0].message.content
    evaluation_score = evaluate_llm_response(
        llm_response=llm_response, user_query=messages[-1]["content"]
    )
    print(f"Evaluation score: {evaluation_score}")
    print("cost: $", Decimal(calculate_token_cost(response=response, model_name=model)))
    return llm_response


if __name__ == "__main__":
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT_FEW_SHOT}
    ]
    user_input: str = input("Enter Password to validate: ")
    messages.append({"role": "user", "content": user_input})
    print(
        get_completion_from_messages(
            messages=messages, model="gpt-4o-mini", temperature=0.5
        )
    )
    print(get_completion_from_messages(messages=messages, model="gpt-5.1"))
    print(get_completion_from_messages(messages=messages, model="gpt-5-nano"))
    print(
        get_completion_from_messages(messages=messages, model="gpt-4.1", temperature=1)
    )
