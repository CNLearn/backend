from typing import Annotated

from fastapi import Depends, Query
from pydantic import RootModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import database
from app.crud.crud_character import character as crud_character
from app.crud.crud_word import word as crud_word
from app.domain.vocabulary.combined import CharacterOut, WordOut
from app.domain.vocabulary.common import Character
from app.domain.vocabulary.word import SimplifiedWord


async def search_simplified_word(
    simplified_word: Annotated[SimplifiedWord, Query(min_length=1, max_length=50)],
    db: AsyncSession = Depends(database.get_async_session),
) -> list[WordOut] | None:
    words = await crud_word.get_by_simplified(db, simplified=simplified_word)
    if words is None:
        return None
    else:
        return RootModel[list[WordOut]].model_validate(words).root


async def search_character(
    character: Annotated[Character, Query(min_length=1, max_length=1)],
    words: bool = False,
    db: AsyncSession = Depends(database.get_async_session),
) -> CharacterOut | None:
    character_object = await crud_character.get_by_character(db, character=character, include_words=words)
    if character_object is None:
        return None
    else:
        if not words:
            return CharacterOut.model_validate({**character_object.__dict__, "words": set()})
        return CharacterOut.model_validate(character_object)
