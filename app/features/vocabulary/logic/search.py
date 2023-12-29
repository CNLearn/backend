import jieba
from pydantic import RootModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exceptions
from app.db.crud.character import character_crud
from app.db.crud.word import word_crud
from app.domain.vocabulary import combined as combined_domain
from app.domain.vocabulary import common as common_domain
from app.domain.vocabulary import word as word_domain


async def search_simplified_words(
    simplified_words: list[word_domain.SimplifiedWord],
    db: AsyncSession,
) -> list[combined_domain.WordOut]:
    words = await word_crud.get_multiple_simplified(db, simplified_words=simplified_words)
    try:
        word_schemas = RootModel[list[combined_domain.WordOut]].model_validate(words).root
    except ValidationError:
        raise exceptions.CNLearnWithMessage(status_code=500, message="There is something wrong with the words.")
    return word_schemas


async def search_characters(
    characters: list[common_domain.Character],
    db: AsyncSession,
    include_words: bool = False,
) -> list[combined_domain.CharacterOut]:
    character_objects = await character_crud.get_multiple_characters(
        db, characters=characters, include_words=include_words
    )
    character_schemas: list[combined_domain.CharacterOut] = []
    if not include_words:
        try:
            character_schemas = [
                combined_domain.CharacterOut.model_validate({**character_object.__dict__, "words": set()})
                for character_object in character_objects
            ]
        except ValidationError:
            raise exceptions.CNLearnWithMessage(
                status_code=500, message="There is something wrong with the characters."
            )
    else:
        try:
            character_schemas = RootModel[list[combined_domain.CharacterOut]].model_validate(character_objects).root
        except ValidationError:
            raise exceptions.CNLearnWithMessage(
                status_code=500, message="There is something wrong with the characters."
            )
    return character_schemas


async def search_phrase(
    phrase: word_domain.SimplifiedWord,
    db: AsyncSession,
    chinese_segmenter: jieba,
) -> combined_domain.DictionarySearchResult:
    # we first segment the phrase into a list of words
    split_words: list[word_domain.SimplifiedWord] = list(chinese_segmenter.cut(phrase))
    word_results = await word_crud.get_multiple_simplified(
        db,
        simplified_words=list(set(split_words)),
    )
    # let's also think about how we will return the not found ones
    not_found: list[word_domain.SimplifiedWord] = list(
        set(split_words).difference(
            set([word_domain.SimplifiedWord(word_domain.Word(w.simplified)) for w in word_results])
        )
    )
    # let's remove any white space ones from the not-found
    not_found = [nf for nf in not_found if nf.strip()]
    try:
        word_schemas = RootModel[list[combined_domain.WordOut]].model_validate(word_results).root
    except ValidationError:
        raise exceptions.CNLearnWithMessage(status_code=500, message="There is something wrong with the words.")
    return combined_domain.DictionarySearchResult(words=word_schemas, not_found=not_found)
