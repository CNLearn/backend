from typing import Annotated

from fastapi import APIRouter, Depends

from app.domain.vocabulary import combined as combined_domain

from .dependencies import search as search_dependencies

router = APIRouter()


@router.get("/get-words", response_model=list[combined_domain.WordOut], name="vocabulary:get-words")
async def get_words(
    result: Annotated[list[combined_domain.WordOut], Depends(search_dependencies.search_simplified_words)]
) -> list[combined_domain.WordOut]:
    return result


@router.get("/get-characters", response_model=list[combined_domain.CharacterOut], name="vocabulary:get-characters")
async def get_characters(
    result: Annotated[list[combined_domain.CharacterOut], Depends(search_dependencies.search_characters)]
) -> list[combined_domain.CharacterOut]:
    return result


@router.get("/search-phrase", response_model=combined_domain.DictionarySearchResult, name="vocabulary:search-phrase")
async def search_phrase(
    result: Annotated[combined_domain.DictionarySearchResult, Depends(search_dependencies.search_phrase)]
) -> combined_domain.DictionarySearchResult:
    return result
