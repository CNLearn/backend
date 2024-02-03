from typing import Awaitable, Callable

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.word import word_crud
from app.db.models import word as word_model
from app.domain.vocabulary import common as common_domain
from app.domain.vocabulary import word as word_domain


@pytest.mark.parametrize(
    (
        "word_simplified",
        "word_traditional",
        "word_pinyin_tone_numbers",
        "word_pinyin_tone_marks",
        "word_pinyin_no_tone_marks",
        "word_pinyin_no_spaces_no_tone",
        "word_also_written",
        "word_also_pronounced",
        "word_classifiers",
        "word_definition",
        "word_frequency",
    ),
    [
        pytest.param(
            "我们",
            "我們",
            "wo3 men5",
            "wǒ men",
            "wo men",
            "women",
            "",
            "",
            "",
            "we; us; ourselves; our",
            12345,
            id="normal word",
        )
    ],
)
@pytest.mark.asyncio
async def test_word_crud_get(
    # the following are pytest parameters
    word_simplified: str,
    word_traditional: str,
    word_pinyin_tone_numbers: str,
    word_pinyin_tone_marks: str,
    word_pinyin_no_tone_marks: str,
    word_pinyin_no_spaces_no_tone: str,
    word_also_written: str,
    word_also_pronounced: str,
    word_classifiers: str,
    word_definition: str,
    word_frequency: int,
    # the following is a root-imported fixture
    generate_word_model: Callable[
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
    ],
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    # let's create a word model for this test
    word_model = await generate_word_model(
        word_domain.SimplifiedWord(word_domain.Word(word_simplified)),
        word_domain.TraditionalWord(word_domain.Word(word_traditional)),
        common_domain.PinyinToneNumbers(word_pinyin_tone_numbers),
        common_domain.PinyinToneMarks(word_pinyin_tone_marks),
        common_domain.PinyinNoToneMarks(word_pinyin_no_tone_marks),
        common_domain.PinyinNoSpacesNoToneMarks(word_pinyin_no_spaces_no_tone),
        word_domain.AlsoWritten(word_also_written),
        word_domain.AlsoPronounced(word_also_pronounced),
        word_domain.Classifiers(word_classifiers),
        common_domain.Definition(word_definition),
        common_domain.Frequency(word_frequency),
    )
    assert word_model.simplified == word_simplified
    assert word_model.traditional == word_traditional
    assert word_model.pinyin_num == word_pinyin_tone_numbers
    assert word_model.pinyin_accent == word_pinyin_tone_marks
    assert word_model.pinyin_clean == word_pinyin_no_tone_marks
    assert word_model.pinyin_no_spaces == word_pinyin_no_spaces_no_tone
    assert word_model.also_written == word_also_written
    assert word_model.also_pronounced == word_also_pronounced
    assert word_model.classifiers == word_classifiers
    assert word_model.definitions == word_definition
    assert word_model.frequency == word_frequency
    assert repr(word_model) == f"<Word(simplified='{word_simplified}', pinyin='{word_pinyin_tone_marks}')>"


@pytest.mark.asyncio
async def test_word_crud_get_multiple_simplified(
    # the following is a root-imported fixture
    generate_word_model: Callable[
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
    ],
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    # let's create a word model for this test
    await generate_word_model(
        word_domain.SimplifiedWord(word_domain.Word("我们")),
        word_domain.TraditionalWord(word_domain.Word("我們")),
        common_domain.PinyinToneNumbers("wo3 men5"),
        common_domain.PinyinToneMarks("wǒ men"),
        common_domain.PinyinNoToneMarks("wo men"),
        common_domain.PinyinNoSpacesNoToneMarks("women"),
        word_domain.AlsoWritten(""),
        word_domain.AlsoPronounced(""),
        word_domain.Classifiers(""),
        common_domain.Definition("we; us; ourselves; our"),
        common_domain.Frequency(12345),
    )
    await generate_word_model(
        word_domain.SimplifiedWord(word_domain.Word("你们")),
        word_domain.TraditionalWord(word_domain.Word("你們")),
        common_domain.PinyinToneNumbers("ni3 men5"),
        common_domain.PinyinToneMarks("nǐ men"),
        common_domain.PinyinNoToneMarks("ni men"),
        common_domain.PinyinNoSpacesNoToneMarks("nimen"),
        word_domain.AlsoWritten(""),
        word_domain.AlsoPronounced(""),
        word_domain.Classifiers(""),
        common_domain.Definition("you (plural)"),
        common_domain.Frequency(12346),
    )
    we_and_you = await word_crud.get_multiple_simplified(
        get_async_db_session_transaction,
        simplified_words=[
            word_domain.SimplifiedWord(word_domain.Word("我们")),
            word_domain.SimplifiedWord(word_domain.Word("你们")),
        ],
    )
    assert len(we_and_you) == 2


@pytest.mark.asyncio
async def test_crud_character_create(
    # the following is a root-imported fixture
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
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    word_schema = generate_word_schema(
        word_domain.SimplifiedWord(word_domain.Word("你们")),
        word_domain.TraditionalWord(word_domain.Word("你們")),
        common_domain.PinyinToneNumbers("ni3 men5"),
        common_domain.PinyinToneMarks("nǐ men"),
        common_domain.PinyinNoToneMarks("ni men"),
        common_domain.PinyinNoSpacesNoToneMarks("nimen"),
        word_domain.AlsoWritten(""),
        word_domain.AlsoPronounced(""),
        word_domain.Classifiers(""),
        common_domain.Definition("you (plural)"),
        common_domain.Frequency(12346),
    )
    # let's pass that to word_crud.create
    created_word = await word_crud.create(get_async_db_session_transaction, obj_in=word_schema)
    # let's make some assertions
    assert created_word is not None
    assert created_word.simplified == "你们"
    assert created_word.traditional == "你們"
    assert created_word.pinyin_num == "ni3 men5"
    assert created_word.pinyin_accent == "nǐ men"
    assert created_word.pinyin_clean == "ni men"
    assert created_word.pinyin_no_spaces == "nimen"
    assert created_word.also_written == ""
    assert created_word.also_pronounced == ""
    assert created_word.classifiers == ""
    assert created_word.definitions == "you (plural)"
    assert created_word.frequency == 12346


@pytest.mark.asyncio
async def test_crud_word_update(
    # the following is a root-imported fixture
    generate_word_model: Callable[
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
    ],
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
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    # let's create a word model for this test
    word_model = await generate_word_model(
        word_domain.SimplifiedWord(word_domain.Word("我们")),
        word_domain.TraditionalWord(word_domain.Word("我們")),
        common_domain.PinyinToneNumbers("wo3 men5"),
        common_domain.PinyinToneMarks("wǒ men"),
        common_domain.PinyinNoToneMarks("wo men"),
        common_domain.PinyinNoSpacesNoToneMarks("women"),
        word_domain.AlsoWritten(""),
        word_domain.AlsoPronounced(""),
        word_domain.Classifiers(""),
        common_domain.Definition("we; us; ourselves; our"),
        common_domain.Frequency(12345),
    )
    # let's make sure it's there and ready for us
    assert word_model.simplified == "我们"

    # let's update this object with a new definition by passing in a dictionary
    await word_crud.update(
        get_async_db_session_transaction,
        db_obj=word_model,
        obj_in={"definitions": "you?? mistake"},
    )
    await get_async_db_session_transaction.refresh(word_model)
    assert word_model.definitions == common_domain.Definition("you?? mistake")

    # now let's update this back by passing it a WordSchema
    word_schema = generate_word_schema(
        word_domain.SimplifiedWord(word_domain.Word("我们")),
        word_domain.TraditionalWord(word_domain.Word("我們")),
        common_domain.PinyinToneNumbers("wo3 men5"),
        common_domain.PinyinToneMarks("wǒ men"),
        common_domain.PinyinNoToneMarks("wo men"),
        common_domain.PinyinNoSpacesNoToneMarks("women"),
        word_domain.AlsoWritten(""),
        word_domain.AlsoPronounced(""),
        word_domain.Classifiers(""),
        common_domain.Definition("we; us; ourselves; our"),
        common_domain.Frequency(12345),
    )
    await word_crud.update(get_async_db_session_transaction, db_obj=word_model, obj_in=word_schema)
    await get_async_db_session_transaction.refresh(word_model)
    assert word_model.definitions == common_domain.Definition("we; us; ourselves; our")


@pytest.mark.asyncio
async def test_word_crud_delete(
    # the following is a root-imported fixture
    generate_word_model: Callable[
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
    ],
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    # let's create a word model for this test
    word_model = await generate_word_model(
        word_domain.SimplifiedWord(word_domain.Word("我们")),
        word_domain.TraditionalWord(word_domain.Word("我們")),
        common_domain.PinyinToneNumbers("wo3 men5"),
        common_domain.PinyinToneMarks("wǒ men"),
        common_domain.PinyinNoToneMarks("wo men"),
        common_domain.PinyinNoSpacesNoToneMarks("women"),
        word_domain.AlsoWritten(""),
        word_domain.AlsoPronounced(""),
        word_domain.Classifiers(""),
        common_domain.Definition("we; us; ourselves; our"),
        common_domain.Frequency(12345),
    )
    # let's check if we can get it using its id
    model_id: int = word_model.id

    got_word = await word_crud.get(get_async_db_session_transaction, model_id)
    assert got_word is not None

    # let's try and delete it
    await word_crud.remove(get_async_db_session_transaction, id=model_id)

    # now let's try and get it again
    possible_got_word = await word_crud.get(get_async_db_session_transaction, model_id)
    assert possible_got_word is None
