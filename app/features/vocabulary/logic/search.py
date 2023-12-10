from pydantic import RootModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exceptions
from app.db.crud.character import character_crud
from app.db.crud.word import word_crud
from app.domain.vocabulary.combined import CharacterOut, WordOut
from app.domain.vocabulary.common import Character
from app.domain.vocabulary.word import SimplifiedWord


async def search_simplified_words(
    simplified_words: list[SimplifiedWord],
    db: AsyncSession,
) -> list[WordOut]:
    words = await word_crud.get_multiple_simplified(db, simplified_words=simplified_words)
    try:
        word_schemas = RootModel[list[WordOut]].model_validate(words).root
    except ValidationError:
        raise exceptions.CNLearnWithMessage(status_code=500, message="There is something wrong with the words.")
    return word_schemas


async def search_characters(
    characters: list[Character],
    db: AsyncSession,
    include_words: bool = False,
) -> list[CharacterOut]:
    character_objects = await character_crud.get_multiple_characters(
        db, characters=characters, include_words=include_words
    )
    character_schemas: list[CharacterOut] = []
    if not include_words:
        try:
            character_schemas = [
                CharacterOut.model_validate({**character_object.__dict__, "words": set()})
                for character_object in character_objects
            ]
        except ValidationError:
            raise exceptions.CNLearnWithMessage(
                status_code=500, message="There is something wrong with the characters."
            )
    else:
        try:
            character_schemas = RootModel[list[CharacterOut]].model_validate(character_objects).root
        except ValidationError:
            raise exceptions.CNLearnWithMessage(
                status_code=500, message="There is something wrong with the characters."
            )
    return character_schemas
