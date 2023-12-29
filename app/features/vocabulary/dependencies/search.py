from typing import Annotated

import jieba
from fastapi import Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.vocabulary import combined as combined_domain
from app.domain.vocabulary import common as common_domain
from app.domain.vocabulary import word as word_domain
from app.features.db import get_async_session

from ..logic import search as search_logic


async def search_simplified_words(
    simplified_words: Annotated[list[word_domain.SimplifiedWord], Query(min_length=1, max_length=10)],
    db: AsyncSession = Depends(get_async_session),
) -> list[combined_domain.WordOut]:
    return await search_logic.search_simplified_words(simplified_words, db)


async def search_characters(
    characters: Annotated[
        list[Annotated[common_domain.Character, Query(min_length=1, max_length=1)]], Query(min_length=1)
    ],
    db: AsyncSession = Depends(get_async_session),
    include_words: bool = False,
) -> list[combined_domain.CharacterOut]:
    return await search_logic.search_characters(characters, db, include_words)


async def search_phrase(
    request: Request,
    phrase: Annotated[word_domain.SimplifiedWord, Query(min_length=2)],
    db: AsyncSession = Depends(get_async_session),
) -> combined_domain.DictionarySearchResult:
    chinese_segmenter: jieba = request.state._chinese_segmenter
    return await search_logic.search_phrase(phrase, db, chinese_segmenter)
