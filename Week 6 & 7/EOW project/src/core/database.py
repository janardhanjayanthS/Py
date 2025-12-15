import io
from ast import Bytes

import psycopg
import pypdf
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from src.core.constants import (
    CONNECTION,
    FILTER_METADATA_BY_SOURCE_QUERY,
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
    if check_existing_src(src=filename):
        return f"File - {filename} - already exists"
    documents = get_documents_from_file_content(content=contents, filename=filename)
    VECTOR_STORE.add_documents(documents)
    return f"File - {filename} - added successfully"


async def add_web_content_as_embedding(url: str) -> str:
    """Fetches web content from a given URL, processes it, and embeds it into the vector store.

    This function first checks if the URL has already been processed and stored. If not,
    it loads the content, splits it into smaller chunks, generates embeddings for the
    chunks, and adds them to the VECTOR_STORE.

    Args:
        url: The URL of the web page whose content is to be embedded.

    Returns:
        A string message indicating whether the content was successfully added or
        if it already existed in the store.
    """
    if check_existing_src(src=url):
        return f"web - {url} - already exists"
    loader = WebBaseLoader([url])
    docs = await loader.aload()
    blog_document_chunks = TEXT_SPLITTER.split_documents(docs)
    VECTOR_STORE.add_documents(blog_document_chunks)
    return f"web - {url} - added successfully"


def check_existing_src(src: str) -> bool:
    """Checks the database directly to see if any document chunks exist with the
    given source in their metadata.

    Args:
        source: The name of the file to check for existence.

    Returns:
        True if the file is found in the database, False otherwise or if an
        error occurs during the database operation.
    """
    pg_connection = CONNECTION.replace("postgresql+psycopg://", "postgresql://")
    try:
        with psycopg.connect(pg_connection) as conn:
            with conn.cursor() as cur:
                cur.execute(FILTER_METADATA_BY_SOURCE_QUERY, (src,))
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
