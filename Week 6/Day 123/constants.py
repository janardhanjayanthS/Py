from os import getenv

from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = getenv("OPENAI_API_KEY")
DELIMITER = "####"

GPT_4o_MINI = "gpt-4o-mini"
GPT_4_1 = "gpt-4.1"
GPT_5_NANO = "gpt-5-nano"
GPT_5_1 = "gpt-5.1"

MODEL_COST_PER_MILLION_TOKENS: dict[str, dict[str, float]] = {
    GPT_4o_MINI: {"i": 0.15, "o": 0.60},
    GPT_5_1: {"i": 1.25, "o": 10.00},
    GPT_4_1: {"i": 2.0, "o": 8.0},
    GPT_5_NANO: {"i": 0.05, "o": 0.40},
}

GPT_4_MODELS = {GPT_4o_MINI, GPT_4_1}
GPT_5_MODELS = {GPT_5_1, GPT_5_NANO}
