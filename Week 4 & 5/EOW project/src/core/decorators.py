from functools import wraps
from typing import Callable, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.jwt import decode_access_token
from src.models.models import User
from src.schema.user import UserRole


def required_roles(*allowed_roles):
    """
    Decorator for authorizing roles

    Args:
        *allowed_roles: list of UserRole enum
    """

    def decorator(func: Callable) -> Callable:
        """
        Decorator for authorizing user

        Args:
            func: function/end point to use this decorator

        Returns:
            Callable: Returns wrapper

        Raises:
            HTTPException: If user's role is not authorized
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Try to get from kwargs first (production)
            request = kwargs.get("request", None)

            handle_missing_request_object(request=request)

            authorization = get_authorization_from_request(request=request)

            token = verify_scheme_and_return_token(authorization=authorization)

            token_data = decode_access_token(token=token)
            user_email = token_data.email
            user_role = token_data.role

            handle_missing_email_in_request(user_email=user_email)

            # Check if user role is authorized
            if user_role not in UserRole.get_values(roles=allowed_roles):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Unauthorized to perform action, you are a {user_role}",
                )

            # Set user info on request state
            request.state.email = user_email
            request.state.role = user_role

            return await func(*args, **kwargs)

        return wrapper

    return decorator


def handle_missing_request_object(request: Request) -> None:
    """
    Raises error if request object is not found in kwargs, and args

    Args:
        request: request object from client's request

    Raises:
        HTTPException: if request object is None
    """
    if not request:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Request object missing",
        )


def handle_missing_email_in_request(user_email: str) -> None:
    """
    Handles missing email in request

    Args:
        user_email: email id of user

    Raises:
        HTTPException: if user_email(param) is empty
    """
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )


def get_authorization_from_request(request: Request) -> str:
    """
    Gets the authorization string from request

    Args:
        request: request from client

    Returns:
        str: authorization string if exists

    Raises:
        HTTPException: [TODO:throw]
    """
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    return authorization


def get_request_from_jwt(kwargs: dict) -> Request:
    """
    gets Request object from client's request

    Args:
        kwargs: keword arguments dictionary

    Returns:
        Request: object if exists

    Raises:
        HTTPException: If there is'nt a request object
    """
    request: Optional[Request] = kwargs.get("request")
    if not request:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Request object missing",
        )
    return request


def verify_scheme_and_return_token(authorization: str) -> str:
    """
    Verifies scheme from authorization string

    Args:
        authorization: string containing scheme and JWT

    Returns:
        str: JWT token

    Raises:
        HTTPException: if there is any problem with scheme
    """
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
    return token


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


def get_current_user(
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


def get_current_admin(
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
