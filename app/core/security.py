import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.settings.base import settings

ALGORITHM = "HS256"

logger = logging.getLogger(__name__)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload: dict = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except (JWTError, ExpiredSignatureError):
        # TODO: log this
        raise
    return payload