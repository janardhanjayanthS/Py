from functools import wraps
from typing import Callable, Optional

from fastapi import HTTPException, Request, status

from src.core.jwt import decode_access_token


def auth_user(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(
        *args,
        **kwargs,
    ):
        request: Optional[Request] = kwargs.get("request")
        if not request:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Request object missing",
            )

        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
            )

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization scheme",
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format",
            )

        token_data = decode_access_token(token=token)
        user_email = token_data.email

        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        request.state.email = user_email
        return await func(*args, **kwargs)

    return wrapper
