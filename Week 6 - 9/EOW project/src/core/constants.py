from enum import Enum

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.core.prompts import SYSTEM_PROMPT
from src.core.secrets.database import get_postgresql_password
from src.core.secrets.openai import get_openai_key

load_dotenv()


# General
class ResponseType(Enum):
    SUCCESS = "success"
    ERROR = "error"


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
    separators=["\n\n", "\n", " ", ""],
)


# AI
class AIModels(Enum):
    GPT_4o_MINI = "gpt-4o-mini"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"


OPENAI_API_KEY = get_openai_key()

MODEL_COST_PER_MILLION_TOKENS: dict[str, dict[str, float]] = {
    AIModels.GPT_4o_MINI.value: {"i": 0.15, "o": 0.60},
}

MESSAGES = [SystemMessage(content=SYSTEM_PROMPT)]


# DB
PG_PWD = get_postgresql_password()

EMBEDDING = OpenAIEmbeddings(
    model=AIModels.TEXT_EMBEDDING_3_LARGE.value, api_key=get_openai_key()
)
FILTER_METADATA_BY_HASH_QUERY = """ 
SELECT id, document, cmetadata 
FROM langchain_pg_embedding 
WHERE cmetadata->>'hash' = %s
"""

# FOR LOCAL
# CONNECTION = f"postgresql+psycopg://postgres:{PG_PWD}@localhost:5432/vector_db"

# FOR AWS
CONNECTION = (
    f"postgresql+psycopg://postgres:{PG_PWD}@host.docker.internal:5432/vector_db"
)

HISTORY = []
