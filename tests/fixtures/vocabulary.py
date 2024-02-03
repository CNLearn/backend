from typing import Awaitable, Callable

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.models import character as character_model
from app.db.models import word as word_model
from app.domain.vocabulary import character as character_domain
from app.domain.vocabulary import common as common_domain
from app.domain.vocabulary import word as word_domain
from app.settings.db import db_settings
from tests.fixtures.data import sample_characters, sample_words


def add_some_words_and_characters() -> None:
    postgres_uri = str(db_settings.CNLEARN_POSTGRES_URI)
    postgres_uri = postgres_uri.replace("+asyncpg", "+psycopg")
    engine = create_engine(postgres_uri)
    engine.connect()
    Session = sessionmaker(engine)
    with Session() as session:
        characters_to_add = sample_characters()
        words_to_add = sample_words()
        for character_schema in characters_to_add:
            character_obj = character_model.Character(**character_schema.model_dump())
            session.add(character_obj)
        for word_schema in words_to_add:
            word_obj = word_model.Word(**word_schema.model_dump())
            session.add(word_obj)
        session.commit()
        all_words = session.execute(select(word_model.Word)).scalars()
        for word in all_words:
            characters: set[str] = set(character for character in word.simplified if character.isalpha())
            if not characters:
                continue
            else:
                # let's get the character object
                character_set: set[character_model.Character] = set()
                for character in characters:
                    try:
                        character_object = session.execute(
                            select(character_model.Character).where(character_model.Character.character == character)
                        ).scalar_one()
                    except NoResultFound:
                        pass
                    else:
                        character_set.add(character_object)
                if character_set:
                    word.characters = character_set
                    session.add(word)
        session.commit()
    engine.dispose()


@pytest.fixture(scope="function")
def generate_character_schema() -> Callable[
    [
        common_domain.Character,
        common_domain.Definition | None,
        common_domain.PinyinToneMarks,
        character_domain.Decomposition | None,
        character_domain.Etymology | None,
        character_domain.Radical,
        character_domain.Matches,
        common_domain.Frequency,
    ],
    character_domain.CharacterSchema,
]:
    def _generate_character_schema(
        character: common_domain.Character,
        definition: common_domain.Definition | None,
        pinyin: common_domain.PinyinToneMarks,
        decomposition: character_domain.Decomposition | None,
        etymology: character_domain.Etymology | None,
        radical: character_domain.Radical,
        matches: character_domain.Matches,
        frequency: common_domain.Frequency,
    ) -> character_domain.CharacterSchema:
        return character_domain.CharacterSchema(
            character=character,
            definition=definition,
            pinyin=pinyin,
            decomposition=decomposition,
            etymology=etymology,
            radical=radical,
            matches=matches,
            frequency=frequency,
        )

    return _generate_character_schema


