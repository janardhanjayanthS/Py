from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Optional

from fastapi import Request
from jose import JWTError, jwt
from src.core.config import settings
from src.core.exceptions import AuthenticationException
from src.core.log import get_logger
from src.schema.token import TokenData
from src.schema.user import UserRole

logger = get_logger(__name__)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT token with user data

    Args:
        data: user's data (eg: name, email)
        expires_delta: token expiry time. Defaults to None.
    """
    to_encode = data.copy()

    to_encode["exp"] = get_expiration_time(expires_delta=expires_delta)

    logger.info(f"To encode: {to_encode}")
    encode_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encode_jwt


def get_expiration_time(expires_delta: timedelta | None) -> datetime:
    """
    gets expiration time for jwt token,
    calcualted based on param or set to 30 from current time

    Args:
        expires_delta: expiration duration for jwt

    Returns:
        datetime: result jwt expiration timestamp
    """
    if expires_delta:
        return datetime.now() + expires_delta
    else:
        return datetime.now() + timedelta(minutes=30)


def decode_access_token(token: str) -> TokenData:
    """
    Decodes incoming jwt token

    Args:
        token: JWT token

    Returns:
        TokenData: pydantic model containing token details

    Raises:
        HTTPException: if invalid/expired token
    """
    try:
        payload: dict = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub", "")
        role: str = payload.get("role", "")

        if email is None:
            raise AuthenticationException(
                message="Could not validate credentials",
                field_errors=[
                    {"field": "token", "message": "Invalid token: missing email"}
                ],
            )

        if role is None:
            raise AuthenticationException(
                message="Could not validate credentials",
                field_errors=[
                    {"field": "token", "message": "Invalid token: missing role"}
                ],
            )

        return TokenData(email=email, role=role)

    except JWTError:
        raise AuthenticationException(
            message="Could not validate credentials",
            field_errors=[{"field": "token", "message": "Invalid or expired token"}],
        )


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
                raise AuthenticationException(
                    message=f"Unauthorized to perform action, you are a {user_role}",
                    field_errors=[
                        {
                            "field": "role",
                            "message": f"Role {user_role} is not authorized for this action",
                        }
                    ],
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
        AuthenticationException: if request object is None
    """
    if not request:
        raise AuthenticationException(
            message="Request object missing",
            field_errors=[{"field": "request", "message": "Request object is missing"}],
        )


def handle_missing_email_in_request(user_email: str) -> None:
    """
    Handles missing email in request

    Args:
        user_email: email id of user

    Raises:
        AuthenticationException: if user_email(param) is empty
    """
    if not user_email:
        raise AuthenticationException(
            message="User not found",
            field_errors=[
                {"field": "email", "message": "User email is missing or invalid"}
            ],
        )


def get_authorization_from_request(request: Request) -> str:
    """
    Gets the authorization string from request

    Args:
        request: request from client

    Returns:
        str: authorization string if exists

    Raises:
        AuthenticationException: if authorization header is missing
    """
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise AuthenticationException(
            message="Authorization header missing",
            field_errors=[
                {
                    "field": "authorization",
                    "message": "Authorization header is required",
                }
            ],
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
        AuthenticationException: If there is'nt a request object
    """
    request: Optional[Request] = kwargs.get("request")
    if not request:
        raise AuthenticationException(
            message="Request object missing",
            field_errors=[
                {"field": "request", "message": "Request object is missing from kwargs"}
            ],
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
        AuthenticationException: if there is any problem with scheme
    """
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise AuthenticationException(
                message="Invalid authorization scheme",
                field_errors=[
                    {
                        "field": "authorization",
                        "message": "Only Bearer scheme is supported",
                    }
                ],
            )
    except ValueError:
        raise AuthenticationException(
            message="Invalid authorization header format",
            field_errors=[
                {
                    "field": "authorization",
                    "message": "Authorization header must be in format 'Bearer <token>'",
                }
            ],
        )
    return token
