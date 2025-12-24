from fastapi import APIRouter, File, HTTPException, UploadFile, status

from src.core.constants import ResponseType, logger
from src.core.database_utility import (
    add_file_as_embedding,
    add_web_content_as_embedding,
)
from src.schema.ai import WebLink

data = APIRouter()


@data.post("/data/upload_pdf")
async def upload_pdf_to_db(file: UploadFile = File(...)):
    """
    Uploads a PDF file and stores its content as embeddings in the vector database.

    Only accepts files with a '.pdf' extension. Reads the file content and
    calls the function to process and add the embeddings.

    Args:
        file: The uploaded file, expected to be a PDF.

    Returns:
        A dictionary with the response status and a message containing the
        database's response upon successful embedding addition.

    Raises:
        HTTPException: If an error occurs during file reading or embedding
                       generation, a 400 Bad Request is raised.
    """
    if not file.filename.endswith(".pdf"):
        message = "Only supports .pdf files"
        logger.error(message)
        raise HTTPException(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=message
        )

    try:
        contents = await file.read()
        file_add_response = add_file_as_embedding(
            contents=contents, filename=file.filename
        )
        return {
            "response": ResponseType.SUCCESS.value,
            "message": {
                "db response": file_add_response,
            },
        }
    except Exception as e:
        logger.error(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while uploading file. Please try again.",
        )


@data.post("/data/upload_web_content")
async def upload_blog_to_db(blog_url: WebLink):
    """
    Fetches content from a specified URL (e.g., a blog) and stores it as
    embeddings in the vector database.

    The URL is extracted from the BlogLink schema and the web content is
    processed for embedding generation.

    Args:
        blog_url: A BlogLink schema object containing the URL of the web content.

    Returns:
        A dictionary with the response status and a message containing the
        database's response upon successful embedding addition.

    Raises:
        HTTPException: If an error occurs during web content retrieval or
                       embedding generation, a 400 Bad Request is raised.
    """
    try:
        web_upload_result = add_web_content_as_embedding(url=str(blog_url.url))
        return {
            "response": ResponseType.SUCCESS.value,
            "message": {
                "db response": web_upload_result,
            },
        }
    except Exception as e:
        logger.error(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while uploading web content. Please try again.",
        )
