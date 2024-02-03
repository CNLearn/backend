from typing import Optional

from pydantic import BaseModel


class DecodedTokenType(BaseModel):
    exp: int
    sub: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
