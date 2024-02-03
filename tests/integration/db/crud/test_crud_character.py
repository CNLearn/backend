from typing import Awaitable, Callable

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.character import character_crud
from app.db.models import character as character_model
from app.domain.vocabulary import character as character_domain
from app.domain.vocabulary import common as common_domain


@pytest.mark.asyncio
@pytest.mark.parametrize(
    (
        "character_character",
        "character_definition",
        "character_pinyin",
        "character_decomposition",
        "character_etymology",
        "character_radical",
        "character_matches",
        "character_frequency",
    ),
    [
        pytest.param(
            "好",
            "good",
            "hǎo",
            "⿰女子",
            character_domain.Etymology(type="ideographic", hint="A woman 女 with a son 子"),
            "女",
            "[[0], [0], [0], [1], [1], [1]]",
            165789,
            id="character with all the fields",
        ),
        pytest.param(
            "好",
            None,
            "hǎo",
            "⿰女子",
            character_domain.Etymology(type="ideographic", hint="A woman 女 with a son 子"),
            "女",
            "[[0], [0], [0], [1], [1], [1]]",
            165789,
            id="character with no definition",
        ),
        pytest.param(
            "好",
            "good",
            "hǎo",
            None,
            character_domain.Etymology(type="ideographic", hint="A woman 女 with a son 子"),
            "女",
            "[[0], [0], [0], [1], [1], [1]]",
            165789,
            id="character with no decomposition",
        ),
        pytest.param(
            "好",
            "good",
            "hǎo",
            "⿰女子",
            None,
            "女",
            "[[0], [0], [0], [1], [1], [1]]",
            165789,
            id="character with no etymology",
        ),
    ],
)
async def test_character_crud_get(
    # the following are pytest Parameters
    character_character: str,
    character_definition: str | None,
    character_pinyin: str,
    character_decomposition: str,
    character_etymology: character_domain.Etymology,
    character_radical: str,
    character_matches: str,
    character_frequency: int,
    # the following is a root-imported fixture
    generate_character_model: Callable[
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
    ],
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    # let's create a character model for this test
    character_model = await generate_character_model(
        common_domain.Character(character_character),
        common_domain.Definition(character_definition) if character_definition else None,
        common_domain.PinyinToneMarks(character_pinyin),
        character_domain.Decomposition(character_decomposition) if character_decomposition else None,
        character_etymology if character_etymology else None,
        character_domain.Radical(character_radical),
        character_domain.Matches(character_matches),
        common_domain.Frequency(character_frequency),
    )

    # let's get the character model we just created
    got_character = await character_crud.get(get_async_db_session_transaction, id=character_model.id)
    assert got_character is not None
    assert character_model.character == character_character
    assert character_model.definition == character_definition
    assert character_model.pinyin == character_pinyin
    assert character_model.decomposition == character_decomposition
    assert character_model.etymology == character_etymology
    assert character_model.radical == character_radical
    assert character_model.matches == character_matches
    assert character_model.frequency == character_frequency
    assert repr(character_model) == f"<Character({character_character}, radical='{character_radical})>"


@pytest.mark.asyncio
async def test_crud_character_get_multi(
    # the following is a root-imported fixture
    generate_character_model: Callable[
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
    ],
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    # let's check how many characters there are currently
    # note these should include the vocabularty fixtures that
    # are loaded on test setup
    all_characters = await character_crud.get_multi(get_async_db_session_transaction)
    n_characters: int = len(all_characters)
    # let's create a character model for this test
    await generate_character_model(
        common_domain.Character("谁"),
        common_domain.Definition("who"),
        common_domain.PinyinToneMarks("sheí"),
        None,
        None,
        character_domain.Radical("讠"),
        character_domain.Matches(""),
        common_domain.Frequency(9000),
    )
    # let's refresh the query
    all_characters = await character_crud.get_multi(get_async_db_session_transaction)
    assert len(all_characters) == n_characters + 1


@pytest.mark.asyncio
async def test_crud_character_create(
    # the following is a root-imported fixture
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
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    # let's create a character schema we can use to create a character model object
    character_schema = generate_character_schema(
        common_domain.Character("谁"),
        common_domain.Definition("who"),
        common_domain.PinyinToneMarks("sheí"),
        None,
        None,
        character_domain.Radical("讠"),
        character_domain.Matches(""),
        common_domain.Frequency(9000),
    )
    # let's pass that to character_crud.create
    created_character = await character_crud.create(get_async_db_session_transaction, obj_in=character_schema)
    # let's assert some comparisons
    assert created_character is not None
    assert created_character.character == character_schema.character
    assert created_character.definition == character_schema.definition
    assert created_character.pinyin == character_schema.pinyin
    assert created_character.decomposition == character_schema.decomposition
    assert created_character.etymology == character_schema.etymology
    assert created_character.radical == character_schema.radical
    assert created_character.matches == character_schema.matches
    assert created_character.frequency == character_schema.frequency


@pytest.mark.asyncio
async def test_crud_character_update(
    # the following is a root-imported fixture
    generate_character_model: Callable[
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
    ],
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
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    # let's create a character model for this test
    new_character_model = await generate_character_model(
        common_domain.Character("谁"),
        common_domain.Definition("who"),
        common_domain.PinyinToneMarks("sheí"),
        None,
        None,
        character_domain.Radical("讠"),
        character_domain.Matches(""),
        common_domain.Frequency(9000),
    )
    # let's check it's there and ready for us
    assert new_character_model.definition == common_domain.Definition("who")

    # let's update this object with a new definition by passing in a dictionary
    await character_crud.update(
        get_async_db_session_transaction, db_obj=new_character_model, obj_in={"definition": "whoooo?"}
    )
    await get_async_db_session_transaction.refresh(new_character_model)
    assert new_character_model.definition == common_domain.Definition("whoooo?")

    # now let's update this object back to the old definition by passing in a CharacterSchema (TODO: at some point need to decide if anything should be updateable)
    new_schema = generate_character_schema(
        common_domain.Character("谁"),
        common_domain.Definition("who"),
        common_domain.PinyinToneMarks("sheí"),
        None,
        None,
        character_domain.Radical("讠"),
        character_domain.Matches(""),
        common_domain.Frequency(9000),
    )
    await character_crud.update(get_async_db_session_transaction, db_obj=new_character_model, obj_in=new_schema)
    await get_async_db_session_transaction.refresh(new_character_model)
    assert new_character_model.definition == common_domain.Definition("who")


@pytest.mark.asyncio
async def test_crud_character_delete(
    # the following is a root-imported fixture
    generate_character_model: Callable[
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
    ],
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    # let's create a character model for this test
    new_character_model = await generate_character_model(
        common_domain.Character("谁"),
        common_domain.Definition("who"),
        common_domain.PinyinToneMarks("sheí"),
        None,
        None,
        character_domain.Radical("讠"),
        character_domain.Matches(""),
        common_domain.Frequency(9000),
    )
    # let's check if we can get it using its id
    model_id: int = new_character_model.id

    got_character = await character_crud.get(get_async_db_session_transaction, model_id)
    assert got_character is not None

    # let's try and delete it
    await character_crud.remove(get_async_db_session_transaction, id=model_id)

    # now let's try and get it again
    possible_got_character = await character_crud.get(get_async_db_session_transaction, model_id)
    assert possible_got_character is None


@pytest.mark.asyncio
async def test_crud_character_get_multiple_characters(
    # the following is a root-imported fixture
    generate_character_model: Callable[
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
    ],
    # the following is a root fixture
    get_async_db_session_transaction: AsyncSession,
) -> None:
    # let's create two character models for this test
    await generate_character_model(
        common_domain.Character("谁"),
        common_domain.Definition("who"),
        common_domain.PinyinToneMarks("sheí"),
        None,
        None,
        character_domain.Radical("讠"),
        character_domain.Matches(""),
        common_domain.Frequency(9000),
    )
    await generate_character_model(
        common_domain.Character("门"),
        common_domain.Definition("door"),
        common_domain.PinyinToneMarks("mén"),
        None,
        None,
        character_domain.Radical("门"),
        character_domain.Matches(""),
        common_domain.Frequency(9001),
    )
    # ok let's try and get both now
    character_models = await character_crud.get_multiple_characters(
        get_async_db_session_transaction,
        characters=[common_domain.Character("谁"), common_domain.Character("门")],
        include_words=True,
    )
    assert len(character_models) == 2
