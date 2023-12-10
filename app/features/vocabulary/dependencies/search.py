from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.vocabulary.combined import CharacterOut, WordOut
from app.domain.vocabulary.common import Character
from app.domain.vocabulary.word import SimplifiedWord
from app.features.db import get_async_session

from ..logic import search as search_logic


async def search_simplified_words(
    simplified_words: Annotated[list[SimplifiedWord], Query(min_length=1, max_length=10)],
    db: AsyncSession = Depends(get_async_session),
) -> list[WordOut]:
    return await search_logic.search_simplified_words(simplified_words, db)


async def search_characters(
    characters: Annotated[list[Annotated[Character, Query(min_length=1, max_length=1)]], Query(min_length=1)],
    db: AsyncSession = Depends(get_async_session),
    include_words: bool = False,
) -> list[CharacterOut]:
    return await search_logic.search_characters(characters, db, include_words)
