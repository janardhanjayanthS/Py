from os import getenv

from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = getenv("OPENAI_API_KEY")
DELIMITER = "####"


MODEL_COST_PER_MILLION_TOKENS: dict[str, dict[str, float]] = {
    "gpt-4o-mini": {"i": 0.15, "o": 0.60},
    "gpt-5.1": {"i": 1.25, "o": 10.00},
    "gpt-4.1": {"i": 2.0, "o": 8.0},
    "gpt-5-nano": {"i": 0.05, "o": 0.40},
}
