from openai.types.responses import Response


def print_token_information(response: Response) -> None:
    print("Completion tokens: ", response.usage.completion_tokens)
    print("Prompt tokens: ", response.usage.prompt_tokens)
    print("Total tokens: ", response.usage.total_tokens)
