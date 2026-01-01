import json
import os
from typing import Dict, Optional

import boto3
from src.core.log import logger

# Cache for secrets to avoid repeated API calls
_secrets_cache: Dict[str, dict] = {}


def get_secret(secret_arn: str) -> Optional[dict]:
    """
    Retrieve secret from AWS Secrets Manager or return None for local dev.
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

        # FIXED: Check if api_key is not None before slicing
        logger.info(
            f"OPENAI API KEY FROM .env file: {api_key[:5] if api_key else 'None'}..."
        )
        return api_key

    # AWS - use Secrets Manager
    secret = get_secret(secret_arn)
    if not secret or "api_key" not in secret:
        raise ValueError(f"Failed to retrieve OpenAI API key from {secret_arn}")

    logger.info(f"OPENAI API KEY FROM Secrets Manager: {secret['api_key'][:5]}...")
    return secret["api_key"]
