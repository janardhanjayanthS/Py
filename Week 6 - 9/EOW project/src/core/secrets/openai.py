from fastapi import HTTPException

from src.core.secrets.utility import (
    environment_variable_from_secrets_manager,
    get_local_env_var_else_raise_error,
    running_on_aws,
)


def get_openai_key() -> str:
    """Retrieves the OpenAI API key based on the current execution environment.

    This function acts as a wrapper that routes the request to AWS Secrets Manager
    if running in a live production environment, or to local environment
    variables/locals.json if running in a development environment.

    Returns:
        str: The retrieved OpenAI API key.

    Raises:
        HTTPException: A 500 error if the key cannot be retrieved from
            AWS Secrets Manager or is missing from the local environment.
    """
    env_var = "OPENAI_API_KEY"
    # Check if we are in real AWS (Not Local SAM)
    if running_on_aws():
        try:
            return environment_variable_from_secrets_manager(env_var_name=env_var)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cloud Secret Error: {e}")
    # Local Dev or SAM Local
    else:
        return get_local_env_var_else_raise_error(env_var_name=env_var)
