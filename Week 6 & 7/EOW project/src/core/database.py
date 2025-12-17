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
from src.core.utility import hash_bytes, hash_str


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


def add_web_content_as_embedding(url: str) -> str:
    """Fetches web content, processes it, and embeds it with metadata into the vector store.

    This function performs a check to prevent duplicate entries based on the URL.
    If unique, it loads the webpage content, generates a hash of the base URL,
    splits the text into chunks, injects source and hash metadata into each chunk,
    and saves them to the PGVector store.

    Args:
        url: The full URL of the web page to be processed.

    Returns:
        A status message indicating if the URL was already present or successfully added.
    """
    if check_existing_src(src=url):
        return f"web - {url} - already exists"

    loader = WebBaseLoader([url])
    docs = loader.load()

    base_url = url.split("#")[0]
    web_url_hash = hash_str(data=base_url)

    web_document_chunks = TEXT_SPLITTER.split_documents(docs)

    add_base_url_and_hash_to_metadata(
        base_url=base_url, hash=web_url_hash, data=web_document_chunks
    )

    VECTOR_STORE.add_documents(web_document_chunks)
    return f"web - {url} - added successfully"


def add_base_url_and_hash_to_metadata(
    base_url: str, hash: str, data: list[Document]
) -> None:
    """Injects source URL and unique hash into the metadata of each document chunk.

    Iterates through a list of LangChain Document objects and modifies their
    metadata dictionaries in-place to include tracking information. This is
    essential for filtering or deleting specific sources later in the vector store.

    Args:
        base_url: The sanitized URL string to be used as the 'source'.
        hash: The generated unique identifier for the specific web source.
        data: A list of Document objects (chunks) to be updated.

    Returns:
        None
    """
    for doc in data:
        doc.metadata["source"] = base_url
        doc.metadata["hash"] = hash

    if data:
        logger.info(f"Blog document chunk metadata: {data[0].metadata}")


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
    pdf_hash = hash_bytes(data=content)
    # imporvements -> using chunks or try to process in chunks
    pdf_file = io.BytesIO(content)
    pdf_reader = pypdf.PdfReader(pdf_file)
    page_documents = []
    for page_num, page in enumerate(pdf_reader.pages, start=1):
        text = page.extract_text()
        if text:
            page_documents.append(
                Document(
                    page_content=text,
                    metadata={"source": filename, "page": page_num, "hash": pdf_hash},
                )
            )
    chunked_document = TEXT_SPLITTER.split_documents(page_documents)
    logger.info(chunked_document)
    return chunked_document
