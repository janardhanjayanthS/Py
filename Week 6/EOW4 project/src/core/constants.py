from enum import Enum
from os import getenv

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage

load_dotenv()


# General
class ResponseType(Enum):
    SUCCESS = "success"
    ERROR = "error"


# DB
PG_PWD = getenv("POSTGRESQL_PWD")
connection = f"postgresql+psycopg://postgres:{PG_PWD}@localhost:5432/vector_db"

# AI
OPENAI_API_KEY = getenv("OPENAI_API_KEY")


class AIModels(Enum):
    GPT_4o_MINI = "gpt-4o-mini"


MODEL_COST_PER_MILLION_TOKENS: dict[str, dict[str, float]] = {
    AIModels.GPT_4o_MINI.value: {"i": 0.15, "o": 0.60},
}


SYSTEM_PROMPT = """
You are a helpful assistant agent, answer the question 
carefully with precise answer. 
"""
MESSAGES = [SystemMessage(content=SYSTEM_PROMPT)]
