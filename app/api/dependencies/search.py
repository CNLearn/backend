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


async def search_simplified_words(
    simplified_words: Annotated[list[SimplifiedWord], Query(min_length=1, max_length=10)],
    db: AsyncSession = Depends(database.get_async_session),
) -> list[WordOut] | None:
    words = await crud_word.get_multiple_simplified(db, simplified_words=simplified_words)
    return RootModel[list[WordOut]].model_validate(words).root


async def search_characters(
    characters: Annotated[list[Annotated[Character, Query(min_length=1, max_length=1)]], Query(min_length=1)],
    include_words: bool = False,
    db: AsyncSession = Depends(database.get_async_session),
) -> list[CharacterOut]:
    character_objects = await crud_character.get_multiple_characters(
        db, characters=characters, include_words=include_words
    )
    if not include_words:
        return [
            CharacterOut.model_validate({**character_object.__dict__, "words": set()})
            for character_object in character_objects
        ]
    return RootModel[list[CharacterOut]].model_validate(character_objects).root
