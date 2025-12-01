from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """
    Token pydantic schema
    """
    access_token: str
    token_type: Optional[str] = "JWt"

class TokenData(Token):
    """
    Token model for data extracted from jwt
    """
    email: Optional[str] = None