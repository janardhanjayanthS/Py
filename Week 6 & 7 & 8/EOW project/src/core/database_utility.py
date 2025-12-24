import os
import tempfile
from ast import Bytes

import psycopg
from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
from langchain_core.documents import Document
from sqlalchemy.orm import Session

from src.core.constants import (
    CONNECTION,
    FILTER_METADATA_BY_HASH_QUERY,
    TEXT_SPLITTER,
    VECTOR_STORE,
    logger,
)
from src.core.utility import hash_bytes, hash_str
from src.models.user import User
from src.schema.user import UserCreate


def add_commit_refresh_db(object: User, db: Session):
    """Adds an object to the database, commits the transaction, and refreshes the instance.

    This helper function handles the standard SQLAlchemy lifecycle for a new or
    updated object to ensure the local instance matches the database state
    (including generated IDs or default values).

    Args:
        object (User): The SQLAlchemy model instance to be persisted.
        db (Session): The active database session.
    """
    db.add(object)
    db.commit()
    db.refresh(object)


def check_existing_user_using_email(db: Session, user: UserCreate) -> bool:
    """Checks if a user already exists in the database based on their email address.

    Args:
        db (Session): The active database session.
        user (UserCreate): A Pydantic schema or object containing the user's
            registration data, specifically the email.

    Returns:
        bool: True if a user with the provided email exists, False otherwise.
    """
    user = db.query(User).filter_by(email=user.email).first()
    return True if user else False


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
    if check_existing_hash(hash=hash_bytes(data=contents)):
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
    if check_existing_hash(hash=hash_str(data=get_base_url(url=url))):
        return f"web - {url} - already exists"

    loader = WebBaseLoader([url])
    docs = loader.load()

    base_url = get_base_url(url=url)
    web_url_hash = hash_str(data=base_url)

    web_document_chunks = TEXT_SPLITTER.split_documents(docs)

    add_base_url_and_hash_to_metadata(
        base_url=base_url, hash=web_url_hash, data=web_document_chunks
    )

    VECTOR_STORE.add_documents(web_document_chunks)
    return f"web - {url} - added successfully"


def get_base_url(url: str) -> str:
    """Extracts the base portion of a URL by removing any fragment identifiers.

    This function splits the URL at the '#' character and returns only the
    preceding part. This is commonly used to normalize URLs and ensure that
    different sections of the same page are treated as the same source.

    Args:
        url: The full URL string, which may include a fragment (e.g., 'example.com/page#section').

    Returns:
        str: The URL without the fragment identifier.
    """
    return url.split("#")[0]


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


def check_existing_hash(hash: str) -> bool:
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
                cur.execute(FILTER_METADATA_BY_HASH_QUERY, (hash,))
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
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
        temp_pdf_file.write(content)
        temp_pdf_filepath = temp_pdf_file.name

    try:
        loader = PyMuPDFLoader(temp_pdf_filepath)
        documents = loader.load()

        for doc in documents:
            doc.metadata["hash"] = pdf_hash
            doc.metadata["source"] = filename

        chunked_documents = TEXT_SPLITTER.split_documents(documents)
        return chunked_documents
    except Exception as e:
        logger.error(f"Error {e}")
        return
    finally:
        if os.path.exists(temp_pdf_filepath):
            os.remove(temp_pdf_filepath)
