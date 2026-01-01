import json
import os
from typing import Optional

import boto3
from fastapi import HTTPException

# secret_name: string identifier used to tell the AWS Secrets Manager service
# exactly which "vault" or "folder" of secrets you want to open.
aws_secret_name = "openai/api_key"
aws_service_name = "secretsmanager"
aws_region = "us-east-1"


def running_on_aws() -> bool:
    """Checks if the application is currently running on a live AWS environment.

    Determines the environment by verifying the presence of the Lambda function
    name while ensuring it is not the local SAM emulator.

    Returns:
        bool: True if running on a real AWS Lambda environment, False otherwise.
    """
    return os.getenv("AWS_LAMBDA_FUNCTION_NAME") and not os.getenv("AWS_SAM_LOCAL")


def environment_vairable_from_secrets_manager(env_var_name: str) -> Optional[str]:
    """Retrieves a specific environment variable value from AWS Secrets Manager.

    Initializes a Boto3 session to connect to AWS Secrets Manager, fetches
    the predefined secret safe, and parses the JSON string to find the
    requested key.

    Args:
        env_var_name (str): The name of the key to look for inside the
            Secrets Manager JSON object.

    Returns:
        Optional[str]: The secret value associated with the key if found,
            otherwise None.

    Raises:
        botocore.exceptions.ClientError: If there is an issue connecting to
            or fetching from AWS Secrets Manager.
        json.JSONDecodeError: If the 'SecretString' is not valid JSON.
    """
    session = boto3.session.Session()
    client = session.client(service_name=aws_service_name, region_name=aws_region)

    response = client.get_secret_value(SecretId=aws_secret_name)
    secret_dict = json.loads(response["SecretString"])
    return secret_dict.get(env_var_name)


def get_local_env_var_else_raise_error(env_var_name: str) -> Optional[str]:
    """Retrieves an environment variable from the local OS or raises an error.

    This function is intended for local development and SAM local testing to
    ensure required configuration variables (like API keys or DB passwords)
    are present before the application starts.

    Args:
        env_var_name (str): The name of the environment variable to retrieve.

    Returns:
        Optional[str]: The value of the environment variable.

    Raises:
        HTTPException: A 500 error if the environment variable is missing,
            signaling a configuration failure.
    """
    key = os.getenv(env_var_name)

    if not key:
        raise HTTPException(
            status_code=500,
            detail=f"{env_var_name} not found in environment or locals.json",
        )
    return key
