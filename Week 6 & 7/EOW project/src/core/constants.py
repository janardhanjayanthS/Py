import logging
from enum import Enum
from os import getenv

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

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


OPENAI_API_KEY = getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


MODEL_COST_PER_MILLION_TOKENS: dict[str, dict[str, float]] = {
    AIModels.GPT_4o_MINI.value: {"i": 0.15, "o": 0.60},
}

EMBEDDING = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, api_key=OPENAI_API_KEY)


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


CONTEXTUALIZE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                Given a chat history and the latest user question 
                which might reference context in the chat history, formulate a standalone 
                question which can be understood without the chat history. 
                Do NOT answer the question, just reformulate it if needed and otherwise 
                return it as is.
            """,
        ),
        MessagesPlaceholder("chat_history"),  # This will hold the conversation
        ("human", "{question}"),
    ]
)

QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Answer the question based on the following context:

{context}""",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ]
)


# DB
PG_PWD = getenv("POSTGRESQL_PWD")

FILTER_METADATA_BY_SOURCE_QUERY = """ 
SELECT id, document, cmetadata 
FROM langchain_pg_embedding 
WHERE cmetadata->>'source' = %s
"""

CONNECTION = f"postgresql+psycopg://postgres:{PG_PWD}@localhost:5432/vector_db"

VECTOR_STORE = PGVector(
    embeddings=EMBEDDING,
    collection_name="uploaded_documents",
    connection=CONNECTION,
    use_jsonb=True,
)

RETRIEVER = VECTOR_STORE.as_retriever(search_kwargs={"k": 10})

HISTORY = []
