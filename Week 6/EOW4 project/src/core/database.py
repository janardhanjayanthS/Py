import io
from ast import Bytes

import psycopg
import pypdf
from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from src.core.constants import (
    CONNECTION,
    DOCUMENT_FORMAT_PROMPT,
    FILTER_METADATA_BY_FILENAME_QUERY,
    TEXT_SPLITTER,
    VECTOR_STORE,
    logger,
)


def query_relavent_contents(query: str, k: int = 5) -> bool:
    results = VECTOR_STORE.similarity_search(query=query, k=k)
    if not results:
        return [False, None]
    return [True, results]


def get_formatted_ai_response(
    results: list[Document], query: str, ai_model
) -> AIMessage:
    context_parts = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        content = doc.page_content[:500]

        context_parts.append(f"Source {i}: {source}, Page {page}\n{content}\n")

    context = "\n---\n".join(context_parts)
    updated_prompt = DOCUMENT_FORMAT_PROMPT.format(query=query, context=context)
    ai_response = ai_model.invoke(updated_prompt)
    return ai_response


def add_file_as_embedding(contents: Bytes, filename: str) -> str:
    if check_existing_file(filename=filename):
        return f"File - {filename} - already exists"
    documents = get_documents_from_file_content(content=contents, filename=filename)
    VECTOR_STORE.add_documents(documents)
    return f"File - {filename} - added successfully"


def check_existing_file(filename: str) -> bool:
    pg_connection = CONNECTION.replace("postgresql+psycopg://", "postgresql://")
    try:
        with psycopg.connect(pg_connection) as conn:
            with conn.cursor() as cur:
                cur.execute(FILTER_METADATA_BY_FILENAME_QUERY, (filename,))
                results = cur.fetchall()
                exists = len(results) > 0
                return exists
    except Exception as e:
        logger.error(f"Error: {e}")
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

    chunked_document = TEXT_SPLITTER.split_documents(page_documents)
    return chunked_document
