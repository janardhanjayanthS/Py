from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.core.constants import logger
from src.core.database import get_db
from src.core.jwt import decode_access_token
from src.models.user import User

security = HTTPBearer()


def authenticate_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    token_data = decode_access_token(token=token)
    logger.info(f"User info from token: {token_data}")
    user = db.query(User).filter_by(id=token_data.id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
