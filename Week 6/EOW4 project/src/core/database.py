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
    """Performs a similarity search against the vector store using the provided query.

    Args:
        query: The user's search query string. This is converted to an embedding for the search.
        k: The number of top-k most relevant documents to retrieve. Defaults to 5.

    Returns:
        A list where the first element is a boolean indicating success (True) or failure (False),
        and the second element is either the list of relevant Document objects or None.
        Example: [True, [Document(...), Document(...)]] or [False, None]
    """
    results = VECTOR_STORE.similarity_search(query=query, k=k)
    if not results:
        return [False, None]
    return [True, results]


def get_formatted_ai_response(
    results: list[Document], query: str, ai_model
) -> AIMessage:
    """Formats the retrieved document chunks and query into a prompt and generates
    a coherent response using the LLM (Large Language Model).

    This function implements the Retrieval-Augmented Generation (RAG) pattern.

    Args:
        results: A list of Document objects retrieved from the vector store.
        query: The original user's question.
        ai_model: The initialized LLM instance used for generating the final answer.

    Returns:
        An AIMessage object containing the final, human-readable answer synthesized
        from the retrieved context and the query.
    """
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
    """Checks if a file already exists in the vector store and, if not, processes
    the file contents, chunks the text, creates embeddings, and adds them to the database.

    Args:
        contents: The raw binary data (Bytes) of the PDF file.
        filename: The name of the file, used as the unique identifier and source metadata.

    Returns:
        A string message indicating whether the file was successfully added or
        if it already existed.
    """
    if check_existing_file(filename=filename):
        return f"File - {filename} - already exists"
    documents = get_documents_from_file_content(content=contents, filename=filename)
    VECTOR_STORE.add_documents(documents)
    return f"File - {filename} - added successfully"


def check_existing_file(filename: str) -> bool:
    """Checks the database directly to see if any document chunks exist with the
    given filename in their metadata.

    Args:
        filename: The name of the file to check for existence.

    Returns:
        True if the file is found in the database, False otherwise or if an
        error occurs during the database operation.
    """
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
    """Parses text from a PDF file's binary content, creates document objects,
    and splits them into smaller, embeddable chunks.

    Args:
        content: The raw binary data (Bytes) of the PDF file.
        filename: The name of the file to be used as the 'source' in the document metadata.

    Returns:
        A list of chunked Document objects ready for embedding and storage.
    """
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
    logger.info(chunked_document)
    return chunked_document
