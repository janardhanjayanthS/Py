from json import load


def get_qa_data(filename: str):
    try:
        with open(filename, "r") as json_file:
            data = load(json_file)
        print(type(data))
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")


def evaluate_llm_response(response_message: str):
    print(f"LLM response: {response_message}")

    print(get_qa_data(filename="qa_dataset.json"))
