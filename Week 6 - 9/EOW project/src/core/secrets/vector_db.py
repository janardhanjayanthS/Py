import os

from src.core.constants import EMBEDDING
from src.core.secrets.database import get_postgresql_password


def get_vector_store():
    """Returns a singleton instance of the Vector Store"""
    # We use a global variable to cache the connection so we don't reconnect every time
    global _VECTOR_STORE_INSTANCE  # noqa: F824

    if "_VECTOR_STORE_INSTANCE" not in globals():
        from langchain_postgres import PGVector

        # Determine connection string based on environment
        db_host = "host.docker.internal" if os.getenv("AWS_SAM_LOCAL") else "localhost"
        db_url = f"postgresql+psycopg://postgres:{get_postgresql_password()}@{db_host}:5432/vector_db"

        globals()["_VECTOR_STORE_INSTANCE"] = PGVector(
            embeddings=EMBEDDING,
            collection_name="uploaded_documents",
            connection=db_url,
            use_jsonb=True,
        )
    return globals()["_VECTOR_STORE_INSTANCE"]
