from decimal import Decimal
from typing import Optional

from constants import GPT_4_MODELS, GPT_5_MODELS, OPENAI_API_KEY
from evaluation import evaluate_llm_response
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from openai.types.responses import Response
from prompt import SYSTEM_PROMPT_FEW_SHOT
from utility import calculate_token_cost


def get_completion_from_messages(
    messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500
) -> Optional[Response]:
    print(f"Model called using: {model}")
    if model in GPT_4_MODELS:
        try:
            gpt_4_client = ChatOpenAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=OPENAI_API_KEY,
            )
            ai_response = gpt_4_client.invoke(
                input=messages,
            )
            return get_response_content_and_print_token_cost(
                response=ai_response, model=model, messages=messages
            )
        except Exception as e:
            print(f"Error: {e}")
    elif model in GPT_5_MODELS:
        try:
            gpt_5_client = ChatOpenAI(
                model=model,
                reasoning_effort="medium",
                api_key=OPENAI_API_KEY,
            )
            ai_response = gpt_5_client.invoke(
                input=messages,
            )
            return get_response_content_and_print_token_cost(
                response=ai_response, model=model, messages=messages
            )
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Model {model} not found")
        return


def get_response_content_and_print_token_cost(
    response: Response, model: str, messages: list
) -> str:
    llm_response = response.content
    evaluation_score = evaluate_llm_response(
        llm_response=llm_response, user_query=messages[-1].content
    )
    print(f"Evaluation score: {evaluation_score}")
    print("cost: $", Decimal(calculate_token_cost(response=response, model_name=model)))
    return llm_response


if __name__ == "__main__":
    messages = [SystemMessage(content=SYSTEM_PROMPT_FEW_SHOT)]
    user_input: str = input("Enter Password to validate: ")
    messages.append(HumanMessage(content=user_input))
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
