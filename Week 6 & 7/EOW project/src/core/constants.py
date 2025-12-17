import logging
from enum import Enum
from os import getenv

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.prompts import SYSTEM_PROMPT

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


OPENAI_API_KEY = getenv("OPENAI_API_KEY")

MODEL_COST_PER_MILLION_TOKENS: dict[str, dict[str, float]] = {
    AIModels.GPT_4o_MINI.value: {"i": 0.15, "o": 0.60},
}

EMBEDDING = OpenAIEmbeddings(
    model=AIModels.TEXT_EMBEDDING_3_LARGE.value, api_key=OPENAI_API_KEY
)

MESSAGES = [SystemMessage(content=SYSTEM_PROMPT)]


# DB
PG_PWD = getenv("POSTGRESQL_PWD")

FILTER_METADATA_BY_HASH_QUERY = """ 
SELECT id, document, cmetadata 
FROM langchain_pg_embedding 
WHERE cmetadata->>'hash' = %s
"""

CONNECTION = f"postgresql+psycopg://postgres:{PG_PWD}@localhost:5432/vector_db"

VECTOR_STORE = PGVector(
    embeddings=EMBEDDING,
    collection_name="uploaded_documents",
    connection=CONNECTION,
    use_jsonb=True,
)

# uses similarity search to get 30 docs -> from that 30 gets top 10 using
# mmr (Maximum Marginal Relevance) and its lambda_mult value
# (1 - most relevant/least diverse, 0 - least relevant/most diverse)
RETRIEVER = VECTOR_STORE.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 15, "fetch_k": 50, "lambda_mult": 0.5},
)

HISTORY = []