@pytest.fixture(scope="function")
def generate_word_schema() -> Callable[
    [
        word_domain.SimplifiedWord,
        word_domain.TraditionalWord,
        common_domain.PinyinToneNumbers,
        common_domain.PinyinToneMarks,
        common_domain.PinyinNoToneMarks,
        common_domain.PinyinNoSpacesNoToneMarks,
        word_domain.AlsoWritten,
        word_domain.AlsoPronounced,
        word_domain.Classifiers,
        common_domain.Definition,
        common_domain.Frequency,
    ],
    word_domain.WordSchema,
]:
    def _generate_word_schema(
        simplified: word_domain.SimplifiedWord,
        traditional: word_domain.TraditionalWord,
        pinyin_num: common_domain.PinyinToneNumbers,
        pinyin_accent: common_domain.PinyinToneMarks,
        pinyin_clean: common_domain.PinyinNoToneMarks,
        pinyin_no_spaces: common_domain.PinyinNoSpacesNoToneMarks,
        also_written: word_domain.AlsoWritten,
        also_pronounced: word_domain.AlsoPronounced,
        classifiers: word_domain.Classifiers,
        definitions: common_domain.Definition,
        frequency: common_domain.Frequency,
    ) -> word_domain.WordSchema:
        return word_domain.WordSchema(
            simplified=simplified,
            traditional=traditional,
            pinyin_num=pinyin_num,
            pinyin_accent=pinyin_accent,
            pinyin_clean=pinyin_clean,
            pinyin_no_spaces=pinyin_no_spaces,
            also_written=also_written,
            also_pronounced=also_pronounced,
            classifiers=classifiers,
            definitions=definitions,
            frequency=frequency,
        )

    return _generate_word_schema


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def generate_character_model(
    # the following is a root conftest fixture
    get_async_db_session_transaction: AsyncSession,
    # the following is a fixture from this module
    generate_character_schema: Callable[
        [
            common_domain.Character,
            common_domain.Definition | None,
            common_domain.PinyinToneMarks,
            character_domain.Decomposition | None,
            character_domain.Etymology | None,
            character_domain.Radical,
            character_domain.Matches,
            common_domain.Frequency,
        ],
        character_domain.CharacterSchema,
    ],
) -> Callable[
    [
        common_domain.Character,
        common_domain.Definition | None,
        common_domain.PinyinToneMarks,
        character_domain.Decomposition | None,
        character_domain.Etymology | None,
        character_domain.Radical,
        character_domain.Matches,
        common_domain.Frequency,
    ],
    Awaitable[character_model.Character],
]:
    async def _generate_character_model(
        character: common_domain.Character,
        definition: common_domain.Definition | None,
        pinyin: common_domain.PinyinToneMarks,
        decomposition: character_domain.Decomposition | None,
        etymology: character_domain.Etymology | None,
        radical: character_domain.Radical,
        matches: character_domain.Matches,
        frequency: common_domain.Frequency,
    ) -> character_model.Character:
        character_schema = generate_character_schema(
            character, definition, pinyin, decomposition, etymology, radical, matches, frequency
        )
        # created_character_model = await character_crud.create(get_async_db_session_transaction, obj_in=character_schema)
        created_character_model = character_model.Character(**character_schema.model_dump(by_alias=False))
        get_async_db_session_transaction.add(created_character_model)
        await get_async_db_session_transaction.commit()
        await get_async_db_session_transaction.refresh(created_character_model)
        return created_character_model

    return _generate_character_model


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def generate_word_model(
    # the following is a root conftest fixture
    get_async_db_session_transaction: AsyncSession,
    # the following is a fixture from this module
    generate_word_schema: Callable[
        [
            word_domain.SimplifiedWord,
            word_domain.TraditionalWord,
            common_domain.PinyinToneNumbers,
            common_domain.PinyinToneMarks,
            common_domain.PinyinNoToneMarks,
            common_domain.PinyinNoSpacesNoToneMarks,
            word_domain.AlsoWritten,
            word_domain.AlsoPronounced,
            word_domain.Classifiers,
            common_domain.Definition,
            common_domain.Frequency,
        ],
        word_domain.WordSchema,
    ],
) -> Callable[
    [
        word_domain.SimplifiedWord,
        word_domain.TraditionalWord,
        common_domain.PinyinToneNumbers,
        common_domain.PinyinToneMarks,
        common_domain.PinyinNoToneMarks,
        common_domain.PinyinNoSpacesNoToneMarks,
        word_domain.AlsoWritten,
        word_domain.AlsoPronounced,
        word_domain.Classifiers,
        common_domain.Definition,
        common_domain.Frequency,
    ],
    Awaitable[word_model.Word],
]:
    async def _generate_word_model(
        simplified: word_domain.SimplifiedWord,
        traditional: word_domain.TraditionalWord,
        pinyin_num: common_domain.PinyinToneNumbers,
        pinyin_accent: common_domain.PinyinToneMarks,
        pinyin_clean: common_domain.PinyinNoToneMarks,
        pinyin_no_spaces: common_domain.PinyinNoSpacesNoToneMarks,
        also_written: word_domain.AlsoWritten,
        also_pronounced: word_domain.AlsoPronounced,
        classifiers: word_domain.Classifiers,
        definitions: common_domain.Definition,
        frequency: common_domain.Frequency,
    ) -> word_model.Word:
        word_schema = generate_word_schema(
            simplified,
            traditional,
            pinyin_num,
            pinyin_accent,
            pinyin_clean,
            pinyin_no_spaces,
            also_written,
            also_pronounced,
            classifiers,
            definitions,
            frequency,
        )
        created_word_model = word_model.Word(**word_schema.model_dump(by_alias=False))
        get_async_db_session_transaction.add(created_word_model)
        await get_async_db_session_transaction.commit()
        await get_async_db_session_transaction.refresh(created_word_model)
        return created_word_model

    return _generate_word_model
