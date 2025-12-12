import io
from ast import Bytes

import psycopg
import pypdf
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.constants import (
    FILTER_METADATA_BY_FILENAME_QUERY,
    OPENAI_API_KEY,
    OPENAI_EMBEDDING_MODEL,
    PG_PWD,
)

connection = f"postgresql+psycopg://postgres:{PG_PWD}@localhost:5432/vector_db"

embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, api_key=OPENAI_API_KEY)


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
    separators=["\n\n", "\n", " ", ""],
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="uploaded_documents",
    connection=connection,
    use_jsonb=True,
)


def add_file_as_embedding(contents: Bytes, filename: str) -> bool:
    if check_existing_file(filename=filename):
        return False
    documents = get_documents_from_file_content(content=contents, filename=filename)
    vector_store.add_documents(documents)
    return True


def check_existing_file(filename: str) -> bool:
    pg_connection = connection.replace("postgresql+psycopg://", "postgresql://")
    try:
        with psycopg.connect(pg_connection) as conn:
            with conn.cursor() as cur:
                cur.execute(FILTER_METADATA_BY_FILENAME_QUERY, (filename,))
                results = cur.fetchall()
                print(f"DB results: {results}")
                exists = len(results) > 0
                return exists
    except Exception as e:
        print(f"Error: {e}")
        return False


def get_documents_from_file_content(content: Bytes, filename: str) -> list[Document]:
    pdf_file = io.BytesIO(content)
    pdf_reader = pypdf.PdfReader(pdf_file)

    page_documents = []

    for page_num, page in enumerate(pdf_reader.pages, start=1):
        text = page.extract_text()

        if text:
            page_documents.append(
                Document(
                    page_content=text, metadata={"source": filename, "page": page_num}
                )
            )

    chunked_document = text_splitter.split_documents(page_documents)
    return chunked_document
