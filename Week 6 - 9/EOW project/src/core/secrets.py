import json
import os
from typing import Dict, Optional

import boto3

# Cache for secrets to avoid repeated API calls
_secrets_cache: Dict[str, dict] = {}


def get_secret(secret_arn: str) -> Optional[dict]:
    """
    Retrieve secret from AWS Secrets Manager or return None for local dev.

    Args:
        secret_arn: ARN of the secret (from environment variable)

    Returns:
        Dictionary containing the secret values
    """
    # Check if already cached
    if secret_arn in _secrets_cache:
        return _secrets_cache[secret_arn]

    # Local development mode
    if not secret_arn or secret_arn == "local":
        return None

    try:
        # Create Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name=os.getenv("AWS_REGION_NAME", "us-east-1"),
        )

        # Retrieve the secret
        response = client.get_secret_value(SecretId=secret_arn)
        secret_dict = json.loads(response["SecretString"])

        # Cache it
        _secrets_cache[secret_arn] = secret_dict

        return secret_dict

    except Exception as e:
        print(f"Error retrieving secret {secret_arn}: {e}")
        return None


def get_openai_api_key() -> str:
    """
    Get OpenAI API key from Secrets Manager (AWS) or .env (local).
    """
    secret_arn = os.getenv("OPENAI_SECRET_ARN", "local")

    # Local development - use .env file
    if secret_arn == "local":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        return api_key

    # AWS - use Secrets Manager
    secret = get_secret(secret_arn)
    if not secret:
        raise ValueError(f"Failed to retrieve OpenAI API key from {secret_arn}")

    return secret["api_key"]


# def get_database_config() -> dict:
#     """
#     Get database configuration from Secrets Manager (AWS) or .env (local).
#     """
#     secret_arn = os.getenv("DB_SECRET_ARN", "local")
#
#     # Local development - use .env file
#     if secret_arn == "local":
#         return {
#             "host": os.getenv("DB_HOST", "localhost"),
#             "port": int(os.getenv("DB_PORT", "5432")),
#             "dbname": os.getenv("DB_NAME", "mydatabase"),
#             "username": os.getenv("DB_USER", "myuser"),
#             "password": os.getenv("DB_PASSWORD", "mypassword"),
#         }

# # AWS - use Secrets Manager
# secret = get_secret(secret_arn)
# if not secret:
#     raise ValueError(f"Failed to retrieve database config from {secret_arn}")
#
# return {
#     "host": secret["host"],
#     "port": int(secret["port"]),
#     "dbname": secret["dbname"],
#     "username": secret["username"],
#     "password": secret["password"],
# }


def get_api_key() -> str:
    """
    Get API key from Secrets Manager (AWS) or .env (local).
    """
    secret_arn = os.getenv("API_KEY_SECRET_ARN", "local")

    # Local development
    if secret_arn == "local":
        return os.getenv("API_KEY", "local-dev-key")

    # AWS
    secret = get_secret(secret_arn)
    if not secret:
        raise ValueError(f"Failed to retrieve API key from {secret_arn}")

    return secret["api_key"]
