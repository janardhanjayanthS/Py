from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """
    Token pydantic schema
    """

    access_token: str
    token_type: Optional[str] = "JWt"


class TokenData(BaseModel):
    """
    Token model for data extracted from jwt
    """

    email: Optional[str] = None
    role: Optional[str] = None
