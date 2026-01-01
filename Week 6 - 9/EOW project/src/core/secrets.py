import json
import os

import boto3
from fastapi import HTTPException

from src.core.constants import EMBEDDING, PG_PWD


def get_openai_key() -> str:
    # Check if we are in real AWS (Not Local SAM)
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME") and not os.getenv("AWS_SAM_LOCAL"):
        try:
            session = boto3.session.Session()
            client = session.client(
                service_name="secretsmanager", region_name="us-east-1"
            )

            response = client.get_secret_value(SecretId="openai/api_key")
            secret_dict = json.loads(response["SecretString"])
            return secret_dict["OPENAI_API_KEY"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cloud Secret Error: {e}")

    # Local Dev or SAM Local
    else:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise HTTPException(
                status_code=500, detail="OPENAI_API_KEY not found in environment"
            )
        return key


def get_vector_store():
    """Returns a singleton instance of the Vector Store"""
    # We use a global variable to cache the connection so we don't reconnect every time
    global _VECTOR_STORE_INSTANCE

    if "_VECTOR_STORE_INSTANCE" not in globals():
        from langchain_postgres import PGVector

        # Determine connection string based on environment
        db_host = "host.docker.internal" if os.getenv("AWS_SAM_LOCAL") else "localhost"
        db_url = f"postgresql+psycopg://postgres:{PG_PWD}@{db_host}:5432/vector_db"

        globals()["_VECTOR_STORE_INSTANCE"] = PGVector(
            embeddings=EMBEDDING,
            collection_name="uploaded_documents",
            connection=db_url,
            use_jsonb=True,
        )
    return globals()["_VECTOR_STORE_INSTANCE"]
