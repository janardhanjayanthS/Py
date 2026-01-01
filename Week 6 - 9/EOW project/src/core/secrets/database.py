from fastapi import HTTPException

from src.core.secrets.utility import (
    environment_variable_from_secrets_manager,
    get_local_env_var_else_raise_error,
    running_on_aws,
)


def get_postgresql_password() -> str:
    """Retrieves the Postgresql password key based on the current execution environment.

    This function acts as a wrapper that routes the request to AWS Secrets Manager
    if running in a live production environment, or to local environment
    variables/locals.json if running in a development environment.

    Returns:
        str: The retrieved Postgresql password.

    Raises:
        HTTPException: A 500 error if the key cannot be retrieved from
            AWS Secrets Manager or is missing from the local environment.
    """
    env_var = "POSTGRESQL_PWD"
    if running_on_aws():
        try:
            return environment_variable_from_secrets_manager(env_var_name=env_var)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cloud Secret Error: {e}")

    else:
        return get_local_env_var_else_raise_error(env_var_name=env_var)
