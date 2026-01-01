from typing import Optional

from fastapi import HTTPException

from src.core.secrets.utility import (
    environment_variable_from_secrets_manager,
    get_local_env_var_else_raise_error,
    running_on_aws,
)


def get_jwt_secret_key() -> Optional[str]:
    env_var = "JWT_SECRET_KEY"
    if running_on_aws():
        try:
            return environment_variable_from_secrets_manager(env_var_name=env_var)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cloud Secret Error: {e}")

    else:
        return get_local_env_var_else_raise_error(env_var_name=env_var)
