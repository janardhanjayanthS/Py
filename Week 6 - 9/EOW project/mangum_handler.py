import json
import os

import boto3
from mangum import Mangum
from src.api.main import app


# Load secrets from AWS Secrets Manager
def load_secrets():
    """Load secrets from AWS Secrets Manager and set as environment variables"""
    secret_name = os.getenv("SECRET_NAME")
    if not secret_name:
        return

    try:
        client = boto3.client("secretsmanager")
        response = client.get_secret_value(SecretId=secret_name)
        secrets = json.loads(response["SecretString"])

        # Set secrets as environment variables
        for key, value in secrets.items():
            os.environ[key] = value
    except Exception as e:
        print(f"Error loading secrets: {e}")


# Load secrets on cold start
load_secrets()

# Update database connection string with environment variables
from src.core import constants

constants.CONNECTION = f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('POSTGRESQL_PWD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Reinitialize database connection and vector store with new connection
from langchain_postgres import PGVector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

constants.engine = create_engine(url=constants.CONNECTION)
constants.session_local = sessionmaker(
    autoflush=False, autocommit=False, bind=constants.engine
)

constants.VECTOR_STORE = PGVector(
    embeddings=constants.EMBEDDING,
    collection_name="uploaded_documents",
    connection=constants.CONNECTION,
    use_jsonb=True,
)

constants.RETRIEVER = constants.VECTOR_STORE.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10},
)

# Create Mangum handler
handler = Mangum(app, lifespan="off")
