from unittest import mock

import pytest

from app.core import exceptions
from app.db.crud.character import character_crud
from app.db.crud.word import word_crud
from app.domain.vocabulary import combined as combined_domain
from app.domain.vocabulary import word as word_domain
from app.features.vocabulary.logic.search import (
    search_characters,
    search_phrase,
    search_simplified_words,
)


@pytest.mark.asyncio
@mock.patch.object(word_crud, "get_multiple_simplified")
async def test_search_simplified_words_validation_error(
    # the following is a mock patch
    mock_get_multiple_simplified: mock.AsyncMock,
) -> None:
    mock_get_multiple_simplified.return_value = ["hi"]
    with pytest.raises(exceptions.CNLearnWithMessage):
        await search_simplified_words([], mock.MagicMock())


@pytest.mark.asyncio
@mock.patch.object(word_crud, "get_multiple_simplified")
async def test_search_simplified_words_everything_works(
    # the following is a mock patch
    mock_get_multiple_simplified: mock.AsyncMock,
) -> None:
    mock_get_multiple_simplified.return_value = []
    result = await search_simplified_words([], mock.MagicMock())
    assert result == []


@pytest.mark.asyncio
@mock.patch.object(character_crud, "get_multiple_characters")
async def test_search_characters_validation_error_without_words(
    # the following is a mock patch
    mock_get_multiple_characters: mock.AsyncMock,
) -> None:
    mock_get_multiple_characters.return_value = [mock.Mock()]
    with pytest.raises(exceptions.CNLearnWithMessage):
        await search_characters([], mock.MagicMock(), include_words=False)


@pytest.mark.asyncio
@mock.patch.object(character_crud, "get_multiple_characters")
async def test_search_characters_validation_error_with_words(
    # the following is a mock patch
    mock_get_multiple_characters: mock.AsyncMock,
) -> None:
    mock_get_multiple_characters.return_value = [mock.Mock()]
    with pytest.raises(exceptions.CNLearnWithMessage):
        await search_characters([], mock.MagicMock(), include_words=True)


@pytest.mark.asyncio
@pytest.mark.parametrize(("with_words"), [pytest.param(True, id="with_words"), pytest.param(False, id="without words")])
@mock.patch.object(character_crud, "get_multiple_characters")
async def test_search_characters_everything_works(
    # the following is a mock patch
    mock_get_multiple_characters: mock.AsyncMock,
    # the following are pytest parameters
    with_words: bool,
) -> None:
    mock_get_multiple_characters.return_value = []
    result = await search_characters([], mock.MagicMock(), include_words=with_words)
    assert result == []


@pytest.mark.asyncio
@mock.patch.object(word_crud, "get_multiple_simplified")
async def test_search_phrase_validation_error(
    # the following is a mock patch
    mock_get_multiple_simplified: mock.AsyncMock,
) -> None:
    mock_chinese_segmenter = mock.MagicMock()
    mock_chinese_segmenter.cut.return_value = []
    mock_get_multiple_simplified.return_value = [mock.Mock()]
    with pytest.raises(exceptions.CNLearnWithMessage):
        await search_phrase(word_domain.SimplifiedWord(word_domain.Word("")), mock.MagicMock(), mock_chinese_segmenter)


@pytest.mark.asyncio
@mock.patch.object(word_crud, "get_multiple_simplified")
async def test_search_phrase_everything_works(
    # the following is a mock patch
    mock_get_multiple_simplified: mock.AsyncMock,
) -> None:
    mock_chinese_segmenter = mock.MagicMock()
    mock_chinese_segmenter.cut.return_value = []
    mock_get_multiple_simplified.return_value = []
    result = await search_phrase(
        word_domain.SimplifiedWord(word_domain.Word("")), mock.MagicMock(), mock_chinese_segmenter
    )
    assert result == combined_domain.DictionarySearchResult(words=[], not_found=[])
