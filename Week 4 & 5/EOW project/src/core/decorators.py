from functools import wraps
from typing import Callable, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.jwt import decode_access_token
from src.models.models import User


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


# Another way
security = HTTPBearer()


def get_user_from_token(credentials: HTTPAuthorizationCredentials, db: Session) -> User:
    """
    Returns user (db instance) from JWT token

    Args:
        credentials: jwt credentials. Defaults to Depends(security).
        db: database object in session. Defaults to Depends(get_db).

    Returns:
        User: db instance of user

    Raises:
        HTTPException: if cannot find user from database
    """
    token = credentials.credentials
    token_data = decode_access_token(token=token)
    user = db.query(User).filter_by(email=token_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Dependency that gets current user from JWT token

    Args:
        credentials: jwt credentials. Defaults to Depends(security).
        db: database object in session. Defaults to Depends(get_db).
    """
    return get_user_from_token(credentials=credentials, db=db)


async def get_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Dependency that gets current user from JWT token

    Args:
        credentials: jwt credentials. Defaults to Depends(security).
        db: database object in session. Defaults to Depends(get_db).
    """
    user = get_user_from_token(credentials=credentials, db=db)
    if user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Current user is not Admin"
        )

    return user
