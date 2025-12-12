import logging
from enum import Enum
from os import getenv

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage

load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H-%M-%S",
)

logger = logging.getLogger(__name__)


# General
class ResponseType(Enum):
    SUCCESS = "success"
    ERROR = "error"


# DB
PG_PWD = getenv("POSTGRESQL_PWD")

FILTER_METADATA_BY_FILENAME_QUERY = """ 
SELECT id, document, cmetadata 
FROM langchain_pg_embedding 
WHERE cmetadata->>'source' = %s
"""

# AI
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


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

DOCUMENT_FORMAT_PROMPT = """Based on the following search results, 
provide a clear and concise answer to the user's question.

User's Question: {query}

Search Results:
{context}

Instructions:
1. Synthesize the information from the search results
2. Provide a clear, direct answer to the question
3. Reference which source(s) the information came from 
    (e.g., "According to algorithms_to_live_by.pdf, page 358...")
4. If the results don't fully answer the question, acknowledge that
5. Keep the response concise but informative
6. Make sure that the response content does not contain any special 
    characters for formatting (\\n, \\t, etc...). give the result as a 
    readable sentence.

Answer:"""
